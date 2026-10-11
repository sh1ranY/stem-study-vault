"""Local invitation pilot API. All learner lookups are scoped by authenticated owner."""
import hashlib
import hmac
import io
import json
import os
import secrets
import threading
import time
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, Request, Response, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image, ImageOps, UnidentifiedImageError
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import delete
from . import store, teaching, model, guided
from .export_record import skill_record

router=APIRouter(prefix='/api/pilot')
LOCK=threading.RLock()
MODEL_LOCK=threading.Lock()
COOKIE='elec270_session'
class Body(BaseModel): model_config=ConfigDict(extra='forbid')
class Login(Body):
    name:str=Field(min_length=1,max_length=60)
    password:str=Field(min_length=10,max_length=200)
    invite:str=''
class TaskRequest(Body):
    topic:str
    phase:str='diagnosis'
    request_id:str=Field(min_length=8,max_length=80)
class Submit(Body):
    task_id:str
    request_id:str=Field(min_length=8,max_length=80)
    answers:dict[str,str]
    working:str=Field(min_length=1,max_length=12000)
    photo_id:Optional[str]=None
    confirmed:bool=False
    prior_seen:bool=False
class Reveal(Body):
    task_id:Optional[str]=None
    lesson_id:Optional[str]=None
    block_id:Optional[str]=None
    kind:str='hint'
class Route(Body):
    topic:str
    route:str
class Progress(Body):
    lesson_id:str
    notes:str=Field(default='',max_length=30000)
class Withdraw(Body):
    reason:str=Field(min_length=1,max_length=1000)
class Operation(Body):
    request_id:str=Field(min_length=8,max_length=80)
class Search(Body):
    query:str=Field(min_length=1,max_length=200)

class TeachingPreference(Body):
    language:Literal['zh-CN','en']
class GuidedMode(Body):
    mode:Literal['bridge','visual','algebra']
class GuidedCheck(Body):
    check_id:str=Field(min_length=1,max_length=80)
    request_id:str=Field(min_length=8,max_length=80)
    number:str=Field(min_length=1,max_length=80)
    choice:str=Field(min_length=1,max_length=40)
class GuidedNext(Body):
    check_id:str=Field(min_length=1,max_length=80)
    use_suggestion:bool=True

def fail(status,msg): raise HTTPException(status,msg)
def required(kind,owner,key,conn=None):
    v=store.fetch(kind,owner,key,conn)
    if v is None: fail(404,'记录不存在或你没有访问权限。')
    return v

def current():
    c=store.fetch('config','shared','current-course')
    if c is None: fail(409,'课程尚未导入，请运行 ELEC270 导入命令。')
    return required('course','shared',c['version'])

def user(request:Request):
    token=request.cookies.get(COOKIE,'')
    session=store.fetch('login','auth',hashlib.sha256(token.encode()).hexdigest()) if token else None
    if not session or session['expires']<time.time(): fail(401,'请先登录。')
    return required('user','auth',session['user_id'])

def event(owner,kind,conn=None,**values):
    return store.save('event',owner,{'id':store.uid(),'kind':kind,'at':store.now(),**values},conn)

def auth_response(u,response):
    token=secrets.token_urlsafe(32)
    store.save('login','auth',{'id':hashlib.sha256(token.encode()).hexdigest(),'user_id':u['id'],'expires':time.time()+30*86400})
    response.set_cookie(COOKIE,token,httponly=True,samesite='strict',secure=os.getenv('STUDIO_COOKIE_SECURE')=='1',max_age=30*86400,path='/api')
    return {'id':u['id'],'name':u['name'],'role':u['role']}

def passwd(value,salt): return hashlib.pbkdf2_hmac('sha256',value.encode(),bytes.fromhex(salt),600000).hex()

