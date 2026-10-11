"""Guided teaching contracts: state transitions, evidence provenance and bilingual identity."""
import io
import json
import math
import unittest
import zipfile
import test_pilot as pilot_tests
from backend.pilot import guided, store


class GuidedTests(unittest.TestCase):
    setUp=pilot_tests.PilotTests.setUp
    tearDown=pilot_tests.PilotTests.tearDown
    learner=pilot_tests.PilotTests.learner

    def start(self):
        r=self.client.post('/api/pilot/learning/ramps/start');self.assertEqual(r.status_code,200);return r.json()

    def check(self,s,number=None,choice=None,key='guided-check-0001'):
        q=guided.checkpoint(s['step'],s['variant'])
        return self.client.post('/api/pilot/learning/ramps/check',json={'check_id':s['check_id'],'request_id':key,'number':str(q['answer']) if number is None else number,'choice':choice or q['correct']})

    def next(self,s,**kwargs):
        return self.client.post('/api/pilot/learning/ramps/next',json={'check_id':s['check_id'],**kwargs})

    def test_start_resume_and_no_answer_leak(self):
        self.assertIsNone(self.client.get('/api/pilot/learning/ramps').json()['lesson'])
        s=self.start();self.assertEqual(self.start()['check_id'],s['check_id'])
        self.assertEqual(s['concept_id'],'shifted-ramp')
        self.assertNotIn('answer',s['checkpoint']);self.assertNotIn('correct',s['checkpoint'])
        self.assertEqual(self.next(s).status_code,409)

    def test_pass_each_step_and_handoff_keeps_mastery_unknown(self):
        s=self.start()
        for i in range(3):
            r=self.check(s,key='guided-pass-'+str(i));self.assertEqual(r.status_code,200)
            self.assertTrue(r.json()['check']['result']['passed'])
            s=self.next(s).json();self.assertEqual(s['step'],i+1)
        self.assertTrue(s['complete']);self.assertNotIn('checkpoint',s);self.assertEqual(len(s['review']),3)
        self.assertEqual(self.next(s).status_code,409)
        self.assertEqual(self.client.get('/api/pilot/state').json()['summaries']['ramps']['status'],'unknown')
        records=self.client.get('/api/pilot/learning/history').json()
        self.assertEqual(len(records),3)
        self.assertTrue(all(r['result']['evidence']=='guided-check' for r in records))

    def test_wrong_reason_and_route_suggestion_then_fresh_parameters(self):
        s=self.start();r=self.check(s,choice='identity')
        result=r.json()['check']['result'];self.assertTrue(result['number_ok']);self.assertFalse(result['passed'])
        self.assertEqual(result['suggested_mode'],'bridge')
        newer=self.next(s).json();self.assertEqual(newer['step'],0);self.assertEqual(newer['variant'],1)
        self.assertEqual(newer['mode'],'bridge');self.assertNotEqual(newer['check_id'],s['check_id'])
        self.assertNotEqual(newer['checkpoint']['prompt'],s['checkpoint']['prompt'])
        self.assertEqual(self.next(s).status_code,409)
        self.assertEqual(self.check(s,key='stale-request-1').status_code,409)

    def test_keep_own_route_on_retry(self):
        s=self.start();self.check(s,choice='identity')
        s=self.next(s,use_suggestion=False).json();self.assertEqual(s['mode'],'visual')

    def test_language_is_separate_from_progress_and_answer_time_evidence(self):
        s=self.start();self.check(s)
        r=self.client.put('/api/pilot/learning/preferences',json={'language':'en'}).json()
        self.assertEqual(r['lesson']['check_id'],s['check_id']);self.assertEqual(r['lesson']['step'],0)
        self.assertEqual(r['lesson']['title'],'Read a shifted ramp')
        self.assertTrue(r['lesson']['result']['feedback'].startswith('Both'))
        old=self.client.get('/api/pilot/learning/history').json()[0]
        self.assertEqual(old['language'],'zh-CN')
        s=self.next(s).json();self.assertEqual(s['language'],'en');self.check(s,key='english-check-1')
        self.assertEqual(self.client.get('/api/pilot/learning/history').json()[-1]['language'],'en')
        self.assertEqual(self.client.put('/api/pilot/learning/preferences',json={'language':'xx'}).status_code,422)

    def test_mode_change_keeps_question_and_check_identity(self):
        s=self.start()
        for mode in guided.MODES:
            r=self.client.post('/api/pilot/learning/ramps/mode',json={'mode':mode}).json()
            self.assertEqual(r['check_id'],s['check_id']);self.assertEqual(r['checkpoint'],s['checkpoint'])
            self.assertEqual(r['body'],guided.CONTENT[0]['routes'][mode]['zh-CN'])

    def test_duplicate_submission_is_idempotent_conflicting_retry_rejected(self):
        s=self.start();first=self.check(s).json();self.assertEqual(self.check(s).json(),first)
        self.assertEqual(len(store.listing('guided-check',self.owner)),1)
        self.assertEqual(self.check(s,number='99').status_code,409)
        self.assertEqual(self.check(s,key='other-request-1').status_code,409)

    def test_invalid_input_cannot_advance_or_persist(self):
        s=self.start()
        for number in ('__import__("os")','1/0','NaN','1e99'):
            self.assertEqual(self.check(s,number=number).status_code,422)
        self.assertEqual(self.check(s,choice='invented').status_code,422)
        self.assertEqual(store.listing('guided-check',self.owner),[])
        self.assertEqual(self.next(s).status_code,409)
        self.assertEqual(self.check(s,number='2−2').status_code,200)

    def test_private_history_preferences_and_submission(self):
        s=self.start();self.check(s);other,_=self.learner()
        self.assertIsNone(other.get('/api/pilot/learning/ramps').json()['lesson'])
        self.assertEqual(other.get('/api/pilot/learning/history').json(),[])
        other.post('/api/pilot/learning/ramps/start')
        self.assertEqual(other.post('/api/pilot/learning/ramps/check',json={'check_id':s['check_id'],'request_id':'attack-check-1','number':'0','choice':'definition'}).status_code,409)
        other.put('/api/pilot/learning/preferences',json={'language':'en'})
        self.assertEqual(self.client.get('/api/pilot/learning/ramps').json()['language'],'zh-CN');other.close()

    def test_course_snapshot_survives_new_import(self):
        s=self.start();store.save('config','shared',{'id':'current-course','version':'new-import'})
        r=self.check(s).json()['check'];self.assertEqual(r['course_version'],'fixture-v1')

    def test_export_and_delete_include_guided_data(self):
        s=self.start();self.check(s);self.client.put('/api/pilot/learning/preferences',json={'language':'en'})
        z=zipfile.ZipFile(io.BytesIO(self.client.get('/api/pilot/export').content))
        r=json.loads(z.read('Maintenance/pilot-record-v1.json'))
        self.assertEqual(len(r['guided-check']),1);self.assertEqual(len(r['guided-session']),1)
        self.assertEqual(r['teaching-preference'][0]['language'],'en')
        self.assertNotIn('answer',r['guided-check'][0]['checkpoint'])
        self.assertIn('Guided learning',z.read('ELEC270 学习记录.md').decode())
        self.client.delete('/api/pilot/my-data')
        self.assertEqual(self.client.get('/api/pilot/learning/history').json(),[])
        self.assertIsNone(self.client.get('/api/pilot/learning/ramps').json()['lesson'])
        self.assertEqual(self.client.get('/api/pilot/learning/ramps').json()['language'],'zh-CN')

    def test_retry_limit_and_old_content_version_guard(self):
        s=self.start();internal=store.fetch('guided-session',self.owner,'ramps')
        internal['variant']=23;store.save('guided-session',self.owner,internal)
        s=self.client.get('/api/pilot/learning/ramps').json()['lesson'];self.check(s,choice='identity')
        self.assertEqual(self.next(s).status_code,409)
        internal['content_version']='future-version';store.save('guided-session',self.owner,internal)
        self.assertEqual(self.client.get('/api/pilot/learning/ramps').status_code,409)

    def test_all_authored_variants_obey_definitions_and_locales_share_keys(self):
        for step in range(3):
            for v in range(24):
                q=guided.checkpoint(step,v)
                a=2+v;b=a+3+v%2;m=2+v%3
                if step==0:
                    t=a-(1+v%3) if v%2==0 else a+2+v%3
                    expected=t-a if t>=a else 0
                elif step==1:
                    t=b+2;expected=m*max(t-a,0)-m*max(t-b,0)
                else:
                    # Required coefficient must zero the entire signal at and after reset.
                    expected=q['answer']
                    for t in (b+2,b+2.01,b+100):
                        self.assertAlmostEqual(m*max(t-a,0)-m*max(t-b,0)+expected,0)
                self.assertAlmostEqual(q['answer'],expected)
                self.assertTrue(guided.assess(step,v,str(expected),q['correct'])['passed'])
                for lang in guided.LANGUAGES:
                    for mode in guided.MODES:
                        s=guided.new_session('test');s.update(step=step,variant=v,mode=mode)
                        p=guided.present(s,lang)
                        self.assertTrue(p['body']);self.assertEqual([c['id'] for c in p['checkpoint']['choices']],q['choices'])
        self.assertEqual(guided.assess(1,0,'999','gap')['suggested_mode'],'algebra')
        self.assertEqual(guided.assess(1,0,'6','zero')['suggested_mode'],'visual')

if __name__=='__main__': unittest.main()
