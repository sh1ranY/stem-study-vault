"""Record invariants; passing tests do not evaluate generated teaching or learners."""
import copy
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/stem-study-vault/scripts/learning_tools.py'
spec = importlib.util.spec_from_file_location('learning_tools', SCRIPT)
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)


class LearningRecords(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / 'examples/diagnosis/signals/record.json').read_text())

    def invalid(self, record=None):
        with self.assertRaises(tools.RecordError):
            tools.validate(self.record if record is None else record)

    def test_three_original_records(self):
        paths = list((ROOT / 'examples/diagnosis').glob('*/record.json'))
        self.assertEqual(len(paths), 3)
        for path in paths:
            with self.subTest(path=path.name):
                tools.validate(json.loads(path.read_text()))

    def test_skip_with_unobserved_dimensions(self):
        for key in ('objectives', 'tasks', 'events', 'claims', 'decisions'):
            self.record[key] = []
        for dimension in self.record['dimensions'].values():
            dimension.update(summary='未观察', evidence_ids=[])
        tools.validate(self.record)

    def test_versions_types_and_missing_dimensions(self):
        for key, bad in [('schema_version', True), ('schema_version', 2),
                         ('events', {}), ('dimensions', {}), ('course_id', '')]:
            r = copy.deepcopy(self.record)
            r[key] = bad
            with self.subTest(key=key, value=bad):
                self.invalid(r)

    def test_duplicate_ids_and_references(self):
        self.record['events'].append(copy.deepcopy(self.record['events'][0]))
        self.invalid()
        self.record['events'].pop()
        self.record['claims'][0]['evidence_ids'] = ['e3', 'e3']
        self.invalid()

    def test_unknown_references_and_wrong_types(self):
        for collection, field in [('events', 'task_id'), ('claims', 'objective_id'),
                                  ('decisions', 'objective_id')]:
            for bad in ('missing', []):
                r = copy.deepcopy(self.record)
                r[collection][0][field] = bad
                with self.subTest(collection=collection, value=bad):
                    self.invalid(r)
        self.record['claims'][0]['evidence_ids'] = ['missing']
        self.invalid()

    def test_synthetic_evidence_cannot_enter_learner_record(self):
        self.record['data_origin'] = 'learner'
        self.invalid()

    def test_self_report_cannot_establish_independence(self):
        self.record['data_origin'] = 'learner'
        for event in self.record['events']:
            event['origin'] = 'attempt'
        self.record['events'][2]['origin'] = 'report'
        self.invalid()

    def test_support_or_exact_task_exposure_prevents_independence(self):
        for field, bad in [('support', 'step'), ('exposure', 'same_question'),
                           ('exposure', 'answer_seen'), ('exposure', 'unknown'),
                           ('correctness', 'partial')]:
            r = copy.deepcopy(self.record)
            r['events'][2][field] = bad
            if field == 'support':
                r['events'][2]['support_text'] = 'hint'
            with self.subTest(field=field, value=bad):
                self.invalid(r)

    def test_support_text_must_match_recorded_help(self):
        self.record['events'][0]['support_text'] = 'hidden hint'
        self.invalid()
        self.record['events'][0]['support_text'] = ''
        self.record['events'][1]['support_text'] = ''
        self.invalid()

    def test_claim_must_match_objective(self):
        self.record['objectives'].append(dict(id='other', description='another capability'))
        self.record['claims'][0]['objective_id'] = 'other'
        self.invalid()

    def test_retention_requires_new_attempt_and_known_delay(self):
        self.record['claims'][0]['status'] = 'retained'
        self.invalid()
        self.record['events'][2]['task_id'] = 'r1'
        self.invalid()
        self.record['events'][2]['delay_days'] = 3
        tools.validate(self.record)
        for delay in (0, -1, True, float('nan')):
            self.record['events'][2]['delay_days'] = delay
            self.invalid()

    def test_decision_cannot_use_future_success(self):
        self.record['decisions'][0]['evidence_ids'].append('e3')
        self.invalid()

    def test_verification_must_target_same_objective(self):
        self.record['objectives'].append(dict(id='other', description='another capability'))
        self.record['tasks'][2]['objective_ids'] = ['other']
        self.record['decisions'][0]['verification_task_id'] = 'r1'
        self.invalid()

    def test_correction_requires_retiring_dependent_current_claims(self):
        old = self.record['events'][2]
        correction = copy.deepcopy(old)
        correction.update(id='e4', supersedes='e3', correctness='incorrect',
                          reason='corrected transcription', response='actual answer was wrong')
        self.record['events'].append(correction)
        self.invalid()  # Old evidence must be marked inactive.
        old['active'] = False
        self.invalid()  # Current claim and dimension still cite retired evidence.
        self.record['claims'][0].update(status='observed', evidence_ids=['e4'], scope='new attempt incorrect')
        self.record['dimensions']['transfer_retention'].update(summary='new attempt incorrect', evidence_ids=['e4'])
        tools.validate(self.record)

    def test_unassessed_has_no_evidence(self):
        self.record['claims'][0]['status'] = 'unassessed'
        self.invalid()
        self.record['claims'][0]['evidence_ids'] = []
        tools.validate(self.record)

    def test_cli_read_only_private_output_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / '学生记录.json'
            for content, code in [(json.dumps(self.record), 0),
                                  (json.dumps({'response': 'PRIVATE_SENTINEL'}), 1),
                                  ('{"PRIVATE_SENTINEL":', 2)]:
                path.write_text(content)
                before = path.read_bytes()
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, code)
                self.assertEqual(path.read_bytes(), before)
                self.assertNotIn('PRIVATE_SENTINEL', result.stdout + result.stderr)
                self.assertNotIn(self.record['events'][0]['response'], result.stdout)
                self.assertEqual(json.loads(result.stdout)['ok'], code == 0)
            result = subprocess.run([sys.executable, str(SCRIPT), str(path.parent / 'missing')],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)


