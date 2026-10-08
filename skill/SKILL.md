---
name: readable
description: Make technical answers, agent prompts, and Markdown easier to understand without losing meaning. Use when writing substantial scientific, engineering, machine learning, AI, or coding explanations, or when asked to make text clearer, less dense, plainer, or better contextualized.
---

# readable

Reduce the effort needed to understand technical material. Preserve the useful information, including the reasoning. A readable explanation may be longer than its source.

Assume a technically capable reader who may be unfamiliar with this particular subject. Use the conversation to judge what the reader already knows. Explain unfamiliar concepts where they matter; do not repeatedly teach concepts the reader already understands.

## Scope and invocation

Apply this skill to new technical answers, research notes, design documents, code explanations, Markdown revisions, and prompts written for another agent. Respect the user's requested audience, length, tone, and format. Scale the guidance down for short answers. Code-only and command-only requests do not need added prose.

Examples of requests:

- `$readable Explain why this optimizer uses a trust region.`
- `$readable documents/plan.md`
- `$readable Rewrite this agent prompt: …`
- `$readable Edit documents/plan.md in place.`

For pasted text, return the rewritten text in chat. For a file path without an editing instruction, save a sibling copy named `plan.readable.md`. Use another unused name if that copy already exists. An explicit request to edit the source authorizes an in-place edit. Preserve relative links when choosing the output location. For a new document, use the requested destination.

If invoked without a new request, use the current writing task or clearly identified text. Ask for the topic or source only when neither is available. The skill changes how the agent writes; it does not create a new task by itself.

## Work through the ideas before the words

1. **Identify the purpose and reader.** Determine what the reader needs to understand or do. Infer background from the request and conversation. Ask only when missing information would materially change the result.
2. **Identify what must survive.** In a rewrite, track claims, reasoning, assumptions, uncertainty, constraints, numbers, technical names, and references. For a prompt, also track instructions and authorization limits.
3. **Find the dependencies.** Notice concepts that need an explanation before a later argument makes sense. Reorder the argument where useful, rather than paraphrasing each sentence independently.
4. **Write with local context.** Usually move from purpose or problem, to intuition, to the technical term and mechanism, then to formal detail or an example. Choose only the parts the reader needs.
5. **Compare and revise.** Check the draft against the source or task. Repair missing conditions, unsupported additions, and passages the reader still has to unpack.

For representative before-and-after examples, read [examples.md](references/examples.md) when a rewrite needs calibration. For equations, code, APIs, or agent prompts, read the relevant section of [technical-material.md](references/technical-material.md).

## Rules in priority order

When rules conflict, preserve accuracy first, then necessary context, then improve density, wording, and formatting.

### Preserve meaning and evidence

- **Simplify the language, not the claim.** Keep important technical distinctions, assumptions, negations, comparisons, units, and uncertainty. “May improve” must not become “improves.” A relationship must not become a proven cause.
- **Keep precise technical terms.** Use plain words when they are equally accurate. Keep names such as *posterior distribution*, *gradient*, and *runtime complexity* when those concepts matter. Explain the term rather than replacing it with a vague phrase.
- **Add context that the evidence supports.** A brief established definition or explicitly hypothetical example can help. Do not invent project motivations, results, implementation behavior, or guarantees. When missing information affects the claim, name the gap or ask a focused question. Flag an apparent source error separately rather than silently repairing it during a readability rewrite.

### Make each idea understandable where it appears

- **Give an unfamiliar concept a role.** Briefly explain what it is and what it does here. Add why it matters when that helps the reader follow the reasoning. A link can provide further detail; it should not carry context needed to understand this paragraph.
- **Introduce ideas in manageable steps.** Aim for one main idea and at most one new important concept per sentence. Introduce a concept before explaining several consequences. Treat sentences around 26 words or longer as review signals, not failures. Count conceptual work, not just words.
- **Keep paragraphs short and connected.** A prose paragraph makes one point in two to four sentences. Detail that belongs with the point but would lengthen the paragraph goes into a list, a table, a figure caption, or the next paragraph. Explain cause, contrast, or dependency with clear transitions such as “because,” “however,” or “so,” so that splitting does not hide the relationship between parts.
- **Give the reader something to picture before the general statement.** Open a mechanism with a concrete instance: a scenario with small numbers, a two-coordinate case, or a short text sketch. After an important equation or rule, show one worked instance with actual values. Label hypothetical numbers and scenarios. Explain what an analogy illustrates and where it stops being accurate when that boundary matters.

### Use direct, consistent language

- **Prefer familiar words and visible actions.** Use “use” for “utilize” and “before” for “prior to” when the meaning is unchanged. Prefer “we compare the results” to “a comparison of the results is performed.” Use active voice when the actor is known and relevant; do not invent an actor to avoid passive voice.
- **Keep terms and references stable.** Use the same term for the same concept. Distinguish related terms when their meanings differ. Expand an unfamiliar acronym at its first important use. Make “this,” “it,” and “they” point to an unmistakable referent.
- **Keep the tone collegial.** Be calm, direct, and explanatory. Avoid inflated academic phrasing, patronizing explanations, and unexplained jargon. Natural contractions and ordinary `-ing` forms are fine.

These language choices are inspired by ASD-STE100. This skill does not enforce its controlled dictionary or certify STE compliance. Context, information density, and explanation order are additional priorities for scientific and conversational writing.

## Shape the output for its purpose

For a chat explanation, lead with the answer or main point. Use connected paragraphs and add headings only when they help navigation.

For a substantial Markdown document, use descriptive headings that expose the argument. The first sentence of a section states its first point; the heading carries the orientation. Avoid an opening such as “This section defines the candidate generator and fixes what k means.” Prefer “CTS generates each candidate by choosing a direction and a distance separately.” Keep definitions and qualifications near the claims they explain. Use bullets for genuine lists and numbered steps for procedures. Use tables for comparisons or mappings, not long explanatory paragraphs. Avoid deep nesting, decorative bolding, and a heading for every paragraph. Leave blank lines around lists and code fences.

For a geometric or quantitative relationship in a document, include a figure. Generate it with a script saved beside the document, keep the script, and reference the rendered image by a relative path. If the plotting library is unavailable, keep the script and state in the delivery note that the figure was not rendered. The caption states whether the figure is an illustration or measured data, what each mark represents, and how to read it: which direction to read, what to compare, and what the comparison shows. In a chat answer, a worked numeric example, a two-dimensional case, or a small text diagram stands in for a figure.

Preserve links, citations, code fences, identifiers, document metadata, and meaningful anchors during a rewrite. If headings change, repair affected links within the document. Keep externally referenced anchors stable when known.

Return the requested answer, prompt, or document. Keep the editing checklist internal. For a saved file, identify its path and mention material unresolved issues briefly. Add a change report only when requested or needed to explain a substantive issue.

## Check before delivering

- Did all useful claims, conditions, reasoning, uncertainty, and references survive?
- Does each important unfamiliar concept have enough nearby context to understand its role?
- Can the reader follow the argument without decoding several new ideas at once?
- Are the terms consistent and the pronoun references clear?
- Do equations and code remain exact, with useful explanations around them?
- For a prompt, are the task, requirements, output, and authorization limits unchanged?
- Does the format help the reader find the main point without fragmenting the explanation?
- Does each important mechanism come with something concrete to picture, and is each prose paragraph short enough to read in one pass?
- Does any section open by announcing what the section will do, rather than with its first point?
- Did any added background turn into an unsupported fact or motivation?

Revise any material failure before delivering. Word counts and readability scores can identify passages to inspect; they cannot establish technical accuracy or sufficient context.
