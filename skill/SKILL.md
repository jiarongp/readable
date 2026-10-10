---
name: readable
description: Use when writing or revising technical explanations, research notes, design documents, code explanations, or agent prompts, especially in science, engineering, machine learning, AI, or coding; also use when asked to make text clearer, less dense, plainer, or better contextualized.
---

# readable

Reduce the effort needed to understand technical material. Preserve the useful information, including the reasoning. A readable explanation may be longer than its source.

Assume a technically capable reader who may be unfamiliar with this particular subject. Use the conversation to judge what the reader already knows. Explain unfamiliar concepts where they matter; do not repeatedly teach concepts the reader already understands.

## Scope and invocation

- **Apply the guidance to the writing task.** Use it for technical answers, research notes, design documents, code explanations, Markdown revisions, and prompts for another agent. Respect the requested audience, length, and tone. Scale the guidance down for short answers; code-only and command-only requests need no added prose.
- **Follow explicit format and editing requests.** A requested format takes precedence over the defaults below. An explicit request to edit a source file authorizes an in-place edit and keeps that file's format.
- **Return conversational text in chat.** Chat answers, inline code explanations, and agent prompts stay in chat. Pasted text also comes back in chat unless the user asks for a document.
- **Use HTML for documents by default.** Plans, research notes, idea write-ups, and explainers of papers or concepts use one self-contained HTML file. Follow [html-page.md](references/html-page.md); text, equations, and initial visuals must be readable offline and without JavaScript. Choose the format by the deliverable, whether writing a new document or rewriting existing text.
- **Save file rewrites beside the source.** For a file path without an editing instruction, write `plan.html` beside `plan.md` and leave the source unchanged. Choose an unused name if the output already exists. Preserve relative links when choosing the location.
- **Confirm the destination for a new document.** Use the destination requested by the user or implied by the conversation. If neither is available, ask where to save it before writing anything.
- **Use the current task when invoked alone.** Work on the current writing task or clearly identified text. Ask for a topic or source only when neither is available. The skill changes how the agent writes; it does not create a task by itself.

Examples of requests:

- `$readable Explain why this optimizer uses a trust region.`
- `$readable documents/plan.md`
- `$readable Rewrite this agent prompt: …`
- `$readable Edit documents/plan.md in place.`
- `$readable Write a note explaining the main idea of paper X for our group.`

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

### Organize the explanation

- **Lead chat answers with the main point.** Use connected paragraphs. Add headings only when they help navigation.
- **Give documents a clear reading order.** Use a long-form technical blog post as the model, with Lilian Weng's Lil'Log as the stylistic reference. Start with one or two paragraphs that orient the reader and say what the document covers, then an anchor-linked table of contents, then the sections. For quantitative calibration and its limits, read [calibration.md](references/calibration.md).
- **Make each paragraph advance the explanation.** Use transitions and brief recaps to make dependencies clear. Remove repetition that adds no context, implication, or orientation. Keep definitions and qualifications near the claims they explain.
- **Open sections on substance.** Descriptive headings expose the argument; the first sentence states the section's first point. Avoid “This section defines the candidate generator and fixes what k means.” Prefer “CTS generates each candidate by choosing a direction and a distance separately.”
- **Choose structure that fits the material.** Use bullets for genuine lists, numbered steps for procedures, and tables for comparisons or mappings. Keep long explanations in prose. Avoid deep nesting, decorative bolding, and a heading for every paragraph. Leave blank lines around lists and code fences.
- **Use math where precision helps.** Use inline math for precise symbols and display equations only where the exact form matters.
- **Introduce sources through their contribution.** Say what a method or paper did and found, linking its author-year citation there. Collect cited sources in a numbered References section at the end. Use available bibliographic details and preserve uncertainty about unverified sources.

### Show relationships with visuals

- **Include visuals for geometric or quantitative relationships.** Choose the form that shows the mechanism best: a static figure, inline SVG, animation, or interactive element such as a slider. Use images from source material when their license allows. In chat, use a worked numeric example, a two-dimensional case, or a small text diagram in place of a figure.
- **Keep generated figures reproducible.** Generate static figures with a script saved beside the document and keep the script. Embed images as data URIs in HTML; use relative paths in Markdown. If the plotting library is unavailable, keep the script and report the unrendered figure in the delivery note.
- **Make visuals understandable at rest.** Follow [html-page.md](references/html-page.md) for interactive and animated elements. Embed an initial visual before JavaScript runs. State the visual's essential explanation in the text too, so the document remains understandable without JavaScript.
- **Write captions that teach the reader how to look.** State whether the visual is an illustration or measured data, what each mark represents, and how to read it. Name the source when the image was not generated here.

### Preserve the source and deliver the result

- **Keep source details intact.** Preserve links, citations, code fences, identifiers, metadata, and meaningful anchors during a rewrite. In HTML, keep link targets and show source metadata with unchanged values.
- **Keep navigation stable.** Preserve explicit anchors and existing heading ids. For Markdown conversions, use the source renderer's heading slugs when known. Otherwise, use a consistent slug convention and check every in-document anchor link. Keep old ids as aliases when renaming linked headings, without creating duplicate ids.
- **Return the requested result.** Keep the editing checklist internal. For saved files, give the path, name any figure scripts, and mention material unresolved issues briefly. Add a change report only when requested or needed to explain a substantive issue.

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
- Does the output follow any explicit format request? For a default HTML document, is it one self-contained file with offline-readable equations and initial visuals, stable heading ids, both themes defined, a table of contents, and a References section when sources are cited?
- Did any added background turn into an unsupported fact or motivation?

Revise any material failure before delivering. Word counts and readability scores can identify passages to inspect; they cannot establish technical accuracy or sufficient context.
