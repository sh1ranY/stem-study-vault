# Learning evidence has one owner per workflow

Status: accepted, 2026-10-12.

The local ELEC270 Skill pilot owns its v1 learning record and derives its resume
summary from that record; Study Studio owns its existing SQLite evidence. We keep
these writers separate until an explicit import/conflict policy exists. A shared
free-form “project memory” would be simpler to write, but could preserve a judgment
after its evidence was corrected or confuse completed course production with
learner mastery. Such errors become costly once real attempts accumulate.

Project terminology, plans and architecture decisions remain in project documents.
Course-building progress stays in course maintenance notes; learner judgments stay
in their evidence system. Handoffs link to those owners instead of becoming another
database. The current trade-off is that Skill and Studio do not automatically sync.
Any future synchronization must specify record identity, evidence provenance,
correction propagation, exposure tracking and conflict resolution before sharing
authority.

Contracts: [learning records](../../skills/stem-study-vault/references/learning-records.md),
[continuation](../../skills/stem-study-vault/references/cross-chat-continuation.md),
[Studio export adapter](../../apps/study-studio/backend/pilot/export_record.py).
