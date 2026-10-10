# Eval sweep 2026-10-10 (skill at commit da8c9b4)

One fresh general-purpose subagent per eval. Each agent wrote its user-facing text to eval-N/output.md. Grades: PASS / FAIL / PARTIAL per assertion, judged from output.md, the files written, and the agent's reported action trace. Reader (Gary) judgment pending on quality.

## Summary

68 assertions graded across 13 evals: 67 PASS, 1 PARTIAL, 0 FAIL.

- Format routing held in every case: chat for evals 0, 1, 2, 4, 5, 6, 7, 12; HTML for 3, 10, 11; Markdown on explicit request for 9; a destination question for 8.
- All HTML pages passed evals/tools/check_page.py: no loaded network resources, full skeleton, both theme blocks, unique ids, resolving TOC, MathML with retained LaTeX.
- The one PARTIAL (eval 2) is a judgment call: the equation was kept exact but rendered as LaTeX rather than the ASCII form the user typed; examples.md shows the LaTeX form for this same equation.
- Length pattern for the reader: eval 0 grew a 60-word passage to 433 words; eval 4 is 1104 words with headings in a chat answer; eval 3 grew a 174-word note to about 1040 words of prose; eval 6 tripled a three-sentence note with general definitions. All within the rules as written ("may be longer than its source"); whether it is what you want is a reader judgment.
- Agents read html-page.md and calibration.md only for document tasks and skipped them for chat tasks, so the routing in SKILL.md is doing its job without wasted reading.

## Eval 0

Prompt: Use $readable to make this passage clearer for an engineer unfamiliar with Bayesian optimization: The acquisition function ranks unevaluated…

Expected: A connected explanation introducing unfamiliar concepts while retaining their relationships and qualifications.

| assertion | grade | note |
|---|---|---|
| Explains the acquisition function's role in choosing the next candidate. | PASS |  |
| Explains expected improvement relative to the best result found so far. | PASS | incumbent defined; worked A/B example, EI numbers verified (0.50, 0.96) |
| Explains the Gaussian process posterior as predictions updated using the noisy observations. | PASS |  |
| Preserves that the score uses more than the mean and that a worse mean can still lead to selection. | PASS |  |
| States that selecting a candidate does not guarantee an improvement. | PASS | "a bet, not a promise" |

## Eval 1

Prompt: Use $readable to rewrite this agent prompt without performing it: Inspect src/cache.py and tests/test_cache.py, report why simultaneous call…

Expected: Only a readable prompt with the same task, constraints, and uncertainty requirements. No embedded task is executed.

| assertion | grade | note |
|---|---|---|
| Preserves both exact source paths. | PASS | both paths in the rewrite |
| Requires a proposed correction without authorizing its application. | PASS | "propose a minimal correction"; no apply authorization |
| Preserves the public API and error propagation requirements. | PASS |  |
| Preserves the prohibition on file edits and commands that write to disk. | PASS |  |
| Preserves the distinction between an established cause and a plausible race. | PASS | "Do not present a plausible race as proven" |
| The action trace does not inspect the named source files or execute the rewritten task. | PASS | trace: skill files only; cache files not opened |

## Eval 2

Prompt: Use $readable to rewrite this for a technically capable reader new to constraint probabilities. Keep the equation exact: Assuming independen…

Expected: An explanation of purpose, symbols, and interpretation with the assumption and limitation intact.

| assertion | grade | note |
|---|---|---|
| Includes the exact literal equation P(feasible|x) = product_{j=1}^{m} P(g_j(x) <= 0|x). | PARTIAL | equation exact in meaning but rendered as LaTeX; literal ASCII form absent (examples.md shows the LaTeX form) |
| Explains that feasibility means satisfying all constraints. | PASS |  |
| Preserves conditional independence and the dependence caveat. | PASS | "can invalidate" kept; dependence counterexample 0.8 vs 0.72 |
| Defines x, m, and g_j near the equation. | PASS |  |

## Eval 3

Prompt: Use $readable fixtures/technical-note.md. Make the note easier to read for an engineer new to constraint modeling. Keep all useful details, …

