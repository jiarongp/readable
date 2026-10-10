# Verdict: plan-sparse-cts-generator (2026-10-08, in progress)

Source: docs/plan/sparse_cts_plan.md §6.1–6.3. Target excerpt: docs/readable/sparse_cts.md (human-preferred).

## Rep 1 (skill with paragraph-contract, picture, figure rules; agent forbidden to run code or write files)

| | Words | Median para | Max para | >80 |
|---|---|---|---|---|
| source | 779 | 75 | 198 | 4 |
| no skill | 1058 | 48 | 107 | 4 |
| skill rep1 | 1520 | 61 | 132 | 6 |
| target excerpt | 1041 | 43 | 61 | 0 |

Preserved: equations, FACT/HYPOTHESIS, § references, VERIFY note. Added worked instances after each equation; all arithmetic checked correct. Added a figure *specification* with a how-to-read caption, but no figure (agent could not run code in this harness).

Reader (Gary): plan output still the problem: no figure, and too long. API v2 judged fine.

Diagnosis candidates (not yet applied; reader asked for more reps first):
- paragraph rule caps sentences, not words; sentences grew long
- section-preview sentences and glosses of known terms add words
- "may be longer than its source" has no ceiling
- "include a figure, or specify one" lets the agent take the no-figure path

## Reps 2–5 (same skill wording; agent allowed to write a plotting script and PNG into repN/)

| run | words | paras | median | max | >80 | words/sentence | figures |
|---|---|---|---|---|---|---|---|
| source | 779 | 10 | 75 | 198 | 4 | 24.4 | 0 |
| no skill | 1058 | 18 | 48 | 107 | 4 | 16.8 | 0 |
| rep1 (no code allowed) | 1520 | 23 | 61 | 132 | 6 | 18.8 | 0 (spec only) |
| rep2 | 1599 | 14 | 61 | 81 | 1 | 17.0 | 2 |
| rep3 | 1555 | 14 | 52 | 76 | 0 | 15.6 | 2 |
| rep4 | 1570 | 10 | 53 | 88 | 1 | 15.3 | 1 |
| rep5 | 1410 | 19 | 46 | 108 | 5 | 18.9 | 2 |
| target excerpt | 1041 | 17 | 43 | 61 | 0 | 13.7 | 2 |

Figures rendered with `uv run --offline --no-project --with matplotlib --with numpy` (no Python on the machine has matplotlib). Reps 2 and 3 found that route themselves; reps 4 and 5 wrote scripts and I rendered them afterwards.

Findings (stable across reps, so attributable to the skill wording, not sampling):
1. **Length doubles.** 1410–1599 words for a 779-word source, 5/5 reps. "A readable explanation may be longer than its source" has no ceiling.
2. **Section-preview sentences.** 11 of 12 section openings begin "This section defines/asks/argues…". The exemplar never does this.
3. **Paragraph shape is now close to target.** Median 46–61 vs 43; max under 90 in 3/4 reps. Sentences 15–19 words vs 13.7. Not the main problem any more.
4. **Figures work when the harness allows code.** 4/4 reps produced 1–2 figures with illustration labels and how-to-read captions. Viewed rep3/active_energy.png (histogram: same mean, different spread, 66% at zero) and rep2/fig_hit_vs_concentration.png (hit probability vs per-hit component over k): both correct and informative. Rep1's missing figure was the test harness forbidding code, not the skill.
5. All reps preserved equations, FACT/HYPOTHESIS, § references, VERIFY note; worked numbers verified by the agents and spot-checked.


## Reps 6–7 (after adding figure recipe and section-opening rule)

| run | words | paras | median | max | >80 | figures | preview openings |
|---|---|---|---|---|---|---|---|
| rep6 | 1557 | 11 | 53 | 101 | 3 | 1 | 2 of 3 |
| rep7 | 1615 | 26 | 50 | 89 | 2 | 2 | 2 of 3 |

Figure recipe works: both reps saved the script beside the output and referenced the PNGs by relative path. Section-opening rule only half worked: §6.2 opens on substance in both reps, §6.1 and §6.3 still open with "This section defines/asks". Tightened with an inline contrast pair in SKILL.md and a checklist line; re-verifying with reps 8–9.

## Reps 8–9 (after inline contrast pair and checklist line for section openings)

| run | words | paras | median | max | >80 | figures | preview openings |
|---|---|---|---|---|---|---|---|
| rep8 | 1502 | 21 | 55 | 84 | 3 | 2 | 0 of 3 |
| rep9 | 1457 | 16 | 62 | 109 | 6 | 2 | 0 of 3 |

