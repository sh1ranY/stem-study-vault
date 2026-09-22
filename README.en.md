# STEM Study Vault

**Turn local lectures, exercise sheets and past papers into a personal Obsidian learning vault.**

A Codex skill for STEM and quantitative-course students. Its default output is a primary self-study text, preserving substantive source content while explaining concepts, reasons, connections and derivations in connected prose. It places independent practice after the relevant teaching and preserves source references and personal notes.

[中文说明](README.md) · [Original example vault](examples/demo-vault/Start.md) · [Validation and limits](VALIDATION.md)

## Teaching-quality revision — 2026-09-22

The revision addresses omissions and overly compressed, fragmented teaching reported during a whole-course trial. It adds item-level source accounting, source-to-lesson checks of actual explanations, explicit handling of conditions/visuals/distinct examples/subparts, and detailed batching for large courses. A topic heading or source link does not establish that the subject was taught.

The bundled [worked teaching standard](skills/stem-study-vault/references/teaching-standard.md) demonstrates justified transitions, model interpretation and connected prose through an original consumer-choice lesson. Its Chinese language and economics topic are illustrative; the skill should apply those teaching decisions to the user's subject and language. There is no fixed word or question quota. See the [teaching rubric](tests/teaching-rubric.md) for output-level evaluation.

An [independent forward-test report](tests/results/2026-09-22-forward-test.md) records the actual output from a three-lecture original source pack, including a post-generation editorial correction and the limits of this small trial.

## Install and use

You need Codex with access to your local files. Use Obsidian to read the result; no community plugins are required. The optional helper needs Python 3.9+. PDF/PPTX extraction has optional dependencies; no separate model API key is required by this project.

Ask Codex:

```text
Use $skill-installer to install the skill at skills/stem-study-vault
from https://github.com/sh1ranY/stem-study-vault.
```

Alternatively, copy the complete `skills/stem-study-vault` directory to `~/.agents/skills/`. Restart Codex if it does not appear. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery locations and invocation; host versions may offer different installation interfaces. This is a standalone skill, not a published plugin-directory entry.

Then ask:

```text
Use $stem-study-vault to build an Obsidian course from my local circuits materials.
Sources: /path/to/materials
Vault: /path/to/my-vault
I want systematic understanding and independent problem solving.
I know derivatives but my integration skills are rusty. Explain in English.
Preserve my existing personal notes. Start with a complete learning unit.
```

The skill inspects sources, asks for missing choices that matter, and builds a learning route. For large courses it works in batches and records progress for continuation. You can also request a complete small course directly. Open the output folder as an Obsidian vault, or open the course entry in your existing vault.

## Try the original demo

Open `examples/demo-vault` as an Obsidian vault and start at `Start.md`. It includes original RC-circuit sources, a complete derivation, three exercises with folded hints/solutions, a transfer problem, and source/question coverage maps. The demo is in Chinese to match the project's initial audience; generated teaching can use your preferred language.

To test a fresh build, ask Codex to use only `examples/demo-vault/Sources/Original` and create a new vault outside the repository. Ask it not to copy the finished demonstration lessons. The demo is a tiny original course, not official university or examination material. GitHub does not fully render Obsidian wiki links and callouts.

## Continue learning

- Add materials and ask for an incremental update while preserving personal notes.
- Share an actual worked attempt and ask for the first misunderstanding and a transfer exercise.
- Switch to exam revision; specify which papers must remain unseen.

Default behavior is systematic learning. Slides-only inputs can be supplemented with clearly authored exercises. Papers-only inputs support a revision route whose full syllabus coverage remains unknown. Scans and handwriting need available visual reading/OCR. The extraction helper supports PDF, PPTX, Markdown and TXT, not legacy PPT, videos or learning-platform downloads.

## Checks and limits

The helper inventories files, extracts text with page/slide boundaries, creates new course scaffolds, checks common wiki links, and compares protected-file hashes. It does not generate teaching by itself. Codex must read the sources and check reasoning, conditions, diagrams and answers. Structural checks do not prove mathematical correctness or improved learning outcomes.

Local helpers do not upload materials or make network requests. Codex processes materials through your configured service environment; model processing is not guaranteed to be offline. Building a private vault does not publish it. MIT covers repository code, documentation and original examples; it does not change the rights attached to your own course materials.

## Development

In a virtual environment, from the repository root:

```sh
python3 -m pip install -r skills/stem-study-vault/scripts/requirements-extract.txt
python3 -m unittest discover -s tests -v
python3 skills/stem-study-vault/scripts/vault_tools.py check --vault examples/demo-vault
```

Without extraction dependencies, PDF/PPTX integration tests are skipped. See [helper documentation](skills/stem-study-vault/references/tools.md) and [behavioral evaluation scenarios](tests/behavioral-evaluation.md). Report reproducible learning problems using minimal original or redistributable examples; exclude private course files from issues and pull requests.

License: [MIT](LICENSE).

## Optional formula checker / 可选公式检查

A read-only KaTeX syntax checker is now included. See [usage and limitations](skills/stem-study-vault/references/tools.md#optional-formula-syntax-check). Run `npm ci`, `npm run check:math` and `npm run test:math` from this repository.
