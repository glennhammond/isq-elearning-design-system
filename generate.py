#!/usr/bin/env python3
"""
ISQ eLearning Design System — live reference site generator.

Reads structured data from /data/*.json, renders it through the
templates in /_templates using Jinja2, and writes a fully static
site to /out. Re-run after any data change; nothing here needs to
be hand-edited in the generated HTML.
"""
import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "_templates"
OUT = ROOT / "out"

env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=False)


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def write(path: Path, html: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def depth_base(out_path: Path) -> str:
    """Relative prefix back to the site root, based on output depth."""
    rel = out_path.relative_to(OUT).parent
    depth = len(rel.parts)
    return "../" * depth if depth else "./"


def render(template_name, out_rel_path, **context):
    out_path = OUT / out_rel_path
    base = depth_base(out_path)
    context.setdefault("base", base)
    html = env.get_template(template_name).render(**context)
    write(out_path, html)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    foundations = load("foundations.json")
    patterns = load("patterns.json")
    learning_design = load("learning-design.json")
    components = load("components.json")
    changelog = load("changelog.json")

    component_names = {c["id"]: c["name"] for c in components}
    categories = sorted({c["category"] for c in components})
    statuses = ["foundation", "core", "approved", "experimental", "course-specific", "legacy", "deprecated"]
    statuses = [s for s in statuses if s in {c["status"] for c in components}]
    implementations = sorted({impl for c in components for impl in c["implementation"]})

    approved_count = len([c for c in components if c["status"] in ("core", "approved", "foundation")])
    exp_course_count = len([c for c in components if c["status"] in ("experimental", "course-specific")])
    legacy_count = len([c for c in components if c["status"] in ("legacy", "deprecated")])

    # ---- Home ----
    render(
        "home.html.j2", "index.html",
        title="Home", description="One design language, defined once, consumed everywhere.",
        section="home",
        quick_paths=[
            {"title": "I am designing a course", "body": "Start with Learning patterns to find the right pattern for the job.", "url": "patterns/index.html"},
            {"title": "I am building in Rise", "body": "Native/custom/post-publish decisions, publishing and troubleshooting.", "url": "platforms/rise/index.html"},
            {"title": "I need an image or media standard", "body": "Taxonomy, dimensions, safe areas and child-safety guidance.", "url": "media/index.html"},
            {"title": "I need a component", "body": "Browse the full catalogue, filterable by category, status and platform.", "url": "components/index.html"},
            {"title": "I am reviewing accessibility", "body": "Every component page states semantics, keyboard, focus and contrast requirements.", "url": "components/index.html"},
            {"title": "I am contributing to the system", "body": "The lifecycle, statuses and contribution model.", "url": "governance/index.html"},
        ],
        architecture=[
            {"eyebrow": "01", "title": "Principles & foundations", "body": "Colour, typography, spacing and the eight experience principles."},
            {"eyebrow": "02", "title": "Learning patterns & components", "body": "Platform-neutral purpose, made concrete as reusable, tested components."},
            {"eyebrow": "03", "title": "Platform implementation & governance", "body": "Rise, Connect & Learn and Storyline consume the same system under one lifecycle."},
        ],
        stats={
            "version": "0.1.0",
            "approved": approved_count,
            "experimental_course": exp_course_count,
            "legacy": legacy_count,
            "updated": "July 2026",
            "roadmap_stage": "5 — Document & demonstrate",
        },
        featured=[
            {"title": "Block Selection & Usage Guide", "body": "Fast day-to-day block decisions.", "url": "patterns/index.html"},
            {"title": "Implementation Guide", "body": "Detailed Rise technical reference.", "url": "platforms/rise/index.html"},
            {"title": "Imagery Guide", "body": "Taxonomy, dimensions and child-safety rules.", "url": "media/index.html"},
            {"title": "Changelog", "body": "What changed, and when.", "url": "changelog/index.html"},
        ],
    )

    # ---- Overview ----
    render("overview.html.j2", "overview/index.html", title="Overview",
           description="Purpose, audiences, architecture and roadmap.", section="overview")

    # ---- Foundations ----
    render("foundations.html.j2", "foundations/index.html", title="Foundations",
           description="Colour, typography, spacing, widths, radius and focus.",
           section="foundations", foundations=foundations)

    # ---- Patterns ----
    render("patterns.html.j2", "patterns/index.html", title="Learning patterns",
           description="The eleven core learning and communication patterns.",
           section="patterns", patterns=patterns, component_names=component_names)

    # ---- Learning Design (parallel preview; not yet in primary navigation or search) ----
    learning_design_groups = [
        {
            "id": "learning-purposes",
            "entity_type": "learning-design-purpose",
            "label": "Learning purpose",
            "title": "Learning purposes",
            "description": "These describe what the designer needs to support for the learner.",
            "definition_key": "learnerNeed",
            "definition_label": "Learner need",
        },
        {
            "id": "experience-structures",
            "entity_type": "experience-structure",
            "label": "Experience structure",
            "title": "Experience structures",
            "description": "These describe repeatable ways to organise sequence, grouping, transition or flow.",
            "definition_key": "structure",
            "definition_label": "Structure",
        },
        {
            "id": "learning-expressions",
            "entity_type": "learning-expression",
            "label": "Learning expression",
            "title": "Learning expressions",
            "description": "These are established ISQ approaches for recurring learning situations.",
            "definition_key": "definingFeatures",
            "definition_label": "Defining features",
        },
    ]
    for group in learning_design_groups:
        group["records"] = [
            record for record in learning_design
            if record["entityType"] == group["entity_type"]
        ]
    render(
        "learning_design.html.j2", "learning-design/index.html",
        title="Learning Design",
        description="Move from learner need to an appropriate experience structure, learning expression and platform implementation.",
        section="learning-design", groups=learning_design_groups,
        component_names=component_names,
    )

    # ---- Components index ----
    render("components_index.html.j2", "components/index.html", title="Components",
           description="The full component catalogue, filterable by category, status and platform.",
           section="components", components=components, categories=categories,
           statuses=statuses, implementations=implementations)

    # ---- Component detail pages ----
    for c in components:
        render("component_detail.html.j2", f"components/{c['id']}/index.html",
               title=c["name"], description=c["purpose"], section="components",
               c=c, component_names=component_names)

    # ---- Platforms ----
    render("platform_rise.html.j2", "platforms/rise/index.html", title="Rise",
           description="Rise delivery architecture, publishing and troubleshooting.", section="platforms")
    render("platform_connect_learn.html.j2", "platforms/connect-learn/index.html", title="Connect & Learn",
           description="Relationship to the Connect & Learn 2027 Experience Blueprint.", section="platforms")
    render("platform_storyline.html.j2", "platforms/storyline/index.html", title="Storyline",
           description="Storyline boundaries and status.", section="platforms")

    # ---- Media ----
    render("media.html.j2", "media/index.html", title="Imagery & media",
           description="Taxonomy, photography direction, dimensions and accessibility.", section="media")

    # ---- Resources ----
    resources = [
        {"title": "HTML snippets", "status": "Populated", "body": "Canonical markup sourced from the supplied Custom Block HTML reference and this catalogue's component pages."},
        {"title": "CSS source", "status": "Populated", "body": "isq-rise-components-v1.0.0.css, loaded live by every component preview on this site."},
        {"title": "JavaScript", "status": "Placeholder", "body": "Scoped interaction scripts for decision points, tabs and self-assessment are referenced but not yet extracted as standalone files."},
        {"title": "Starter courses", "status": "Placeholder", "body": "Standard, scenario-led and media-rich Rise starters — not yet supplied."},
        {"title": "Image templates", "status": "Placeholder", "body": "Five master canvases plus safe-area overlays — dimensions documented under Imagery & media; template files not yet supplied."},
        {"title": "QA checklists", "status": "Documented", "body": "Component approval, course release, accessibility and published-package checklists — content below, files not yet produced."},
        {"title": "Storyboard resources", "status": "Placeholder", "body": "Course map, SME review and development storyboard templates — not yet supplied."},
        {"title": "Governance records", "status": "Placeholder", "body": "Component inventory, changelog, decision log and dependency register — changelog live; others pending."},
    ]
    render("resources.html.j2", "resources/index.html", title="Resources",
           description="Templates, snippets, checklists and storyboards.", section="resources", resources=resources)

    # ---- Governance ----
    render("governance.html.j2", "governance/index.html", title="Governance",
           description="Lifecycle, statuses, contribution model and audit findings.", section="governance")

    # ---- Changelog ----
    render("changelog.html.j2", "changelog/index.html", title="Changelog",
           description="Added, changed, fixed, deprecated and removed, by release.",
           section="changelog", releases=changelog)

    # ---- Copy assets & data ----
    shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
    (OUT / "assets" / "vendor").mkdir(parents=True, exist_ok=True)
    production_css = Path("/mnt/user-data/uploads/isq-rise-components-v1_0_0.css")
    if production_css.exists():
        shutil.copy(production_css, OUT / "assets" / "vendor" / "isq-rise-components-v1.0.0.css")
    (OUT / "data").mkdir(parents=True, exist_ok=True)
    for name in ["foundations.json", "patterns.json", "learning-design.json", "components.json", "changelog.json"]:
        shutil.copy(DATA / name, OUT / "data" / name)

    # ---- Search index ----
    search_items = []
    for c in components:
        haystack = " ".join([c["name"], c["purpose"], c["category"], c["status"], " ".join(c["classes"])]).lower()
        search_items.append({"kind": "Component", "name": c["name"], "summary": c["purpose"],
                              "url": f"components/{c['id']}/index.html", "haystack": haystack})
    for p in patterns:
        haystack = " ".join([p["name"], p["purpose"]]).lower()
        search_items.append({"kind": "Pattern", "name": p["name"], "summary": p["purpose"],
                              "url": f"patterns/index.html#{p['id']}", "haystack": haystack})
    write(OUT / "data" / "search-index.json", json.dumps(search_items, ensure_ascii=False))

    print(f"Built {len(list(OUT.rglob('*.html')))} HTML pages into {OUT}")


if __name__ == "__main__":
    main()
