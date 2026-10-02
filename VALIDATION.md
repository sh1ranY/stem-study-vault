# Validation and known limits

Initial release: 2026-09-20. Teaching-depth revision: 2026-09-22.

## Initial release checks (2026-09-20)

- The bundled skill-creator frontmatter/name validator accepted the skill.
- 26 Python tests passed on macOS with Python 3.9.6, pypdf 6.13.3 and python-pptx 1.0.2; no tests were skipped. These include real generated PDF/PPTX extraction fixtures, blank-page handling, table text, PDF page bounds, safe initialization, overwrite refusal, source preservation, protected-file changes/deletions, ambiguous/missing links and a CLI workflow.
- The original demo contains 12 Markdown notes and 34 checked wiki links: no broken/ambiguous links or checker warnings were detected before Obsidian created its local settings directory.
- The RC worked numbers were independently recomputed; the zero-initial-condition solution was substituted into the governing differential equation at several times. The derivations and nonzero-initial-condition solution were also read against the original demonstration inputs.
- 99 math spans in the ten generated/non-source demo notes passed a local KaTeX parser check. This was a development-environment check, not a dependency bundled with the skill.
- In Obsidian 1.13.7, the demo was opened as a new vault. The start-page link opened the lesson. Representative integrals, fractions, exponentials and the boxed response formula rendered correctly. The P1 hint and solution were initially collapsed, and the solution expanded with its equations readable.

## Teaching-depth revision checks (2026-09-22)

- The skill frontmatter/name validator passed. The 26 Python tests were rerun and passed with no skips; the four bundled Node.js math-checker tests also passed.
- The seven skill reference documents contain 145 math spans; the bundled KaTeX checker reported no syntax errors. This is syntax validation, not a claim of mathematical correctness or Obsidian rendering.
- The new original [teaching standard](skills/stem-study-vault/references/teaching-standard.md) was read for continuous explanation, defined conditions, justified optima, state comparisons, geometry, interpretation and independent practice. Its two numerical scenarios were recomputed separately, including budget feasibility, target utility, tangency, minimum expenditure and the sum of the two effects. The minimum expenditure was also checked against the AM–GM lower bound.
- An isolated agent generated four Chinese lessons and P1–P3 from 16 source sections (15 substantive plus one administrative). The parent reviewer read all source sections, lessons and ten practice subparts, checked the source-to-passage correspondence and independently recomputed the numerical cases. See the [forward-test report](tests/results/2026-09-22-forward-test.md) for exact findings, a minor post-generation editorial correction and limits.
- The independent vault passed 150 internal wiki-link checks and parsed 477 math spans in its 15 non-source notes. The source/skill input hashes remained unchanged. A browser HTML/KaTeX fallback was visually inspected for representative formulas, three diagrams and folded solutions; this revision was not tested in Obsidian itself. The [test output archive](tests/results/consumer-choice-vault-2026-09-22.zip) is available for inspection.
- The accompanying diagram was generated from the stated equations and visually inspected: its A/B/C coordinates, budget-line slopes, old/new utility curves and labels agree with the teaching text.
- Local Markdown link targets in the public documentation were checked separately from the bundled wiki-link checker. No missing target was found. This does not certify external URLs or every heading fragment.

## Reading and practice revision checks (2026-09-29)

This change updates teaching instructions, review criteria and an [original progression example](skills/stem-study-vault/references/reading-and-practice-example.md); helper code is unchanged.

- The skill validator passed. The bundled math checker parsed 222 spans across eight reference documents without syntax errors, and all local Markdown link targets in the repository resolved. A syntax/link check does not establish teaching quality.
- All five numerical cases in the new example were checked with exact rational arithmetic using a finite-sum expression independently of its step-by-step recurrence calculations. Twelve input/state combinations also confirmed the direction condition in the changed-coefficient task.
- Manual reading checked the worked example and all four exercises for complete local inputs, separate folded hints/solutions, explicit initial-state resets, an identifiable change of demand and prerequisites taught before use. Review caught that the direction-comparison method deserved a visible explanation before the final variation; that explanation was added instead of leaving it only in an earlier solution.
- The new source-screenshot rules and behavioral scenario were reviewed as instructions; no new source-image extraction trial, independent agent run or learner study was performed for this revision. The September 22 forward-test results describe that earlier frozen version and must not be treated as observed validation of the new practice behavior. No new full-course or Obsidian-native rendering result is claimed.

## Optional learning-diagnosis revision checks (2026-10-02)

