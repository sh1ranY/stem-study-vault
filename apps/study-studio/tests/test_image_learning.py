"""Image unit checks use isolated learner data and never invoke a model API."""
import io
import json
import math
import unittest
import zipfile
from unittest.mock import patch
from fastapi.testclient import TestClient
import test_pilot as pilot_tests
from backend import app
from backend.pilot import catalog, image_learning as lesson, model, store

BASE = '/api/pilot/learning/images'


class ImageLearningTests(unittest.TestCase):
    setUp = pilot_tests.PilotTests.setUp
    tearDown = pilot_tests.PilotTests.tearDown
    learner = pilot_tests.PilotTests.learner

    def start(self, client=None):
        r = (client or self.client).post(BASE+'/start')
        self.assertEqual(r.status_code, 200, r.text)
        return r.json()

    def submit(self, s, index=0, **changes):
        state = s['questions'][index]
        q = lesson.question(state['kind'], state['variant'])
        body = {'revision': s['revision'], 'question_id': state['id'],
                'request_id': 'image-check-'+state['id'], 'number': str(q['answer']),
                'choice': q['correct'], 'working': 'My own ungraded explanation.'}
        body.update(changes)
        return self.client.post(BASE+'/check', json=body)

    def reveal(self, s, index=0, kind='hint'):
        return self.client.post(BASE+'/reveal', json={'revision': s['revision'],
            'question_id': s['questions'][index]['id'], 'kind': kind})

    def retry(self, s, index=0):
        return self.client.post(BASE+'/retry', json={'revision': s['revision'],
            'question_id': s['questions'][index]['id']})

    def test_start_resume_no_answer_leak_and_no_model(self):
        self.assertIsNone(self.client.get(BASE).json()['session'])
        with patch.object(model, 'call') as call:
            s = self.start()
            self.assertEqual(self.start(), s)
            self.assertEqual(self.client.get(BASE).json()['session'], s)
            self.assertEqual(len(s['questions']), 4)
            for q in s['questions']:
                self.assertNotIn('answer', q)
                self.assertNotIn('correct', q)
                self.assertEqual(q['help'], {})
            self.submit(s)
            call.assert_not_called()

    def test_patch_resume_drafts_language_and_conflict(self):
        s = self.start(); qid = s['questions'][0]['id']
        payload = {'revision': s['revision'], 'stage': 2, 'prediction': 'Edges may soften.',
                   'reflection': 'Noise and texture both change.', 'bridge': 'pixels',
                   'controls': {'passes': 3, 'row': 20, 'noise': .2, 'pattern': 'stripes'},
                   'drafts': {qid: {'number': '80/2', 'choice': 'weighted', 'working': 'Keep this draft.'}}}
        r = self.client.patch(BASE+'/session', json=payload)
        self.assertEqual(r.status_code, 200, r.text)
        saved = r.json()
        self.assertEqual(saved['stage'], 2); self.assertEqual(saved['opened_bridges'], ['pixels'])
        self.assertEqual(saved['drafts'][qid]['working'], 'Keep this draft.')
        self.assertEqual(self.client.patch(BASE+'/session', json=payload).status_code, 409)
        self.client.put('/api/pilot/learning/preferences', json={'language': 'en'})
        en = self.client.get(BASE).json()['session']
        self.assertEqual(en['revision'], saved['revision'])
        self.assertEqual(en['questions'][0]['id'], qid)
        self.assertEqual(en['drafts'], saved['drafts'])
        self.assertEqual(en['prediction'], saved['prediction'])
        self.assertIn('interior pixel', en['questions'][0]['prompt'])
        with TestClient(app.app) as client:
            client.cookies.update(self.client.cookies)
            self.assertEqual(client.get(BASE).json()['session'], en)

    def test_invalid_patch_does_not_write(self):
        s = self.start(); qid = s['questions'][0]['id']
        bad = [{'stage': 5}, {'stage': True}, {'bridge': 'invented'},
               {'controls': {'passes': -1, 'row': 0, 'noise': 0, 'pattern': 'scene'}},
               {'controls': {'passes': 1, 'row': 96, 'noise': 0, 'pattern': 'scene'}},
               {'controls': {'passes': 1, 'row': 0, 'noise': .36, 'pattern': 'scene'}},
               {'drafts': {qid: {'choice': 'invented'}}}]
        for fields in bad:
            self.assertEqual(self.client.patch(BASE+'/session', json={'revision': s['revision'], **fields}).status_code, 422)
        self.assertEqual(self.client.patch(BASE+'/session', json={'revision': s['revision'], 'drafts': {'other-user-question': {'number': '1'}}}).status_code, 409)
        self.assertEqual(self.client.get(BASE).json()['session'], s)

    def test_check_idempotency_conflict_and_bounded_evidence(self):
        s = self.start(); r = self.submit(s)
        self.assertEqual(r.status_code, 200, r.text)
        checked = r.json(); result = checked['questions'][0]['result']
        self.assertTrue(result['passed']); self.assertEqual(result['status'], 'independent')
        self.assertFalse(result['working_assessed']); self.assertEqual(result['retention'], 'unassessed')
        self.assertEqual(self.submit(s).json(), checked)
        self.assertEqual(self.submit(s, number='999').status_code, 409)
        self.assertEqual(self.submit(checked, request_id='new-request-0001').status_code, 409)
        self.assertEqual(len(store.listing('image-check', self.owner)), 1)
        self.assertEqual(self.client.get('/api/pilot/state').json()['summaries']['ramps']['status'], 'unknown')
        self.assertEqual(self.client.get('/api/pilot/learning/history').json(), [])

    def test_invalid_numbers_reasons_and_stale_revision_do_not_write(self):
        s = self.start()
        for number in ('NaN', '1e99', '1/0', '__import__("os")'):
            self.assertEqual(self.submit(s, number=number).status_code, 422)
        self.assertEqual(self.submit(s, choice='invented').status_code, 422)
        self.assertEqual(self.submit(s, revision=s['revision']+1).status_code, 409)
        self.assertEqual(store.listing('image-check', self.owner), [])

    def test_help_exposure_then_retry_cannot_become_independent(self):
        s = self.start(); initial_id = s['questions'][0]['id']
        s = self.reveal(s).json()
        self.assertIn('hint', s['questions'][0]['help'])
        self.assertNotIn('solution', s['questions'][0]['help'])
        s = self.reveal(s, kind='solution').json()
        self.assertIn('solution', s['questions'][0]['help'])
        s = self.submit(s).json()
        self.assertEqual(s['questions'][0]['result']['status'], 'supported')
        s = self.retry(s).json()
        self.assertNotEqual(s['questions'][0]['id'], initial_id)
        self.assertEqual(s['questions'][0]['help'], {})
        self.assertNotIn(initial_id, s['drafts'])
        s = self.submit(s).json()
        self.assertEqual(s['questions'][0]['result']['status'], 'supported')
        self.assertEqual(len(s['history']), 2)
        self.assertEqual(s['history'][0]['exposure_before'], ['hint', 'solution'])

    def test_wrong_reason_targeted_feedback_and_history_translation(self):
        s = self.start()
        s = self.submit(s, index=1, choice='always-noise').json()
        result = s['questions'][1]['result']
        self.assertTrue(result['number_ok']); self.assertFalse(result['choice_ok'])
        self.assertEqual(result['status'], 'needs_review'); self.assertEqual(result['suggested_bridge'], 'frequency')
        original = s['history'][0]
        self.client.put('/api/pilot/learning/preferences', json={'language': 'en'})
        en = self.client.get(BASE).json()['session']
        self.assertEqual(en['history'][0]['id'], original['id'])
        self.assertEqual(en['history'][0]['language'], 'zh-CN')
        self.assertIn('High frequencies', en['history'][0]['result']['feedback'])
        self.assertNotEqual(en['history'][0]['result']['feedback'], original['result']['feedback'])

    def test_owner_isolation_and_auth_on_every_endpoint(self):
        s = self.start(); other, _ = self.learner()
        self.assertIsNone(other.get(BASE).json()['session'])
        os = self.start(other)
        for endpoint, payload in [('check', {'revision': os['revision'], 'question_id': s['questions'][0]['id'], 'request_id': 'cross-owner-001', 'number': '42', 'choice': 'weighted'}),
                                  ('reveal', {'revision': os['revision'], 'question_id': s['questions'][0]['id'], 'kind': 'solution'}),
                                  ('retry', {'revision': os['revision'], 'question_id': s['questions'][0]['id']})]:
            self.assertEqual(other.post(BASE+'/'+endpoint, json=payload).status_code, 409)
        self.assertEqual(other.get(BASE).json()['session']['history'], [])
        other.close()
        with TestClient(app.app) as anonymous:
            self.assertEqual(anonymous.get(BASE).status_code, 401)
            self.assertEqual(anonymous.post(BASE+'/start').status_code, 401)
            self.assertEqual(anonymous.patch(BASE+'/session', json={'revision': 1, 'stage': 1}).status_code, 401)
            self.assertEqual(anonymous.post(BASE+'/check', json={'revision': 1, 'question_id': 'x', 'request_id': 'anonymous-01', 'number': '0', 'choice': 'weighted'}).status_code, 401)
            self.assertEqual(anonymous.post(BASE+'/reveal', json={'revision': 1, 'question_id': 'x', 'kind': 'solution'}).status_code, 401)
            self.assertEqual(anonymous.post(BASE+'/retry', json={'revision': 1, 'question_id': 'x'}).status_code, 401)

    def test_course_scope_and_snapshot_survives_import(self):
        s = self.start()
        old = store.fetch('course', 'shared', 'fixture-v1')
        comp = {**old, 'id': 'comp207-v1', 'code': 'COMP207', 'title': 'COMP207'}
        with store.engine.begin() as conn: catalog.register(comp, conn)
        headers = {'X-Study-Course': 'COMP207'}
        self.assertEqual(self.client.get(BASE, headers=headers).status_code, 409)
        self.assertEqual(self.client.post(BASE+'/start', headers=headers).status_code, 409)
        self.assertEqual(self.client.patch(BASE+'/session', headers=headers, json={'revision': s['revision'], 'stage': 1}).status_code, 409)
        self.assertEqual(catalog.groups(self.owner, comp)['image-session'], [])
        new = {**old, 'id': 'fixture-v2', 'code': 'ELEC270'}
        with store.engine.begin() as conn: catalog.register(new, conn)
        checked = self.submit(s).json()
        self.assertEqual(checked['course_version'], 'fixture-v1')
        self.assertEqual(store.listing('image-check', self.owner)[0]['course_version'], 'fixture-v1')

    def test_export_delete_and_version_guard(self):
        s = self.start(); s = self.reveal(s, kind='solution').json(); self.submit(s)
        with zipfile.ZipFile(io.BytesIO(self.client.get('/api/pilot/export').content)) as z:
            data = json.loads(z.read('Maintenance/pilot-record-v1.json'))
            self.assertEqual(len(data['image-session']), 1)
            self.assertEqual(len(data['image-check']), 1)
            self.assertNotIn('answer', data['image-session'][0]['questions'][0])
            self.assertNotIn('solution', data['image-session'][0]['questions'][0])
            self.assertIn('Image-processing application', z.read('ELEC270 学习记录.md').decode())
        internal = store.fetch('image-session', self.owner, lesson.UNIT_ID)
        internal['content_version'] = 'old-version'; store.save('image-session', self.owner, internal)
        self.assertEqual(self.client.get(BASE).status_code, 409)
        self.assertEqual(self.client.post(BASE+'/start').status_code, 409)
        self.client.delete('/api/pilot/my-data')
        self.assertIsNone(self.client.get(BASE).json()['session'])
        self.assertEqual(store.listing('image-check', self.owner), [])

    def test_variant_limit_and_no_skip_without_attempt_or_help(self):
        s = self.start()
        self.assertEqual(self.retry(s).status_code, 409)
        for variant in range(lesson.MAX_VARIANTS):
            self.assertEqual(s['questions'][0]['variant'], variant)
            s = self.submit(s).json()
            r = self.retry(s)
            if variant + 1 < lesson.MAX_VARIANTS:
                self.assertEqual(r.status_code, 200, r.text); s = r.json()
            else:
                self.assertFalse(s['questions'][0]['retry_available'])
                self.assertEqual(r.status_code, 409)

    def test_authored_math_variants_and_bilingual_parity(self):
        for variant in range(lesson.MAX_VARIANTS):
            for kind in lesson.KINDS:
                q = lesson.question(kind, variant)
                self.assertTrue(lesson.assess(q, str(q['answer']), q['correct'], False)['passed'])
                for key in ('prompt', 'number_label', 'hint', 'solution'):
                    self.assertEqual(set(q[key]), {'zh-CN', 'en'})
                    self.assertTrue(q[key]['en']); self.assertTrue(q[key]['zh-CN'])
            k = variant + 1
            smooth = .25*(20+8*k) + .5*(80+4*k) + .25*(160-8*k)
            self.assertEqual(lesson.question('smoothing', variant)['answer'], smooth)
            amplitude = 8+4*k
            x = lambda n: 128 + amplitude*math.cos(math.pi*n/2)
            y0 = .25*x(-1) + .5*x(0) + .25*x(1)
            self.assertAlmostEqual(y0-128, lesson.question('frequency', variant)['answer'])
            self.assertEqual(lesson.question('transfer', variant)['answer'], (800+200*k)/4)
            c = 96+4*k
            for n in range(4):
                alt = lambda n: c + amplitude*(-1)**n
                self.assertAlmostEqual(.25*alt(n-1)+.5*alt(n)+.25*alt(n+1), c)
            self.assertEqual(lesson.question('recovery', variant)['answer'], 0)


if __name__ == '__main__':
    unittest.main()
