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
