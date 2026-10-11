# Pilot implementation history

**Current installation and usage:** [README.md](README.md) / [English](GETTING_STARTED.en.md). Current verification is recorded in [VALIDATION.md](VALIDATION.md).

The local app now supports three courses, a standalone original demo, per-account course selection and bilingual original content. The sections below preserve the earlier ELEC270 milestone; its counts, setup defaults and limitations describe that historical revision, not the current installer.

---

# ELEC270 local pilot

This document describes local operation. The subsequent bilingual invited-pilot milestone and hosted setup are documented in [DEPLOYMENT.md](DEPLOYMENT.md); validation history is in [VALIDATION.md](VALIDATION.md).

Run `./start.command`, then open http://127.0.0.1:8765. The first user creates the local owner account. Owners can create one-time invitations for separate learners on this computer. Original prototype remains at `/?prototype=1`, restricted to the owner after pilot setup.

## Delivered

- Read-only course import from Obsidian Weeks and desktop ELEC270 originals, content-addressed attachments, provenance and version snapshots. Source Markdown stays unchanged.
- Thirteen units available to read and search by keyword. Hint/solution callouts are separate from default publication and search; source downloads record exposure. Markdown, math, images, wiki headings and block anchors display in the reader.
- Authored ramp, rectangular-convolution and Fourier-normalisation task families. Each has diagnosis, practice and distinct review parameters. These do not imply automatic assessment of every official exercise.
- Numeric checks, local prerequisite/visual/algebra explanations, switching teaching routes, saved task evidence and conservative independence/exposure rules. Written reasoning remains unassessed unless explicitly requesting AI advice, which is separately labelled and cannot change numeric verdicts.
- JPEG/PNG/WebP submission, original image preservation, EXIF correction, bounded model image, optional Responses transcription, user-confirmed transcription and numeric fields. Manual transcription works with no provider.
- Private records, notes, corrections, model runs, source usage, export/delete. Skill V1 adapter plus raw pilot format. Legacy prototype sessions can be archived unchanged into the owner's export as unverified historical records, never inferred mastery.

## Local model configuration

Copy `.env.example` to `.env` only if `.env` does not exist. Set `OPENAI_API_KEY` and an image-capable `STUDIO_VISION_MODEL` available to your account. Restart the server. Never put keys in `VITE_` variables or source control. Only a user-triggered transcription/feedback action makes a provider request; course import makes none.

Responses calls use structured JSON, `store: false`, one call maximum per operation, a 75-second request timeout and 2500 output tokens. The default is 30 model operations per account per UTC day (`STUDIO_DAILY_MODEL_CALLS`). This is a usage guard, not a monetary spending guarantee. Runs preserve provider usage and error state; failed/unknown calls do not retry automatically. If the server stops during a request, its state becomes interrupted/unknown for display. Check provider usage before an intentional retry.

## Content refresh

```sh
.venv/bin/python -m backend.pilot.import_course
```

Defaults are `~/Documents/Obsidian` and `~/Desktop/ELEC270 课程资料`. The expected course layout is `10 Y2上学期/ELEC270 信号与系统/Weeks/*.md` inside the vault. Personal course materials are not included in Git. Override roots with `STUDIO_VAULT_ROOT` and `STUDIO_ELEC270_SOURCES` or `--vault` and `--desktop`. Same content is idempotent; changed content gets a new course version. Old task attempts keep their version. Back up `data/` before machine migration; original vault sources are never rewritten. This is a selective importer for the observed ELEC270 Markdown conventions, not a universal Obsidian parser. Missing links are reported. PDF/PPT format groups are candidate relationships, not a verified slide-to-page alignment.

## Storage / deployment boundary

Default: single-process loopback FastAPI and SQLite through SQLAlchemy, private assets on disk. `STUDIO_DATABASE_URL=postgresql+psycopg://...` selects PostgreSQL; the checked-in Alembic migration creates the versioned record schema. Run `.venv/bin/python -m alembic upgrade head` before deployment.

PostgreSQL and Supabase deployment have not been integration-tested in this delivery. Do not expose this local pilot as a public multi-worker service. Production work still includes hosted identity/storage, database-level authorisation, durable worker/queue integration, backup/restore drill, semantic retrieval, tested infrastructure and live model evaluation. The records table is an initial portable domain-object store, not the final relational schema from the architecture proposal. Passwords use salted PBKDF2-SHA256; sessions are random HttpOnly SameSite cookies. The localhost launcher uses one worker.

## Tests

```sh
.venv/bin/python -m unittest discover -s tests -v
npm run build
```

Tests isolate storage and mock provider responses. Live handwriting accuracy, AI teaching correctness, delayed retention and learning benefit require separate evaluation. Test fixtures never become real learner evidence. See VALIDATION.md and the delivery report for observed checks.

## Guided teaching iteration (2026-10-11)

Ramp construction now has a three-step lesson (shifted ramp, slope cancellation, height reset). Every step offers prerequisite, visual and algebra explanations, a deterministic numerical-plus-selected-reason checkpoint, and a specific retry recommendation. The visual route has keyboard-accessible interactive graphs, including explicit open/closed breakpoint markers. Each step has 24 bounded checkpoint variants. Completion hands off to the existing independent practice area; completed explanations remain available for review.

`backend/pilot/guided.py` owns content, stable concept/choice identifiers and evaluation. `GuidedLearning.tsx`, `RampGraph.tsx` and `guidedLocale.ts` provide the UI. `/api/pilot/learning/*` stores owner-scoped sessions, preferences and immutable check records; repeated submissions are idempotent and stale transitions are rejected. Guided checks are separate from independent practice and never change mastery/retention claims. Their JSON and Markdown records are included in personal export and removed by the existing personal-data deletion action. Skill V1 independent-task evidence remains unchanged; guided records reside in the raw Pilot export and Markdown.

Chinese and English are authored for this module only, with a persisted per-account teaching-language preference. Switching language keeps question identity, numerical rules and progress; past evidence retains the language used at submission. Course, content and translation versions are recorded separately. Source documents, main navigation, existing independent tasks, OCR and AI feedback have not all been localised. This is not a complete English product release. No nationality/background inference is made. Unsubmitted input does not survive a refresh; completed checks and lesson progress do.

Validation: 59 tests passed (including 13 new guided tests), frontend build passed. Browser validation used an isolated synthetic account with model calls disabled: wrong answer → suggested route → fresh variant → three steps → existing independent practice; language switching, reload, completed-lesson review, history, breakpoint values, and 390px layout. The existing bundle-size warning remains. Real learning effectiveness and professional translation review have not been evaluated.
