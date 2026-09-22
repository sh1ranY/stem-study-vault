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

Use a textbook voice: precise, readable sentences that develop one idea and lead into the next. A paragraph should add a useful meaning, reason, distinction, condition or consequence. Prefer explicit connections such as “this quantity is held fixed so that…” and “we can make this substitution because…” to a row of disconnected conclusions.

Introduce a concept through the problem it resolves; explain its meaning in the current setting; connect it to the mathematical formulation; then show what it lets the learner infer. Do not force these functions into four little headings for every concept. Use headings at natural conceptual boundaries and lists/tables where the information is actually parallel. Keep derivation and comparison tables when useful, rather than imposing a ban on all lists.

For contrastive concepts, keep the comparison dimension explicit: what is chosen, what is fixed, what is optimized, and what question each model answers. Saying “A fixes income, B fixes utility” can summarize an explanation; it cannot replace the explanation of why the two experiments differ.

A short recap belongs after the developed account. Do not compress an entire lecture into “key points → one worked example → one self-test” when its sources contain multiple distinct teaching units. Do not pad with repeated reassurance, rhetorical questions, unrelated analogies or statements of importance. Useful density means retaining distinct explanatory content; neither word count nor the absence of paragraph breaks measures it.

## Make a derivation reproducible

Before manipulating symbols, establish the question, variables, givens, assumptions and governing definition/model. For every non-obvious transition, explain both the mathematical permission and its purpose in the solution.

For example, if a calculation suddenly uses a tangency condition, teach where it comes from and when an interior tangency is appropriate. If it then combines that condition with a constraint, explain why both equations are needed: one chooses the best point along a feasible set, the other locates that set. A passage saying “minimize expenditure, hence y = 2x” omits the central reasoning.

Match mathematical detail to the learner's stated foundation. Refresh an unfamiliar derivative, integral, optimization condition or algebraic manipulation when it is needed, using a small check or explanation, then return to the actual problem. Routine arithmetic need not receive a paragraph per operation. Do not silently presume an earlier lesson teaches a prerequisite: link to the actual explanation, and briefly reactivate the part used now. An absent, unread or merely planned prerequisite needs an explanation here or an honest dependency note.

Include exceptional cases that matter in the source: a denominator that can vanish, a corner solution, an initial condition, an approximation region, a convergence requirement or a sign convention. A short independent example cannot stand in for a distinct supplied example that exists to teach another case.

Use inline `$...$` and display `$$...$$` for mathematics, not backtick code spans or plain-text chains of subscripts. Separate a displayed equation from the paragraph explaining it. Define notation and physical units when relevant; economic quantities and dimensionless indices need their interpretation rather than invented physical units. A parsing check is separate from a mathematical check.

## Use examples to teach decisions

Keep each substantive supplied example and all of its requested subparts traceable. An example should let the reader see how its givens suggest a model, why that method is suitable, how the result follows and what the answer means. Interleave working with explanation; do not place all the reasoning in an optional folded solution if it is required before the first independent attempt.

When a problem compares several states, name the states before calculating their differences. Record what changes and what stays fixed at each transition. In a diagram, use consistent point labels, axes and constraints so “from the first point to the compensated point” has an unambiguous meaning. Interpret the sign and units of the result; where two pieces should add to a total, check that identity and its interpretation.

Visually inspect the source's essential figures/tables. Teach the relationships they contain; retain or faithfully redraw them when necessary. For a new explanatory figure, state its model and verify coordinates, labels, signs and correspondence with the text. A decorative image does not replace a needed geometry, waveform, circuit or algorithm trace.

Check answers with a method that could expose a mistake: substitution into the original relation, dimensions, limiting cases, a second derivation or numerical evaluation. Distinguish official final answers from authored expanded working, and flag contradictions rather than silently repairing source data.

## Practice after teaching its prerequisites

Allocate supplied questions by prerequisite readiness and training purpose, not a fixed count per lesson. Keep distinct methods, conditions and subparts. Repetitive same-method items can be optional reinforcement; they still need a recorded destination. Multi-topic problems belong after their dependencies. Respect any reserved unseen papers.

A check that asks only for substitution into the immediately preceding example is weak evidence of understanding. Where appropriate, use an additional task that changes a condition, requires selecting a method, interpreting a result or explaining why an approach fails. Clearly label authored questions. Do not manufacture filler when supplied questions already provide that practice.

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

Read the source alongside the lesson, then attempt a relevant supplied question using the lesson alone. Look for missing concepts/branches, unexplained transitions, undefined notation and reliance on absent diagrams or source pages. A successful familiar worked example does not test all the source's other cases.

Explain the lesson's conceptual connections in ordinary language. If its paragraphs can be replaced by a short list without losing any reasoning, inspect whether it is still only a recap. Repair the specific missing substance instead of inflating every section to a word quota.

Keep content-review status distinct from student proficiency. Record only actual attempts or reported feedback as learning evidence. Generating all files, passing link checks, rendering equations and having a populated audit table do not establish that the content was fully taught or that the learner has mastered it.
