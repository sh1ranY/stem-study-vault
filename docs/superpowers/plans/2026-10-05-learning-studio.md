# Learning Studio Implementation Plan

**Goal:** Deliver an English, locally runnable professor demonstration of upload → lesson → attempt → targeted support → fresh check → persistent resume/export.

**Architecture:** React/Vite reading workspace with a loopback-only FastAPI service and SQLite persistence. Original ELEC270-aligned material supports a fully working prepared mode without an API key. Optional server-side OpenAI/DeepSeek adapters can create source-grounded units when configured; they are not claimed as live-tested without credentials. No cloud publishing, billing, school accounts or external messages in this task.

**Spec:** Current chat's approved third step and Q1–Q30; CONTEXT.md contains settled terminology. This is a prototype inside the existing repository, not a separate Sites deployment. User workflow preferences override redundant design approvals, forced commits and test bureaucracy.

## Constraints and risks

- Only original example content is distributable. Supplied university PDFs stay in ignored local storage. English default. No secrets in the browser or exports.
- Distinguish prepared teaching/rule checks from live model inference. Arbitrary unrecognised source files must not silently receive unrelated canned lessons.
- Preserve actual attempts, hints/answer exposure and feedback. Same-task retry cannot claim independence; retention stays unassessed without a real later check.
- Structured checks support narrow claims; free written explanations in prepared mode are stored, not semantically graded.
- Upload validation, bounded parsing/model calls, restore after refresh, concurrent writes, export fidelity and generated-content safety need explicit checks.

## Tasks

- [x] Backend + authored signal unit: persistent sessions, upload/preview, attempts, support selection, fresh task variants, notes, events, delete and Markdown/JSON ZIP export. Tests cover misconception branches, equivalent numeric inputs, exposure, restart and bad uploads.
- [x] Optional model adapter: server-only configuration, source-grounded JSON validation and bounded requests; test with mock provider, report live use as unverified.
- [x] Frontend: library, source import, three-part lesson, original waveform visual, exercise panel, intervention cards, evidence view, tutor support, notes, resume and export. Responsive, keyboard accessible, visible prepared-mode status.
- [x] Run backend tests/build; interact with complete prepared workflow in browser, refresh/resume/export, inspect desktop and narrow layouts. Write runbook and demonstration instructions, leave local server running.

## Progress

- Initial inspection: existing Skill is usable, repository has no web app. No OpenAI or DeepSeek key configured; user confirmed none. Prepared mode is required for the live demonstration. API integration will have mock-contract coverage only.
- Branch: codex/learning-studio-prototype. Existing untracked CONTEXT.md preserved.

- Delivered under `apps/study-studio/`: prepared teaching loop, optional unverified live adapter, real import/persistence/export, one-click launcher, English professor walkthrough and validation record.
- Validation: 19 isolated backend tests passed; TypeScript/Vite build passed; real browser wrong → support → corrected → fresh independent check, notes/read-position reload, upload, ZIP download and responsive widths verified. See app VALIDATION.md for boundaries.
- Local server remains at http://127.0.0.1:8765. No push, commit, cloud deployment or paid API call performed.