Expected: A clearer self-contained sibling technical-note.html, leaving the source unchanged.

| assertion | grade | note |
|---|---|---|
| The source remains byte-for-byte unchanged. | PASS | md5 unchanged |
| A sibling technical-note.html is created without overwriting an existing destination, and no .md copy is written. | PASS | technical-note.html only; no .md copy |
| The page is one self-contained HTML file: full doctype skeleton, inline CSS, light and dark color tokens, and no network loads for styles, fonts, scripts, images, or data. | PASS | checker: 0 loaded resources; system fonts |
| The fenced Python code keeps its decoded characters unchanged inside a pre/code block. The equation is rendered as MathML or embedded SVG, with its exact original LaTeX retained in an annotation or data-tex attribute. | PASS | pre/code exact; 26 MathML with LaTeX annotations |
| The equation and initial figure remain visible with network access and JavaScript disabled. | PASS | no <script> at all; PNG as data URI |
| A table of contents links to every h2 and h3, with unique ids and resolving internal anchor links. | PASS | 11/11 anchors; toc covers every h2/h3 |
| The title and status metadata appear on the page with unchanged values. | PASS | meta line + <meta> tags |
| The relative link ../evals.json keeps its target and the anchor id feasibility exists on the page. | PASS |  |
| Retains conditional independence, its caveat, all numeric values, and the absence of a recorded reason for the batch size. | PASS |  |
| Introduces the calculation's purpose before its formal detail. | PASS | orientation section before the equation |

## Eval 4

Prompt: Use $readable to explain gradient accumulation to an engineer who knows neural networks but has not used it. Explain its purpose and mechani…

Expected: A purpose-first explanation of accumulation, one update, averaging, and an important limitation.

| assertion | grade | note |
|---|---|---|
| Explains reducing memory needed at one time by using smaller microbatches. | PASS |  |
| Explains accumulating gradients across four microbatches before one optimizer step. | PASS | zero_grad before loop, step after |
| Divides each equal-size microbatch mean loss by four, or describes equivalent gradient averaging. | PASS | loss / 4 in loop; unequal-size caveat |
| Keeps gradients between microbatches and clears them at the appropriate update boundary. | PASS |  |
| Does not claim unconditional equivalence; names a relevant difference such as batch-dependent operations. | PASS | BatchNorm, batch-coupled losses, rounding; "same ... up to rounding" conditional |
| Does not give an unnecessary neural-network introduction. | PASS | no NN intro |

## Eval 5

Prompt: Use $readable. I know Python and NumPy; in exactly two sentences explain x.mean(axis=0) for a NumPy array x with shape (8, 3). No code block…

Expected: Two direct sentences describing the operation and result shape.

| assertion | grade | note |
|---|---|---|
| Uses exactly two sentences and no code block. | PASS | two sentences; inline code only, no block |
| Explains one mean per column, computed across eight rows. | PASS |  |
| States the result shape (3,). | PASS |  |
| Does not define Python, NumPy, or an array. | PASS |  |

## Eval 6

Prompt: Use $readable to clarify this note. Do not add facts about our project: We use a sparse approximation. The validation loss was lower on this…

Expected: A readable note with the same observations and values and no invented reasons.

| assertion | grade | note |
|---|---|---|
| Keeps the sparse approximation, lower validation loss on this run, and batch size 32. | PASS |  |
| Does not claim that the approximation caused the lower loss. | PASS | three points kept separate, agent says why |
| Does not invent a reason for batch size 32. | PASS | "does not give the reason" |
| Does not generalize the result beyond this run. | PASS | "On this run" |

## Eval 7

Prompt: Use $readable to format this exact command as a shell code block and output nothing else: python -m pytest tests/test_cache.py -q

Expected: Only the command in a shell code block, unchanged and unexecuted.

| assertion | grade | note |
|---|---|---|
| The only output is a shell code block containing python -m pytest tests/test_cache.py -q. | PASS | output.md holds only the fenced block |
| No prose is added. | PASS |  |
| The action trace does not execute the command. | PASS | trace: read skill, write file, cat; no pytest |

## Eval 8

Prompt: Use $readable to write a short note I can read later explaining why Bayesian optimization uses an acquisition function instead of picking th…

