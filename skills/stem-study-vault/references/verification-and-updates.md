# Verification, handover and continuation

## Verify what matters

1. **Scope and source fidelity:** Work from the sources back into the actual lesson passages using the content obligations in the coverage map. Account for each source page/slide/section in the agreed batch. Check that conditions, non-obvious derivation steps, informative visuals, distinct worked examples and all question subparts survive. A broad matching heading or a link to the source does not pass this check. Inspect problem givens and distinguish official statements, your interpretation and added explanation. Report omissions with reasons; unresolved substantive items mean the batch is not fully taught.
2. **Learning usability:** Follow one complete learning unit as a student. Can they understand the notation, reproduce an example and attempt the next exercise without an untaught prerequisite or a missing diagram? Check that hints/answers are folded and no answer appears before an intended attempt.
3. **Subject correctness:** Independently recompute worked results and check key derivations, assumptions, dimensions and limiting cases. Use symbolic/numerical tools where appropriate. Formula rendering alone does not certify correctness. State which answers remain unverified.
4. **Structure and rendering:** Run the bundled wiki-link checker or an equivalent. Resolve newly introduced broken/ambiguous paths, headings and block IDs. Inspect actual Obsidian rendering when a supported UI is available; otherwise use an available Markdown/math renderer and explicitly identify that fallback. Do not claim rendered checks from regex checks. Test at least representative formulas, images, tables and callouts.
5. **Preservation:** Compare the protected-path snapshot; confirm original source copies against their hashes. Recheck incoming links where filenames or anchors changed. Compare against the pre-existing broken-link baseline rather than claiming the entire vault was clean.

Do not “repair” a protected note to make a checker pass. Fix the generated destination or report the conflict. Helpers are best-effort checks: their supported formats and limits are in [tools.md](tools.md).

## Useful delivery

Give the entry note, covered scope, a concrete next learning action and material limitations. Keep detailed source/validation records available in `Maintenance`. Explain how to continue by adding files, asking for a concept explanation, submitting a worked attempt or switching to review. Do not use file counts or word counts as evidence of learning improvement.

## Incremental updates

1. Read `Learning profile.md`, `Maintenance/Progress.md` and the current source/question maps.
2. Generate a fresh inventory outside the source tree. Compare relative identities and hashes with the prior inventory. A renamed identical file is not a new body of content; a same-named changed file is a new version to inspect.
3. Read changed sources; identify affected units and questions. Preserve old source identities/versions where needed to explain historical references. Do not infer that a changed hash means a changed conclusion.
4. Update affected generated notes, links and mappings in manageable batches. Preserve personal edits; where generated and personal text are mixed, keep personal text unchanged or add an adjacent supplement rather than replacing the page wholesale.
5. Run affected verification and preservation checks. Record completed work, unresolved questions and next steps. If interrupted, mark draft units accurately so a later session resumes rather than starts again.

Do not automatically create whole-vault backups, delete old sources, change Obsidian settings, publish anything or introduce automatic synchronization. If recovery is needed for an authorized substantial rewrite, use the user's existing versioning approach or a scoped copy with a clear purpose. A hash snapshot is not a backup.

## Evaluate usefulness after release

Ask willing users about a specific learning attempt: where they became stuck, whether they could solve a variation, whether source links helped resolve uncertainty and which maintenance step was difficult. Record evidence and limitations. Do not promise improved grades or present an unmeasured efficiency gain as established fact.
