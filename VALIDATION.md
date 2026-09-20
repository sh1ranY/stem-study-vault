# Validation and known limits

Release preparation: 2026-09-20.

## Checks actually performed

- The bundled skill-creator frontmatter/name validator accepted the skill.
- 26 Python tests passed on macOS with Python 3.9.6, pypdf 6.13.3 and python-pptx 1.0.2; no tests were skipped. These include real generated PDF/PPTX extraction fixtures, blank-page handling, table text, PDF page bounds, safe initialization, overwrite refusal, source preservation, protected-file changes/deletions, ambiguous/missing links and a CLI workflow.
- The original demo contains 12 Markdown notes and 34 checked wiki links: no broken/ambiguous links or checker warnings were detected before Obsidian created its local settings directory.
- The RC worked numbers were independently recomputed; the zero-initial-condition solution was substituted into the governing differential equation at several times. The derivations and nonzero-initial-condition solution were also read against the original demonstration inputs.
- 99 math spans in the ten generated/non-source demo notes passed a local KaTeX parser check. This was a development-environment check, not a dependency bundled with the skill.
- In Obsidian 1.13.7, the demo was opened as a new vault. The start-page link opened the lesson. Representative integrals, fractions, exponentials and the boxed response formula rendered correctly. The P1 hint and solution were initially collapsed, and the solution expanded with its equations readable.

## What those checks do not establish

- No controlled learning study, time-saving measurement or grade improvement has been performed.
- No independent fresh-agent evaluation suite has been run. The manual scenarios in `tests/behavioral-evaluation.md` are reusable evaluation plans, not claimed results.
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
