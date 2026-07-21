---

name: translation-terminology-consistency-review
description: Review an English-to-Chinese chapter against its source and termbase, guide terminology decisions, and compile accepted decisions into exact line-by-line replacement rules.
disable-model-invocation: true
------------------------------

# Translation Terminology Review

Use a **three-gate terminology ledger**:

1. **Diagnose** inconsistencies and termbase violations.
2. **Decide** only the items selected by the user.
3. **Compile** accepted decisions into exact replacement rules.

Each run completes one user-facing gate and stops. The terminology ledger is the single source of truth across the three gates.

## Required inputs

All three inputs are mandatory:

1. the Chinese translation under review;
2. the corresponding English source;
3. the applicable glossary or termbase.

The termbase may be small. It may also explicitly declare that it currently contains no entries. Its purpose is to impose approved translation constraints, not to enumerate every term that may become a candidate in the current chapter.

A usable termbase entry contains:

* English source term;
* approved Chinese translation;
* optional sense or definition;
* optional part of speech;
* optional scope;
* optional notes or examples.

When sense, part of speech, or scope is omitted, infer applicability from context and surface uncertainty when the entry could reasonably have more than one interpretation.

## Authority model

The three inputs govern different questions:

| Input               | Authority                                                                           |
| ------------------- | ----------------------------------------------------------------------------------- |
| English source      | What the source means at this occurrence                                            |
| Termbase            | How that meaning must be translated when the entry applies                          |
| Chinese translation | What wording currently appears, how it reads in context, and which line must change |

A termbase entry is binding only when the source occurrence matches its sense, grammatical role, and scope.

When an occurrence clearly falls outside an entry's scope, leave the entry unapplied. When applicability remains uncertain, report an applicability issue instead of enforcing the entry mechanically.

A chapter-level decision may add to the termbase. It may override an existing entry only when the user explicitly accepts a **termbase amendment**.

## Preflight

Run this preflight before Gate 1:

1. confirm that all three required inputs are present;
2. confirm that the English and Chinese documents represent the same chapter or passage;
3. freeze stable physical line numbers for the Chinese document;
4. load every termbase entry and its available applicability metadata.

When an input is missing or the source pairing cannot be established, return only a compact input report and stop.

Preflight is complete when the three inputs are usable, the source pair is confirmed, and every Chinese physical line has a stable line number.

## Select the gate

Choose the gate from the user's current request:

* **Gate 1 — Diagnose:** identify suspicious wording, inconsistency, or termbase violations.
* **Gate 2 — Decide:** evaluate selected IDs or compare proposed translations.
* **Gate 3 — Compile:** use explicitly accepted decisions to produce replacement rules.

Advice, preference, or comparison requests belong to Gate 2. A proposal becomes accepted only through explicit user confirmation.

# Gate 1 — Diagnose

## Steps

1. Read the complete Chinese chapter, including headings, prose, tables, exercises, answer keys, summaries, notes, and footnotes.
2. Align the English source to the Chinese chapter by headings, sequence, repeated examples, and concepts. Sentence-level alignment may remain approximate where the structure differs.
3. Build the terminology ledger with:

   * English source term or phrase;
   * source sense and grammatical role;
   * recurring concept or concrete referent;
   * every Chinese rendering;
   * every Chinese line number;
   * matching termbase entry, when any;
   * audit lens;
   * confidence;
   * reason for suspicion.
4. Run the **termbase compliance pass**.
5. Run the **open terminology pass** using every audit lens.
6. Apply the semantic-identity test and remove weak stylistic findings.
7. Assign IDs by first Chinese occurrence:

   * `T01`, `T02`, ... for confirmed termbase violations;
   * `A01`, `A02`, ... for termbase applicability issues;
   * `C01`, `C02`, ... for open terminology candidates.
8. Return the Gate 1 deliverable.

## Termbase compliance pass

For every termbase entry:

1. locate every relevant occurrence of its English source term;
2. determine whether the entry applies at each occurrence;
3. compare the approved Chinese translation with the actual Chinese wording;
4. classify the result:

   * **compliant** — approved wording is used;
   * **violation** — the entry clearly applies and the approved wording is not used;
   * **applicability issue** — sense, part of speech, or scope cannot be resolved confidently;
   * **out of scope** — the occurrence represents another sense or function.