@router.get('/status')
def status(request:Request):
    c=store.fetch('config','shared','current-course');u=None
    try: u=user(request)
    except HTTPException: pass
    return {'setup_required':not bool(store.listing('user','auth')),'course_ready':bool(c),'model_available':model.available(),'user':{'id':u['id'],'name':u['name'],'role':u['role']} if u else None,'deployment':'local-invitation','database':'postgresql' if store.URL.startswith('postgres') else 'sqlite-local','notice':'本机试点 · 三主题数值检查可离线使用；AI 转写与过程反馈需要配置模型。'}

@router.post('/auth/register')
def register(body:Login,response:Response):
    name=body.name.strip()
    if not name: fail(422,'请输入用户名。')
    with LOCK, store.engine.begin() as conn:
        users=store.listing('user','auth',conn)
        if any(x['name'].casefold()==name.casefold() for x in users): fail(409,'这个用户名已存在。')
        if users:
            invite=store.fetch('invite','auth',hashlib.sha256(body.invite.encode()).hexdigest(),conn)
            if not invite or invite['used']: fail(403,'需要有效的一次性邀请码。')
            invite['used']=True;store.save('invite','auth',invite,conn)
        salt=secrets.token_hex(16)
        u={'id':store.uid(),'name':name,'salt':salt,'password_hash':passwd(body.password,salt),'password_algorithm':'pbkdf2-sha256-600000','role':'learner' if users else 'owner','created_at':store.now()}
        store.save('user','auth',u,conn)
    return auth_response(u,response)

@router.post('/auth/login')
def login(body:Login,response:Response):
    # Persist failed counts without recording supplied passwords.
    key=hashlib.sha256(body.name.casefold().encode()).hexdigest()
    with LOCK:
        limit=store.fetch('throttle','auth',key) or {'id':key,'count':0,'until':0}
        if limit['until']>time.time() and limit['count']>=8: fail(429,'尝试次数过多，请十五分钟后再试。')
        u=next((u for u in store.listing('user','auth') if u['name'].casefold()==body.name.strip().casefold()),None)
        valid=hmac.compare_digest(passwd(body.password,u['salt'] if u else '00'*16),u['password_hash'] if u else '00'*32)
        if not u or not valid:
            if limit['until']<time.time(): limit['count']=0
            limit.update(count=limit['count']+1,until=time.time()+900);store.save('throttle','auth',limit);fail(401,'用户名或密码不正确。')
        store.remove('throttle','auth',key)
    return auth_response(u,response)

@router.post('/auth/logout')
def logout(request:Request,response:Response,u=Depends(user)):
    store.remove('login','auth',hashlib.sha256(request.cookies[COOKIE].encode()).hexdigest())
    response.delete_cookie(COOKIE,path='/api');return {'ok':True}

@router.post('/auth/invite')
def invite(u=Depends(user)):
    if u['role']!='owner': fail(403,'仅本机课程所有者可创建邀请。')
    token=secrets.token_urlsafe(18);store.save('invite','auth',{'id':hashlib.sha256(token.encode()).hexdigest(),'used':False,'created_at':store.now()});return {'invite':token}

@router.post('/legacy/import')
def import_old(u=Depends(user)):
    if u['role']!='owner': fail(403,'仅所有者可以读取本机旧原型记录。')
    from .migrate_legacy import import_legacy
    return {'count':import_legacy(u['id'])}

@router.get('/legacy')
def old_records(u=Depends(user)):
    return [{'id':r['id'],'title':r['snapshot']['unit']['title'],'attempt_count':len(r['snapshot'].get('attempts',[])),'note':r['note']} for r in store.listing('legacy-session',u['id'])]

@router.get('/course')
def course(u=Depends(user)):
    c=current()
    return {'id':c['id'],'title':c['title'],'imported_at':c['imported_at'],'lessons':[{'id':l['id'],'title':l['title'],'week':l['week']} for l in c['lessons']],
            'topics':{k:{'title':v['title'],'week':v['week'],'objective':v['objective'],'routes':list(v['routes'])} for k,v in teaching.TOPICS.items()},
            'asset_count':len(c['assets']),'warnings':c['warnings'],'legacy_records':c['legacy_records'] if u['role']=='owner' else []}

