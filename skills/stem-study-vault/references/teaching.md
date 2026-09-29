# Write a primary learning text

For a new course or a major teaching rewrite, read this reference before drafting. Read [teaching-standard.md](teaching-standard.md) once for a concrete depth/style example. Its economics topic and Chinese language are illustrative; transfer the explanatory decisions to the learner's subject and preferred language.

## Preserve difficulty; supply the path through it

The default output is a text the learner can study from, not a digest of what the course mentions. Preserve substantive source content using the coverage procedure in [sources-and-questions.md](sources-and-questions.md). Accessibility comes from supplying explanations and prerequisites, not from deleting the course's more demanding ideas, conditions, derivations or examples.

Distinguish three kinds of apparent coverage:

- **Named:** the topic appears as a heading or brief definition.
- **Stated:** a formula/result and perhaps its meaning are given.
- **Taught:** the learner can follow why it arises, when it applies and how to use it at the level required by the source material.

Only the third meets the primary-text standard. A correct formula followed by a source link is not a substitute for the intervening teaching. Pages assigned to later batches remain pending; they do not become optional just because the current batch is finished.

## Explain in connected paragraphs

Keep the information needed for the current step at the reading location: define notation before use; supply the actual table, diagram, initial conditions and assumptions for an example or question. A reusable local embed or a separately expandable input panel is preferable to copying large data repeatedly. Keep input visible without opening a hint or solution, and distinguish source figures, worked-example data and exercise data. Check that the embed resolves and is readable; a link that sends the learner elsewhere to recover necessary givens is not equivalent.

Use a textbook voice: precise, readable sentences that develop one idea and lead into the next. A paragraph should add a useful meaning, reason, distinction, condition or consequence. Prefer explicit connections such as “this quantity is held fixed so that…” and “we can make this substitution because…” to a row of disconnected conclusions.

Introduce a concept through the problem it resolves; explain its meaning in the current setting; connect it to the mathematical formulation; then show what it lets the learner infer. Do not force these functions into four little headings for every concept. Use headings at natural conceptual boundaries and lists/tables where the information is actually parallel. Keep derivation and comparison tables when useful, rather than imposing a ban on all lists.

For contrastive concepts, keep the comparison dimension explicit: what is chosen, what is fixed, what is optimized, and what question each model answers. Saying “A fixes income, B fixes utility” can summarize an explanation; it cannot replace the explanation of why the two experiments differ.

A short recap belongs after the developed account. Do not compress an entire lecture into “key points → one worked example → one self-test” when its sources contain multiple distinct teaching units. Do not pad with repeated reassurance, rhetorical questions, unrelated analogies or statements of importance. Useful density means retaining distinct explanatory content; neither word count nor the absence of paragraph breaks measures it.

## Make a derivation reproducible

Before manipulating symbols, establish the question, variables, givens, assumptions and governing definition/model. For every non-obvious transition, explain both the mathematical permission and its purpose in the solution. Name the premise before using the result, explain changes of representation, and connect the conclusion back to the question. Expand the step where the stated learner would otherwise have to guess; repeated definitions and routine arithmetic do not create depth.

For example, if a calculation suddenly uses a tangency condition, teach where it comes from and when an interior tangency is appropriate. If it then combines that condition with a constraint, explain why both equations are needed: one chooses the best point along a feasible set, the other locates that set. A passage saying “minimize expenditure, hence y = 2x” omits the central reasoning.

Match mathematical detail to the learner's stated foundation. Refresh an unfamiliar derivative, integral, optimization condition or algebraic manipulation when it is needed, using a small check or explanation, then return to the actual problem. Routine arithmetic need not receive a paragraph per operation. Do not silently presume an earlier lesson teaches a prerequisite: link to the actual explanation, and briefly reactivate the part used now. An absent, unread or merely planned prerequisite needs an explanation here or an honest dependency note.

Include exceptional cases that matter in the source: a denominator that can vanish, a corner solution, an initial condition, an approximation region, a convergence requirement or a sign convention. A short independent example cannot stand in for a distinct supplied example that exists to teach another case.

Use inline `$...$` and display `$$...$$` for mathematics, not backtick code spans or plain-text chains of subscripts. Separate a displayed equation from the paragraph explaining it. Define notation and physical units when relevant; economic quantities and dimensionless indices need their interpretation rather than invented physical units. A parsing check is separate from a mathematical check.

For algorithms and processes, make the mechanism reproducible as well: show the initial state, the operation, the relevant intermediate state and the check on the result. For example, a join needs its actual input rows and intermediate matches; a transaction trace needs shared values distinguished from local values. Explain why a step is permitted, rather than presenting only the final table or labeling the algorithm. Keep the detail proportional to the concept being taught.

## Use examples to teach decisions

Keep each substantive supplied example and all of its requested subparts traceable. An example should let the reader see how its givens suggest a model, why that method is suitable, how the result follows and what the answer means. Interleave working with explanation; do not place all the reasoning in an optional folded solution if it is required before the first independent attempt.

