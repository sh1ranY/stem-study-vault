"""Presentation identity, draft isolation/conflicts and continuation decisions."""
import io
import json
import zipfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import test_pilot as fixtures
from backend.pilot import teaching, localization, store, model

class WorkspaceTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    make=fixtures.PilotTests.make
    payload=fixtures.PilotTests.payload
    submit=fixtures.PilotTests.submit
    state=fixtures.PilotTests.state
    learner=fixtures.PilotTests.learner
    picture=fixtures.PilotTests.picture

    def draft(self,t,**changes):
        value={'revision':0,'answers':{'A':'3'},'working':'Unfinished explanation','photo_id':None,'prior_seen':False};value.update(changes)
        return self.client.put('/api/pilot/drafts/'+t['id'],json=value)

    def english(self):
        self.assertEqual(self.client.put('/api/pilot/learning/preferences',json={'language':'en'}).status_code,200)

    def test_all_translation_variants_keep_identity_answers_and_redaction(self):
        for topic in teaching.TOPICS:
            for phase in ('diagnosis','practice','review'):
                for n in range(24):
                    original=teaching.task(topic,phase,n);en=localization.task(original,'en')
                    self.assertEqual(en['id'],original['id'])
                    self.assertEqual([(f['id'],f['answer']) for f in en['fields']],[(f['id'],f['answer']) for f in original['fields']])
                    self.assertNotEqual(en['prompt'],original['prompt'])
                    public=localization.public_task(original,'en')
                    self.assertNotIn('solution',public);self.assertNotIn('answer',public['fields'][0])
                    self.assertTrue(teaching.evaluate(en,{f['id']:str(f['answer']) for f in en['fields']},False,False)['passed'])
                    self.assertNotIn('language',original)

    def test_language_switch_preserves_historical_evidence(self):
        t=self.make();a=self.submit(t).json();self.english()
        self.assertEqual(self.client.get('/api/pilot/status').json()['language'],'en')
        self.assertEqual(self.client.get('/api/pilot/course').json()['topics']['ramps']['title'],'Basic signals and ramp construction')
        s=self.state();self.assertEqual(s['tasks'][0]['id'],t['id']);self.assertIn('All checked answers',s['attempts'][0]['result']['feedback'])
        self.assertEqual(store.fetch('attempt',self.owner,a['id'])['language'],'zh-CN')
        self.assertIn('本题',store.fetch('attempt',self.owner,a['id'])['result']['feedback'])
        self.assertIn('Handle',self.client.post('/api/pilot/reveal',json={'task_id':t['id'],'kind':'hint'}).json()['body'])
        self.assertIn('Evaluate',self.client.get('/api/pilot/teaching/ramps?route=bridge').json()['body'])

    def test_english_submission_and_idempotency(self):
        self.english();t=self.make('convolution');a=self.submit(t).json()
        self.assertEqual(a['language'],'en');self.assertEqual(a['result']['status'],'independent')
        self.assertIn('All checked answers',a['result']['feedback']);self.assertEqual(self.submit(t).json()['result'],a['result'])

    def test_draft_restore_privacy_and_no_evidence(self):
        t=self.make();saved=self.draft(t).json();self.assertEqual(saved['revision'],1)
        self.assertEqual(self.client.get('/api/pilot/drafts/'+t['id']).json(),saved)
        self.assertEqual(self.state()['drafts'],[saved]);self.assertEqual(self.state()['attempts'],[])
        other,_=self.learner();other.post('/api/pilot/tasks',json={'topic':'ramps','phase':'practice','request_id':'other-task-1'})
        self.assertIsNone(other.get('/api/pilot/drafts/'+t['id']).json());self.assertEqual(other.get('/api/pilot/state').json()['drafts'],[]);other.close()

    def test_draft_conflict_and_safe_replay(self):
        t=self.make();first=self.draft(t).json();self.assertEqual(self.draft(t).json(),first)
        self.assertEqual(self.draft(t,working='Conflicting').status_code,409)
        second=self.draft(t,revision=1,working='New version').json();self.assertEqual(second['revision'],2)
        self.assertEqual(self.client.get('/api/pilot/drafts/'+t['id']).json()['working'],'New version')

    def test_draft_photo_and_field_validation(self):
        t=self.make();other=self.make(key='new-task-0002');photo=self.picture(other)
        self.assertEqual(self.draft(t,photo_id=photo['id']).status_code,422)
        self.assertEqual(self.draft(t,answers={'injected':'0'}).status_code,422)
        self.assertEqual(self.draft(t,answers={'A':'x'*201}).status_code,422)
        self.assertEqual(self.draft(t,revision=-1).status_code,422)

    def test_draft_export_delete_separate_from_evidence(self):
        t=self.make();self.draft(t)
        z=zipfile.ZipFile(io.BytesIO(self.client.get('/api/pilot/export').content));data=json.loads(z.read('Maintenance/pilot-record-v1.json'))
        self.assertEqual(len(data['answer-draft']),1);self.assertEqual(data['attempt'],[]);self.assertNotIn('answer',data['task'][0]['fields'][0])
        self.client.delete('/api/pilot/my-data');self.assertEqual(self.state()['drafts'],[])

    def test_overview_continuation_failure_due_and_withdrawal(self):
        overview=lambda:self.client.get('/api/pilot/learning/overview').json()['topics'][0]
        self.assertEqual(overview()['action'],'diagnosis')
        t=self.make();self.assertEqual(overview()['action'],'resume');self.draft(t);self.assertTrue(overview()['draft_saved'])
        bad=self.submit(t,answers={f['id']:'999' for f in t['fields']}).json();self.assertEqual(overview()['action'],'revisit')
        self.client.post('/api/pilot/attempts/'+bad['id']+'/withdraw',json={'reason':'Wrong entry'});self.assertEqual(overview()['action'],'diagnosis')
        t=self.make(key='new-task-0002');a=self.submit(t,key='good-attempt-02').json();self.assertEqual(overview()['action'],'practice')
        internal=store.fetch('attempt',self.owner,a['id']);internal['review_due']=(datetime.now(timezone.utc)-timedelta(minutes=1)).isoformat();store.save('attempt',self.owner,internal)
        self.assertEqual(overview()['action'],'review');self.assertEqual(overview()['retention'],'unassessed');self.assertEqual(overview()['latest_attempt_id'],a['id'])

    def test_guided_overview_is_private_and_not_independent(self):
        self.client.post('/api/pilot/learning/ramps/start');row=self.client.get('/api/pilot/learning/overview').json()['topics'][0]
        self.assertEqual(row['action'],'guided');self.assertEqual(row['independent'],0)
        other,_=self.learner();self.assertEqual(other.get('/api/pilot/learning/overview').json()['topics'][0]['action'],'diagnosis');other.close()

    def test_throttle_canonicalises_username(self):
        for i in range(8):self.assertEqual(self.client.post('/api/pilot/auth/login',json={'name':'Owner'+' '*i,'password':'wrong-password'}).status_code,401)
        self.assertEqual(self.client.post('/api/pilot/auth/login',json={'name':' Owner ','password':'wrong-password'}).status_code,429)

    def test_model_language_contract(self):
        class Response:
            status_code=200
            def json(self):return {'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':json.dumps({'working':'original','fields':[],'uncertainties':[]})}]}]}
        with patch.dict('os.environ',{'OPENAI_API_KEY':'synthetic-key','STUDIO_VISION_MODEL':'fixture-model'}),patch('httpx.Client.post',return_value=Response()) as request:
            model.call('transcribe',{'task':{'fields':[]},'language':'en'},b'fixture')
            instructions=request.call_args.kwargs['json']['instructions'];self.assertIn('must be in English',instructions);self.assertIn('Preserve the original language',instructions)
