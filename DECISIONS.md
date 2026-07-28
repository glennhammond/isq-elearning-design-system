# DECISIONS.md

## Architecture choices

- **Static HTML + Jinja2 build script, no client framework.** Matches the brief's constraint and Document 1's own recommendation ("begin with a static HTML site"). Content lives in `/data/*.json`; `generate.py` renders it through `/​_templates`. Re-running the generator is the only way to update the published site — hand-editing `/out` will be overwritten.
- **Live component previews load the real production CSS** (`assets/vendor/isq-rise-components-v1.0.0.css`, copied verbatim from the supplied file) rather than a re-implementation, per the brief's explicit requirement.
- **`.docs-` prefix is used exclusively for site chrome**; `.isq-` never appears in this site's own CSS, only inside rendered component examples. Verified by grep as part of this build (`grep -r "\.isq-" assets/css/` returns nothing).
- **Client-side search index** (`data/search-index.json`) generated at build time from component and pattern data — no server dependency, per Document 5 Section 9.

## Naming choices

- **Role split** adopted as the canonical component name (matches the CSS class); "Role comparison" retained as the *pattern* name. See AUDIT.md #2.
- **"Restricted" folded into "Experimental"** for the Divider component, to keep the confirmed seven-value status lifecycle authoritative. See AUDIT.md #1.

## Technical choices

- Heading font: Century Gothic is confirmed as genuinely loaded via a licensed woff2 inside Rise itself, but that font file was not supplied to this site. **Poppins loads locally as the working substitute**, with the full documented stack (`"Century Gothic", "Poppins", "Avenir Next", Avenir, Futura, Arial, sans-serif`) declared so that dropping in the real woff2 later requires no other change. This mirrors the same substitution already made in the Connect & Learn 2027 blueprint, for consistency between the two properties.
- `--isq-warning: #333333` (identical to Charcoal) is reproduced exactly as declared in the production CSS rather than "corrected" to a distinct hue — see Open questions below.

## Exclusions (this release)

- **One page per learning pattern was not built.** All 11 patterns are documented in full on a single `/patterns/` page with anchors, rather than 11 separate pages, to keep the v1 build achievable in one pass. The content (purpose, use when, avoid when, related components) is complete; only the one-file-per-pattern structure Document 5 describes is simplified. Splitting into individual pages later is a template change, not a content one.
- **Storyline platform page is a stub.** No Storyline source material exists yet — populating it before there is anything to document would misrepresent the system's maturity.
- **Starter courses, image template files, and storyboard templates are not produced** — the Resources page states this plainly rather than linking to files that don't exist.
- **A generalised Tabs component was not invented from scratch.** The only current working tabs implementation in the production CSS is the course-specific Harm tabs. Rather than fabricate a generic example that doesn't exist in production, the Tabs pattern page documents the pattern and points to Harm tabs as its current reference implementation, with the generalisation gap stated explicitly.

## Assumptions

- The production CSS file supplied (`isq-rise-components-v1_0_0.css`) is the current live version referenced by the course, matching its internal header (`Version: 1.0.0`).
- The 14 supplied screenshots and the self-assessment screenshot represent the Child Protection for Principals and Board Members course specifically (consistent with prior project context).
- No course beyond Child Protection currently exists to validate the system against, per Document 1's own "pilot beyond Child Protection" recommendation — this remains open.

## Open questions (carried from the source documents, not yet answered by this project)

- Formal system owner and approval path — not named in any supplied source.
- Whether `--isq-warning` sharing Charcoal's value is intentional.
- Whether to migrate the Able/Willing and flip-card course content onto the shared Role split component, or formally document the one-off as its own reviewed pattern.
- Next CSS release number and immutable hosting path for `isq-elearning-rise-v1.1.0.css`.
- Whether the Self-assessment specification drafted in this release matches the actual exported course markup — has not been verified against a real Rise export.
