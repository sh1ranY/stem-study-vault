"""Isolated pilot integration tests. Provider calls are explicitly mocked; no live inference."""
import os
import tempfile
PILOT_TEMP=tempfile.TemporaryDirectory()
os.environ['STUDIO_DATA_DIR']=PILOT_TEMP.name
os.environ['STUDIO_DATABASE_URL']='sqlite:///'+PILOT_TEMP.name+'/pilot.sqlite3'
import io
import json
import math
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from PIL import Image
from backend import app
from backend.pilot import store, teaching, model
from backend.pilot.import_course import Importer
from sqlalchemy import delete

class PilotTests(unittest.TestCase):
    def setUp(self):
        self.env=patch.dict(os.environ,{'OPENAI_API_KEY':'','STUDIO_MODEL':'','STUDIO_VISION_MODEL':''});self.env.start()
        with store.engine.begin() as c: c.execute(delete(store.records))
        self.client=TestClient(app.app)
        self.lesson_ids=['week1','week2','week3']
        course={'id':'fixture-v1','title':'ELEC270 fixture','imported_at':store.now(),'lessons':[{'id':f'week{i}','week':i,'title':'Fixture '+str(i),'source_hash':'abc','blocks':[{'id':f'b{i}','role':'lesson','body':'Ramp convolution Fourier definitions.'},{'id':f's{i}','role':'solution','title':'完整解答','body':'SECRET SOLUTION '+str(i)}]} for i in range(1,4)],'assets':[],'warnings':[],'legacy_records':[]}
        store.save('course','shared',course);store.save('config','shared',{'id':'current-course','version':'fixture-v1'})
        r=self.client.post('/api/pilot/auth/register',json={'name':'Owner','password':'safe-test-password'});self.assertEqual(r.status_code,200);self.owner=r.json()['id']
    def tearDown(self): self.client.close();self.env.stop()
    def make(self,topic='ramps',phase='practice',key='new-task-0001'):
        r=self.client.post('/api/pilot/tasks',json={'topic':topic,'phase':phase,'request_id':key});self.assertEqual(r.status_code,200);return r.json()
    def payload(self,t,key='attempt-0001',**changes):
        internal=store.fetch('task',self.owner,t['id']);v={'task_id':t['id'],'request_id':key,'answers':{f['id']:str(f['answer']) for f in internal['fields']},'working':'I calculate the change in slope, then the remaining height.','confirmed':True};v.update(changes);return v
    def submit(self,t,**kw): return self.client.post('/api/pilot/attempts',json=self.payload(t,**kw))
    def state(self): return self.client.get('/api/pilot/state').json()
    def picture(self,t):
        b=io.BytesIO();Image.new('RGB',(100,100),'white').save(b,'PNG')
        r=self.client.post('/api/pilot/photos/'+t['id'],files={'file':('working.png',b.getvalue(),'image/png')});self.assertEqual(r.status_code,200);return r.json()
    def learner(self):
        token=self.client.post('/api/pilot/auth/invite').json()['invite'];c=TestClient(app.app)
        self.assertEqual(c.post('/api/pilot/auth/register',json={'name':'Learner','password':'second-user-password','invite':token}).status_code,200)
        return c,token
    def test_auth_cookie_and_invite_boundaries(self):
        c=TestClient(app.app)
        self.assertEqual(c.get('/api/pilot/state').status_code,401)
        self.assertEqual(c.post('/api/pilot/auth/register',json={'name':'NoInvite','password':'safe-test-password'}).status_code,403)
        other,invite=self.learner()
        self.assertEqual(other.post('/api/pilot/auth/invite').status_code,403)
        self.assertEqual(c.post('/api/pilot/auth/register',json={'name':'Reuse','password':'safe-test-password','invite':invite}).status_code,403)
        self.assertIn('HttpOnly',self.client.post('/api/pilot/auth/login',json={'name':'Owner','password':'safe-test-password'}).headers['set-cookie'])
        c.close();other.close()
    def test_cross_origin_rejected(self):
        self.assertEqual(self.client.post('/api/pilot/tasks',json={},headers={'Origin':'https://untrusted.example'}).status_code,403)
    def test_source_solutions_hidden_and_not_searchable(self):
        text=self.client.get('/api/pilot/lessons/week1').text;self.assertNotIn('SECRET SOLUTION',text)
        self.assertEqual(self.client.post('/api/pilot/search',json={'query':'SECRET'}).json(),[])
        r=self.client.post('/api/pilot/reveal',json={'lesson_id':'week1','block_id':'s1'});self.assertIn('SECRET',r.json()['body'])
        self.assertIn('SECRET',self.client.get('/api/pilot/lessons/week1').text)
        other,_=self.learner();self.assertNotIn('SECRET SOLUTION',other.get('/api/pilot/lessons/week1').text);other.close()
    def test_task_idempotency_and_no_answer_fields(self):
        t=self.make();self.assertNotIn('"answer"',json.dumps(t));self.assertNotIn('solution',t)
        self.assertEqual(self.make()['id'],t['id']);self.assertEqual(len(self.state()['tasks']),1)
        self.assertEqual(self.client.post('/api/pilot/tasks',json={'topic':'fourier','phase':'practice','request_id':'new-task-0001'}).status_code,409)
    def test_attempt_idempotency_and_persistence(self):
        t=self.make();r=self.submit(t);self.assertEqual(r.status_code,200);self.assertEqual(r.json()['result']['status'],'independent')
        self.assertEqual(self.submit(t).json()['id'],r.json()['id']);self.assertEqual(len(self.state()['attempts']),1)
        self.assertEqual(self.submit(t,working='different').status_code,409)
        with TestClient(app.app) as c:
            c.cookies.update(self.client.cookies);self.assertEqual(len(c.get('/api/pilot/state').json()['attempts']),1)
    def test_confirmation_is_required(self):
        t=self.make();self.assertEqual(self.submit(t,confirmed=False).status_code,422);self.assertEqual(self.submit(t,working=' ').status_code,422)
        self.assertEqual(len(self.state()['attempts']),0)
    def test_hint_and_retry_are_not_independent(self):
        t=self.make();self.client.post('/api/pilot/reveal',json={'task_id':t['id'],'kind':'hint'})
        self.assertEqual(self.submit(t).json()['result']['status'],'supported')
        fresh=self.make(key='new-task-0002');self.assertEqual(self.submit(fresh,key='attempt-0002').json()['result']['status'],'independent')
        self.assertEqual(self.submit(fresh,key='attempt-0003').json()['result']['status'],'supported')
    def test_self_reported_prior_exposure(self):
        t=self.make();self.assertEqual(self.submit(t,prior_seen=True).json()['result']['status'],'supported')
    def test_withdrawal_recomputes_summary_but_keeps_exposure(self):
        t=self.make();a=self.submit(t).json()
        self.assertEqual(self.client.post('/api/pilot/attempts/'+a['id']+'/withdraw',json={'reason':'Photo transcription was incorrect.'}).status_code,200)
        s=self.state();self.assertEqual(s['summaries']['ramps']['independent'],0);self.assertEqual(s['summaries']['ramps']['status'],'unknown')
        self.assertEqual(self.submit(t,key='attempt-0002').json()['result']['status'],'supported')
    def test_photo_access_ownership_and_confirmation(self):
        t=self.make();p=self.picture(t);self.assertNotIn('path',p);self.assertNotIn('original_path',self.state()['photos'][0])
        self.assertEqual(self.client.get('/api/pilot/photos/'+p['id']).status_code,200)
        other,_=self.learner();self.assertEqual(other.get('/api/pilot/photos/'+p['id']).status_code,404)
        self.assertEqual(other.post('/api/pilot/attempts',json=self.payload(t,photo_id=p['id'])).status_code,404)
        self.assertEqual(self.submit(t,photo_id=p['id']).status_code,200);other.close()
    def test_photo_cannot_cross_task(self):
        t=self.make();p=self.picture(t);t2=self.make(key='new-task-0002')
        self.assertEqual(self.submit(t2,photo_id=p['id']).status_code,422)
    def test_missing_provider_does_not_fake_recognition(self):
        t=self.make();p=self.picture(t)
        with patch.object(model,'call') as call:
            r=self.client.post('/api/pilot/photos/'+p['id']+'/transcribe',json={'request_id':'ocr-request-0001'})
            self.assertEqual(r.status_code,409);call.assert_not_called()
        self.assertIsNone(self.state()['photos'][0]['transcription']);self.assertEqual(self.state()['runs'],[])
    def test_mock_photo_flow_and_revised_text(self):
        t=self.make();p=self.picture(t);recognized={'working':'A questionable - sign','fields':[{'id':'A','value':'-3'}],'uncertainties':['A 的符号不清楚']}
        with patch.object(model,'available',return_value=True),patch.object(model,'call',return_value=(recognized,{'usage':{'total_tokens':10}})) as call:
            for _ in range(2):
                self.assertEqual(self.client.post('/api/pilot/photos/'+p['id']+'/transcribe',json={'request_id':'ocr-request-0001'}).status_code,200)
            self.assertEqual(call.call_count,1)
        a=self.submit(t,photo_id=p['id'],working='A = +3; I corrected the OCR sign.').json()
        self.assertEqual(a['recognition']['working'],'A questionable - sign');self.assertIn('+3',a['working'])
    def test_model_failure_records_no_retry(self):
        t=self.make();p=self.picture(t)
        with patch.object(model,'available',return_value=True),patch.object(model,'call',side_effect=ValueError('failed')) as call:
            self.assertEqual(self.client.post('/api/pilot/photos/'+p['id']+'/transcribe',json={'request_id':'ocr-request-0001'}).status_code,502)
            self.assertEqual(self.client.post('/api/pilot/photos/'+p['id']+'/transcribe',json={'request_id':'ocr-request-0001'}).status_code,409)
            self.assertEqual(call.call_count,1)
        self.assertEqual(self.state()['runs'][0]['status'],'failed');self.assertIsNone(self.state()['photos'][0]['transcription'])
    def test_model_feedback_is_separate_from_verdict_and_owner(self):
        t=self.make();a=self.submit(t).json();other,_=self.learner()
        self.assertEqual(other.post('/api/pilot/attempts/'+a['id']+'/feedback',json={'request_id':'feedback-0001'}).status_code,404)
        with patch.object(model,'available',return_value=True),patch.object(model,'call',return_value=({'feedback':'Check a switching boundary.','uncertainties':[],'source_ids':['week1']},{})):
            self.assertEqual(self.client.post('/api/pilot/attempts/'+a['id']+'/feedback',json={'request_id':'feedback-0001'}).status_code,200)
        self.assertEqual(self.state()['attempts'][0]['result'],a['result']);self.assertEqual(len(self.state()['feedback']),1);other.close()
    def test_export_and_delete_only_current_owner(self):
        t=self.make();p=self.picture(t);self.submit(t,photo_id=p['id'])
        other,_=self.learner();other.post('/api/pilot/tasks',json={'topic':'fourier','phase':'practice','request_id':'other-task-0001'})
        r=self.client.get('/api/pilot/export');self.assertEqual(r.status_code,200)
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            import importlib.util
            spec=importlib.util.spec_from_file_location('learning_tools',Path(__file__).resolve().parents[3]/'skills/stem-study-vault/scripts/learning_tools.py');validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(validator)
            validator.validate(json.loads(z.read('Maintenance/Learning/record.json')))
            record=json.loads(z.read('Maintenance/pilot-record-v1.json'));self.assertEqual(len(record['attempt']),1);self.assertNotIn('solution',record['task'][0]);self.assertIn('Photos/'+p['id']+'.jpg',z.namelist())
        self.assertEqual(self.client.delete('/api/pilot/my-data').status_code,200);self.assertEqual(len(self.state()['attempts']),0)
        self.assertEqual(len(other.get('/api/pilot/state').json()['tasks']),1);self.assertEqual(self.client.get('/api/pilot/photos/'+p['id']).status_code,404);other.close()
    def test_numeric_attack_and_unknown_fields_do_not_write(self):
        t=self.make();data=self.payload(t);data['answers']['A']='__import__("os")'
        self.assertEqual(self.client.post('/api/pilot/attempts',json=data).status_code,422);self.assertEqual(self.state()['attempts'],[])
    def test_review_uses_different_parameters(self):
        for topic in teaching.TOPICS:
            prompts=[teaching.task(topic,phase,n)['prompt'] for phase in ('diagnosis','practice','review') for n in range(24)]
            self.assertEqual(len(prompts),len(set(prompts)))
    def test_all_ramp_families_reconstruct_actual_waveform(self):
        for phase in ('diagnosis','practice','review'):
            for n in range(24):
                t=teaching.task('ramps',phase,n);f={x['id']:x['answer'] for x in t['fields']};k=n+1+(24 if phase=='review' else 0);a=k if phase=='diagnosis' else k+2;b=a+(3 if phase=='diagnosis' else 4);c=b+3;m=2 if phase=='diagnosis' else 3
                for time in (a-1,a,(a+b)/2,b,c-0.1,c,c+2):
                    actual=f['A']*max(time-a,0)+f['B']*max(time-b,0)+f['C']*(time>=c)
                    expected=0 if time<a or time>=c else m*min(time-a,b-a)
                    self.assertAlmostEqual(actual,expected)
    def test_known_convolution_and_fourier_cases(self):
        c=teaching.task('convolution','practice',0);fields={f['id']:f['answer'] for f in c['fields']}
        # x: height2 width3, h: height3 width3 at t3.5 -> overlap [0.5,3], area15.
        self.assertEqual(fields,{'left':0.5,'right':3.5,'L':0.5,'U':3,'y':15})
        f=teaching.task('fourier','practice',0);fields={x['id']:x['answer'] for x in f['fields']}
        self.assertEqual(fields['area'],6);self.assertEqual(fields['a0'],1);self.assertAlmostEqual(fields['omega'],1/3);self.assertEqual(fields['b1'],0)
    def test_legacy_api_requires_owner_once_accounts_exist(self):
        other,_=self.learner()
        self.assertEqual(other.get('/api/sessions').status_code,403)
        self.assertEqual(self.client.get('/api/sessions').status_code,200)
        other.close()
    def test_delete_during_model_call_does_not_restore_private_data(self):
        t=self.make();p=self.picture(t)
        def finish(*args):
            from backend.pilot.routes import delete_data
            delete_data(store.fetch('user','auth',self.owner))
            return {'working':'test','fields':[],'uncertainties':[]},{}
        with patch.object(model,'available',return_value=True),patch.object(model,'call',side_effect=finish):
            self.assertEqual(self.client.post('/api/pilot/photos/'+p['id']+'/transcribe',json={'request_id':'ocr-request-delete'}).status_code,409)
        self.assertEqual(self.state()['runs'],[]);self.assertEqual(self.state()['photos'],[])
    def test_legacy_import_is_idempotent_and_unassessed(self):
        from backend.pilot.migrate_legacy import import_legacy
        import sqlite3
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'old.sqlite3'
            with sqlite3.connect(path) as db:
                db.execute('CREATE TABLE records (kind TEXT,id TEXT,body TEXT)')
                db.execute('INSERT INTO records VALUES (?,?,?)',('session','old-1',json.dumps({'id':'old-1','unit':{'title':'Legacy demo'},'attempts':[{'working':'old demo'}]})))
            self.assertEqual(import_legacy(self.owner,path),1);self.assertEqual(import_legacy(self.owner,path),1)
            self.assertEqual(len(store.listing('legacy-session',self.owner)),1);self.assertEqual(self.state()['attempts'],[])
            self.assertEqual(self.client.get('/api/pilot/legacy').json()[0]['attempt_count'],1)
    def test_empty_import_cannot_replace_existing_course(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): Importer(Path(d),Path(d)).run()
        self.assertEqual(store.fetch('config','shared','current-course')['version'],'fixture-v1')
    def test_bad_images_are_rejected(self):
        t=self.make();r=self.client.post('/api/pilot/photos/'+t['id'],files={'file':('not.jpg',b'not an image','image/jpeg')});self.assertEqual(r.status_code,422)
    def test_provider_contract_rejects_truncation_and_unprovided_citations(self):
        with patch.dict(os.environ,{'OPENAI_API_KEY':'dummy','STUDIO_VISION_MODEL':'test-model'}),patch.object(model.httpx,'Client') as client:
            response=client.return_value.__enter__.return_value.post.return_value;response.status_code=200
            response.json.return_value={'status':'incomplete','output':[]}
            with self.assertRaises(ValueError): model.call('feedback',{'source_ids':['week1']})
            response.json.return_value={'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':json.dumps({'feedback':'text','uncertainties':[],'source_ids':['invented']})}]}]}
            with self.assertRaises(ValueError): model.call('feedback',{'source_ids':['week1']})
            self.assertFalse(client.return_value.__enter__.return_value.post.call_args.kwargs['json']['store'])

