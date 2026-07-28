# AUDIT.md

Audit performed against: the six source docx publications (v1.1, July 2026), `isq-rise-components-v1_0_0.css` (internal header v1.0.0, 2,356 lines, 168 classes), 14 Rise custom-block screenshots, the supplied `Custom_Block_HTML.docx` reference source, one self-assessment screenshot, and the Connect & Learn 2027 Experience Blueprint PDF.

## Source files reviewed

| File | Role |
|---|---|
| 1. ISQ eLearning Design System v1.1.docx | Umbrella strategy, architecture, governance |
| 2. ISQ Rise Design System: Implementation and Component Guide v1.1.docx | Detailed Rise component specification |
| 3. ISQ Rise Block Selection and Usage Guide v1.1.docx | Day-to-day block selection guidance |
| 4. ISQ Digital Learning Imagery and Media Guide v1.1.docx | Image taxonomy, dimensions, child-safety guidance |
| 5. ISQ eLearning Design System Component Catalogue v1.1.docx | Blueprint for this site itself |
| 6. ISQ Templates and Production Resources v1.1.docx | Asset library and checklist inventory |
| isq-rise-components-v1_0_0.css | Current rendered source of truth for available components |
| Rise_custom_blocks_-_screenshots.zip (14 images) | Visual reference for the live Child Protection course |
| Custom_Block_HTML.docx | Canonical HTML source for several components, as actually shipped |
| Self-assessment screenshot | Visual reference for the previously undocumented self-assessment component |
| ISQ Connect & Learn 2027 Experience Blueprint.pdf | Platform-level (Moodle) sibling document |

## Current component inventory (this release)

21 components across structural (5), content (5), scenario (4), interaction (4), support (4, one component — Meta tags — double-counted with support/structural boundary; see components.json), legacy (1). Full inventory: `data/components.json`.

- Core / Approved / Foundation: 18
- Experimental / Course-specific: 4
- Legacy: 1

## Terminology conflicts found and resolved

1. **Status vocabulary.** Document 1 confirms a seven-value lifecycle (Foundation, Core, Approved, Experimental, Course-specific, Legacy, Deprecated). Document 2 separately labels the Divider component "Restricted" — a status outside that set. Resolved by folding "Restricted" into **Experimental**, consistent with Document 1's own component-audit table, which independently calls the same component "Experimental / decorative."
2. **Naming instability — Role split vs Role comparison.** Document 1's own component audit table flags `.isq-role-split` as "Approved pattern — confirm naming." Different documents use "Role comparison" (a pattern-layer term) and "Role split" (the CSS class). Resolved: **Role split** is the canonical component name; "Role comparison" remains the name of the *learning pattern* it serves — these are two different layers of the system, not competing names for one thing.
3. **Colour-value drift between sibling documents.** The Connect & Learn 2027 blueprint's palette (explicitly marked "indicative" in that document) gives Positive `#1E6B45` / Negative `#A03232`. The production Rise CSS defines `--isq-success: #266141` / `--isq-error: #A22B2A`. This site treats the **CSS values as current source of truth** (per Document 1's own rule: "production code governs the current rendered implementation") and reproduces the blueprint's figures nowhere as if they were approved tokens.
4. **`--isq-warning` shares its value with Charcoal** (`#333333`) rather than being a distinct hue, paired with `--isq-warning-pale` (`#FFF7DF`). Plausibly intentional — dark text stays legible on a pale-yellow surface — but unconfirmed. Flagged in DECISIONS.md rather than silently resolved.

## Gaps found

1. **Undocumented shipped component — Self-assessment.** `.isq-self-assessment` (14 classes: table, radio, choice, scale-label, mobile-scale, corner, feedback, intro, actions, body, prompt, number, row) exists in the production CSS and renders in the live Child Protection course (confirmed by the supplied screenshot: a five-point confidence-rating table, "Save my reflection" / "Reset" actions). It appears in **none** of the six governing documents. A first specification has been drafted for this release from the CSS class names and the screenshot, and ships as **Course-specific** pending verification against the actual exported course markup — see `components/self-assessment/`.
2. **Course-specific comparisons bypass the shared component.** The supplied `Custom_Block_HTML.docx` shows the live course's "Significant harm test / Parent test" flip cards and "Able / Willing" comparison implemented as bespoke, self-contained markup (`.isq-test-cards`, `.isq-able-willing`) with an embedded `<style>` block that **redeclares** `--isq-gold: #D9A928` locally — a different value from the shared `--isq-yellow: #FFC72A` (and from the legacy `--isq-gold` alias in the production CSS, which points at `--isq-yellow`). This is a real instance of exactly the drift Document 2's "do not duplicate shared CSS" rule exists to prevent, and it means the shared `.isq-role-split` component the documents describe as "Approved" is **not actually the component the live course uses** for this learning moment. Recorded as an open decision (migrate the course to the shared component, or formalise the one-off as its own reviewed component) rather than silently merged.
3. **Missing class-index entries.** `.isq-band` / `.isq-band__inner`, `.isq-grid` / `--two` / `--three`, and `.isq-process` are named as primitives or components in Document 2's prose but were absent from its technical class index. Added to this catalogue's data model.
4. **No live ISQ photography, icon SVG set, or licensed Century Gothic woff2 was supplied** — the site substitutes a local Poppins load and an inline placeholder graphic, both clearly labelled as substitutions (see DECISIONS.md).

## Unresolved decisions

See DECISIONS.md.

## Legacy items

`.isq-reflection-editorial` — confirmed Legacy in Document 1's own audit; no replacement migration has been scheduled. Carried into this catalogue unchanged, status Legacy, with that gap stated explicitly on its component page.

## Proposed MVP scope (delivered this release)

Foundations (colour, typography, spacing, widths, radius, focus): complete. Learning patterns: all 11, on one page with anchors (see DECISIONS.md for why). Components: 21 populated of the ~26 named across the source documents (Tabs ships as a documented pattern with Harm tabs as its only current working implementation, rather than a separately invented generic example — see its Known limitations). Platforms: Rise complete; Connect & Learn summarised with a link to the source blueprint; Storyline stubbed pending source material. Governance: complete, including this audit. Changelog: v0.1.0 initial entry.