When a problem compares several states, name the states before calculating their differences. Record what changes and what stays fixed at each transition. In a diagram, use consistent point labels, axes and constraints so “from the first point to the compensated point” has an unambiguous meaning. Interpret the sign and units of the result; where two pieces should add to a total, check that identity and its interpretation.

### Use source screenshots where they help explain

Inspect the actual source page before selecting a screenshot. Include it when spatial relationships, connections, a sequence or a table materially help the learner follow the explanation; do not add one to every section as a quota. Crop to the useful region while retaining essential labels, axes, units, legends and conditions. Save a readable local asset, cite the actual file/version and physical page or slide, and place it beside the paragraph that uses it.

Explain what to look at and how the visible relationship supports the reasoning: identify the relevant node, row, arrow or interval, then connect it to the quantities or steps in the text. Supply required symbols and givens in readable text as well; an image or a caption saying “see the slide” cannot replace the explanation. Distinguish the source figure's data from nearby authored examples and exercise inputs.

Check the image at an ordinary reading width, including table and formula legibility. If a source image is unclear, seek a better source or make a verified redraw explicitly labeled as authored; do not guess unreadable labels or silently correct the original. State any source discrepancy beside the image. Preserve the original file and distinguish annotations/redraws from untouched source content. For a new explanatory figure, verify coordinates, connections, signs and labels against the model and accompanying text. Source-image use within an authorized private vault does not authorize public redistribution.

Check answers with a method that could expose a mistake: substitution into the original relation, dimensions, limiting cases, a second derivation or numerical evaluation. Distinguish official final answers from authored expanded working, and flag contradictions rather than silently repairing source data.

## Build connected practice with increasing independence

Allocate supplied questions by prerequisite readiness and training purpose, not a fixed count per lesson. Keep distinct methods, conditions and subparts. Repetitive same-method items can be optional reinforcement; they still need a recorded destination. Multi-topic problems belong after their dependencies. Respect any reserved unseen papers.

Place a useful attempt near the explanation that enables it, at a natural conceptual boundary rather than after every paragraph. Build a sequence around an identifiable capability. A possible progression is a fully explained example, a lightly guided attempt, an independent reconstruction, a changed condition or method-selection problem, then a later mixed revisit. These are design choices, not mandatory stages or a fixed question count. Reuse supplied problems first and label any authored bridge or variation.

For each transition, identify what becomes harder: less prompting, an extra decision, a changed assumption, a new representation or combining already-taught ideas. Larger numbers or longer algebra alone do not establish progression. Early steps should usually change one major demand at a time; if an advanced supplied problem jumps over an untaught prerequisite, teach a bridge or schedule it after that prerequisite, keeping the original problem traceable. Introduce new ideas in teaching, not for the first time in a solution.

Keep the chain understandable without making later attempts depend on obtaining an earlier answer. State whether inputs reset or carry forward; when an earlier result is intentionally needed, provide it at the later task as a clearly labeled continuation so one mistake does not block the whole sequence. Do not expose an earlier reserved answer before its intended attempt. Give each step enough local data and a route back to the exact explanation if the learner gets stuck.

Use later cumulative or mixed practice when it serves retention and method selection, after the constituent ideas have been taught. If actual attempts show a gap, return to the earliest missing step with targeted support; if the learner demonstrates readiness, reduce scaffolding or skip redundant drills. Do not infer readiness from files generated, an answer revealed or a page read. A sequence can increase challenge overall without increasing difficulty on every single question. Read [reading-and-practice-example.md](reading-and-practice-example.md) when designing a new sequence or diagnosing an abrupt difficulty jump.

Provide enough givens and diagrams to attempt the question. Keep hints and full solutions separately folded; their titles must not reveal answers. Do not leak a reserved or self-test answer through a nearby summary, caption, alias or uncollapsed numerical check.

```markdown
### Practice — Q-S01-2

Question, givens and source/original/adapted/authored identity.

> [!hint]- Hint
> A first useful step, without giving the result.

> [!success]- Solution — authored working
> Explain method selection, justified steps, interpretation and a check.
>
> $$\text{equation here}$$
```

## Review the actual teaching before declaring the batch complete

Read the source alongside the lesson, then attempt a relevant supplied question using only the lesson and its local inputs. Follow at least one transition between practice steps: identify the prerequisite already taught and the new demand, verify that the later task is solvable without guessing data or reading its solution, and check that a previous wrong answer does not silently corrupt it. Inspect one screenshot/figure with its explanation when visuals are used. Look for missing concepts/branches, unexplained transitions, undefined notation and reliance on absent diagrams or source pages. A successful familiar worked example does not test all the source's other cases.

Explain the lesson's conceptual connections in ordinary language. If its paragraphs can be replaced by a short list without losing any reasoning, inspect whether it is still only a recap. Repair the specific missing substance instead of inflating every section to a word quota.

Keep content-review status distinct from student proficiency. Record only actual attempts or reported feedback as learning evidence. Generating all files, passing link checks, rendering equations and having a populated audit table do not establish that the content was fully taught or that the learner has mastered it.
