# readable

A skill for Claude Code and Codex that makes technical writing easier to understand without changing what it claims. It applies when an agent writes or revises technical explanations, research notes, plans, design documents, code explanations, or prompts for another agent, especially in science, engineering, machine learning and programming.

Invoke it with `/readable` in Claude Code or `$readable` in Codex, or let it trigger from its description. The agent then applies the rules to the current writing task. Documents such as plans, notes and explainers come back as one self-contained HTML file that reads offline and without JavaScript. Chat answers, inline code explanations and agent prompts stay in chat.

## What the skill asks for

The reader is technically capable but may not know this particular concept, method, library or field. The goal is to preserve the information while reducing the effort needed to understand it. Readability is not brevity. A clearer explanation may be longer than its source, and reasoning, assumptions and qualifications are never cut to save words.

The rules, in priority order:

- **Accuracy before simplicity.** Simplify the language and presentation, not the claim. Keep conditions, negations, uncertainty and precise technical terms.
- **Context before mechanism.** Give an unfamiliar concept a role before its name. Open with a concrete instance, then move from purpose to intuition to formal detail.
- **Even density.** One main idea per sentence, one point per short paragraph, and a visual wherever a relationship is geometric or quantitative.
- **Plain, stable wording.** Familiar words, visible actions, one term per concept.
- **Shape for the purpose.** Chat answers lead with the main point. Documents follow a long-form technical blog post, with Lilian Weng's Lil'Log as the calibration reference.

The full rules and the pre-delivery checklist are in [skill/SKILL.md](skill/SKILL.md). The agent reads supporting references on demand: [calibration](skill/references/calibration.md), [before-and-after examples](skill/references/examples.md), the [HTML page baseline](skill/references/html-page.md), and [equations, code, APIs and prompts](skill/references/technical-material.md). The literature the rules draw on is listed in [docs/references.md](docs/references.md).

## Install

Through a marketplace: [jiarongp/claude-marketplace](https://github.com/jiarongp/claude-marketplace) vendors `skill/` as a loose skill and links it into `~/.claude/skills` and `~/.agents/skills`.

Directly: clone this repository and symlink the skill folder.

```
ln -s /path/to/readable/skill ~/.claude/skills/readable   # Claude Code
ln -s /path/to/readable/skill ~/.agents/skills/readable   # Codex
```

HTML documents use two local tools, both named in `html-page.md`: the `katex` CLI (`npm install -g katex`) to pre-render equations as MathML, and `uv` to run figure scripts with matplotlib without a project environment.

## Repository layout

```
skill/   the skill as installed: SKILL.md, references/, agents/openai.yaml (Codex settings), evals/ (eval definitions and fixture)
evals/   development evidence: comparison cases with verdicts, full eval sweeps, check_page.py
docs/    references.md (the literature behind the rules) and design records
```

## Development

Rules change only on evidence. A candidate rule is tested by running fresh agents on a real passage, with and without the skill, saving both outputs under `evals/comparisons/<case>/` with a `verdict.md`, measuring density with `evals/tools/check_page.py`, and reading the outputs before editing `SKILL.md`. Assertion-based evals live in `skill/evals/evals.json`, and each full sweep is recorded under `evals/runs/<date>/`. See [evals/README.md](evals/README.md).
