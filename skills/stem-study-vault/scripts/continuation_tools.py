"""Local single-unit continuation on the v1 record (macOS/Linux, standard library).

Assessment is supplied by a tutor; this is not a natural-language grader.
Only this helper should write its managed directory. Summary.md is disposable.
"""
import argparse
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile
import uuid

from learning_tools import DIMENSIONS, RecordError, require, validate

SUPPORT = ("none", "general", "step", "demonstration", "answer")
EXPOSURE = ("unseen", "related_instruction", "unknown", "same_question", "answer_seen")


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def atomic_write(path, data):
    fd, name = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def new_record(unit, origin):
    return {"schema_version": 1, "course_id": unit["course_id"], "data_origin": origin,
            "objectives": [unit["objective"]],
            "tasks": [{k: v for k, v in t.items() if k != "prompt"} for t in unit["tasks"]],
            "events": [], "claims": [], "decisions": [],
            "dimensions": {k: {"summary": "尚未观察。", "evidence_ids": []} for k in DIMENSIONS},
            "continuation": {"version": 1, "unit_digest": digest(encoded(unit)),
                             "unit_id": unit["unit_id"], "presented": [], "pending": None,
                             "retired_judgments": []}}


def next_task(record):
    state = record["continuation"]
    if state["pending"]:
        return state["pending"]["task_id"]
    return next((t["id"] for t in record["tasks"] if t["id"] not in state["presented"]), None)


def rebuild(record):
    """Conservative current judgment; all original/corrected observations remain."""
    active = [e for e in record["events"] if e["active"]]
    event = active[-1] if active else None
    status = "unassessed"
    if event:
        status = "observed"
        if event["support"] != "none" or event["exposure"] in ("same_question", "answer_seen"):
            status = "supported"
        elif event["correctness"] == "correct" and event["origin"] != "report" and event["exposure"] in ("unseen", "related_instruction"):
            status = "independent"
    evidence = [event["id"]] if event else []
    objective = record["objectives"][0]["id"]
    record["claims"] = [{"id": "current", "objective_id": objective, "status": status,
                         "scope": "仅最近评阅的这次作答；不代表单元全面掌握或延迟保持。", "evidence_ids": evidence}]
    record["decisions"] = []
    target = next_task(record)
    if event and target:
        change = ("复核本题表达式、数值与理由后，用改变条件的新题继续验证。" if status == "independent"
                  else "根据最近评阅定位卡点，补讲斜率、高度或端点；撤去帮助后用新题验证。")
        record["decisions"] = [{"id": "next", "objective_id": objective,
            "after_event_id": event["id"], "evidence_ids": evidence,
            "strategy_id": "ramps-evidence-v1", "change": change, "verification_task_id": target}]
    record["dimensions"] = {k: {"summary": "尚未观察；不从其他维度推断。", "evidence_ids": []} for k in DIMENSIONS}
    if event:
        record["dimensions"]["representations"] = {"summary": event["reason"], "evidence_ids": evidence}
        record["dimensions"]["support"] = {"summary": "最近作答的帮助程度：" + event["support"], "evidence_ids": evidence}
    record["dimensions"]["transfer_retention"] = {"summary": "仅记录本单元作答；没有真实延迟复查，不判断保持。", "evidence_ids": []}


def card(record, revision, unit):
    state = record["continuation"]
    active = [e for e in record["events"] if e["active"]]
    task_id = next_task(record)
    return {"ok": True, "revision": revision, "course_id": record["course_id"],
            "unit_id": state["unit_id"], "data_origin": record["data_origin"],
            "claim": record["claims"][0],
            "last_assessment": ({k: active[-1][k] for k in ("id", "task_id", "correctness", "reason", "support", "exposure")} if active else None),
            "next_task_id": task_id,
            "task": next((t for t in unit["tasks"] if state["pending"] and t["id"] == task_id), None),
            "pending_help": state["pending"],
            "next_action": (record["decisions"][0]["change"] if record["decisions"] else
                            "可开始当前单元；初次尝试可以跳过，先学习正文。" if task_id else
                            "任务已用完。先评阅现有证据；需要继续验证时创建新版本任务包，勿把旧题重标为未见。"),
            "lesson": unit["lesson"], "source": unit["source"],
            "limits": "摘要由 record.json 派生；未记录不等于未见过，外部帮助需如实记录；不认证延迟保持。"}


def summary(result):
    labels = {"unassessed": "尚未评估", "observed": "已有作答，仍需核查", "supported": "有帮助或旧题曝光，独立性未确认", "independent": "最近这道题独立完成"}
    last = result["last_assessment"]
    return ("# ELEC270 续学摘要\n\n自动派生，请勿在此修改学习结论。\n\n"
            f"记录版本：`{result['revision']}`\n\n数据来源：`{result['data_origin']}`\n\n"
            f"当前判断：{labels[result['claim']['status']]}。{result['claim']['scope']}\n\n"
            + (f"最近评阅：{last['reason']}\n\n" if last else "尚无真实作答。\n\n")
            + f"下一步：{result['next_action']}\n\n下一题：{result['next_task_id'] or '待补充'}。\n\n"
            + result["limits"] + "\n").encode("utf-8")