@router.get('/lessons/{id}')
def lesson(id:str,u=Depends(user)):
    c=current();l=next((l for l in c['lessons'] if l['id']==id),None)
    if l is None: fail(404,'未找到这个学习单元。')
    unlocked={e.get('block_id') for e in store.listing('event',u['id']) if e['kind']=='block_reveal' and e.get('version')==c['id']}
    return {**{k:v for k,v in l.items() if k not in ('blocks','source_path')},'version':c['id'],'blocks':[{**b,'body':b['body'] if b['role']=='lesson' or b['id'] in unlocked else None} for b in l['blocks']]}

@router.post('/search')
def search(body:Search,u=Depends(user)):
    c=current();terms=body.query.lower().split();matches=[]
    for l in c['lessons']:
        for b in l['blocks']:
            if b['role']!='lesson': continue
            text=b['body'];score=sum(text.lower().count(t) for t in terms)
            if score:
                pos=min([text.lower().find(t) for t in terms if t in text.lower()]);matches.append({'lesson_id':l['id'],'title':l['title'],'block_id':b['id'],'excerpt':text[max(0,pos-70):pos+230],'score':score})
    return sorted(matches,key=lambda x:x['score'],reverse=True)[:20]

@router.get('/sources')
def sources(u=Depends(user)):
    return [{k:v for k,v in a.items() if k not in ('path','original_path')} for a in current()['assets'] if a['suffix'] in ('.pdf','.pptx')]

@router.get('/assets/{id}')
def asset(id:str,u=Depends(user)):
    a=next((a for a in current()['assets'] if a['id']==id),None)
    if not a: fail(404,'附件不存在。')
    if a['suffix'] in ('.pdf','.pptx'): event(u['id'],'source_opened',asset_id=id,exposure='source-may-include-solutions')
    # SVG from course source files is served as image, no inline HTML execution.
    headers={'Content-Security-Policy':"default-src 'none'; sandbox"}
    return FileResponse(a['path'],media_type={'.svg':'image/svg+xml','.pdf':'application/pdf'}.get(a['suffix']),headers=headers)

@router.get('/state')
def state(u=Depends(user)):
    owner=u['id'];attempts=sorted(store.listing('attempt',owner),key=lambda a:a['at']);events=store.listing('event',owner)
    active=[a for a in attempts if a['active']];summaries={}
    for topic in teaching.TOPICS:
        seen=[a for a in active if a['topic']==topic]
        summaries[topic]={'attempts':len(seen),'independent':sum(a['result']['status']=='independent' for a in seen),'status':seen[-1]['result']['status'] if seen else 'unknown',
          'due_at':seen[-1].get('review_due') if seen else None,'route':(store.fetch('route',owner,topic) or {}).get('route',seen[-1]['result']['route'] if seen else 'visual')}
    return {'attempts':attempts,'tasks':[teaching.public_task(t) for t in sorted(store.listing('task',owner),key=lambda t:t['created_at'])],
            'events':events,'summaries':summaries,'progress':store.listing('progress',owner),'photos':[{k:v for k,v in p.items() if k not in ('path','original_path')} for p in store.listing('photo',owner)],
            'runs':[{**r,'status':'interrupted_or_unknown' if r['status']=='running' and (datetime.now(timezone.utc)-datetime.fromisoformat(r['at'])).total_seconds()>120 else r['status']} for r in store.listing('run',owner)],'feedback':store.listing('feedback',owner)}

