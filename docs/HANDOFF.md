# STEM Study Vault — image unit handoff

Updated 2026-10-19. Verify Git status and the PR revision before continuing.

The bilingual ELEC270 image-processing unit opens at
`/?course=ELEC270&unit=image-filtering`. It connects prediction, a deterministic
image lab, five optional foundation bridges, four families of bounded checks and
reflection to existing course practice. See the
[release notes](releases/2026-10-19-image-processing.md),
[design and scope](plans/2026-10-19-interest-led-learning.md),
[usage](../apps/study-studio/README.md) and
[validation](../apps/study-studio/VALIDATION.md).

This PR is based on main and contains only the image unit and related skill,
documentation and tests. Earlier curriculum expansion, translation caching and
cross-chat continuation work are separate changes; this PR does not merge them.

The teaching rules live in the existing skill and
`references/interest-and-applications.md`. Unit activity belongs to the Study
Studio account database; it is not automatically copied into Skill learning
records. Keep personal evidence separate from synthetic tests and development
progress. Private course documents, local databases and API configuration are
not included in this release.

The unit needs no model calls. Its numerical/choice checks do not grade arbitrary
written reasoning or prove long-term retention. Real student/professor feedback
and physical-device accessibility testing remain future validation work. No
cloud deployment is part of this change.