class ImportTests(unittest.TestCase):
    def test_snapshot_dedup_gates_links_and_idempotent_reimport(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);vault=root/'vault';course=vault/'10 Y2上学期/ELEC270 信号与系统';weeks=course/'Weeks';assets=course/'Assets';desktop=root/'desktop'
            for p in (weeks,assets,desktop):p.mkdir(parents=True)
            (assets/'plot.png').write_bytes(b'fixture-image');(desktop/'Lecture1.pdf').write_bytes(b'fixture-pdf');(course/'Sources').mkdir();(course/'Sources'/'Lecture1.pdf').write_bytes(b'fixture-pdf')
            (weeks/'Week 01 - test.md').write_text('# Test\n\n## Ramp\nDefinition.\n\n![[10 Y2上学期/ELEC270 信号与系统/Assets/plot.png]]\n\n> [!hint]- 提示\n> use time\n\n> [!success]- 完整解答\n> SECRET\n\n## More\nReading text.')
            first=Importer(vault,desktop).run();second=Importer(vault,desktop).run();self.assertEqual(first['version'],second['version']);self.assertEqual(first['assets'],2);self.assertEqual(first['locations'],3);self.assertEqual(first['hidden_blocks'],2);self.assertEqual(first['warnings'],[])
            saved=store.fetch('course','shared',first['version']);plain='\n'.join(b['body'] for b in saved['lessons'][0]['blocks'] if b['role']=='lesson');self.assertNotIn('SECRET',plain);self.assertIn('/api/pilot/assets/',plain)
            original=(weeks/'Week 01 - test.md').read_text();self.assertIn('[[',original)

if __name__=='__main__':unittest.main()
