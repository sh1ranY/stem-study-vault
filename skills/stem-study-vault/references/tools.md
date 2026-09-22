# Local helpers

Use Python 3.9 or newer. Locate `scripts/vault_tools.py` relative to this skill, not relative to the learner's current working directory. Quote paths containing spaces. The examples below assume a shell opened at the skill directory; replace example paths with the actual authorized locations. Windows users can use `py` instead of `python3` and normal Windows paths.

```sh
python3 scripts/vault_tools.py inventory --source "/path/to/course-materials"
python3 scripts/vault_tools.py inventory --source "/path/to/course-materials" --output "/path/to/source-inventory-v1.json"
python3 scripts/vault_tools.py init --vault "/path/to/My Vault" --course circuits --title "Circuits"
python3 scripts/vault_tools.py check --vault "/path/to/My Vault"
python3 scripts/vault_tools.py snapshot --source "/path/to/My Vault/circuits/Personal" --output "/path/to/personal-before.json"
python3 scripts/vault_tools.py compare --source "/path/to/My Vault/circuits/Personal" --snapshot "/path/to/personal-before.json"
```

Inventory/snapshot records relative names, sizes and SHA-256 hashes, skipping hidden entries and symlinks with an explicit skipped list. Use a snapshot for each protected directory; include personal attachments and dependencies where relevant. Snapshot files must live outside the scanned tree and must not already exist. `compare` reports changed, missing and added paths; additions alone do not violate preservation. Inspect skipped paths separately if they matter. None of these operations backs up content.

`init` creates a new course folder and a few navigation/profile/progress pages; it refuses an existing course. It does not copy sources or generate teaching content. Use it for a new course only. For an established vault, adapt the existing layout directly. Do not delete a course to make initialization succeed.

## Optional extraction

If no suitable PDF/PPTX reader is already available, install the extraction dependencies in an isolated environment using the host's normal package workflow:

```sh
python3 -m venv /path/to/study-tools-venv
/path/to/study-tools-venv/bin/python -m pip install -r scripts/requirements-extract.txt
/path/to/study-tools-venv/bin/python scripts/vault_tools.py extract --source "/path/to/course-materials" --output "/path/to/extracted-v1"
```

On Windows the environment interpreter is `study-tools-venv\Scripts\python.exe`. The extraction output must be a new directory, disjoint from the source tree. Original files are never modified. Each PDF/PPTX produces JSON with physical page/slide positions. MD/TXT retain their text. Unsupported files, empty text units and errors remain visible in `manifest.json`; partial extraction returns a nonzero status. An empty text unit can mean a scanned page or an intentional blank, so inspect it rather than guessing. Image-only content requires available OCR or visual reading. PDF/PPTX extraction does not read images, reliably reconstruct equations or certify coverage.

## Link checker scope

`check` reads Markdown and validates Obsidian wiki targets, ordinary headings, block IDs and attachment existence. PDF page bounds are checked when pypdf is available. It ignores code fences/inline code and frontmatter; it skips hidden paths and symlinks. Prefer explicit vault-relative wiki paths to avoid ambiguous basenames.

Markdown-style links, complex/nested heading selectors, Canvas files, external URLs, aliases declared only in YAML, transcluded block semantics, math, semantic source alignment and actual Obsidian rendering are outside this check. Warnings expose unchecked Markdown links and PDF fragments. Use appropriate additional tools or manual inspection when these occur; do not equate an `ok` result with a fully verified course.

Exit codes: `0` completed/no detected errors; `1` detected broken links, preservation changes or incomplete extraction; `2` invalid inputs or operational failure. JSON output is intended for inspection and saved reports, not direct insertion into learning pages.

## Optional formula syntax check

From the repository root, use Node.js 22+ and run `npm ci`, then:

```sh
node skills/stem-study-vault/scripts/katex_check.mjs examples/demo-vault
npm run test:math
```

Pass any authorized course directory instead of the demo path. The read-only checker reports JSON with file/formula counts and errors. It checks dollar and LaTeX math delimiters, KaTeX syntax, and common bare commands; code spans/fences, source folders, hidden entries, symlinks and node_modules are skipped. Exit 0 means no detected syntax errors, 1 means errors, and 2 means invalid input. Output includes file paths, so review before sharing reports.

This tool is adapted from the personal knowledge-base validation workflow. It does not establish mathematical correctness, correspondence with source material, or identical rendering in Obsidian. Unescaped currency dollars may need manual interpretation. It is optional; ordinary learning tasks do not require installing Node dependencies.
