# ELEC270 local continuation — observed checks, 12 October 2026

Implementation: `continuation_tools.py` on the existing v1 learning record, original
three-task unit, lesson/rubric and fresh-chat protocol. No Study Studio changes.

## Observed automated results

- 57 Python tests passed, no skips, including the existing extraction tests.
  The 12 additions cover fresh-process continuation, stale summaries, corrections,
  stale and simultaneous writers, saved help, unknown exposure, pending tasks,
  invalid submissions, reinitialization refusal, skipped diagnosis, bank exhaustion,
  changed lesson content, identity/version rejection and the new signal answer.
- 4 existing Node math-checker tests passed. KaTeX parsed 250 formula spans across
  14 reference documents with no syntax errors. The new negative-slope task was
  separately checked at nine times, including transition endpoints. Existing ramp
  answer tests also passed.
- New behavior tests were observed failing before implementation: initially absent
  helper, then missing skip behavior, then acceptance of changed lesson content.
  They subsequently passed against the implemented helper.
- The real empty pilot and synthetic final record both passed the original
  read-only v1 validator. Private runtime files are excluded by `.gitignore`.

## Synthetic walkthrough

Each command started a new process reading the same disk record; no in-process
learning state was carried between commands. The 12-command sequence:

1. Initialize explicitly synthetic data and present d1.
2. Save the simulated misconception that cancelling slopes makes height zero.
3. Resume from disk: the observed gap remains and t1 is the next unused task.
4. Present t1; save a deliberately erroneous assessment of a response whose
   expression is correct but whose value at the jump is wrong.
5. Resume: the earlier evaluator-supplied independent judgment is visible.
6. Correct that assessment to partial because the step at zero equals one.
   The old observation remains inactive; current judgment is rebuilt and t1
   cannot become unused again.
7. Resume, present t2, save a correct response explaining the negative-slope
   reversal, then resume again. Independence is scoped to that last task;
   retention remains unknown and the finite bank is exhausted.

The trace and preview are in the ignored local validation directory. The user's
separate learner record has **zero attempts** and is **unassessed**.

## Presentation and limits

The lesson was rendered through Markdown and KaTeX in a local Chrome preview at
1100 and 390 px widths. Both screenshots were visually inspected for readable
paragraphs, equations and answer text; neither page overflowed horizontally.
The answer section started closed and could be expanded. This is a browser
fallback, not a new Obsidian-native rendering check.

This validates storage/protocol behavior using separate processes and synthetic
assessments. It is not an independently executed new-chat tutor evaluation, a real
learner session, an automatic mathematical grader or an efficacy study. The tutor
must still evaluate reasoning, record external help honestly and follow the
fresh-chat protocol. No multi-device synchronization, existing-record migration,
automatic task-bank extension or Windows writer support is claimed.
