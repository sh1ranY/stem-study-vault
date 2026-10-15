# STEM Study Vault — development handoff

Updated 2026-10-12. Verify current files and Git status before using this snapshot.

The local ELEC270 continuation pilot is implemented. Selected Matt Pocock source
and adapted course/project-memory guidance are now integrated into the existing
skill. Check Git history and the associated pull request for delivery status;
this handoff does not imply deployment or automatic synchronization with Study Studio.

Read only what the requested continuation needs:

- [CONTEXT.md](../CONTEXT.md): established product and learning vocabulary.
- [Evidence ownership decision](adr/0001-learning-evidence-authority.md): why
  project memory, course-production progress and learner evidence stay separate.
- [Course/project-memory protocol](../skills/stem-study-vault/references/project-memory.md):
  active adapted workflow, including bounded batches, handoff and sparse decisions.
- [ELEC270 implementation outcome](plans/2026-10-12-cross-chat-continuation.md) and
  [observed checks](../tests/results/2026-10-12-continuation.md): implementation
  and tested scope; private pilot entry is `.local/ELEC270/Course.md` when present.
- [Upstream source map](../third_party/mattpocock-skills/README.md): included
  modules, fixed revision, adaptation boundaries and update procedure.

To continue learning, read the private course entry and run the continuation
protocol's `resume` against the actual learner record. Synthetic validation belongs
to its separate directory. To change the implementation, begin with the relevant
contract and affected tests; use the current repository state over this snapshot.

Known limits: the learning pilot covers one original three-task unit. A real
cross-chat learner trial, task-bank migration/extension, Windows writer support and
Studio synchronization remain unimplemented or unmeasured. They are possible later
work, not authorization to expand the current task.