@router.post('/tasks')
def make_task(body:TaskRequest,u=Depends(user)):
    with LOCK, store.engine.begin() as conn:
        previous=store.fetch('request',u['id'],body.request_id,conn)
        signature={'topic':body.topic,'phase':body.phase}
        if previous:
            if previous['signature']!=signature: fail(409,'这个请求编号已用于其他操作。')
            return teaching.public_task(required('task',u['id'],previous['task_id'],conn))
        tasks=store.listing('task',u['id'],conn)
        n=sum(t['topic']==body.topic and t['phase']==body.phase for t in tasks)
        try: t=teaching.task(body.topic,body.phase,n)
        except ValueError as e: fail(422,str(e))
        t['course_version']=current()['id'];store.save('task',u['id'],t,conn)
        store.save('request',u['id'],{'id':body.request_id,'signature':signature,'task_id':t['id']},conn)
        event(u['id'],'task_opened',conn,task_id=t['id'],topic=t['topic'])
        return teaching.public_task(t)

@router.post('/route')
def choose_route(body:Route,u=Depends(user)):
    if body.topic not in teaching.TOPICS or body.route not in teaching.TOPICS[body.topic]['routes']: fail(422,'未知教学路径。')
    with LOCK,store.engine.begin() as conn:
        store.save('route',u['id'],{'id':body.topic,'route':body.route,'at':store.now()},conn)
        event(u['id'],'route_chosen',conn,topic=body.topic,route=body.route)
    return {'body':teaching.TOPICS[body.topic]['routes'][body.route],'example':teaching.TOPICS[body.topic]['example']}

@router.get('/teaching/{topic}')
def help_topic(topic:str,route:str='visual',u=Depends(user)):
    if topic not in teaching.TOPICS or route not in teaching.TOPICS[topic]['routes']: fail(404,'未知教学路径。')
    return {'body':teaching.TOPICS[topic]['routes'][route],'example':teaching.TOPICS[topic]['example']}

@router.patch('/progress')
def progress(body:Progress,u=Depends(user)):
    if not any(l['id']==body.lesson_id for l in current()['lessons']): fail(422,'未知学习单元。')
    return store.save('progress',u['id'],{'id':body.lesson_id,'notes':body.notes,'at':store.now(),'version':current()['id']})

@router.post('/reveal')
def reveal(body:Reveal,u=Depends(user)):
    if body.task_id:
        if body.kind not in ('hint','solution'): fail(422,'未知提示类型。')
        t=required('task',u['id'],body.task_id);event(u['id'],body.kind,task_id=t['id']);return {'body':t[body.kind]}
    c=current();l=next((l for l in c['lessons'] if l['id']==body.lesson_id),None)
    b=next((b for b in l['blocks'] if b['id']==body.block_id),None) if l else None
    if not b: fail(404,'未找到内容。')
    event(u['id'],'block_reveal',block_id=b['id'],lesson_id=l['id'],version=c['id'],role=b['role']);return {'body':b['body']}

@router.post('/photos/{task_id}')
async def photo(task_id:str,file:UploadFile=File(...),u=Depends(user)):
    required('task',u['id'],task_id)
    data=await file.read(10*1024*1024+1)
    if len(data)>10*1024*1024: fail(413,'照片超过 10 MB，请压缩后重试。')
    try:
        with Image.open(io.BytesIO(data)) as im:
            if im.width*im.height>30_000_000: fail(413,'照片像素过大，请裁切到解题区域。')
            if im.format not in ('JPEG','PNG','WEBP'): fail(415,'请使用 JPEG、PNG 或 WebP 照片。')
            original_format=im.format
            corrected=ImageOps.exif_transpose(im).convert('RGB');corrected.thumbnail((2000,2000))
            buf=io.BytesIO();corrected.save(buf,format='JPEG',quality=90)
    except (UnidentifiedImageError,OSError,Image.DecompressionBombError): fail(422,'这张照片无法读取，请重新拍照或输入文字。')
    key=store.uid();folder=store.DATA/'photos'/u['id'];folder.mkdir(parents=True,exist_ok=True)
    path=folder/(key+'.jpg');path.write_bytes(buf.getvalue())
    original=folder/(key+'.original');original.write_bytes(data)
    p={'id':key,'task_id':task_id,'path':str(path),'original_path':str(original),'original_format':original_format,'sha256':hashlib.sha256(data).hexdigest(),'at':store.now(),'transcription':None}
    store.save('photo',u['id'],p)
    return {k:v for k,v in p.items() if k not in ('path','original_path')}

