---
name: readable
description: <What the skill does, in one sentence. Then when to use it: the user phrases, file types, and situations that should trigger it. This field is the only thing Claude sees before deciding to load the skill, so be specific and a little pushy.>
---

<!--
Template for the readable skill. Replace every <placeholder>. Delete these
comments when the section is written. Keep this file under ~500 lines; move
detail into references/ and point to it from here.
-->

# <Skill title>

<One paragraph: what this skill turns input into, and who the reader of the
output is. Write for the model that will run the skill, and explain why the
reader needs this, so it can make judgment calls the rules do not cover.>

## Invocation

<!-- How the skill is called and what each form produces. Delete the table
if there is only one form. -->

| Form | Mode | Output |
|---|---|---|
| `/readable <path>` | <mode> | <where the output goes; whether the source is ever overwritten> |
| `/readable` | <mode> | <...> |
| `<flag>` | <mode> | <...> |

## Process

<!-- Ordered steps the model works through. Say why each step exists so the
model knows what breaks if it is skipped. -->

1. **<Step>.** <What to do and why.>
2. **<Step>.** <...>
3. **<Step>.** <...>

## Rules

<!-- The core rules the output must follow. Keep each to one bold lead and
one or two sentences. Full detail and before/after pairs belong in
references/style.md, not here. -->

- **<Rule>.** <Why it matters. Example if short.>
- **<Rule>.** <...>

## Output structure

<!-- The shape every output takes. Use an exact template if the shape is
fixed; otherwise describe it and point to references/structure.md. -->

```markdown
# <Title>
## <Section>
## <Section>
```

## Figures

<!-- When a figure earns its place, which tool draws it, and where it is
saved. Point to references/figures.md and scripts/ for mechanics. -->

## Self-check before delivering

<!-- A checklist the model runs against its own draft. Each item must be
checkable by reading the output. -->

- [ ] <Check>
- [ ] <Check>

## Example

<!-- One short before/after pair that shows the rules applied together. -->

Source:

> <dense source sentence>

Rewrite:

> <rewritten version>

<One line naming which rules the rewrite applied.>
