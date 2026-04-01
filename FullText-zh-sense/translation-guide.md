# Translation Guide: Critical Thinking (Robert Ennis) - Chinese Edition

This guide provides concrete, executable rules for the sense-for-sense translation and review of Robert Ennis's *Critical Thinking*. It establishes the project-specific handbook required for all translation and review tasks.

## 1. Core Workflow & Review Policy

### The Review Loop
All translations must undergo an independent bilingual review to ensure fidelity and structural integrity.
1. **The Verdict**: The first line of any review output must be exactly **`Okay`** or **`Reject`**.
2. **Rejection**: If the verdict is `Reject`, the reviewer must provide specific line numbers and corrective actions.
3. **Approval**: A chapter is complete only when it receives an `Okay` verdict.

### Reopen Policy
If `termbase.md` or this `translation-guide.md` is updated with rules affecting previously approved chapters, those chapters must be **reopened** for targeted updates and a fresh review.

### Consistency Authority
- **Termbase**: `FullText-zh-sense/termbase.md` is the **canonical authority**. All technical and pedagogical terms must follow it exactly.

---

## 2. Translate These

Translate all human-readable text into natural, modern Chinese, except for items explicitly exempted in the "Preserve" section.
- **Headings & Body Text**: Use plain, modern Chinese. Avoid "translationese" and excessive "的".
- **Table Content**: Translate all English prose and logic words (e.g., `not`, `and`, `or`, `therefore`).
- **Figure Alt Text**: Translate descriptions in `![alt text](path)`. Ensure the description accurately reflects the image's pedagogical function.
- **Exercise Prompts & Answer Keys**: Translate the instructions and the content of answers.
- **Explanatory Notes**: Translate footnotes that provide additional context or explanation.
- **Emphasized Content**: Translate English examples quoted inside prose when the author discusses their meaning (keep italics/bolding).
- **Pedagogical Labels**:
  - `Check-Up` → `检查练习`
  - `Suggested Answers` → `参考答案`
  - `True or False` → `判断正误`
  - `Short Answer` → `简答题`
  - `Medium Answer` → `中等篇幅作答`
  - `Long Answer` → `长篇作答`
  - `Identification` → `辨析题`

---

## 3. Usually Preserve These

Certain elements function as structural markers, names, or logical variables. **Keep these in English.**
- **Acronyms & Names**: `FRISCO`, `Literary Digest`, `Zenith Aspirin`.
- **Logic Labels**: `AA`, `DA`, `AC`, `DC`, `DV`, `DI` (referring to logic forms like Affirming the Antecedent).
- **Logical Variables**: `p`, `q`, `r`, `A`, `B`, `C` when used in formal logic patterns (e.g., `p → q`).
- **Sequence Labels**: `a.`, `b.`, `c.`, `1:1`, `6:32` (example and item numbering).
- **Structural Symbols**:
  - `&#43;` (marks extended sections).
  - `&nbsp;` (spacing in answer keys).
- **Raw Paths**: Markdown link targets and image paths (e.g., `(images/fig.png)`).
- **Bibliographic Metadata**: Author names, book titles, and publication data in references/footnotes should stay in English to facilitate source lookup.

---

## 4. Consistency Rules

- **Structural Integrity**: Preserve heading levels (`#`, `##`), list numbering, table shapes, footnote labels (`[^1]`), and paragraph order exactly.
- **Logic Indicator Terms**: Use consistent Chinese equivalents for logical connectors:
  - `if...then...` → `如果……那么……`
  - `therefore` → `因此` or `所以`
  - `because` / `since` → `因为` or `由于`
- **Glossed Terms**: If a technical term is glossed (e.g., `argument`), follow the `termbase.md` rendering and keep any source emphasis.
- **No Accidental English**: Ensure ordinary English logic words in tables (like `not`) are translated, while logical symbols (like `→`) are preserved.

---

## 5. Review Prompt Requirements

When invoking a reviewer, require:
- Comparison of `FullText-en/` (Source) and `FullText-zh-sense/` (Target).
- Verification that all prose, including table text and `not` markers, is translated.
- Verification that structural labels (`AA`, `p`, `q`, `&nbsp;`) are preserved.
- A first-line verdict of `Okay` or `Reject`.

---

## 6. Concrete Corpus Patterns & Examples

### Logic Tables (Chapter 06)
**Source:**
| | Antecedent | Consequent |
| --- | --- | --- |
| Affirming | Deductively Valid | Deductively Invalid |

**Correct Translation:**
| | 前件 | 后件 |
| --- | --- | --- |
| 肯定 | 演绎有效 | 演绎无效 |
*(Note: Do not leave "Antecedent" or "Consequent" in English.)*

### Logic Pattern (Chapter 06)
**Source:** `b. not q`
**Correct Translation:** `b. 非 q` or `b. 不是 q` (depending on prose context; follow `termbase.md`).

### Latin & Technical Terms (Chapter 08, 13)
- **Post hoc**: Translate explanation, keep label.
  - *Trans:* “后此谬误”（*post hoc* fallacy）。
- **Prima facie**: Sense-based handling.
  - *Trans:* 一个表面证据确凿的案例（*prima facie* case）。
- **Generalization**: Usually `概括`.
  - *Note:* In Ch 10, be careful with `Glittering generality` (`光辉概括`) and `Overgeneralization` (`过度概括`).

### Answer Keys
**Source:** `1:1 F &nbsp; 1:2 T`
**Correct Translation:** `1:1 F &nbsp; 1:2 T`
*(Note: 'F' and 'T' are labels in the answer key context; keep them alongside the preserved `&nbsp;`.)*