Report violations and applicability issues. Keep compliant and out-of-scope occurrences in the ledger for coverage accounting.

## Open terminology pass

Find material inconsistencies not already settled by the termbase.

A candidate belongs in the report when at least one condition holds:

* one English term in the same sense has multiple Chinese renderings;
* distinct English terms share one Chinese rendering and the lost distinction matters;
* the same formal label or recurring referent drifts across the chapter;
* wording changes logical force, certainty, scope, agency, causality, or conceptual precision;
* a technical rendering is likely to make the reader form the wrong concept.

## Confidence

Use exactly one label:

* **明确** — the source or repeated context establishes the issue;
* **较可能** — the issue is strongly indicated, but a contextual distinction remains possible;
* **需进一步判定** — source alignment or termbase applicability remains insufficiently clear.

## Deliverable

Start with counts for:

* confirmed termbase violations;
* termbase applicability issues;
* clear open candidates;
* likely or unresolved open candidates.

### Termbase findings

| ID | English term | Required Chinese | Actual Chinese | Chinese lines | Status | Confidence | Why |
| -- | ------------ | ---------------- | -------------- | ------------- | ------ | ---------- | --- |

Include `Txx` and `Axx` items only.

### Open terminology candidates

| ID | English source | Chinese variants | Chinese lines | Audit lens | Confidence | Why suspicious |
| -- | -------------- | ---------------- | ------------- | ---------- | ---------- | -------------- |

Use one row per concept or referent. Keep all variants and occurrences together.

Add `## Important exclusions` only when a borderline case is likely to be mistaken for an inconsistency.

End with a compact invitation to select IDs for Gate 2.

## Completion criterion

Gate 1 is complete only when:

* the entire Chinese chapter and corresponding English source have been reviewed;
* every termbase entry has been checked against every relevant English occurrence;
* every recurring formal term and referent has been checked across all structural locations;
* every audit lens has been applied;
* every reported item has exact Chinese line numbers and a confidence label;
* every open candidate passes the semantic-identity test;
* the response contains diagnostics only.

# Gate 2 — Decide

## Steps

For every selected `Txx`, `Axx`, or `Cxx` item:

1. retrieve all recorded occurrences from the terminology ledger;
2. recheck the relevant English passages and termbase entries;
3. compare the available Chinese wordings for:

   * fidelity to the source meaning;
   * termbase compliance;
   * Chinese naturalness;
   * technical precision;
   * stability across headings, prose, tables, exercises, and summaries;
   * compatibility with established terminology elsewhere;
4. consider a new translation when none of the existing variants is satisfactory;
5. evaluate the user's preferred wording on its merits;
6. identify every downstream phrase or label affected by the decision;
7. classify the proposed action.

## Decision actions

Use exactly one action for each selected item:

* **Enforce termbase** — the existing entry applies and should be restored.
* **Clarify applicability** — decide whether the existing entry governs the occurrence.
* **Add chapter decision** — establish wording for a concept not governed by the termbase.
* **Propose termbase addition** — recommend promoting an accepted chapter decision into the termbase.
* **Propose termbase amendment** — recommend changing an existing normative entry.

An existing termbase entry remains authoritative until the user explicitly accepts an amendment.

## Deliverable

| ID | Source term | Current options | Recommendation | Acceptable alternative | Action | Rationale | Downstream effect |
| -- | ----------- | --------------- | -------------- | ---------------------- | ------ | --------- | ----------------- |

Use these judgment labels where useful:

* **推荐**
* **可接受**
* **不建议**

Then output:

### Proposed decisions — awaiting confirmation

```text
ID | action | source term -> proposed Chinese wording
```

For a proposed amendment, include both sides:

```text
ID | amend termbase | source term: old approved wording -> proposed approved wording
```

Include only selected items. Keep every entry explicitly marked as proposed.

End by asking the user to confirm, revise, or reject the proposed decisions.

## Completion criterion

Gate 2 is complete only when:

* every selected item has one clear recommendation and one action;
* each recommendation is grounded in the English meaning;
* each termbase-related judgment tests sense, grammatical role, and scope;
* downstream effects are identified;
* unselected items remain untouched;
* proposed decisions remain distinct from accepted decisions;
* no replacement rules are produced.

