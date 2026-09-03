# eLearning Design System — live reference site

The live operational reference for reusable eLearning design and development, generated as a static site from a structured JSON data model.

## Purpose

Connects learning design, experience patterns, visual foundations, components, platform implementation and governance in one maintained system. ISQ is the first mature branded implementation and evidence base; its governing documents and production Rise CSS currently provide much of the implemented source material.

## Local preview

Install the generator dependency, regenerate the site, then open it through a local server rather than `file://` so client-side search can use `fetch()`:

```
python3 -m pip install -r requirements.txt
python3 generate.py
cd site
python3 -m http.server 8000
# visit http://localhost:8000
```

## Publishing

Copy the contents of `/site` to any static host (the site has no server dependency). Update the governed ISQ Rise stylesheet in `assets/vendor/` if a newer immutable production version is released — see Platforms → Rise for the versioning rule.

## Folder structure

```
data/                 Source of truth — foundations.json, patterns.json, components.json, changelog.json
_templates/            Jinja2 templates (one per page type), not part of the published site
assets/                CSS, JS, icons and governed platform assets used by the generated site
generate.py            Build script — reads /data, writes /site
requirements.txt       Python build dependency declaration
site/                  Generated static site (this is what you publish)
README.md, AUDIT.md, DECISIONS.md, CHANGELOG.md   Project records (this folder)
```

## Content update process

1. Edit the relevant JSON file in `data/` — never hand-edit generated HTML in `site/`.
2. Run `python3 generate.py`.
3. Re-run the link checker described in AUDIT.md if you've added new component IDs or relationships.
4. Re-publish `site/`.

## Component addition process

Follow the contribution model documented on the Governance page: propose → prototype → review → document → approve → release → evaluate. Add the new entry to `data/components.json` following the existing schema (see DECISIONS.md for the field list), then regenerate.

## Deployment notes

- No build framework or server dependency — plain HTML/CSS/vanilla JS.
- Component live previews load the governed `assets/vendor/isq-rise-components-v1.0.0.css`, copied into the generated site at build time with the other source assets.
- Search is a client-side JSON index generated at build time (`data/search-index.json`) — no server-side search dependency.

## Known limitations (v0.1.0)

- Learning pattern pages are combined into one page with anchors rather than one file per pattern, to keep the v1 scope achievable — see DECISIONS.md.
- Several Resources entries are placeholders (starter courses, image template files, storyboard templates) — no source files for these were supplied yet.
- The Self-assessment component specification was drafted from CSS + a screenshot, not from verified exported course markup — see AUDIT.md.
- Storyline platform page is a stub; no Storyline source material has been supplied.
- No live ISQ photography was supplied; imagery examples use a local placeholder graphic.
