# Source fidelity and question coverage

## Source registry

Keep original files unchanged. Use `inventory` to obtain relative paths, sizes and SHA-256 hashes. Assign a stable source ID once; do not use a changing hash as the only identity. Add human-assessed metadata in `Maintenance/Sources.md`: title, source ID, edition/year when evidenced, role, authority, read status and limitations.

Useful authority labels are current official, historical official, supplementary, learner-provided unverified and authored demonstration. A filename containing “official” does not verify authority. A source may contain an official final answer without official working. Record conflicts instead of silently selecting a convenient answer.

Every substantive teaching unit should cite its actual source locator:

- PDF: physical file page counted from 1, separately from any printed number.
- PPTX: slide position from 1, noting hidden slides or a differing PDF export.
- Text/Markdown: a heading or stable block, and file/version.
- Image/scan: image file and region/page; record unreadable text precisely.

A PDF link may use `[[Sources/Original/lecture.pdf#page=7]]`. Page count checks do not show that page 7 actually supports the claim. Inspect the relevant page. Text extraction can lose subscripts, fraction bars, vector marks, tables and diagram connections; it is a reading aid, not evidence of complete visual coverage. Mark source reading as complete only when the content needed for the stated scope was actually inspected.

Where source material and a correct independent derivation disagree, show the discrepancy and assumptions. Do not silently rewrite an official question or pretend an authored correction is official.

## Coverage map

Track meaningful teaching units, not every decorative slide. In `Maintenance/Coverage.md`, record source ID/locator, concept, prerequisites, lesson destination, worked example/practice and status. Explain exclusions such as administration, duplication or beyond-scope content. Distinguish mapped, drafted, reviewed and blocked. Keep a separate unresolved-material list when needed.

## Question registry

Use `Maintenance/Questions.md` (a table is sufficient):

| Field | Meaning |
| --- | --- |
| Question ID | Stable ID distinguishing source/version and original question/subpart |
| Source locator | Source ID, physical page/slide/heading and original numbering |
| Concept/prerequisites | What is practiced and what must already be known |
| Use | Worked / immediate / reinforcement / synthesis / unseen mock / out of scope |
| Destination | Exact note and heading/block, or withheld mock source |
| Answer provenance | Official final answer / official working / authored / unknown |
| Status | Arranged / blocked with reason / deliberately withheld / duplicate |

Do not assign the same ID to different papers' Q1. Repeated numbering within one source requires an extra locator. Keep subparts traceable; a continuation of an answer is not a new question. Record duplicate relationships without inflating coverage counts. Preserve omitted or out-of-scope questions in the registry with a reason.

For unseen mocks, ask which papers the learner has already attempted and which should be held back. If no choice is available, leave potential reserve papers unsplit, continue with exercise sheets, and record that decision as pending. Do not include withheld question text, answers or revealing topic breakdowns in the normal learning route. Do not claim a paper is unseen when you do not know the learner's history.

Historical papers support practice and a description of observed question types. They do not establish current assessment rules, an exhaustive syllabus or the probability of a future topic.
