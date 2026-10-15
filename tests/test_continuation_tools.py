"""Exercise the durable protocol through fresh processes, not shared Python state."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/stem-study-vault"
SCRIPT = SKILL / "scripts/continuation_tools.py"
UNIT = SKILL / "references/units/elec270-ramps.json"


class Continuation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name) / "Learning"
        self.unit = UNIT

    def run_cli(self, command, *args, code=0):
        result = subprocess.run([sys.executable, str(SCRIPT), command,
            "--directory", str(self.directory), "--unit", str(self.unit), *args],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def start(self):
        return self.run_cli("init", "--origin", "synthetic")

    def submit(self, revision, correctness="incorrect", support="none", exposure="unseen"):
        path = Path(self.temp.name) / "submission.json"
        path.write_text(json.dumps({"response": "private reasoning sentinel",
            "correctness": correctness, "reason": "平台高度计算需复查" if correctness != "correct" else "表达式与端点检查正确",
            "support": support, "support_text": "先代入一个数" if support != "none" else "",
            "exposure": exposure, "observed_at": None}), encoding="utf-8")
        return self.run_cli("attempt", "--expect", revision, "--submission", str(path))

    def test_restart_continues_with_new_task_and_ignores_stale_summary(self):
        initial = self.start()
        first = self.run_cli("present", "--expect", initial["revision"])
        self.assertEqual(first["task"]["id"], "d1")
        saved = self.submit(first["revision"])
        (self.directory / "Summary.md").write_text("已经掌握全部内容", encoding="utf-8")
        resumed = self.run_cli("resume")
        self.assertEqual(resumed["revision"], saved["revision"])
        self.assertEqual(resumed["claim"]["status"], "observed")
        self.assertEqual(resumed["next_task_id"], "t1")
        self.assertNotIn("private reasoning sentinel", json.dumps(resumed))
        fresh = self.run_cli("present", "--expect", resumed["revision"])
        verified = self.submit(fresh["revision"], "correct", exposure="related_instruction")
        self.assertEqual(verified["claim"]["status"], "independent")
        self.assertEqual(self.run_cli("resume")["next_task_id"], "t2")

    def test_correction_retires_judgments_but_never_makes_used_task_unseen(self):
        a = self.start()
        a = self.run_cli("present", "--expect", a["revision"])
        a = self.submit(a["revision"], "correct")
        event_id = a["claim"]["evidence_ids"][0]
        path = Path(self.temp.name) / "correction.json"
        path.write_text(json.dumps({"correctness": "incorrect", "reason": "旧批改漏查跳变点"}), encoding="utf-8")
        corrected = self.run_cli("correct", "--expect", a["revision"], "--event", event_id, "--submission", str(path))
        self.assertEqual(corrected["claim"]["status"], "observed")
        self.assertEqual(corrected["next_task_id"], "t1")
        record = json.loads((self.directory / "record.json").read_text())
        self.assertFalse(record["events"][0]["active"])
        self.assertEqual(record["events"][1]["supersedes"], event_id)
        self.assertEqual(record["events"][0]["response"], record["events"][1]["response"])
        self.assertNotIn(event_id, record["claims"][0]["evidence_ids"])
        self.assertTrue(record["continuation"]["retired_judgments"])
        self.assertNotIn("独立完成", (self.directory / "Summary.md").read_text())

    def test_stale_writer_and_reinit_leave_canonical_bytes_unchanged(self):
        a = self.start()
        self.run_cli("present", "--expect", a["revision"])
        before = (self.directory / "record.json").read_bytes()
        self.run_cli("present", "--expect", a["revision"], code=1)
        self.run_cli("init", code=1)
        self.assertEqual(before, (self.directory / "record.json").read_bytes())

    def test_help_and_unknown_exposure_do_not_support_independence(self):
        a = self.start()
        a = self.run_cli("present", "--expect", a["revision"])
        a = self.submit(a["revision"], "correct", "step")
        self.assertEqual(a["claim"]["status"], "supported")
        a = self.run_cli("present", "--expect", a["revision"])
        a = self.submit(a["revision"], "correct", exposure="unknown")
        self.assertEqual(a["claim"]["status"], "observed")

    def test_task_exhaustion_requests_new_material_instead_of_reusing_answers(self):
        a = self.start()
        for task in ("d1", "t1", "t2"):
            a = self.run_cli("present", "--expect", a["revision"])
            self.assertEqual(a["task"]["id"], task)
            a = self.submit(a["revision"])
        self.assertIsNone(a["next_task_id"])
        self.run_cli("present", "--expect", a["revision"], code=1)

    def test_version_or_course_mismatch_refuses_resume(self):
        self.start()
        changed = json.loads(UNIT.read_text())
        changed["course_id"] = "COMP207"
        self.unit = Path(self.temp.name) / "other.json"
        self.unit.write_text(json.dumps(changed))
        self.run_cli("resume", code=1)

    def test_changed_lesson_refuses_to_reinterpret_existing_evidence(self):
        lesson = Path(self.temp.name) / "lesson.md"
        lesson.write_text("original source", encoding="utf-8")
        changed = json.loads(UNIT.read_text())
        changed["lesson"] = str(lesson)
        self.unit = Path(self.temp.name) / "unit.json"
        self.unit.write_text(json.dumps(changed))
        self.start()
        lesson.write_text("new source with changed boundary convention", encoding="utf-8")
        self.run_cli("resume", code=1)

    def test_pending_question_survives_restart_and_invalid_submission(self):
        a = self.start()
        a = self.run_cli("present", "--expect", a["revision"])
        again = self.run_cli("present", "--expect", a["revision"])
        self.assertEqual(a["revision"], again["revision"])
        self.assertEqual(again["task"]["id"], "d1")
        path = Path(self.temp.name) / "bad.json"
        path.write_text('{}')
        self.run_cli("attempt", "--expect", a["revision"], "--submission", str(path), code=1)
        self.assertEqual(self.run_cli("resume")["revision"], a["revision"])

    def test_recorded_help_cannot_be_forgotten_by_next_chat(self):
        a = self.start()
        a = self.run_cli("present", "--expect", a["revision"])
        path = Path(self.temp.name) / "help.json"
        path.write_text(json.dumps({"support": "answer", "support_text": "已经展示完整答案"}))
        a = self.run_cli("help", "--expect", a["revision"], "--submission", str(path))
        self.assertEqual(self.run_cli("resume")["pending_help"]["support"], "answer")
        a = self.submit(a["revision"], "correct", exposure="unseen")
        self.assertEqual(a["claim"]["status"], "supported")

    def test_simultaneous_writers_only_one_can_save_the_same_revision(self):
        a = self.start()
        command = [sys.executable, str(SCRIPT), "present", "--directory", str(self.directory),
                   "--unit", str(self.unit), "--expect", a["revision"]]
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for process in processes:
            process.communicate(timeout=10)
        self.assertEqual(sorted(p.returncode for p in processes), [0, 1])

    def test_skipping_diagnosis_preserves_unassessed_state(self):
        a = self.start()
        a = self.run_cli("present", "--expect", a["revision"])
        a = self.run_cli("skip", "--expect", a["revision"])
        self.assertEqual(a["claim"]["status"], "unassessed")
        self.assertEqual(a["next_task_id"], "t1")
        record = json.loads((self.directory / "record.json").read_text())
        self.assertEqual(record["events"], [])
        self.assertEqual(record["continuation"]["presented"], ["d1"])


class OriginalSignalAnswer(unittest.TestCase):
    def test_negative_slope_transfer_matches_piecewise_spec_including_jumps(self):
        # Independent piecewise oracle, including both sides of the transitions.
        for time, expected in [(-1, 0), (0, 4), (0.5, 4), (1, 4), (2, 2),
                               (2.5, 1), (3, 0), (3.5, 0), (5, 0)]:
            with self.subTest(time=time):
                actual = 4 * (time >= 0) - 2 * max(time - 1, 0) + 2 * max(time - 3, 0)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
