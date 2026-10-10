# Readability calibration

Lilian Weng's Lil'Log is the stylistic reference for a substantial technical document: an argument developed through connected paragraphs, equations, examples, visuals, and citations. Use the writing recipe in SKILL.md to produce that shape.

## Measurements

Measured on 2026-10-10 from the published HTML of two Lil'Log posts:

- https://lilianweng.github.io/posts/2023-06-23-agent/ (LLM Powered Autonomous Agents, June 23, 2023)
- https://lilianweng.github.io/posts/2025-05-01-thinking/ (Why We Think, May 1, 2025)

Counting method: text inside the `post-content` div only. Paragraphs are `<p>` elements after tag stripping and HTML unescaping; list items, captions, headings, code blocks, tables, and the References list are excluded from paragraph and sentence counts. Sentences are split on `. ! ?` followed by a capital letter. Words are whitespace-separated tokens, so inline math and citations count as words. Figures are `<figure>` elements. Headings are h2 and h3. Reading-time lines on the posts were not used.

| Measure | Agents post | Why We Think | Note |
|---|---|---|---|
| Words in paragraphs | 3430 | 6629 | |
| Paragraphs | 97 | 134 | |
| Median paragraph, words | 26 | 33 | 90th percentile 75 and 106; longest 163 and 238 |
| Median sentence, words | 17 | 20 | means 18.4 and 22.5 |
| Figures | 13 | 29 | one per 263 and 228 words |
| Headings (h2 + h3) | 7 | 15 | one per 490 and 441 words |
| Display equations | 0 | 5 | inline math is common in the second post |
| Tables | 0 | 0 | |

Both posts open with one or two orienting paragraphs, then a table of contents, and close with a Citation block and a numbered References list. Figure captions are one sentence and end with the image source in parentheses. Inline citations are author-year links.

These are two posts, not a corpus, and the paragraph counts exclude lists and captions, which carry part of her content. Use them as reference points to check a draft against, not as output targets.

## Use measurements to locate passages to inspect

Check whether a long paragraph asks the reader to learn several unfamiliar ideas at once. Check whether an unusually short paragraph has lost a connection to the next one. A caption needs enough context to explain what to compare, but can refer to definitions already given nearby.

Choose headings for changes in the argument and visuals for relationships the reader needs to picture. Preserve the main skill's paragraph guidance and the user's requested length. Numerical resemblance to a reference does not establish clarity or technical accuracy.
