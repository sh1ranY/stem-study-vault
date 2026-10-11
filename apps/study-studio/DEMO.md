# Professor demonstration · Learning Studio

**Purpose:** demonstrate a working mechanism, then ask for technical and pedagogical criticism. This is a focused ELEC270 Week 1 signal-construction example. The session below is scripted by the developer, not an experiment on students.

## Before the meeting

1. Double-click `start.command`; keep its terminal window open. Open http://127.0.0.1:8765 in a normal browser. No API key is required.
2. From My workspace, choose **Open sample unit** to create a fresh session. Existing work is preserved. A new session has one checkpoint and six new-construction variants available.
3. Keep `sample-material/signal-construction-brief.md` nearby for the import demonstration. It is original demonstration material; it is not a university slide deck.
4. The prepared mode does not need internet once dependencies are installed. Keep an Obsidian vault available if you want to open the final exported Markdown.

## Opening statement · 30 seconds

> This is a small working prototype of a source-grounded personal learning workspace. The student reads an explanation, attempts a problem, receives support selected from the evidence, and checks a fresh problem. Today I am demonstrating that loop with original prepared ELEC270 material. I am not claiming that these rules already diagnose general learning ability or that we have demonstrated improved learning outcomes.

## Walkthrough · 8–10 minutes

| Time | Action | What the professor can inspect |
| --- | --- | --- |
| 0–1 min | My workspace → Import a unit → choose the original Markdown brief. Expand its extracted text. Open the prepared ELEC270 unit. | The upload is real. Imported references and original prepared teaching are explicitly separate. The new-source generation button is disabled without a key. |
| 1–3 min | Read “Read the argument first”; mark read and continue to the plateau section. Move the graph's time slider. | Connected prose, intermediate substitutions, graph–formula correspondence, an explicit endpoint convention and optional prerequisite explanation. |
| 3–4 min | In the checkpoint, enter `3, 0, 0`; choose “The tail is zero because the slopes cancel.” Write “The slopes cancel, so I think the value is zero.” | The system sees correct substitution alongside incorrect tail values. It proposes a slope–height confusion, while acknowledging another possible explanation. It does not grade the written prose. |
| 4–5 min | Inspect the feedback and the addition to the plateau lesson. Open a hint; revise the tail values to `2, 2` and choose the explanation about preserving separation. | The support explains why cancelling growth does not remove height. A correct retry is guided/supported, not independent. |
| 5–6 min | Choose **Try a fresh construction**. For the first variant, enter `A=2`, `B=−2`, `C=−6`, `x(6)=0`. Select “The delayed ramp stops growth; the final step removes the plateau height.” Write `2 × (4 − 1) = 6, so the last step removes 6.` Submit without hints. | A first correct response to this new construction is recorded as a narrow independent check. This is near transfer, not proof of general mastery or delayed retention. |
| 6–7 min | Open **Learning record**. Compare the wrong attempt, supported correction and fresh check. | Each claim has an actual attempt. Reading progress, help exposure, confidence and independent checks are separate. Unobserved dimensions remain unassessed. |
| 7–8 min | Open Notes, save a personal explanation and refresh the page. Then export to Obsidian. | The reading position, notes and submitted attempts persist. The ZIP contains real Markdown, an SVG, original/extracted sources and the full learning record. Exporting worked answers records exposure for opened tasks. |
| Optional | Select **This observation needs correcting** on the wrong attempt. Give a reason and withdraw it. | Revisability without silently deleting the history or resetting answer exposure. |

Avoid opening hints or exporting before the independent-task step: both deliberately count as exposure for tasks already opened. The six fresh variants differ in timings and slopes; later answers are therefore different.

## Questions to put to the professors

1. **Diagnostic validity:** Is the observed combination of correct substitution and incorrect tail values sufficient to choose this next explanation? What short follow-up would distinguish conceptual confusion from an algebra slip?
2. **Task design:** Which counterexample or representation change would provide stronger evidence than another construction from the same family? How should we test retention later?
3. **Technical architecture:** Which boundary should be strengthened first: extracting mathematical sources, assessing open working, selecting support, or maintaining a reliable learner record? Would a reviewed task-bank layer be preferable to generating everything live?
4. **A feasible next study:** Could we build one reviewed task pack together, then compare adaptive support with an equally well-written generic lesson under the same study-time budget? What recruitment, supervision and data handling would your setting require?

## What to say when asked about AI

> The prepared path is deliberately authored and deterministic, so we can inspect the learning decisions. There is an optional server-side adapter for source-based draft generation, but it has only been tested with mocked responses. We do not yet have a key for a live test. A future agent could use the existing Skill to produce candidate lessons and task packs, but it would need separate validation before those packs drove learning claims.

## What this milestone does and does not establish

It establishes that the user journey, branch selection, evidence history, corrections, persistence and export can be made concrete. It does not establish that a particular student learns more, that six dimensions have been psychometrically validated, or that the system can replace an instructor across a course. Those are the questions for the next reviewed pilot.
