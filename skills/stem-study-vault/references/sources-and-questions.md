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

For a primary-text build, inspect every source page/slide or text section in the agreed batch. Track meaningful content items, not only broad lecture topics. A single slide may contain a definition, a validity condition, a diagram and a worked example that impose different teaching obligations. Conversely, several slides may develop one derivation. Choose a granularity that makes missing substance visible without creating a row for every sentence.

In `Maintenance/Coverage.md`, record:

| Field | What to record |
| --- | --- |
| Item ID and locator | Stable item ID, source identity/version and actual page/slide/section |
| Kind | Concept / condition / derivation / figure or table / worked example / exercise |
| Content obligation | What must survive into the teaching; include distinctions, branches and subparts |
| Prerequisites | What the learner needs before this item, and where a refresher belongs if needed |
| Teaching destination | The exact section/block that actually explains or uses this content |
| Disposition and evidence | Mapped / drafted / checked / blocked / excluded with a concrete reason |

For each kind, account for the relevant substance:

- **Concept:** meaning, distinction from related concepts, and any important case the source makes.
- **Condition or convention:** when a statement applies, exceptional cases, sign/normalization choices and limits. Do not drop these while retaining the headline formula.
- **Derivation:** the starting assumptions, non-obvious transformations and final result. Supply missing reasoning needed by the stated learner; identify added explanations as authored.
- **Figure or table:** the actual relationships, labels, axes, values or comparisons it conveys. A note saying “see figure on slide 8” does not replace the explanation. Retain a useful original or recreate it faithfully when appropriate.
- **Worked example:** its givens, requested result, method choice, essential working and conclusion. Preserve a distinct method/condition example even if another example uses similar formulas. Another question using the same broad topic is not automatically a substitute.
- **Exercise:** original identity, all requested subparts and their learning destination. Use the question registry below for detailed allocation rather than duplicating its entire table.

Explain exclusions such as administration, decoration or an explicit scope boundary. For duplicates, identify the retained teaching item and preserve any new conditions or subparts. “Basic,” “advanced,” “not an exam priority,” “already mentioned” and “too long” do not by themselves justify omitting substantive content from an authorized full teaching build.

Account for every page/slide/section, including pages with no substantive teaching item, so an uninspected page cannot disappear from the audit. Keep this accounting in the maintenance layer; students should encounter readable teaching, not a repetitive audit report.

Before marking an item checked, reopen the source and its teaching destination. Verify that the destination satisfies the content obligation, not merely that a link resolves or a topic word appears. Unreadable regions and unwritten explanations remain blocked or drafted, with a concrete next step. A populated coverage table is not proof of coverage.

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