This revision adds optional diagnosis/adaptation instructions, subject-specific task guidance, strategy extraction, a versioned record contract and a **read-only** record validator. Existing vaults do not require records or migration. The three [original examples](examples/diagnosis/README.md) contain authored teaching and explicitly synthetic responses, not outputs of a fresh generation run or real student results.

- All 45 Python tests passed with no skips: 26 existing tests plus 19 record/answer tests. Environment: macOS, Python 3.9.6, pypdf 6.19.0, python-pptx 1.0.2. The initial run skipped two extraction tests because dependencies were absent; the rerun after installing those dependencies in an isolated development environment passed both. The skill-creator validator also passed after adding PyYAML 6.0.3 to that environment.
- Record tests cover all three valid fixtures, skipped diagnosis, malformed references/types, synthetic/real separation, self-report limits, support and exact-task exposure, objective matching, unknown retention, decision ordering, correction propagation, and CLI read-only behavior/output privacy. These tests validate a contract, not the semantic truth of answers or provenance.
- Critical original answers were independently recomputed: two ramp constructions against piecewise specifications at 14 times including transition endpoints; three requirement counterexamples; and 14 independent relational insertions, each on a reset in-memory SQLite database with foreign keys enabled. This is not a MySQL compatibility test or a natural-language grader.
- All four Node.js checker tests passed. KaTeX parsed 57 formula spans in the new example materials, 222 in the skill references and 99 in the existing RC demo with no syntax errors. The existing demo retained 34 valid wiki links and no warnings. Local Markdown file targets were also checked with no missing file; this does not certify external links or heading fragments.
- Six example task/teaching pages were rendered in a local HTML/KaTeX preview at widths 1100 and 390 pixels. No page overflow was detected; all three answer sections started closed and expanded successfully at both widths. The three desktop teaching screenshots were visually inspected for paragraph readability, displayed mathematics and code. This is a browser fallback, not a new Obsidian-native check; mobile layout was checked programmatically rather than by a separate visual review.
- Public Markdown, JSON and Python files were scanned for local account paths and clipboard attachment paths; none were found. Public fixtures contain no supplied university screenshots, private course documents or real attempts. This targeted check is not a general secret scanner.

The new behavioral scenarios remain evaluation protocols. No new independent-agent forward run, full-course output assessment, fresh installation trial or learner study was performed. No automatic grading, adaptive model training, record-writing/migration service, concurrency control or learning efficacy is claimed. Snapshot writing is an instructed, checked workflow performed by the agent; the new helper only reads.

## What those checks do not establish

- No controlled learning study, time-saving measurement or grade improvement has been performed.
- One fresh-agent forward run was performed on a small original three-lecture course; see the [observed-output report](tests/results/2026-09-22-forward-test.md). Other scenarios in `tests/behavioral-evaluation.md` remain plans, not claimed results. This is not a repeated evaluation suite or a full-semester test.
- The skill was authored and exercised in a Codex session. Installation/discovery in a separate fresh Codex environment, Windows and Linux were not tested. The helper uses cross-platform Python interfaces, but that is not equivalent to observed cross-platform success.
- The tiny RC demo does not establish teaching quality across every STEM discipline or a complete semester of source material.
- Link checking does not validate ordinary Markdown links, semantic source support, every Obsidian feature, or mathematical truth. Optional text extraction does not perform OCR or recover image-based equations/diagrams reliably.
- Render inspection covered representative lesson content and callouts, not every note on every device/theme.

## Reproduce the automated checks

From the repository root, preferably in a virtual environment:

```sh
python3 -m pip install -r skills/stem-study-vault/scripts/requirements-extract.txt
python3 -m unittest discover -s tests -v
python3 skills/stem-study-vault/scripts/vault_tools.py check --vault examples/demo-vault
```

If PDF/PPTX dependencies are missing, their integration tests are skipped. Inspect test output rather than treating a skipped check as a pass. Opening the demo in Obsidian adds local `.obsidian` settings, which are intentionally excluded from the release and link scan.

## Optional math checker addition — 22 September 2026

Four Node.js behavioral tests passed: valid math with code exclusion, malformed syntax/unmatched delimiters, excluded directories, and bare commands. The bundled demo produced 10 checked files, 99 formula spans and no syntax errors under KaTeX 0.17.0. The optional checker is now bundled; the earlier development-only limitation above describes the initial release. Mathematical truth and Obsidian rendering remain outside this syntax check.
