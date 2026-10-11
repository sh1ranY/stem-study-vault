# ELEC270 guided learning, iteration 2

Authorized scope: complete the next teaching loop and prepare for learners using different languages/backgrounds. Preserve current course sources, private learner data, legacy study flow, and local-only deployment.

Deliver a three-concept ramp lesson with prerequisite/visual/algebra explanations, an accessible interactive signal diagram, misconception-specific checks, retry/advance decisions, durable progress, and a handoff to existing independent practice. Checks are guided evidence, never independent mastery claims. User can choose another explanation; routing is based on a particular answer, never nationality or a fixed learning-style label.

Internationalisation: ship Chinese and English for this guided module only. Use stable concept/choice IDs, separately version authored translations, preserve answer-time language and course version, and persist per-account teaching language. Original source material and the surrounding prototype remain in their original language. Full interface localisation, other courses/languages, dialect/notation adaptation, RTL, and cloud deployment are later milestones.

Implementation:
1. Authored bilingual content and deterministic check/routing rules.
2. Authenticated, owner-scoped session/check endpoints; idempotent submissions and transition guards; export/delete integration.
3. Guided lesson component, interactive graph, language toggle, results and resume.
4. Focused mathematical, state-machine, privacy, locale, export and regression tests; frontend build; browser checks in isolated test data.

Validation/outcomes: pending.

Outcome: implemented in backend/pilot/guided.py, backend/pilot/routes.py, src/GuidedLearning.tsx, src/RampGraph.tsx, src/guidedLocale.ts, src/guided.css, extracted src/PilotMarkdown.tsx, and tests/test_guided.py. Existing course/task flows preserved. 59 tests pass and build succeeds. Browser verifies bilingual guided flow, failure/retry, persistence, completed review, practice handoff, separate history, graph boundary and 390px layout. Local-only; main UI and existing task/model content remain primarily Chinese. No live model calls made for this change.
