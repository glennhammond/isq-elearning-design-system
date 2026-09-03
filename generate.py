#!/usr/bin/env python3
"""
eLearning Design System — live reference site generator.

Reads structured data from /data/*.json, renders it through the
templates in /_templates using Jinja2, and writes a fully static
site to /site. Re-run after any data change; nothing here needs to
be hand-edited in the generated HTML.
"""
import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "_templates"
OUT = ROOT / "site"

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
            {"title": "I am choosing a learning approach", "body": "Start with learner need, experience structure and a suitable learning expression.", "url": "learning-design/index.html"},
            {"title": "I am implementing the system", "body": "Choose a governed organisation, product and platform implementation.", "url": "implementations/index.html"},
            {"title": "I need a component", "body": "Browse the full catalogue, filterable by category, status and platform.", "url": "components/index.html"},
            {"title": "I am reviewing accessibility", "body": "Every component page states semantics, keyboard, focus and contrast requirements.", "url": "components/index.html"},
            {"title": "I am contributing to the system", "body": "The lifecycle, statuses and contribution model.", "url": "governance/index.html"},
        ],
        architecture=[
            {"eyebrow": "01", "title": "Core system", "body": "Learning intent, semantic foundations, patterns, component contracts and quality requirements."},
            {"eyebrow": "02", "title": "Implementations", "body": "Organisation themes and platform-specific technical expressions of the shared core."},
            {"eyebrow": "03", "title": "Course applications", "body": "Source-controlled learning experiences that use and provide evidence back to the system."},
        ],
        stats={
            "version": "0.2.0",
            "approved": approved_count,
            "experimental_course": exp_course_count,
            "legacy": legacy_count,
            "updated": "September 2026",
            "roadmap_stage": "5 — Document & demonstrate",
        },
        featured=[
            {"title": "Block Selection & Usage Guide", "body": "Fast day-to-day block decisions.", "url": "patterns/index.html"},
            {"title": "Implementation directory", "body": "Organisation, product and platform expressions.", "url": "implementations/index.html"},
            {"title": "Course applications", "body": "Source-controlled uses and qualification evidence.", "url": "applications/index.html"},
            {"title": "Changelog", "body": "What changed, and when.", "url": "changelog/index.html"},
        ],
    )

    # ---- Overview ----
    render("overview.html.j2", "overview/index.html", title="Overview",
           description="Purpose, audiences, architecture and roadmap.", section="overview")

    # ---- Foundations ----
    render("foundations.html.j2", "foundations/index.html", title="Foundations",
           description="Implementation-independent semantic, layout, interaction and accessibility foundations.",
           section="foundations")

    # ---- Patterns ----
    render("patterns.html.j2", "patterns/index.html", title="Learning patterns",
           description="The eleven core learning and communication patterns.",
           section="patterns", patterns=patterns, component_names=component_names)

    # ---- Learning Design ----
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
            "description": "These are established approaches for recurring learning situations.",
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

    # ---- Implementations ----
    render("implementations_index.html.j2", "implementations/index.html", title="Implementations",
           description="Organisation, product and platform expressions of the shared core.",
           section="implementations")
    render("implementation_isq.html.j2", "implementations/isq/index.html", title="ISQ implementation",
           description="Independent Schools Queensland theme, platforms, production assets and evidence.",
           section="implementations")
    render("implementation_isq_foundations.html.j2", "implementations/isq/foundations/index.html",
           title="ISQ foundations", description="ISQ colour, typography, spacing and production tokens.",
           section="implementations", foundations=foundations)
    render("platform_rise.html.j2", "implementations/isq/platforms/rise/index.html", title="ISQ · Rise",
           description="ISQ Rise delivery architecture, publishing and troubleshooting.", section="implementations")
    render("platform_connect_learn.html.j2", "implementations/isq/platforms/connect-learn/index.html",
           title="ISQ · Connect & Learn",
           description="ISQ relationship to the Connect & Learn 2027 Experience Blueprint.",
           section="implementations")
    render("platform_storyline.html.j2", "implementations/isq/platforms/storyline/index.html",
           title="ISQ · Storyline", description="ISQ Storyline boundaries and status.",
           section="implementations")
    render("media.html.j2", "implementations/isq/media/index.html", title="ISQ · Imagery & media",
           description="ISQ taxonomy, photography direction, dimensions and accessibility.",
           section="implementations")

    # Preserve earlier deep links while making the implementation boundary explicit.
    legacy_routes = [
        ("platforms/rise/index.html", "implementations/isq/platforms/rise/index.html", "ISQ Rise implementation"),
        ("platforms/connect-learn/index.html", "implementations/isq/platforms/connect-learn/index.html", "ISQ Connect & Learn implementation"),
        ("platforms/storyline/index.html", "implementations/isq/platforms/storyline/index.html", "ISQ Storyline implementation"),
        ("media/index.html", "implementations/isq/media/index.html", "ISQ imagery and media implementation"),
    ]
    for old_path, target, destination in legacy_routes:
        render("redirect.html.j2", old_path, title="Reference moved",
               target=target, destination=destination)

    # ---- Course applications ----
    render("applications.html.j2", "applications/index.html", title="Course applications",
           description="Course-level uses and evidence for the core system and named implementations.",
           section="applications")

    # ---- Resources ----
    resources = [
        {"title": "HTML snippets", "status": "ISQ implementation", "body": "Current production markup is documented through the component catalogue and explicitly identified as the ISQ Rise expression."},
        {"title": "CSS source", "status": "ISQ implementation", "body": "The governed isq-rise-components-v1.0.0.css is loaded only by ISQ implementation previews."},
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
    search_items.extend([
        {"kind": "Core", "name": "Learning Design", "summary": "Move from learner need to structure, expression and implementation.",
         "url": "learning-design/index.html", "haystack": "learning design learner need purpose structure expression implementation"},
        {"kind": "Core", "name": "Foundations", "summary": "Semantic colour, typography, layout, interaction and accessibility contracts.",
         "url": "foundations/index.html", "haystack": "foundations semantic colour typography layout spacing interaction accessibility"},
        {"kind": "Directory", "name": "Implementations", "summary": "Organisation, product and platform expressions of the shared core.",
         "url": "implementations/index.html", "haystack": "implementations themes organisations platforms"},
        {"kind": "Implementation", "name": "Independent Schools Queensland", "summary": "ISQ theme, Rise production assets and platform guidance.",
         "url": "implementations/isq/index.html", "haystack": "isq independent schools queensland rise moodle storyline theme"},
        {"kind": "Directory", "name": "Course applications", "summary": "Course-level uses and qualification evidence.",
         "url": "applications/index.html", "haystack": "course applications child protection teachers principals board directors"},
    ])
    write(OUT / "data" / "search-index.json", json.dumps(search_items, ensure_ascii=False))

    print(f"Built {len(list(OUT.rglob('*.html')))} HTML pages into {OUT}")


if __name__ == "__main__":
    main()
