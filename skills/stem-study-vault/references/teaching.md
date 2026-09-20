# Teaching for understanding and transfer

Organize by concept dependencies, retaining a visible mapping to lectures. A lecture index is not automatically a calendar week. Keep the first-learning path readable in sequence, with topic pages for later connections and method selection.

## A complete learning unit

Use the following sequence where it helps the subject; combine short elements naturally:

1. A concrete question or situation, and why the concept helps.
2. An intuitive explanation connected to the rigorous definition.
3. Symbols, dimensions, assumptions, valid domain and sign conventions.
4. The reasoning/derivation, explaining each non-obvious transition.
5. A worked example showing how to identify and choose the method.
6. An independent problem after its prerequisites, with separate folded hint and solution.
7. A common error, a transfer question and a short check of understanding.

Use coherent explanatory paragraphs. Do not replace teaching with lists of facts, literal slide translations or excessive conversational filler. A useful analogy states its correspondence and where it stops applying. Refresh a rusty prerequisite at the point of use, then return to the actual problem.

## Equations and derivations

- Define quantities before use, including whether they are scalars, vectors, samples or continuous functions. Explain units and normalization conventions.
- State assumptions before the result: initial conditions, linearity, domain, independence, approximation, convergence or operating region as applicable.
- Show why a transformation is allowed. Check denominators, endpoints, exceptional cases and whether an operation loses solutions.
- Distinguish exact equalities, approximations and empirical rules. A course convention is not necessarily universal.
- In worked answers, verify through substitution, differentiation, dimensional analysis, limiting behavior, a second method or appropriate numerical computation. Pick checks that could catch the actual error.
- Use a diagram when geometry, a circuit, a waveform or a dependency is hard to understand in prose. Check labels, axes, units and correspondence with the equations. Visually inspect source figures before recreating them; do not invent missing circuit connections or graph values.

The same principle extends beyond calculus: algorithms need preconditions and invariants, proofs need justified implications, experiments need measurement assumptions and uncertainty, and statistical conclusions need model assumptions.

## Practice design

Prefer supplied questions that match the just-taught prerequisites. Include subparts; do not count answer continuation pages as new questions. Put repeated same-method questions in optional reinforcement, multi-topic problems after their prerequisites, and unseen mock exams in a separate route. Never enforce an arbitrary number of questions per concept.

When supplied material has a genuine gap, author a clearly labeled exercise. A worked example reused as a test is seen practice, not unseen assessment. Provide sufficient data so exercises can be attempted without hunting through unrelated pages.

Use this Obsidian pattern, including `>` on every line inside the callout:

```markdown
### Practice — Q-S01-2

Question and givens. Source and original/adapted/authored status.

> [!hint]- Hint
> The first useful step; no answer in the title.

> [!success]- Solution — independently derived
> Explain the method, steps, result and a check.
>
> $$\text{equation here}$$
```

Do not leak answers in preceding headings, summaries, figure filenames/captions, aliases or hints. If original scans contain printed answers, use a question-only crop or transcribe the problem accurately and label it. Preserve the original file separately. “Official answer” may describe the final result while the expanded working remains authored; say so explicitly.

## Learning evidence and review

A useful self-check asks the student to explain why the method applies, solve a modest variation and identify a situation where the method fails. Record reported attempts in their own review log only within the requested scope. Distinguish unassessed, needs review and demonstrated on a specific task; never invent scores or infer mastery from reading.

Build revision pages around choosing between methods, contrasting easily confused ideas and connecting topics. Recommend the next exercise based on observed errors when available. Plan revisits flexibly; no fixed spacing schedule or promised grade is required.