@router.get('/photos/{id}')
def image(id:str,u=Depends(user)):
    return FileResponse(required('photo',u['id'],id)['path'],media_type='image/jpeg')


def run_model(owner,request_id,operation,reference,execute):
    if not model.available(): fail(409,'尚未配置模型。照片已保存；可手动录入并确认解题过程，或先配置本机模型密钥。')
    with LOCK:
        existing=store.fetch('run',owner,request_id)
        if existing:
            if existing['operation']!=operation or existing['reference']!=reference: fail(409,'请求编号已用于其他任务。')
            if existing['status']=='completed': return existing['result']
            fail(409,'该调用已发出，状态为 '+existing['status']+'。未自动重试；请核对调用状态后另发请求。')
        recent=[r for r in store.listing('run',owner) if r['at'][:10]==store.now()[:10]]
        if len(recent)>=int(os.getenv('STUDIO_DAILY_MODEL_CALLS','30')): fail(429,'已达到今天的模型调用上限。已有课程和离线检查仍可使用。')
        if not MODEL_LOCK.acquire(False): fail(409,'已有模型任务正在运行，请稍后再试。')
        run={'id':request_id,'operation':operation,'reference':reference,'status':'running','at':store.now(),'call_limit':1,'model':model.settings()[1],'prompt_version':model.PROMPT_VERSION}
        store.save('run',owner,run)
    try:
        result,usage=execute()
        with LOCK:
            if store.fetch('run',owner,request_id) is None: fail(409,'任务记录已删除，结果未重新保存。')
            run.update(status='completed',result=result,usage=usage,finished_at=store.now());store.save('run',owner,run)
        return result
    except HTTPException:
        raise
    except Exception as exc:
        run.update(status='failed',finished_at=store.now(),error='服务未完成或输出校验失败')
        with LOCK:
            if store.fetch('run',owner,request_id) is not None: store.save('run',owner,run)
        fail(502,str(exc) if isinstance(exc,ValueError) and len(str(exc))<300 else '模型未返回有效结果，未自动重试。')
    finally: MODEL_LOCK.release()

@router.post('/photos/{id}/transcribe')
def transcribe(id:str,body:Operation,u=Depends(user)):
    p=required('photo',u['id'],id);t=required('task',u['id'],p['task_id'])
    result=run_model(u['id'],body.request_id,'transcribe',id,lambda:model.call('transcribe',{'task':teaching.public_task(t)},Path(p['path']).read_bytes()))
    with LOCK:
        p=required('photo',u['id'],id);p['transcription']=result;p.setdefault('revisions',[])
        if not any(r['run_id']==body.request_id for r in p['revisions']): p['revisions'].append({'run_id':body.request_id,'at':store.now(),'value':result})
        store.save('photo',u['id'],p)
    return result

@router.post('/attempts')
def submit(body:Submit,u=Depends(user)):
    if not body.working.strip() or not body.confirmed: fail(422,'请核对解题过程与关键公式，然后确认提交。')
    signature=hashlib.sha256(body.model_dump_json().encode()).hexdigest()
    with LOCK,store.engine.begin() as conn:
        old=store.fetch('attempt',u['id'],body.request_id,conn)
        if old:
            if old['signature']!=signature: fail(409,'同一提交编号的内容不同，请刷新后重试。')
            return old
        t=required('task',u['id'],body.task_id,conn)
        p=required('photo',u['id'],body.photo_id,conn) if body.photo_id else None
        if p and p['task_id']!=t['id']: fail(422,'照片属于另一道题。')
        events=store.listing('event',u['id'],conn);prior=any(a['task_id']==t['id'] for a in store.listing('attempt',u['id'],conn))
        exposed=body.prior_seen or any(e.get('task_id')==t['id'] and e['kind'] in ('hint','solution','feedback') for e in events)
        try: result=teaching.evaluate(t,body.answers,exposed,prior)
        except ValueError as e: fail(422,str(e))
        record={'id':body.request_id,'signature':signature,'task_id':t['id'],'topic':t['topic'],'course_version':t['course_version'],'task_version':t['version'],'at':store.now(),
          'answers':body.answers,'working':body.working,'photo_id':body.photo_id,'recognition':p.get('transcription') if p else None,'confirmed':True,'exposure_before':exposed,'prior_attempt':prior,'active':True,'result':result,
          'review_due':(datetime.now(timezone.utc)+timedelta(days=2)).isoformat(),'origin':'synthetic' if u.get('synthetic') else 'learner-submitted'}
        store.save('attempt',u['id'],record,conn)
        event(u['id'],'attempt',conn,task_id=t['id'],attempt_id=record['id'])
        event(u['id'],'teaching_decision',conn,attempt_id=record['id'],topic=t['topic'],route=result['route'],reason=result['feedback'])
        return record

