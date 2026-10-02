#!/usr/bin/env python3
"""Read-only validation of optional course learning records (Python 3.9+)."""
import argparse
import json
import math
from pathlib import Path


DIMENSIONS = ("prerequisites", "representations", "support", "transfer_retention",
              "self_assessment", "goals_preferences")


class RecordError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise RecordError(message)


def string(value):
    return isinstance(value, str) and bool(value.strip())


def rows(record, key):
    items = record.get(key)
    require(isinstance(items, list), key + " must be a list")
    result = {}
    for index, item in enumerate(items):
        require(isinstance(item, dict), key + " entries must be objects")
        ident = item.get("id")
        require(string(ident), key + " entries require an id")
        require(ident not in result, key + " contains a duplicate id")
        result[ident] = (index, item)
    return result


def refs(value, known, label, allow_empty=False):
    require(isinstance(value, list), label + " must be a list")
    require(allow_empty or bool(value), label + " must not be empty")
    require(all(string(x) for x in value), label + " must contain ids")
    require(len(value) == len(set(value)), label + " contains duplicate references")
    require(all(x in known for x in value), label + " has an unknown reference")
    return value


def validate(record):
    """Raise RecordError on an invalid current snapshot; never grade responses."""
    require(isinstance(record, dict), "record must be an object")
    require(type(record.get("schema_version")) is int and record["schema_version"] == 1,
            "unsupported schema_version")
    require(string(record.get("course_id")), "course_id is required")
    require(record.get("data_origin") in ("learner", "synthetic"), "invalid data_origin")
    objectives = rows(record, "objectives")
    tasks = rows(record, "tasks")
    events = rows(record, "events")
    claims = rows(record, "claims")
    decisions = rows(record, "decisions")
    for _, item in objectives.values():
        require(string(item.get("description")), "objective description is required")
    for _, task in tasks.values():
        refs(task.get("objective_ids"), objectives, "task.objective_ids")
        require(task.get("kind") in ("diagnosis", "practice", "transfer", "retention"),
                "invalid task kind")
        require(string(task.get("version")) and string(task.get("source_version")),
                "task and source versions are required (use authored-v1 for authored tasks)")
    for index, event in events.values():
        require(string(event.get("task_id")) and event["task_id"] in tasks, "event has an unknown task")
        require(string(event.get("response")), "event response is required")
        require(event.get("origin") in ("attempt", "report", "synthetic"), "invalid event origin")
        require((event["origin"] == "synthetic") == (record["data_origin"] == "synthetic"),
                "synthetic and learner evidence must be kept in separate records")
        require(event.get("correctness") in ("correct", "partial", "incorrect", "unassessed"),
                "invalid correctness")
        require(string(event.get("reason")), "event grading reason is required")
        require(type(event.get("active")) is bool, "event.active must be boolean")
        require(event.get("support") in ("none", "general", "step", "demonstration", "answer"),
                "invalid support")
        require(isinstance(event.get("support_text"), str), "support_text must be text")
        require(event["support"] == "none" or string(event["support_text"]),
                "record the support actually given")
        require(event["support"] != "none" or not event["support_text"].strip(),
                "support none cannot contain a recorded hint")
        require(event.get("exposure") in ("unseen", "related_instruction", "same_question",
                                          "answer_seen", "unknown"), "invalid exposure")
        require("observed_at" in event and (event["observed_at"] is None or string(event["observed_at"])),
                "observed_at must be provided or explicitly null")
        if event.get("supersedes") is not None:
            prior = event["supersedes"]
            require(isinstance(prior, str) and prior in events and events[prior][0] < index,
                    "supersedes must refer to an earlier event")
            require(events[prior][1]["active"] is False, "superseded evidence must be inactive")
        delay = event.get("delay_days")
        require(delay is None or (type(delay) in (int, float) and math.isfinite(delay) and delay > 0),
                "delay_days must be positive or unknown")

    def evidence(item, label, empty=False):
        selected = refs(item.get("evidence_ids"), events, label + ".evidence_ids", empty)
        require(all(events[x][1]["active"] for x in selected), label + " references retired evidence")
        return [events[x][1] for x in selected]

    for _, claim in claims.values():
        objective = claim.get("objective_id")
        require(string(objective) and objective in objectives, "claim has an unknown objective")
        status = claim.get("status")
        require(status in ("unassessed", "observed", "supported", "independent", "retained"),
                "invalid claim status")
        selected = evidence(claim, "claim", status == "unassessed")
        require(status != "unassessed" or not selected, "unassessed claim cannot cite graded evidence")
        require(string(claim.get("scope")), "claim must state its limited scope")
        for event in selected:
            require(objective in tasks[event["task_id"]][1]["objective_ids"],
                    "claim evidence targets another objective")
        if status in ("independent", "retained"):
            require(all(e["origin"] != "report" and e["correctness"] == "correct" and e["support"] == "none"
                        and e["exposure"] in ("unseen", "related_instruction") for e in selected),
                    "independent/retained claim requires correct observed work, without assistance or exact-task exposure")
        if status == "supported":
            require(any(e["support"] != "none" or e["exposure"] in ("same_question", "answer_seen")
                        for e in selected), "supported claim needs support or repeated/answer exposure")
        if status == "retained":
            require(all(tasks[e["task_id"]][1]["kind"] == "retention"
                        and e.get("delay_days") is not None for e in selected),
                    "retention requires an attempted retention task and known delay")
    for _, decision in decisions.values():
        require(string(decision.get("objective_id")) and decision["objective_id"] in objectives, "decision has an unknown objective")
        selected = evidence(decision, "decision")
        require(all(decision["objective_id"] in tasks[e["task_id"]][1]["objective_ids"]
                    for e in selected), "decision evidence targets another objective")
        cutoff = decision.get("after_event_id")
        require(isinstance(cutoff, str) and cutoff in events, "decision requires its event cutoff")
        require(all(events[x][0] <= events[cutoff][0] for x in decision["evidence_ids"]),
                "decision references future evidence")
        require(string(decision.get("strategy_id")) and string(decision.get("change")),
                "decision requires a strategy and concrete teaching change")
        check = decision.get("verification_task_id")
        require(isinstance(check, str) and check in tasks, "decision verification task is missing")
        require(decision["objective_id"] in tasks[check][1]["objective_ids"],
                "verification task does not target the decision objective")
    dimensions = record.get("dimensions")
    require(isinstance(dimensions, dict) and set(dimensions) == set(DIMENSIONS),
            "dimensions must contain the six named observations")
    for dimension in dimensions.values():
        require(isinstance(dimension, dict) and string(dimension.get("summary")),
                "dimension summary is required; use unobserved where appropriate")
        evidence(dimension, "dimension", True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", help="One optional learning-record JSON file; never modified")
    args = parser.parse_args(argv)
    try:
        raw = Path(args.record).read_text(encoding="utf-8")
        record = json.loads(raw)
    except (OSError, UnicodeError, ValueError):
        print(json.dumps({"ok": False, "error": "Cannot read a UTF-8 JSON record"}))
        return 2
    try:
        validate(record)
    except RecordError as error:
        print(json.dumps({"ok": False, "error": str(error)}))
        return 1
    except (TypeError, KeyError):
        print(json.dumps({"ok": False, "error": "Invalid field type or missing required field"}))
        return 1
    print(json.dumps({"ok": True, "scope": "record structure only; no grading or efficacy validation"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
