"""Fresh-install, course isolation and independently calculated computing checks."""
import io
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch
import zipfile
import test_pilot as fixtures
from backend.pilot import catalog, computing, demo_course, localization, store, teaching
from backend.pilot.import_course import Importer
from sqlalchemy import delete
import start


class CourseTests(unittest.TestCase):
    setUp = fixtures.PilotTests.setUp
    tearDown = fixtures.PilotTests.tearDown
    make = fixtures.PilotTests.make
    payload = fixtures.PilotTests.payload
    submit = fixtures.PilotTests.submit
    state = fixtures.PilotTests.state
    learner = fixtures.PilotTests.learner
    picture = fixtures.PilotTests.picture

    def select(self, code):
        r=self.client.post('/api/pilot/courses/select', json={'code':code})
        self.assertEqual(r.status_code,200)

    def test_seed_preserves_private_course_and_is_idempotent(self):
        original=catalog.selected()
        self.assertTrue(demo_course.seed())
        self.assertEqual(catalog.selected(),original)
        self.assertEqual(set(catalog.versions()),set(catalog.COURSES))
        self.assertFalse(demo_course.seed())
        self.assertEqual(len(store.listing('course','shared')),3)

    def test_clean_demo_has_three_bilingual_courses_no_private_paths(self):
        with store.engine.begin() as c: c.execute(delete(store.records).where(store.records.c.owner=='shared'))
        self.assertTrue(demo_course.seed())
        for code in catalog.COURSES:
            self.select(code)
            course=self.client.get('/api/pilot/course').json()
            self.assertEqual(course['mode'],'demo');self.assertEqual(len(course['lessons']),3)
            self.assertEqual(course['asset_count'],0)
            self.client.put('/api/pilot/learning/preferences',json={'language':'en'})
            lesson=self.client.get('/api/pilot/lessons/'+course['lessons'][0]['id']).json()
            self.assertIn('Learning objective',lesson['blocks'][0]['body'])
            serialized=json.dumps(catalog.selected({'id':self.owner}),ensure_ascii=False)
            self.assertNotIn('/Users/',serialized);self.assertNotIn('source_path',serialized)
            self.assertNotIn('body_en',json.dumps(lesson))

    def test_registry_keeps_snapshots_and_source_exposure_in_course_export(self):
        original=catalog.selected();original['assets']=[{'id':'source-asset','suffix':'.pdf'}]
        store.save('course','shared',original)
        with store.engine.begin() as conn:
            catalog.register({**original,'imported_at':'changed-date'},conn)
        self.assertEqual(catalog.selected()['imported_at'],original['imported_at'])
        store.save('event',self.owner,{'id':'source-event','kind':'source_opened','asset_id':'source-asset','at':store.now()})
        self.assertIn('source-event',{e['id'] for e in catalog.groups(self.owner,original)['event']})

    def test_course_switch_keeps_notes_drafts_photos_attempts_separate(self):
        demo_course.seed()
        elec=self.make();self.submit(elec)
        self.client.patch('/api/pilot/progress',json={'lesson_id':'week1','notes':'private ELEC note'})
        self.select('COMP201')
        self.assertEqual(self.state()['attempts'],[])
        task=self.make('petri',key='comp201-task-1');photo=self.picture(task)
        self.client.put('/api/pilot/drafts/'+task['id'],json={'revision':0,'answers':{'P':'2'},'working':'Petri draft','photo_id':photo['id']})
        self.submit(task,key='comp201-attempt',photo_id=photo['id'])
        self.assertEqual(set(self.state()['summaries']),set(computing.topics('COMP201')))
        self.assertEqual(len(self.state()['photos']),1)
        self.assertNotIn('private ELEC',json.dumps(self.state()))
        self.select('COMP207');self.assertEqual(self.state()['drafts'],[]);self.assertEqual(self.state()['photos'],[])
        self.select('COMP201');self.assertEqual(self.state()['drafts'][0]['working'],'Petri draft')
        self.select('ELEC270');self.assertEqual(self.state()['progress'][0]['notes'],'private ELEC note')
        self.assertEqual(self.state()['tasks'][0]['id'],elec['id'])
        self.assertEqual(len(store.listing('attempt',self.owner)),2)

    def test_account_preference_and_tab_header_are_independent(self):
        demo_course.seed();other,_=self.learner()
        self.select('COMP201')
        self.assertEqual(other.get('/api/pilot/course').json()['code'],'ELEC270')
        self.assertEqual(self.client.get('/api/pilot/course',headers={'X-Study-Course':'COMP207'}).json()['code'],'COMP207')
        self.assertEqual(self.client.get('/api/pilot/course').json()['code'],'COMP201')
        self.assertEqual(self.client.get('/api/pilot/course',headers={'X-Study-Course':'NOPE'}).status_code,409)
        self.assertEqual(self.client.post('/api/pilot/tasks',json={'topic':'joins','request_id':'wrong-course-id'}).status_code,422)
        self.assertEqual(self.client.post('/api/pilot/learning/ramps/start').status_code,409)
        other.close()

    def test_course_export_scopes_skill_contract_and_photo(self):
        demo_course.seed();elec=self.make();self.submit(elec)
        self.select('COMP207');t=self.make('joins',key='comp207-task-1');self.submit(t,key='comp207-attempt')
        exported=self.client.get('/api/pilot/export?course=COMP207')
        self.assertIn('COMP207',exported.headers['content-disposition'])
        with zipfile.ZipFile(io.BytesIO(exported.content)) as z:
            contract=json.loads(z.read('Maintenance/Learning/record.json'))
            data=json.loads(z.read('Maintenance/pilot-record-v1.json'))
            self.assertEqual(contract['course_id'],'COMP207');self.assertEqual(len(data['attempt']),1)
            self.assertEqual({o['id'] for o in contract['objectives']},set(computing.topics('COMP207')))
            self.assertNotIn('answer',data['task'][0]['fields'][0]);self.assertIn('COMP207 学习记录.md',z.namelist())

    def test_all_course_topic_flows_and_localized_evidence(self):
        demo_course.seed()
        for code in catalog.COURSES:
            self.select(code)
            self.client.put('/api/pilot/learning/preferences',json={'language':'en'})
            for key in teaching.topics(code):
                t=self.make(key,key='task-'+key+'-001')
                self.assertNotIn('solution',t)
                a=self.submit(t,key='attempt-'+key+'-001')
                self.assertEqual(a.status_code,200);self.assertTrue(a.json()['result']['passed'])
                self.assertEqual(self.client.get('/api/pilot/teaching/'+key).status_code,200)
            rows=self.client.get('/api/pilot/learning/overview').json()['topics']
            self.assertEqual({r['topic'] for r in rows},set(teaching.topics(code)))

    def test_generic_nested_import_preserves_other_courses_and_originals(self):
        demo_course.seed()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);notes=root/'own-course';week=notes/'Weeks'/'2026-27';week.mkdir(parents=True)
            source=week/'Week 04 - Own lesson.md';text='# My Petri lesson\n\nOriginal text.\n\n> [!solution] Answer\n> Hidden result\n'
            source.write_text(text)
            result=Importer(root,root/'sources','COMP201',notes).run()
            self.assertEqual(result['lessons'],1);self.assertEqual(source.read_text(),text)
            self.assertEqual(catalog.selected()['id'],'fixture-v1')
            self.select('COMP201');c=self.client.get('/api/pilot/course').json()
            self.assertEqual(c['mode'],'imported');self.assertEqual(c['lessons'][0]['week'],4)
            l=self.client.get('/api/pilot/lessons/'+c['lessons'][0]['id'])
            self.assertNotIn('Hidden result',l.text)
            self.assertEqual(result['version'],Importer(root,root/'sources','COMP201',notes).run()['version'])

    def test_fresh_missing_directory_migrates_without_private_files(self):
        with tempfile.TemporaryDirectory() as directory:
            data=Path(directory)/'new-directory'
            env={**os.environ,'STUDIO_DATA_DIR':str(data),'STUDIO_DATABASE_URL':'sqlite:///'+str(data/'pilot.sqlite3'),'OPENAI_API_KEY':'','STUDIO_VISION_MODEL':'','STUDIO_DEPLOYMENT':'local'}
            subprocess.run([sys.executable,'-m','alembic','upgrade','head'],check=True,env=env,capture_output=True,cwd=start.ROOT)
            subprocess.run([sys.executable,'-m','backend.pilot.demo_course'],check=True,env=env,capture_output=True,cwd=start.ROOT)
            with sqlite3.connect(data/'pilot.sqlite3') as db:
                courses=[json.loads(row[0]) for row in db.execute("SELECT body FROM pilot_records WHERE kind='course'")]
            self.assertEqual({c['code'] for c in courses},set(catalog.COURSES))
            self.assertTrue(all(c['mode']=='demo' and not c['assets'] for c in courses))

    def test_demo_launcher_overrides_private_settings(self):
        with patch.dict(os.environ,{'OPENAI_API_KEY':'private-value','STUDIO_DATABASE_URL':'private-db','STUDIO_DEPLOYMENT':'hosted'}):
            env=start.environment(True)
            self.assertEqual(env['OPENAI_API_KEY'],'');self.assertEqual(env['STUDIO_DEPLOYMENT'],'local')
            self.assertIn('data-demo',env['STUDIO_DATABASE_URL'])
            self.assertNotEqual(env['STUDIO_DATABASE_URL'],'private-db')
            self.assertEqual(start.environment(False)['STUDIO_DATABASE_URL'],'private-db')