def check_managed(record, unit):
    validate(record)
    state = record["continuation"]
    require(state["version"] == 1 and state["unit_id"] == unit["unit_id"] and
            state["unit_digest"] == digest(encoded(unit)) and record["course_id"] == unit["course_id"],
            "课程或任务版本不一致；请先核对材料，不能自动迁移旧证据。")
    require(record["tasks"] == new_record(unit, record["data_origin"])["tasks"] and
            record["objectives"] == [unit["objective"]], "任务或目标与当前单元不一致。")
    require(isinstance(state["presented"], list) and len(set(state["presented"])) == len(state["presented"]) and
            set(state["presented"]) <= {t["id"] for t in record["tasks"]}, "曝光记录无效。")
    pending = state["pending"]
    require(pending is None or (pending["task_id"] in state["presented"] and
            pending["support"] in SUPPORT and isinstance(pending["support_text"], str)), "待作答状态无效。")
    require(all(e["task_id"] in state["presented"] for e in record["events"]), "作答缺少题目曝光记录。")


def apply_action(args, record):
    state = record["continuation"]
    if args.command == "skip":
        require(state["pending"] is not None, "请先读取当前题目。")
        state["pending"] = None
        return
    if args.command == "present":
        task_id = next_task(record)
        require(task_id is not None, "本版任务已用完；请补充新题，不能重置曝光。")
        if not state["pending"]:
            state["presented"].append(task_id)
            state["pending"] = {"task_id": task_id, "support": "none", "support_text": ""}
        return
    submission = json.loads(args.submission.read_text(encoding="utf-8"))
    require(isinstance(submission, dict), "提交必须为 JSON 对象。")
    if args.command == "correct":
        require(set(submission) == {"correctness", "reason"}, "更正只接受 correctness 和 reason，保留原作答和帮助记录。")
        event = next((e for e in record["events"] if e["id"] == args.event and e["active"]), None)
        require(event is not None, "找不到有效的待更正记录。")
        state["retired_judgments"].append({"record_revision": args.expect,
            "claims": copy.deepcopy(record["claims"]), "decisions": copy.deepcopy(record["decisions"]),
            "reason": "历史判断已撤回；不得用于当前续学。"})
        event["active"] = False
        replacement = dict(event, **submission)
        replacement.update(id=uuid.uuid4().hex, active=True, supersedes=event["id"])
        record["events"].append(replacement)
        return
    pending = state["pending"]
    require(pending is not None, "请先展示题目，再记录帮助或作答。")
    if args.command == "help":
        require(set(submission) == {"support", "support_text"}, "帮助只接受 support 和 support_text。")
        require(submission["support"] in SUPPORT[1:] and isinstance(submission["support_text"], str) and
                submission["support_text"].strip(), "请记录实际展示的帮助内容。")
        pending["support"] = max((pending["support"], submission["support"]), key=SUPPORT.index)
        pending["support_text"] += ("\n" if pending["support_text"] else "") + submission["support_text"]
        return
    require(set(submission) == {"response", "correctness", "reason", "support", "support_text", "exposure", "observed_at"},
            "作答字段不完整或有未知字段；不得伪造 id、origin 或 task_id。")
    require(submission["support"] in SUPPORT and submission["exposure"] in EXPOSURE, "帮助或曝光类别无效。")
    require(isinstance(submission["support_text"], str), "帮助内容须为文字。")
    if pending["support"] != "none":
        submission["support"] = max((pending["support"], submission["support"]), key=SUPPORT.index)
        submission["support_text"] = "\n".join(filter(None, (pending["support_text"], submission["support_text"])))
    if submission["support"] == "answer":
        submission["exposure"] = "answer_seen"
    record["events"].append(dict(submission, id=uuid.uuid4().hex, task_id=pending["task_id"],
        origin="synthetic" if record["data_origin"] == "synthetic" else "attempt", active=True))
    state["pending"] = None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("init", "resume", "present", "help", "attempt", "correct", "skip"):
        sub = commands.add_parser(command)
        sub.add_argument("--directory", type=Path, required=True)
        sub.add_argument("--unit", type=Path, required=True)
        if command == "init":
            sub.add_argument("--origin", choices=("learner", "synthetic"), default="learner")
        elif command != "resume":
            sub.add_argument("--expect", required=True)
        if command in ("help", "attempt", "correct"):
            sub.add_argument("--submission", type=Path, required=True)
        if command == "correct":
            sub.add_argument("--event", required=True)
    args = parser.parse_args(argv)
    try:
        unit = json.loads(args.unit.read_text(encoding="utf-8"))
        require(isinstance(unit, dict) and isinstance(unit.get("tasks"), list) and unit["tasks"] and
                all(isinstance(t.get("prompt"), str) and t["prompt"].strip() for t in unit["tasks"]), "任务包缺少题干。")
        unit["lesson_sha256"] = digest((args.unit.parent / unit["lesson"]).read_bytes())
        directory = args.directory
        if args.command == "init":
            directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        require(directory.is_dir() and not directory.is_symlink(), "记录目录不存在或为符号链接。")
        path = directory / "record.json"
        require(not any((directory / name).is_symlink() for name in ("record.json", "Summary.md", ".writer.lock")), "拒绝写入符号链接。")
        with (directory / ".writer.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if args.command == "init":
                require(not path.exists(), "已有记录；禁止重新初始化覆盖。")
                record = new_record(unit, args.origin)
                original = None
            else:
                original = path.read_bytes()
                record = json.loads(original)
                check_managed(record, unit)
                if args.command != "resume":
                    require(args.expect == digest(original), "记录已变化，请重新续学读取；本次提交未保存。")
                    apply_action(args, record)
            rebuild(record)
            check_managed(record, unit)
            data = original if args.command == "resume" else encoded(record)
            revision = digest(data)
            result = card(record, revision, unit)
            if args.command != "resume":
                if data != original:
                    atomic_write(path, data)
                try:
                    atomic_write(directory / "Summary.md", summary(result))
                except OSError:
                    result["warning"] = "记录已保存；摘要生成失败，续学时以 record.json 为准。"
            print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, KeyError, IndexError, RecordError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
