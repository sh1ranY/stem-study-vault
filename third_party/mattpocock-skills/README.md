# Matt Pocock skills — selected upstream source

Source: [mattpocock/skills](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336),
commit `49dd158d1076134a641b33efb035946536778336`, retrieved 2026-10-12.
The files listed in [UPSTREAM.json](UPSTREAM.json) are unchanged upstream files,
including their UI metadata. [LICENSE](LICENSE) is the original MIT notice.

This is a source archive for comparison and attribution, not a second installation.
Do not execute its workflows or discover its nested skills as part of ordinary
STEM Study Vault use. The active adaptation is inside
[the STEM skill](../../skills/stem-study-vault/references/project-memory.md), with
a [portable attribution notice](../../skills/stem-study-vault/THIRD_PARTY_NOTICES.md).
That installed skill needs neither this directory nor Matt's global skills.

| Upstream module | Adopted in STEM Study Vault | Deliberately adapted |
| --- | --- | --- |
| domain-modeling | Reuse established vocabulary; record consequential decisions and why | Keep existing CONTEXT.md and course terminology; create records only when needed |
| handoff | Short, actionable handoff that points to original artifacts | Persistent course/project entry rather than temporary OS storage; learner evidence stays canonical |
| to-spec | Agreed problem, scope, constraints and observable completion | Bounded course batches in existing progress notes; no issue publication, long story lists or mandatory extra approval |
| retro | Fix demonstrated navigation or validation failures | Narrow, evidence-based corrections; no routine session-log scans or compulsory review agent |
| writing-for-agents | Conditional pointers, progressive disclosure and one authority per fact | Self-contained references inside the existing skill, without extra skills to install |

Setup, interview/grilling, ticketing, review orchestration and plugin manifests are
not included. They are not needed for the course-memory workflow.

## Updating this archive

Fetch a chosen upstream commit into a separate temporary checkout. Compare only the
listed modules and their license; do not run setup scripts. Review changes against
the adaptation table, then replace the selected originals verbatim and update the
commit, retrieval date and file hashes in UPSTREAM.json. Keep adaptations outside
this directory. Update the portable notice/license if necessary, validate the
skill and affected behavior, and preserve private records. No automatic updater
is configured; an upstream change cannot silently replace the local workflow.
