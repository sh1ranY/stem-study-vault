# Project entry points

For project work, read `CONTEXT.md` for established terminology and the relevant
plan under `docs/plans/`. Preserve private course material and learner records.

For resuming development, read `docs/HANDOFF.md`; for decisions affecting learning
evidence ownership, read `docs/adr/0001-learning-evidence-authority.md`.
For multi-session course work, use the skill's `references/project-memory.md`.
`third_party/mattpocock-skills` contains archived upstream source for maintenance,
not active project instructions. Runtime guidance lives in the STEM skill.

For the ELEC270 cross-chat learning pilot:

- Read `skills/stem-study-vault/SKILL.md` and
  `skills/stem-study-vault/references/cross-chat-continuation.md`.
- This checkout's private entry is `.local/ELEC270/Course.md`, when present.
  The canonical record is in its `Maintenance/Learning` directory.
- Run the helper's `resume` before tutoring. Do not infer current evidence from
  previous chats, `Summary.md`, project progress or synthetic tests.
- Use the revision-checked helper for managed records. Do not fabricate attempts
  to demonstrate a loop in a learner's directory.

Validation: `python3 -m unittest discover -s tests -v`; inspect any skipped tests.
Use `npm run test:math` and the KaTeX checker when changing math material.
