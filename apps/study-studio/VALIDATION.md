# Validation record

Revision: local prototype on `codex/learning-studio-prototype`, 5 October 2026.

## Observed automated checks

- **19 tests passed** with isolated temporary SQLite storage: answer redaction, safe arithmetic, invalid input rejection, separate remediation branches, first fresh attempt versus retry, hints/solutions/general-help exposure, corrections preserving exposure, six unrecycled variants, read/notes persistence, ZIP export with original source and SVG, export-answer exposure, upload limits and malformed files, scanned PDF warning, PPTX extraction, absent-key behaviour, cross-origin rejection, model-output schema validation, mocked provider contract, draft assessment exclusion.
- TypeScript type checking and Vite production build passed. KaTeX/fonts are included locally. Vite reports a non-blocking bundle-size warning (math/Markdown rendering is bundled); this is a local prototype, and loading was tested.
- `start.command` passed zsh syntax validation. The existing-server launch path was exercised locally; first-time installation on a clean second machine was not tested.

## Observed browser walkthrough

Using the Codex in-app browser against the running local service:

1. Opened an original prepared unit.
2. Submitted the checkpoint with correct shift but incorrect tail values. Received slope-versus-height support, with an alternative explanation acknowledged.
3. Opened a hint and corrected the answer. The result was supported.
4. Opened the first fresh construction and answered it correctly without task-specific help. One independent check appeared in the record alongside the two checkpoint attempts.
5. Saved an explicitly labelled developer-demo note, marked section one read, refreshed, and verified note, attempts and section-two reading position survived.
6. Imported the original example Markdown file using the browser file chooser, inspected the extracted content and opened a prepared session with the file attached separately.
7. Downloaded the Obsidian ZIP through the export control. Inspected its Markdown, original source, SVG and learning-record entries.
8. Checked responsive widths 1280, 983 and 390 pixels. Document width matched the viewport; no page-level horizontal overflow. Inspected screenshots at desktop and mobile widths.
9. Checked browser error/warning logs during the walkthrough: none captured by the browser tool.

Screenshots and local developer walkthrough data are demonstration artifacts, not learning-effectiveness evidence. No participants were tested.

## Limits

No real API request was made. Optional provider behaviour is only covered by mocks and schema tests. No claim of improved attainment, delayed retention, full-course coverage or validated learner classification is supported. There was no clean-machine install, hosted multi-user test, formal accessibility audit, OCR test, open-response grading or concurrent multi-tab edit test.

## ELEC270 pilot, 2026-10-10

See `PILOT.md` for the new application and scope. New isolated integration tests cover source/solution separation, invitations and owner-scoped evidence, image upload/ownership/confirmation, idempotency, correction, export and Skill V1 compatibility, deletion during model calls, source import idempotency, legacy archival, numeric checks and provider failure contracts. Provider outputs are mocked; no live OCR/AI quality claim follows from these tests.

A separate browser-test data directory was used for diagnosis error → selected remediation → fresh task → synthetic photo upload → manual confirmation → numerical feedback → record persistence. Week01 rendering was inspected, including display math and anchors; mobile-width checks found no horizontal overflow. Original vault and desktop materials were not modified.

## 2026-10-11 guided learning

59 unit/integration tests pass, including 13 focused guided-learning tests. Covers 72 parameter sets, both authored languages, three explanation routes, correct-number/wrong-reason separation, idempotency, stale/invalid transitions, per-user isolation, import-version stability, export/deletion and retry bounds. Frontend production build passes (existing >500kB chunk warning).

Browser: isolated synthetic GuidedDemo account at localhost:5177, separate database, no provider calls. Validated wrong-answer remediation, fresh variants, complete three-step flow, English/Chinese switching with retained input/progress, refresh restoration, signal value at t=6 under u(0)=1, completed explanations, transfer to existing practice, and separate guided history. At 390px the document has no horizontal overflow; no KaTeX errors observed. Production data not used for test answers.


## Pilot live API connection check, 2026-10-10

The pilot Responses adapter completed two real gpt-4.1 API requests: transcription of a synthetic printed answer image and process feedback following explicit confirmation. All six printed numerical fields matched the fixture. An isolated temporary database kept test records out of the real learner database. The feedback included redundant checks of already-correct work, so successful transport is not a teaching-quality evaluation. Real handwriting accuracy and learning effectiveness remain untested. The earlier “no real API request” statement refers to the original legacy prototype adapter.