@router.post('/attempts/{id}/feedback')
def feedback(id:str,body:Operation,u=Depends(user)):
    a=required('attempt',u['id'],id)
    if not a['active']: fail(409,'这条作答已撤回。')
    t=required('task',u['id'],a['task_id']);c=required('course','shared',a['course_version'])
    l=next(l for l in c['lessons'] if l['week']==teaching.TOPICS[t['topic']]['week'])
    # Authored topic core is the bounded teaching context. Raw answers/solutions never enter tutor context.
    data={'task':teaching.public_task(t),'working':a['working'],'answers':a['answers'],'checks':a['result']['checks'],
          'teaching_core':teaching.TOPICS[t['topic']]['routes'],'source_ids':[l['id']],'source_context':{'id':l['id'],'title':l['title'],'excerpt':'\n'.join(b['body'] for b in l['blocks'] if b['role']=='lesson')[:10000]}}
    result=run_model(u['id'],body.request_id,'feedback',id,lambda:model.call('feedback',data))
    with LOCK,store.engine.begin() as conn:
        latest=required('attempt',u['id'],id,conn)
        if not latest['active']: fail(409,'作答已在生成期间撤回，反馈未应用。')
        existing=store.fetch('feedback',u['id'],body.request_id,conn)
        if not existing:
            store.save('feedback',u['id'],{'id':body.request_id,'attempt_id':id,'at':store.now(),'value':result,'label':'AI 建议，尚未独立核实'},conn)
            event(u['id'],'feedback',conn,task_id=t['id'],attempt_id=id)
    return result

@router.post('/attempts/{id}/withdraw')
def withdraw(id:str,body:Withdraw,u=Depends(user)):
    if not body.reason.strip(): fail(422,'请写明更正原因。')
    with LOCK,store.engine.begin() as conn:
        a=required('attempt',u['id'],id,conn);a['active']=False;a['withdrawal_reason']=body.reason;store.save('attempt',u['id'],a,conn)
        event(u['id'],'withdrawal',conn,attempt_id=id,reason=body.reason)
    return {'ok':True}