class OriginalAnswerChecks(unittest.TestCase):
    def test_ramp_expressions_against_piecewise_specification(self):
        # Independent piecewise expectations include all transition endpoints.
        for start, stop, drop, slope in [(1, 4, 6, 2), (2, 5, 7, 3)]:
            for t in [start - 1, start, start + .5, stop, stop + .5, drop, drop + 1]:
                expected = 0 if t < start or t >= drop else slope * (min(t, stop) - start)
                actual = slope * max(t - start, 0) - slope * max(t - stop, 0)
                actual -= slope * (stop - start) * (t >= drop)
                self.assertEqual(actual, expected)

    def test_requirement_counterexamples(self):
        for data, threshold, required, mean in [([1]*4+[6], 2, 5, 2),
                                                ([3]*97+[7]*3, 4, 98, 3.12),
                                                ([2]*47+[5]*3, 3, 48, 2.18)]:
            self.assertAlmostEqual(sum(data) / len(data), mean)
            self.assertLessEqual(mean, threshold)
            self.assertLess(sum(x <= threshold for x in data), required)

    def test_relational_rules_on_reset_isolated_database(self):
        packs = [([11, 12], ['DB', 'SE', 'AI'], [(11, 'DB'), (11, 'SE'), (12, 'DB')],
                  [(11, 'AI'), (11, 'DB'), (99, 'AI'), (None, 'AI')], [True, False, False, False]),
                 ([21, 22], [31, 32], [(21, 31)],
                  [(21, 32), (22, 31), (21, 31), (99, 32), (None, 32)], [True, True, False, False, False]),
                 (['A', 'B'], [21, 22], [('A', 21)],
                  [('A', 22), ('B', 21), ('A', 21), ('C', 21), ('A', None)], [True, True, False, False, False])]
        for parents_a, parents_b, initial, attempts, outcomes in packs:
            for attempt, expected in zip(attempts, outcomes):
                with self.subTest(attempt=attempt), sqlite3.connect(':memory:') as db:
                    db.execute('PRAGMA foreign_keys=ON')
                    db.executescript('CREATE TABLE A(id PRIMARY KEY); CREATE TABLE B(id PRIMARY KEY);'
                                     'CREATE TABLE R(a NOT NULL REFERENCES A(id), b NOT NULL REFERENCES B(id), PRIMARY KEY(a,b));')
                    db.executemany('INSERT INTO A VALUES (?)', [(x,) for x in parents_a])
                    db.executemany('INSERT INTO B VALUES (?)', [(x,) for x in parents_b])
                    db.executemany('INSERT INTO R VALUES (?,?)', initial)
                    try:
                        db.execute('INSERT INTO R VALUES (?,?)', attempt)
                        accepted = True
                    except sqlite3.IntegrityError:
                        accepted = False
                    self.assertEqual(accepted, expected)


if __name__ == '__main__':
    unittest.main()
