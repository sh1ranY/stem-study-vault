# Independent forward test — 22 September 2026

## Scope and method

A fresh Codex agent received an isolated copy of the revised skill, the three original files in [the consumer-choice fixture](../fixtures/consumer-choice), and a request to build the complete small course in Chinese as a primary learning text for a student who knows basic derivatives but is rusty in constrained optimization. Conversation history was not passed to the agent. It did not receive the review rubric or expected answers, and it could not copy the existing finished RC vault. The parent agent reviewed the resulting teaching against the source files after generation.

This is a single observed run in Codex desktop on macOS, using the session's inherited model settings. An exact independent model identifier was not recorded. The topic is deliberately close to the bundled teaching standard; the fixture changes numerical cases and adds a linear-utility corner, a distinct compensation rule, two elasticities and ten practice subparts. This tests execution and near transfer, not generalization to every subject or the capacity to finish a full semester in one context.

The frozen teaching instructions were used without changes during generation. The release also contains a diagram added to the bundled teaching standard after the test snapshot, and preserves the remote optional formula-checker addition. These later packaging additions were checked separately.

## Inspect the generated vault

[Download the complete test output](consumer-choice-vault-2026-09-22.zip), extract it, and open `consumer-choice-vault` in Obsidian starting at `Course.md`. The archive contains the generated lessons, three SVG diagrams, practice, original sources and maintenance records. Only machine-specific local image paths in the rendering report were replaced with portable relative paths; the teaching text is the observed output with the editorial correction disclosed below.

## Findings from reading the actual output

The reviewer read all three inputs, all four generated lessons and the full P1–P3 practice pages. All 15 substantive source sections were taught; the remaining administrative section does not create a learning obligation. All ten requested subparts survived with separate folded hints and authored solutions.

| Input obligation | Observed teaching and independent checks |
| --- | --- |
| F01 Slides 1–2: budget, domain, ordinary optimum | Lesson 01 explains budget intercepts and slope, rules out zero-quantity optima for `u=xy`, justifies spending the budget, substitutes the constraint, checks the feasible domain and negative second derivative, and explains equal expenditure shares as model-specific. |
| F01 Slide 3: tangency and the distinct corner | Lesson 01 derives the indifference-curve slope, interprets MRS and solves the linear-utility case by both utility per spending and a decreasing objective along the budget. The distinct answer `(0,16)` is retained; the text explains why the inconsistent tangency equation does not mean there is no optimum. |
| F01 Slide 4: both scaling comparisons | Lesson 01 preserves the original `(10,20)` choice with utility 200, the price-only doubling case `(5,10)` with utility 50, and the price-and-income doubling case restoring `(10,20)`. Spending and intercepts are included. |
| F02 Slides 1–2: compensated problem and minimum | Lesson 02 distinguishes inputs from outcomes, proves the utility constraint binds by scaling both quantities, derives expenditure as a function of one positive variable, rejects the negative root and checks the second derivative and boundary behavior. Tangency is connected to minimizing expenditure. |
| F02 Slides 3–4: full decomposition and geometry | Lesson 03 names all experiments before calculating: A=(16,16), B=(8,32), C=(4,16); utilities 256, 256, 64; expenditures 32, 64, 32. It explains the hypothetical expenditure, the two effects −8 and −4, three budget lines, shared utility versus shared price ratio, and relabeling the diagram. |
| F02 Slide 5: distinct compensation | Lesson 03 distinguishes total incomes 64 versus 80 from additional compensation 32 versus 48. It explains why allowing a new bundle can lower the cost of restoring old utility and why affording the old bundle does not force the consumer to choose it. |
| F02 Slide 6: direction and assumptions | Lesson 03 derives positive income derivatives for both ordinary demands and connects the income-effect sign to normal goods rather than generalizing it to every preference. |
| F03 Slides 1–2: both elasticities and finite change | Lesson 04 separately differentiates at fixed income versus fixed utility, obtains −1 and −1/2, explains signed versus absolute conventions and computes the exact doubling ratios 1/2 and 1/√2. It explains why a local elasticity cannot simply multiply a large percentage price change. |
| F03 Slide 3: P1(a–c) | Full derivation and spending check yield `(8,12)`; MRS is 3/2; changing to linear utility yields the explained corner `(0,24)`. |
| F03 Slide 4: P2(a–d) | A=(15,15), B=(5,45), C=(5/3,15); effects −10 and −10/3 sum to −40/3. Additional compensations are 60 and 120. All three budget-line equations, slopes and vertical intercepts are supplied. |
| F03 Slide 5: P3(a–c) | Both derivatives and fixed variables are stated, exact tripling changes are −2/3 and 1/√3−1, and the explanation distinguishes the experiments without fixing utility and income simultaneously. |

The passages develop the model and its reasons in connected paragraphs. Comparisons use tables where useful; worked reasoning remains visible before independent practice. The result is substantially more developed than a short list of conclusions followed by one generic example. This is a review judgment of the observed output, not a measured learning outcome.

One minor wording defect was found after generation: Lesson 02 referred to analyzing the “cause of a price rise” where it meant the effects of that rise on choice. The reviewer requested that specific editorial correction. No substantive source omission or numerical discrepancy was identified in the passages reviewed. The test is therefore not described as wholly intervention-free.

## Numerical, preservation and rendering evidence

The generating agent recorded 31 successful checks covering independent grid searches for ordinary and corner choices, target-utility and expenditure identities, budget/tangency checks, finite-difference elasticity estimates, exact finite price ratios, source hashes and retained question structure. The parent reviewer also independently recomputed the finite decompositions and minimum expenditures, read the remaining derivations and checked the source obligations against the actual passages rather than treating these numerical checks as proof of teaching quality.

The final vault passed the bundled check with 18 Markdown notes, 150 internal wiki links, no missing/ambiguous targets and no warnings. The bundled math checker parsed 477 spans in all 15 non-source notes without syntax errors. All 14 frozen skill/source input files retained their original hashes.

An HTML fallback using marked and KaTeX rendered 475 math spans across 11 selected notes without a parser error. The three diagrams loaded and all six practice disclosures were initially closed. Representative prose, equations, diagrams and the P2 question/answer layout were visually inspected. This was a browser-based approximation of Obsidian callouts, **not an actual Obsidian render check for this new vault**. The renderer and temporary browser are development tools, not new skill requirements.

## Reproduction and limits

Use the prompt and procedure in [behavioral-evaluation.md](../behavioral-evaluation.md), then compare actual passages against [teaching-rubric.md](../teaching-rubric.md). A successful file/link/formula check does not substitute for that reading.

The test used clean, original Markdown source sections. It did not test OCR, reading complex real lecture figures, fresh installation on another computer, long-course interruption/resumption, or learning gains. The original failed whole-course source files were unavailable, so this run cannot measure the omission rate of that failed build or prove all of its causes have been removed.