@router.get('/export')
def export(u=Depends(user)):
    groups={kind:store.listing(kind,u['id']) for kind in ('attempt','event','progress','task','photo','feedback','route','run','legacy-session','teaching-preference','guided-session','guided-check')}
    # This export excludes solutions, so exporting personal evidence is not solution exposure.
    groups['task']=[teaching.public_task(t) for t in groups['task']]
    photos=groups['photo'];groups['photo']=[{k:v for k,v in p.items() if k not in ('path','original_path')} for p in photos]
    md='# ELEC270 学习记录\n\n来源：本机试点；延迟保持未自动推断。\n\n'
    for a in groups['attempt']:
        md+=f'## {a["at"]} · {teaching.TOPICS[a["topic"]]["title"]}\n\n状态：{a["result"]["status"]}'+('（已撤回）' if not a['active'] else '')+'\n\n'+a['working']+'\n\n'+a['result']['feedback']+'\n\n'
        if a['photo_id']: md+=f'![[Photos/{a["photo_id"]}.jpg]]\n\n'
    if groups['guided-check']:
        md+='## 分步教学 / Guided learning\n\n讲解后的检查，不等于独立掌握。 / Guided checks do not establish independent mastery.\n\n'
        for g in groups['guided-check']:
            md+=f'- {g["at"]} · {g["concept_id"]} · {g["language"]} · {g["mode"]} · '+('符合判据 / Check passed' if g['result']['passed'] else '待核对 / Needs review')+'\n'
    blob=io.BytesIO()
    with zipfile.ZipFile(blob,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('ELEC270 学习记录.md',md)
        z.writestr('Maintenance/Learning/record.json',json.dumps(skill_record(groups, u.get('synthetic',False)),ensure_ascii=False,indent=2))
        z.writestr('Maintenance/pilot-record-v1.json',json.dumps({'schema':'study-studio-pilot-v1','exported_at':store.now(),**groups},ensure_ascii=False,indent=2))
        for p in photos: z.write(p['path'],'Photos/'+p['id']+'.jpg')
        for p in groups['progress']: z.writestr('Notes/'+p['id']+'.md',p['notes'])
        for record in groups['legacy-session']: z.writestr('Maintenance/Legacy/'+record['id']+'.json',json.dumps(record,ensure_ascii=False,indent=2))
        z.writestr('README.md','# ELEC270 个人导出\n\n可解压到单独的 Obsidian 文件夹。包含个人证据、照片与笔记，不含题目解答。原始 JSON 为 Pilot v1 格式，同时附带 Skill V1 格式的学习记录快照。')
    return Response(blob.getvalue(),media_type='application/zip',headers={'Content-Disposition':'attachment; filename="ELEC270-learning-record.zip"'})

@router.delete('/my-data')
def delete_data(u=Depends(user)):
    with LOCK,store.engine.begin() as conn:
        photos=store.listing('photo',u['id'],conn)
        conn.execute(delete(store.records).where(store.records.c.owner==u['id']))
    for p in photos:
        for key in ('path','original_path'):
            if p.get(key): Path(p[key]).unlink(missing_ok=True)
    return {'ok':True}


# Guided checks have their own evidence type and never change independent-task summaries.
def teaching_language(owner,conn=None):
    return (store.fetch('teaching-preference',owner,'language',conn) or {}).get('language','zh-CN')

def guided_session(owner,conn=None):
    s=required('guided-session',owner,'ramps',conn)
    if s['content_version']!=guided.VERSION: fail(409,'教学版本已更新，请联系课程所有者。 / Lesson version changed; contact the course owner.')
    return s

@router.get('/learning/ramps')
def get_guided(u=Depends(user)):
    s=store.fetch('guided-session',u['id'],'ramps')
    return {'language':teaching_language(u['id']),'lesson':guided.present(guided_session(u['id']),teaching_language(u['id'])) if s else None}

@router.put('/learning/preferences')
def teaching_preferences(body:TeachingPreference,u=Depends(user)):
    with LOCK,store.engine.begin() as conn:
        store.save('teaching-preference',u['id'],{'id':'language','language':body.language,'at':store.now()},conn)
        event(u['id'],'teaching_language_chosen',conn,language=body.language)
    return get_guided(u)

@router.post('/learning/ramps/start')
def start_guided(u=Depends(user)):
    with LOCK,store.engine.begin() as conn:
        s=store.fetch('guided-session',u['id'],'ramps',conn)
        if s is None:
            c=current()
            if not any(l['week']==1 for l in c['lessons']): fail(409,'缺少对应课程。 / Course unit missing.')
            route=(store.fetch('route',u['id'],'ramps',conn) or {}).get('route','visual')
            s=guided.new_session(c['id'],route)
            store.save('guided-session',u['id'],s,conn)
            event(u['id'],'guided_started',conn,content_version=guided.VERSION,course_version=c['id'])
        if s['content_version']!=guided.VERSION: fail(409,'教学版本已更新，请联系课程所有者。 / Lesson version changed; contact the course owner.')
        return guided.present(s,teaching_language(u['id'],conn))

@router.post('/learning/ramps/mode')
def guided_mode(body:GuidedMode,u=Depends(user)):
    with LOCK,store.engine.begin() as conn:
        s=guided_session(u['id'],conn);s.update(mode=body.mode,at=store.now())
        store.save('guided-session',u['id'],s,conn)
        event(u['id'],'guided_mode_chosen',conn,mode=body.mode,check_id=s['check_id'])
        return guided.present(s,teaching_language(u['id'],conn))

@router.post('/learning/ramps/check')
def check_guided(body:GuidedCheck,u=Depends(user)):
    signature=hashlib.sha256(body.model_dump_json().encode()).hexdigest()
    with LOCK,store.engine.begin() as conn:
        s=guided_session(u['id'],conn);language=teaching_language(u['id'],conn)
        old=store.fetch('guided-check',u['id'],body.request_id,conn)
        if old:
            if old['signature']!=signature: fail(409,'请求编号已用于其他作答。 / Request ID already used.')
            return {'check':old,'lesson':guided.present(s,language)}
        if s['step']==3 or s['check_id']!=body.check_id or s.get('result'):
            fail(409,'小检查已变化或已提交，请载入当前进度。 / Check changed or already submitted; reload your progress.')
        try: result=guided.assess(s['step'],s['variant'],body.number,body.choice)
        except ValueError as e:
            fail(422,'请选择理由并输入数值或简单算式（如 3/2）。 / Choose a reason and enter a number or simple arithmetic (e.g. 3/2).')
        record={'id':body.request_id,'signature':signature,'check_id':body.check_id,'concept_id':guided.CONCEPTS[s['step']],
                'step':s['step'],'variant':s['variant'],'mode':s['mode'],'language':language,
                'course_version':s['course_version'],'content_version':s['content_version'],'translation_version':guided.TRANSLATION_VERSION,
                'number':body.number,'choice':body.choice,'result':result,'at':store.now(),
                'checkpoint':guided.present(s,language)['checkpoint'],'origin':'synthetic' if u.get('synthetic') else 'learner-submitted'}
        store.save('guided-check',u['id'],record,conn)
        s.update(result=result,at=store.now());store.save('guided-session',u['id'],s,conn)
        event(u['id'],'guided_checked',conn,check_id=body.check_id,concept_id=record['concept_id'],passed=result['passed'],evidence='guided-check')
        return {'check':record,'lesson':guided.present(s,language)}

@router.post('/learning/ramps/next')
def next_guided(body:GuidedNext,u=Depends(user)):
    with LOCK,store.engine.begin() as conn:
        s=guided_session(u['id'],conn)
        if s['step']==3 or s['check_id']!=body.check_id or not s.get('result'):
            fail(409,'请先完成当前小检查。 / Complete the current checkpoint first.')
        result=s['result']
        if result['passed']:
            s.update(step=s['step']+1,variant=0)
        else:
            if s['variant']>=23: fail(409,'本节已核查的小题已用完，可继续阅读或尝试独立练习。 / No unused checks remain; review the lesson or try independent practice.')
            s['variant']+=1
            if body.use_suggestion: s['mode']=result['suggested_mode']
        s.update(check_id=store.uid(),result=None,at=store.now())
        store.save('guided-session',u['id'],s,conn)
        event(u['id'],'guided_transition',conn,step=s['step'],mode=s['mode'],completed=s['step']==3,
              reason='check_passed' if result['passed'] else result['feedback_code'],from_check=body.check_id)
        return guided.present(s,teaching_language(u['id'],conn))

@router.get('/learning/history')
def guided_history(u=Depends(user)):
    return sorted(store.listing('guided-check',u['id']),key=lambda r:r['at'])
