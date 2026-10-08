# Verdict: api-lbfgsb-bounds (2026-10-08)

Skill version: commit 69edaaf plus working-tree SKILL.md (83 lines), one run each, fresh subagent.

| Dimension | Control (no skill) | Skill output | Reader verdict |
|---|---|---|---|
| Accuracy | Mostly right; several unverifiable specifics stated as fact | Mostly right; one uncertain point explicitly flagged | Skill better |
| Context | Names dropped without role (Moré–Thuente, maxcor) | Each concept gets a role before its name | Skill good |
| Density | Nested bullets, jargon-packed | Same word count; long paragraphs, each packed with detail; reader tires | **Skill still fails: wordy, long paragraphs** |
| Vocabulary | Fine | Fine, terms explained | Skill good |
| Structure | Mechanics before the answer; has a runnable example | Short answer first, sections mirror the questions; lost the example | OK; example loss noted |

Reader (Gary) feedback: context and vocabulary good; structure OK; too dense in words, not in information; long paragraphs filled with details. Wants the skill to prioritize visual understanding and intuition, in the style of docs/readable/sparse_cts.md.

Repeated-failure candidates (one sample so far):
- Paragraph shape: skill output averages far more words per paragraph than the exemplar.
- No concrete picture: no small numeric example, no geometric picture, no figure, even where the mechanism is geometric (a box, a projected path).

## Rep 2 (skill-output-v2.md, after paragraph-contract, picture, figure rules)

Median paragraph 72 -> 49 words, max 124 -> 103, three still over 80; total 740 -> 872 words. Added a two-variable worked example (gradient and projected gradient verified by hand). Uncertainty flag on finite differences kept. New unverified specifics: ValueError on lb > ub, strong Wolfe line search.

Reader (Gary): API fine now.