class ComputingOracleTests(unittest.TestCase):
    def test_no_identical_questions_across_diagnosis_practice_review(self):
        for topic in computing.PACKS:
            prompts=[computing.task(topic,phase,n)['prompt'] for phase in ('diagnosis','practice','review') for n in range(24)]
            self.assertEqual(len(set(prompts)),72,topic)

    def test_sql_results_match_sqlite_for_every_parameter(self):
        for phase in ('diagnosis','practice','review'):
            for number in range(24):
                k=number+1+{'diagnosis':0,'practice':24,'review':48}[phase]
                with sqlite3.connect(':memory:') as db:
                    db.executescript('CREATE TABLE Customers(id TEXT PRIMARY KEY); CREATE TABLE Orders(order_id INTEGER PRIMARY KEY, customer_id TEXT); CREATE TABLE Sales(team TEXT, amount INTEGER);')
                    db.executemany('INSERT INTO Customers VALUES (?)',[(x,) for x in 'ABC'])
                    db.executemany('INSERT INTO Orders(customer_id) VALUES (?)',[('A',)]*(k+1)+[('C',)]*(k+2))
                    inner=db.execute('SELECT COUNT(*) FROM Customers c JOIN Orders o ON c.id=o.customer_id').fetchone()[0]
                    left=db.execute('SELECT COUNT(*) FROM Customers c LEFT JOIN Orders o ON c.id=o.customer_id').fetchone()[0]
                    b=db.execute("SELECT COUNT(*),COUNT(o.order_id) FROM Customers c LEFT JOIN Orders o ON c.id=o.customer_id WHERE c.id='B'").fetchone()
                    answers={f['id']:f['answer'] for f in computing.task('joins',phase,number)['fields']}
                    self.assertEqual(answers,dict(inner=inner,left=left,star=b[0],column=b[1]))
                    db.executemany('INSERT INTO Sales VALUES (?,?)',[('A',k-1),('A',k+2),('A',k+4),('B',k),('B',k-1)])
                    rows=db.execute('SELECT COUNT(*) FROM Sales WHERE amount>=?',(k,)).fetchone()[0]
                    sums=dict(db.execute('SELECT team,SUM(amount) FROM Sales WHERE amount>=? GROUP BY team',(k,)))
                    groups=len(db.execute('SELECT team,SUM(amount) FROM Sales WHERE amount>=? GROUP BY team HAVING SUM(amount)>?',(k,k)).fetchall())
                    answers={f['id']:f['answer'] for f in computing.task('aggregation',phase,number)['fields']}
                    self.assertEqual(answers,dict(rows=rows,A=sums['A'],B=sums['B'],groups=groups))

    def test_translations_and_all_keys_with_independent_oracles(self):
        for topic in computing.PACKS:
            for phase in ('diagnosis','practice','review'):
                for n in range(24):
                    t=teaching.task(topic,phase,n);en=localization.task(t,'en')
                    answers={f['id']:f['answer'] for f in t['fields']}
                    self.assertEqual(answers,{f['id']:f['answer'] for f in en['fields']})
                    self.assertNotEqual(t['prompt'],en['prompt']);self.assertEqual(t['id'],en['id'])
                    self.assertNotIn('answer',localization.public_task(t,'en')['fields'][0])
                    self.assertTrue(teaching.evaluate(t,{k:str(v) for k,v in answers.items()},False,False)['passed'])
                    k=n+1+{'diagnosis':0,'practice':24,'review':48}[phase]
                    if topic=='petri':
                        tokens=k+2;firings=0
                        while tokens>=2: tokens-=2;firings+=1
                        self.assertEqual(answers['firings'],firings);self.assertEqual(answers['P'],k);self.assertEqual(answers['Q'],k+1)
                    elif topic=='boundaries':
                        points=list(answers.values());self.assertEqual(points,sorted(set(points)))
                        self.assertEqual([k+5<=x<=k+15 for x in points],[False,True,True,True,True,False])
                    elif topic=='requirements':
                        total=20*(k+1);minimum=next(i for i in range(total+1) if 10*i>=9*total)
                        self.assertEqual(answers['minimum'],minimum);self.assertEqual(answers['passes'],int(k%2==0))
                    elif topic=='serial':
                        schedule=[('A','r'),('B','r'),('A','w'),('B','w')] if k%2 else [('A','r'),('A','w'),('B','r'),('B','w')]
                        edges={(a,b) for i,(a,op) in enumerate(schedule) for b,other in schedule[i+1:] if a!=b and 'w' in (op,other)}
                        self.assertEqual(answers['edges'],len(edges));self.assertEqual(answers['AB'],int(('A','B') in edges));self.assertEqual(answers['BA'],int(('B','A') in edges))
                        self.assertEqual(answers['serialisable'],int(not ({('A','B'),('B','A')}<=edges)))