# Gate 3 — Compile

## Effective glossary

Freeze an effective glossary from:

1. applicable existing termbase entries;
2. explicitly accepted chapter decisions;
3. explicitly accepted termbase additions or amendments.

An accepted amendment replaces the previous termbase entry for this compilation. Undecided, rejected, and merely proposed wording stays outside the effective glossary.

## Steps

1. rescan the complete Chinese chapter from the beginning using the effective glossary;
2. check headings, prose, tables, exercises, answer keys, summaries, notes, and footnotes;
3. verify the corresponding English occurrence before changing each Chinese occurrence;
4. account for every occurrence governed by each effective glossary entry;
5. create the smallest safe replacement:

   * word-level when unambiguous;
   * phrase-level when grammar, meaning, or disambiguation requires context;
6. validate each old substring against the frozen Chinese line;
7. sort operations by ascending line number;
8. return the Gate 3 deliverable.

## Replacement format

Use one operation per line:

```text
23:可信度:可信性
```

The fields are:

```text
Chinese line number:exact old substring:exact new substring
```

When a colon inside the text would make the rule ambiguous, use:

```text
23 | old: text containing a colon | new: replacement text
```

When one line needs several independent changes, output several operations for that line. Preserve Markdown markers, punctuation, spacing, and capitalization unless the accepted decision changes them.

## Deliverable

Output one code block containing only the replacement operations.

Then report:

* unique affected lines;
* total replacement operations;
* effective glossary entries that required no change;
* governed occurrences retained because the approved wording was already present;
* occurrences left unchanged because they were out of scope;
* unresolved occurrences that remain unsafe to replace automatically.

When the user accepted termbase additions or amendments, also output:

### Proposed termbase delta

```text
ADD | source term -> approved Chinese wording
AMEND | source term: old approved wording -> new approved wording
```

This delta is a maintenance artifact. It does not modify the user's termbase unless the user separately requests that action.

## Completion criterion

Gate 3 is complete only when:

* every effective glossary entry has been rescanned across the full chapter;
* every governed occurrence is replaced, already compliant, or explicitly accounted for;
* every old substring exists exactly on the stated Chinese line;
* operations on the same line do not conflict;
* no undecided or rejected wording appears in the rules;
* termbase additions and amendments match the user's accepted decisions;
* the operation and line counts are correct.

# Audit lenses

Apply all lenses in Gate 1. Reuse the relevant lenses in Gates 2 and 3.

## 1. Source-term divergence

One English term or fixed phrase, used in the same sense, has multiple Chinese renderings.

Prioritize chapter-defining concepts, headings, formal labels, numbered criteria, argumentation terms, and recurring instructional language.

## 2. Source-term collapse

Distinct English terms share one Chinese rendering and the lost distinction affects interpretation.

## 3. Structural drift

The same concept changes between its heading, definition, explanation, table, exercise, answer key, or summary.

## 4. Referent drift

The same person, title, institution, brand, object, place, case, event, action, injury, or example receives unstable naming.

## 5. Scale drift

A rating, category, confidence level, or table label changes between the table and its explanation or summary.

## 6. Logical-force drift

Wording changes possibility, probability, obligation, scope, evidence, causality, agency, or the difference between credibility and truth.

Treat this as semantic drift rather than simple terminology variation.

## 7. Technical phrasing

A Chinese rendering is structurally unnatural or attaches a property to the wrong object, action, or result, producing a misleading technical concept.

# Boundary rules

* Stable source concepts favor stable Chinese terminology.
* Generic source words may take different Chinese forms when their sense or grammatical function changes.
* Recurring referents favor one stable name unless context requires a fuller or shorter form.
* Synonymy alone does not establish inconsistency.
* Sentence-level fluency belongs outside this review unless it affects terminology, conceptual identity, logical force, or translation accuracy.
* Punctuation, typography, and general proofreading enter scope only through an explicit user request.
* The English source resolves meaning.
* The termbase resolves approved wording within scope.
* Chinese context resolves natural phrasing and replacement boundaries.
* The terminology ledger is the single source of truth during the review.
* The effective glossary is the single source of truth during compilation.

# Response language

Respond in the user's language. Keep explanations compact and evidence-driven. Use exact Chinese line numbers whenever discussing the translation.
