# Optional structured learning records

Use when attempts need to survive across sessions or drive multiple teaching updates. A short first lesson can use a plain Markdown evidence note instead. Old vaults without this file remain valid; never require students to edit JSON.

For the first implementation, use **one current snapshot** at `Maintenance/Learning/record.json` rather than several independently written state files. Keep the existing course profile for explicitly stated preferences. Add a generated `Summary.md` when useful; it is derived from the snapshot, not a second authority. Adapt paths to an existing vault and preserve personal files.

## Version 1 fields

| Field | Contract |
| --- | --- |
| `schema_version` | Integer `1`; reject unknown versions instead of guessing a migration |
| `course_id` | One course identity; do not combine unrelated course performance |
| `data_origin` | `learner` or `synthetic`; synthetic data stays in examples/tests, not a real student's record |
| `objectives` | Objects with unique `id`, `description` |
| `tasks` | Unique `id`, `objective_ids`, `kind` (`diagnosis`, `practice`, `transfer`, `retention`), `version`, `source_version` |
| `events` | Ordered actual observations or explicitly synthetic fixtures, as below |
| `claims` | Current limited judgments: `id`, `objective_id`, `status`, `scope`, `evidence_ids` |
| `decisions` | Current teaching choices: `id`, `objective_id`, `after_event_id`, `evidence_ids`, `strategy_id`, concrete `change`, `verification_task_id` |
| `dimensions` | Six summaries keyed by `prerequisites`, `representations`, `support`, `transfer_retention`, `self_assessment`, `goals_preferences`; each has `summary`, `evidence_ids` |

Events contain `id`, `task_id`, `response`, `origin` (`attempt`, `report`, `synthetic`), `correctness` (`correct`, `partial`, `incorrect`, `unassessed`), grading `reason`, boolean `active`, `support` (`none`, `general`, `step`, `demonstration`, `answer`), `support_text`, `exposure` (`unseen`, `related_instruction`, `same_question`, `answer_seen`, `unknown`), and `observed_at` (a known timestamp or null). Optional `delay_days` is a known positive interval, not an estimate invented to fill the field. Optional `supersedes` references an earlier event explicitly marked inactive. Additional user-provided context or pre-feedback confidence may be retained as optional fields; the checker does not interpret them.

The ordered list indicates observation sequence, not a fabricated chronology. `after_event_id` records the latest event available when a decision was made. A later successful transfer cannot retrospectively justify an earlier intervention. Source and task versions preserve which question was answered; if a task changes, assign a new task ID/version and reassess whether earlier evidence applies.

Claim statuses are `unassessed` (no evidence), `observed` (limited observation), `supported`, `independent` or `retained`. These are descriptions, not interval scores or a guaranteed progression. A self-report such as “I can do this” cannot establish independent performance. Independent claims need correct observed work on a task without help or exact-question/answer exposure; prior related instruction is expected and is distinct from having seen this question. Retention also needs an actually attempted delayed task and known interval. Scope should say, for example, “one new plateau construction”, not “all signal processing mastered”.

Leave delayed retention, absent confidence and unrelated prerequisites explicitly unobserved. Preferences may be attributed to learner self-report; do not fabricate a task event for a stated language preference. The six dimensions are an observation framework, not a diagnostic scale.

## Preserve evidence and recover from corrections

Keep original attempts and add a correction event; mark superseded observations inactive. Remove or revise dependent *current* claims, decisions and summaries. Historical decisions can stay in the user's existing version history or a scoped prior snapshot, clearly retired. Do not keep an invalid judgment active merely to make an append-only log convenient.

Before an authorized write, read the existing snapshot, prepare the candidate, validate it, check that the original has not changed, and replace only the intended generated record. Use one writer. If a check fails or a concurrent edit is detected, preserve the prior file and candidate separately; do not overwrite with an empty record. Reuse existing versioning or make a scoped recoverable copy when needed. Generate the human summary after the snapshot succeeds and identify its revision; if interrupted, regenerate it next time. The bundled checker itself performs **no writing, locking, migration or recovery**.

Respect deletion requests across evidence, generated summaries and any scoped copies. Avoid unrelated identifiers. Keep private records out of public examples, commits and reports.

## Read-only check

From the skill directory:

```sh
python3 scripts/learning_tools.py "/path/to/course/Maintenance/Learning/record.json"
```

Exit 0: no detected structural violations; 1: invalid record; 2: unreadable or invalid JSON. Output omits student answers. The checker validates required fields, references, origin separation, support/exposure conditions, current evidence and decision ordering. It does not grade natural language, verify timestamps, authenticate origin, establish source correspondence or show learning effectiveness. Additional fields are not semantically validated. No third-party Python dependency is required.

A skipped diagnostic can have empty task/event/decision lists and explicitly unobserved summaries. Creating such a file is optional. A completed course without any record remains a supported output.