Section-opening rule now binds: 0 of 6 openings are previews (was 4 of 6 in reps 6–7, 11 of 12 in reps 2–5). Figure recipe holds. Length unchanged at roughly 2x source; reader accepted that length given the figures.

## State of the skill after this case
Rules added this session, each verified against this case: paragraph contract; picture before mechanism; figure recipe with script beside the document and how-to-read caption; section opens on substance (with contrast pair); two checklist lines.

## Rep 10 (2026-10-10, skill after the HTML-output change; output in rep10-html/)

Fresh subagent, same prompt but asked to save into rep10-html/ instead of returning Markdown. The agent loaded `artifact-design` (as html-page.md says) and also `dataviz` for the figure palette. It did not read earlier reps or the target excerpt.

| | words | p count | median p | max p | p >80 | figures |
|---|---|---|---|---|---|---|
| source | 779 | 10 | 75 | 198 | 4 | 0 |
| target excerpt | 1041 | 17 | 43 | 61 | 0 | 2 |
| rep10 visible text | 1995 | 25 | 58 | 116 | 7 | 2 (light+dark variants) |

Word count includes the legend paragraph, two captions (90 and 162 words), and a closing symbol table.

Mechanical checks, all pass: full skeleton; only KaTeX 0.16.11 and Google Fonts external; both theme blocks; 4 PNGs embedded as data URIs (light and dark variant per figure, swapped by a CSS token); heading ids match Markdown slugs of the source headings; all 5 display equations present character for character; FACT, HYPOTHESIS and VERIFY labels kept at their positions (rendered as tags) plus one legend; §2, §4, Step 0, Step 3 references kept; Rashidi et al. 2024 citation kept. Page is 570 KB.

Observations for the reader:
- Longest output of any rep (1995 words vs 1410-1599 for reps 2-5). The 162-word caption on figure 2 and the symbol table are new kinds of length.
- Two sentences of inference the agent flagged itself: "away from the walls where the truncation acts" as a gloss on "in the interior", and the §6.2 heading link sentence.
- The agent kept a `.template.html` with figure placeholders beside the deliverable. Not asked for by the skill; harmless, but it is a second file the user did not request.

Reader (Gary): pending.

## Rep 11 (2026-10-10, after Gary's rewrite of the skill; output in rep11-html/)

Fresh subagent, same prompt as rep 10. Loaded `artifact-design` and `dataviz`. Rendered all math offline with `katex -F mathml` (154 MathML elements, LaTeX retained), three figures in light and dark variants, no JavaScript at all. Took headless-Chrome screenshots itself at desktop and phone width and in dark theme, and fixed a display-equation alignment bug it found. Wrote a build.py and page_template.html alongside the deliverable.

Mechanical checks (tools/check_page.py): all pass. No network loads, full skeleton, both theme blocks, 6 data-URI images, unique ids, 15/15 anchors resolve, TOC covers every heading, References present, all 5 display equations retained exactly. FACT/HYPOTHESIS/VERIFY labels and §2, §4, Step 0, Step 3 references kept.

| | words | p count | median p | p90 | max p | p >80 | sentence median / mean | visuals | headings |
|---|---|---|---|---|---|---|---|---|---|
| source | 779 | 10 | 75 | | 198 | 4 | 24.4 mean | 0 | 3 |
| target excerpt | 1041 | 17 | 43 | | 61 | 0 | 13.7 mean | 2 | |
| rep10 (prose only, this tool) | 1450 | 25 | 58 | 90 | 116 | 7 | 18.5 / 18.6 | 2 | 4 |
| rep11 (prose only, this tool) | 2174 | 30 | 71.5 | 118 | 130 | 13 | 22.0 / 24.7 | 3 | 14 |
| Lil'Log (2 posts) | | | 26–33 | 75–106 | | | 17–20 / 18–22 | 1 per ~250 w | 1 per ~450 w |

Observations for the reader:
- Density moved the wrong way on this rep: paragraphs are longer than rep 10 and than the source median; 13 paragraphs over 80 words; sentences averaging 24.7 words. One rep, so sampling may explain part of it. Candidate cause to test with more reps: the rewrite's document guidance now lives in three places (SKILL.md "Organize the explanation", calibration.md, html-page.md) and the paragraph rule competes with the new "make each paragraph advance the explanation" bullet.
- Heading every 155 words (h3 under every h2 subsection), visual every 724 words; captions of 140, 91 and 190 words. Inverse of the reference shape.
- The agent added a reference the source does not cite (Eriksson et al. 2019, TuRBO), flagged it in the delivery note and in the References entry.
- Extra files beside the deliverable (build.py, page_template.html). Useful for regeneration; not requested.
- Formats and offline rules: fully met, first rep to do so.

Reader (Gary): pending.
