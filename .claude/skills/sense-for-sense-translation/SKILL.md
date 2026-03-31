---
name: sense-for-sense-translation
description: Translate English Markdown source files into natural Chinese using sense-for-sense translation while preserving Markdown structure. Use for bilingual book or article translation tasks where headings, tables, emphasized terms, quoted examples, answer keys, image links, and references must stay structurally intact, but the textual content itself should still be translated. Especially useful for textbook chapters, study notes, and OCR-cleanup workflows that require a review loop with an independent bilingual verdict.
---

# Sense-for-Sense Translation

Translate meaning, not surface wording, but preserve the document's structure exactly.

## Workflow

1. Read the source Markdown and identify any special structures: headings, tables, block quotes, lists, footnotes, image links, reference definitions, answer keys, and lettered labels.
2. Translate all human-readable text into natural Chinese unless the text is explicitly exempt.
3. Keep Markdown syntax and ordering unchanged.
4. If image paths already work in the target tree, do not copy assets. Only copy images when links would otherwise break.
5. After translation, run an independent bilingual review that returns only `Okay` or `Reject`. If it returns `Reject`, fix the cited issues and review again until it returns `Okay`.

## Translation Rules

### Translate These

- Headings, body text, table contents, figure alt text, exercise prompts, answer keys, and explanatory notes.
- Terms inside emphasis, quotation marks, or parentheses when they are part of the content rather than bibliographic data.
- English examples quoted inside the prose when the author is discussing their meaning. Keep formatting such as italics if present.
- Logic indicator terms in tables or inline discussion, such as `therefore`, `because`, `since`, `although`, `must`, `should`, and similar items, unless the task explicitly asks to preserve the English wordform for analysis.
- Glossed technical terms such as `argument`, `position paper`, `circular argument`, `appeal to authority`, `persuasive definition`, and `criteria`; keep emphasis if the source emphasized them.

### Usually Preserve These

- Acronyms or fixed labels that are functioning as names, such as `FRISCO`.
- Sequence letters or proposition labels such as `A`, `B`, `C`, `a`, `b`, `c`.
- Raw Markdown link targets and image paths.
- Bibliographic citations and publication metadata when they appear as references rather than running prose.

## Consistency Rules

- Preserve heading levels, list numbering, table shape, footnote labels, and paragraph order.
- Do not silently drop English just because it is italicized, quoted, or inside a table.
- If a term has already been translated in the same file, reuse that translation unless context clearly demands otherwise.
- Translate recurring pedagogical labels consistently. Example: translate `Check-Up` as `检查练习` throughout.

## Review Prompt Requirements

When invoking a clean-context reviewer, require all of the following:

- Compare only the English source and Chinese target.
- Check meaning fidelity and structure preservation.
- Verify that emphasized terms, quoted examples, and table text were translated when appropriate.
- First line of output must be exactly `Okay` or `Reject`.
- If `Reject`, require concrete issues with target-file line numbers whenever possible.

## Output Standard

The final translated Markdown should read naturally in Chinese, preserve the source's pedagogical function, and keep all structural cues intact for side-by-side comparison.