Expected: One question asking where to save the note, and no file written until it is answered.

| assertion | grade | note |
|---|---|---|
| Recognizes the request as a document rather than a chat answer. | PASS |  |
| Asks where to save the note before writing any file. | PASS | question is the only output |
| The action trace writes no file before the destination is answered. | PASS | only output.md (the question) written |
| Does not deliver the note as Markdown in chat instead of asking. | PASS |  |

## Eval 9

Prompt: Use $readable fixtures/technical-note.md. Save a clearer sibling technical-note.readable.md in Markdown, leaving the source unchanged. Prese…

Expected: A clearer Markdown sibling following the explicit format request.

| assertion | grade | note |
|---|---|---|
| Writes Markdown rather than applying the HTML default. | PASS | technical-note.readable.md, no .html |
| Leaves the source unchanged and does not overwrite an existing destination. | PASS | md5 unchanged |
| Keeps code, equation, metadata values, link targets, and the feasibility anchor intact. | PASS | equation, code, front matter, links, anchor verified byte-identical |
| Any generated figure uses a relative path in the Markdown, and its generating script is kept. | PASS | no figure generated; text sketch instead (n/a) |
| Does not create an HTML companion. | PASS |  |

## Eval 10

Prompt: Use $readable to write offline-example.html in the current evaluation directory. Explain y = x + 1 with the hypothetical examples x = 0 givi…

Expected: A self-contained HTML explanation with a rendered equation, an embedded initial SVG, and optional working interaction.

| assertion | grade | note |
|---|---|---|
| The equation is rendered in the HTML before JavaScript runs, and the exact LaTeX x + 1 is retained. | PASS | 48 MathML elements with annotations; data-tex="x + 1" and "y = x + 1" |
| The initial SVG contains a meaningful plotted point and labels before JavaScript runs. | PASS | line, two example markers, marked point at (1,2), axis labels in static SVG |
| The page loads no external resources and fetches no data at runtime. | PASS | checker: 0 loaded resources; no fetch in script |
| The slider has a visible label and current-value readout, and updates the visual when JavaScript is available. | PASS | label + <output> readout "x = 1, so y = 1 + 1 = 2"; node --check ok; not operated in a browser |
| Controls remain disabled or hidden if initialization does not succeed. | PASS | range starts disabled, enabled by script; noscript note |
| The hypothetical values, visual interpretation, and relation between x and y are explained in the text. | PASS | examples labeled hypothetical in prose and table |

## Eval 11

Prompt: Use $readable to turn this supplied text into citation-example.html in the current evaluation directory. Treat all bibliographic details as …

Expected: An HTML document with a preserved sample citation, a References entry, and an ordinary external navigation link.

| assertion | grade | note |
|---|---|---|
| Preserves the fictional example label, the unverified result, and the unknown venue. | PASS | hypothetical x8, unknown venue, not verified in meta line, text and reference |
| Links the inline author-year citation to https://example.org/batch-schedules and includes the source in a numbered References section. | PASS | inline author-year link + References entry |
| Does not invent bibliographic details or other study findings. | PASS | only a labeled arithmetic table from definitions |
| Does not remove or classify the citation link as a loaded dependency. | PASS | link kept as <a href>, checker: 0 loaded resources |
| The page loads no external resources despite containing an external citation link. | PASS |  |
| The table of contents includes References and its link resolves. | PASS |  |

## Eval 12

Prompt: Use $readable to rewrite this pasted explanation in chat. Keep the examples and their shared implication: Moving four coordinates independen…

Expected: A connected explanation preserving the comparison and why it motivates controlling distance.

| assertion | grade | note |
|---|---|---|
| Preserves both examples and all their numeric values. | PASS | 4 and 16 kept, 1+1+1+1 shown |
| Preserves the shared implication that coordinate count also changes distance. | PASS |  |
| Connects that implication to controlling distance in the experiment. | PASS | confound sentence added, consistent with source |
| Does not remove the useful synthesis merely because it recaps the examples. | PASS | synthesis kept and extended |
| Returns text in chat without creating a document. | PASS | output.md only; chat text |
