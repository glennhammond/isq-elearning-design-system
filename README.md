# ISQ eLearning Design System — live reference site

The live operational reference for ISQ digital learning design and development, generated as a static site from a structured JSON data model.

## Purpose

Translates six governing documents (umbrella strategy, Rise implementation guide, block selection guide, imagery guide, component catalogue blueprint, templates & production resources) plus the production Rise CSS into a searchable, maintainable, live-rendered reference — not a copy of the Word documents.

## Custom Block Library

The governed production implementation layer for reusable custom eLearning components lives in `custom-block-library/`.

The library is part of this design system, not a parallel system. It contains only components that meet the reusable-component governance threshold and keeps learner interaction behaviour separate from governed xAPI transport where technically sensible.

The first candidate family is **Knowledge Check**, with Single and Sequence variants. See `custom-block-library/PHASE-02-REVIEW.md` for the current promotion gate.

## Local preview

The site is fully static but uses `fetch()` for client-side search, so open it through a local server rather than `file://`:

```
cd out
python3 -m http.server 8000
# visit http://localhost:8000
```

## Publishing

Copy the contents of `/out` to any static host (the site has no server dependency). Update the `<link>` in `assets/vendor/isq-rise-components-v1.0.0.css` if a newer immutable production CSS version is released — see Platforms → Rise for the versioning rule.

## Folder structure

```
data/                 Source of truth — foundations.json, patterns.json, components.json, changelog.json
_templates/            Jinja2 templates (one per page type), not part of the published site
assets/                CSS, JS and icons for the site's own chrome (.docs- namespace)
custom-block-library/  Governed source implementations for approved/candidate custom blocks
generate.py            Build script — reads /data, writes /out
out/                   Generated static site (this is what you publish)
README.md, AUDIT.md, DECISIONS.md, CHANGELOG.md   Project records (this folder)
```

## Content update process

1. Edit the relevant JSON file in `data/` — never hand-edit generated HTML in `out/`.
2. Run `python3 generate.py`.
3. Re-run the link checker described in AUDIT.md if you've added new component IDs or relationships.
4. Re-publish `out/`.

## Component addition process

Follow the contribution model documented on the Governance page: propose → prototype → review → document → approve → release → evaluate. Add the new entry to `data/components.json` following the existing schema (see DECISIONS.md for the field list), then regenerate.

Custom block candidates additionally follow the lifecycle and release requirements in `custom-block-library/README.md` before they can be marked Approved.

## Deployment notes

- No build framework or server dependency — plain HTML/CSS/vanilla JS.
- Component live previews load the real `isq-rise-components-v1.0.0.css`, copied into `assets/vendor/` at build time from the supplied production stylesheet. If that source file moves, update the path in `generate.py`.
- Search is a client-side JSON index generated at build time (`data/search-index.json`) — no server-side search dependency.

## Known limitations (v0.1.0)

- Learning pattern pages are combined into one page with anchors rather than one file per pattern, to keep the v1 scope achievable — see DECISIONS.md.
- Several Resources entries are placeholders (starter courses, image template files, storyboard templates) — no source files for these were supplied yet.
- The Self-assessment component specification was drafted from CSS + a screenshot, not from verified exported course markup — see AUDIT.md.
- Storyline platform page is a stub; no Storyline source material has been supplied.
- No live ISQ photography was supplied; imagery examples use a local placeholder graphic.
