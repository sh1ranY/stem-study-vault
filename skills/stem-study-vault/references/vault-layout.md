# Vault layout and note conventions

For a new course, a modest structure is enough:

```text
My Vault/
  Circuits/
    Course.md
    Learning profile.md
    Lessons/
    Topics/
    Practice/
    Personal/
    Sources/Original/
    Sources/Extracted/
    Assets/
    Maintenance/
      Progress.md
      Sources.md
      Coverage.md
      Questions.md
```

Create meaningful pages as they are needed. A new empty course created by the helper is a scaffold, not a completed knowledge base. Folder labels and teaching language may differ; retain an existing learner's organization. Never assume a semester length or course count. Use `Lessons` for dependency-ordered learning units even if a source calls them weeks, parts or lectures.

`Course.md` is the daily entry: learning goal, next lesson, sequence, practice/revision and source entry points. Keep build logs and extraction details under `Maintenance`. Personal notes are user-owned; generated corrections or explanations should live beside them unless the user requests edits.

Use simple frontmatter when helpful:

```yaml
---
type: lesson
course: circuits
status: draft
source_ids: [S01]
---
```

Content status describes writing/review progress; track learner proficiency separately and only with evidence. Store local dates only when relevant and known. Prefer stable filenames and block IDs for question targets, such as `^q-s02-1a`.

Inside a vault, use unambiguous vault-relative links for repeated names: `[[Circuits/Lessons/01 RC response#Time constant|Time constant]]`. Adapt this if the course itself is the vault root. In a table, escape an alias separator as `\|`. Use source page links and embedded local assets. Avoid absolute machine-specific paths and dependencies on Dataview or other community plugins.

When renaming generated notes, inspect incoming links first. Preserve compatible headings/block IDs where protected notes link to them. If a move would require rewriting protected personal notes, use a compatible entry point or defer the move; never silently break their learning record.
