"""Read-only adapter from pilot evidence to the Skill's Version 1 exchange contract."""
from . import teaching

def skill_record(groups,synthetic=False,course_code="ELEC270"):
    TOPICS=teaching.topics(course_code)
    tasks={t['id']:t for t in groups['task']}; events=[];claims=[];decisions=[]
    observations=sorted(groups['attempt'],key=lambda a:a['at'])
    for a in observations:
        helps=[e for e in groups['event'] if e.get('task_id')==a['task_id'] and e['at']<=a['at'] and e['kind'] in ('hint','solution','feedback')]
        solution=next((e for e in helps if e['kind']=='solution'),None)
        supported=bool(helps) or a['exposure_before']
        support='answer' if solution else 'general' if supported else 'none'
        events.append({'id':a['id'],'task_id':a['task_id'],'response':a['working']+'\n关键数值：'+str(a['answers']),
            'origin':'synthetic' if synthetic else 'attempt','correctness':'correct' if a['result']['passed'] else 'partial' if any(a['result']['checks'].values()) else 'incorrect',
            'reason':a['result']['feedback']+' 评价范围仅为题目关键数值，未认证自由解题过程。','active':a['active'],
            'support':support,'support_text':('已查看完整解答' if solution else '已查看提示 / 过程反馈，或自报曾见原题 / 外部帮助') if supported else '',
            'exposure':'answer_seen' if solution else 'same_question' if a['prior_attempt'] or a['exposure_before'] else 'related_instruction','observed_at':a['at']})
    for topic in TOPICS:
        active=[a for a in observations if a['topic']==topic and a['active']]
        if not active:
            claims.append({'id':'claim-'+topic,'objective_id':topic,'status':'unassessed','scope':'本试点目标尚无有效作答。','evidence_ids':[]});continue
        a=active[-1];status={'independent':'independent','supported':'supported'}.get(a['result']['status'],'observed')
        claims.append({'id':'claim-'+topic,'objective_id':topic,'status':status,'scope':'仅本题关键数值与边界判据；自由推理、整个主题掌握和延迟保持尚未认证。','evidence_ids':[a['id']]})
        # A verification task only becomes a contract object when actually created.
        later=sorted([t for t in tasks.values() if t['topic']==topic and t['created_at']>a['at']],key=lambda t:t['created_at'])
        if later:
            decisions.append({'id':'decision-'+a['id'],'objective_id':topic,'after_event_id':a['id'],'evidence_ids':[a['id']],
                'strategy_id':a['result']['route']+'-v1','change':a['result']['teaching'],'verification_task_id':later[0]['id']})
    return {'schema_version':1,'course_id':course_code,'data_origin':'synthetic' if synthetic else 'learner',
      'objectives':[{'id':k,'description':v['objective']} for k,v in TOPICS.items()],
      'tasks':[{'id':t['id'],'objective_ids':[t['topic']],'kind':{'diagnosis':'diagnosis','practice':'transfer','review':'retention'}[t['phase']], 'version':t['version'],'source_version':t['course_version']} for t in tasks.values()],
      'events':events,'claims':claims,'decisions':decisions,'dimensions':{key:{'summary':summary,'evidence_ids':[]} for key,summary in {
        'prerequisites':'局部前置诊断保存在作答中；未建立完整基础能力量表。','representations':'路径按当前数值证据选择，不归类为固定学习风格。',
        'support':'实际提示、解答曝光及过程反馈另保存在原始事件中。','transfer_retention':'独立性只针对当前新题的数值检查，延迟保持未认证。',
        'self_assessment':'未收集量化信心，不推断自我评价能力。','goals_preferences':'只保存用户主动选择的教学路径；无其他偏好推断。'}.items()}}
