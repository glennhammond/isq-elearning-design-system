#!/usr/bin/env python3
"""Validate the Learning Design model and, optionally, its generated route."""

import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
LEARNING_DESIGN_PATH = ROOT / "data" / "learning-design.json"
PATTERNS_PATH = ROOT / "data" / "patterns.json"
COMPONENTS_PATH = ROOT / "data" / "components.json"
GENERATED_ROUTE = ROOT / "out" / "learning-design" / "index.html"

EXPECTED_TOTAL = 12
EXPECTED_ENTITY_COUNTS = {
    "learning-design-purpose": 5,
    "experience-structure": 5,
    "learning-expression": 2,
}
DEFINITION_FIELDS = {
    "learning-design-purpose": "learnerNeed",
    "experience-structure": "structure",
    "learning-expression": "definingFeatures",
}
IMPLEMENTATION_KINDS = {
    "component",
    "recipe",
    "native-capability",
    "platform-implementation",
}
GOVERNANCE_VALUES = {
    "maturity": {"experimental", "candidate", "validated", "approved"},
    "reuseScope": {"system-wide", "platform", "course-family", "course-specific"},
    "supportState": {"active", "legacy", "deprecated", "retired"},
}
COMMON_FIELDS = {
    "id",
    "name",
    "entityType",
    "summary",
    "useWhen",
    "avoidWhen",
    "designGuidance",
    "definition",
    "implementations",
    "platformGuidance",
    "relatedRecords",
    "governance",
    "legacy",
}
EXTERNAL_METHODOLOGY_PATTERNS = {
    "ADDIE": r"\baddie\b",
    "Bloom's taxonomy": r"\bbloom(?:'s|’s)? taxonomy\b",
    "backward design": r"\bbackward design\b",
    "Gagne's events": r"\bgagn(?:e|é)(?:'s|’s)? (?:nine )?events\b",
    "Kirkpatrick model": r"\bkirkpatrick(?: model)?\b",
    "SAM model": r"\bsam model\b",
    "Universal Design for Learning": r"\buniversal design for learning\b|\budl framework\b",
}


class LearningDesignHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.record_ids = []
        self.record_entity_types = []
        self.group_ids = []
        self.record_disclosures = Counter()
        self.current_record_id = None
        self.links = []
        self.sources = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        if "docs-learning-group" in classes:
            self.group_ids.append(attributes.get("id"))
        if "data-learning-design-record" in attributes:
            self.record_ids.append(attributes.get("id"))
            self.record_entity_types.append(attributes.get("data-entity-type"))
            self.current_record_id = attributes.get("id")
        if tag == "details" and "docs-learning-guidance" in classes:
            self.record_disclosures[self.current_record_id] += 1
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])
        if tag in {"img", "script"} and attributes.get("src"):
            self.sources.append(attributes["src"])

    def handle_endtag(self, tag):
        if tag == "article":
            self.current_record_id = None


def validate_generated_route(errors, records):
    if not GENERATED_ROUTE.exists():
        errors.append("Generated route out/learning-design/index.html does not exist; run generate.py first.")
        return

    parser = LearningDesignHTMLParser()
    parser.feed(GENERATED_ROUTE.read_text(encoding="utf-8"))

    if len(parser.record_entity_types) != EXPECTED_TOTAL:
        errors.append(
            f"Generated route has {len(parser.record_entity_types)} Learning Design records; expected {EXPECTED_TOTAL}."
        )
    expected_record_ids = {record.get("id") for record in records}
    if set(parser.record_ids) != expected_record_ids or len(parser.record_ids) != EXPECTED_TOTAL:
        errors.append("Generated Learning Design record IDs do not match the source model exactly once.")
    invalid_disclosures = {
        record_id: parser.record_disclosures[record_id]
        for record_id in expected_record_ids
        if parser.record_disclosures[record_id] != 1
    }
    if invalid_disclosures:
        errors.append(
            "Each generated Learning Design record must contain exactly one disclosure; "
            f"found {invalid_disclosures}."
        )
    duplicate_html_ids = sorted(item_id for item_id, count in Counter(parser.ids).items() if count > 1)
    if duplicate_html_ids:
        errors.append(f"Generated route contains duplicate HTML IDs: {duplicate_html_ids}")
    generated_counts = Counter(parser.record_entity_types)
    for entity_type, expected_count in EXPECTED_ENTITY_COUNTS.items():
        if generated_counts.get(entity_type, 0) != expected_count:
            errors.append(
                f"Generated route has {generated_counts.get(entity_type, 0)} {entity_type} records; expected {expected_count}."
            )

    expected_group_ids = {"learning-purposes", "experience-structures", "learning-expressions"}
    if set(parser.group_ids) != expected_group_ids or len(parser.group_ids) != 3:
        errors.append(
            f"Generated route groups are {parser.group_ids!r}; expected each of {sorted(expected_group_ids)} exactly once."
        )

    record_navigation_links = Counter(
        href for href in parser.links if href in {f"#{record_id}" for record_id in expected_record_ids}
    )
    invalid_navigation_links = {
        record_id: record_navigation_links[f"#{record_id}"]
        for record_id in expected_record_ids
        if record_navigation_links[f"#{record_id}"] != 1
    }
    if invalid_navigation_links:
        errors.append(
            "Each Learning Design record must have exactly one section-navigation link; "
            f"found {invalid_navigation_links}."
        )

    expected_component_links = Counter(
        f"../components/{implementation['ref']}/index.html"
        for record in records
        for implementation in record.get("implementations", [])
        if implementation.get("kind") == "component"
    )
    actual_component_links = Counter(
        href
        for href in parser.links
        if re.fullmatch(r"\.\./components/[^/]+/index\.html", href)
    )
    if actual_component_links != expected_component_links:
        errors.append("Generated component links do not match Learning Design component implementations.")

    for reference in parser.links + parser.sources:
        parsed = urlsplit(reference)
        if not parsed.path and parsed.fragment and parsed.fragment not in parser.ids:
            errors.append(f"Generated route contains a broken local anchor: {reference}")
            continue
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (GENERATED_ROUTE.parent / unquote(parsed.path)).resolve()
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            errors.append(f"Generated route contains a broken local reference: {reference}")

    patterns_route = ROOT / "out" / "patterns" / "index.html"
    if not patterns_route.exists():
        errors.append("Legacy route out/patterns/index.html was not generated.")


def load_json(path):
    def reject_duplicate_keys(pairs):
        value = {}
        for key, child in pairs:
            if key in value:
                raise ValueError(f"Duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            value[key] = child
        return value

    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def is_nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def validate_string_list(errors, label, field, value, allow_empty=False):
    if not isinstance(value, list):
        errors.append(f"{label}.{field} must be an array.")
    elif not allow_empty and not value:
        errors.append(f"{label}.{field} must not be empty.")
    elif any(not is_nonempty_string(item) for item in value):
        errors.append(f"{label}.{field} must contain only non-empty strings.")


def main():
    errors = []
    try:
        records = load_json(LEARNING_DESIGN_PATH)
        patterns = load_json(PATTERNS_PATH)
        components = load_json(COMPONENTS_PATH)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Learning Design validation failed:\n- {error}", file=sys.stderr)
        return 1

    if not isinstance(records, list):
        print("Learning Design validation failed:\n- Root value must be an array.", file=sys.stderr)
        return 1

    pattern_ids = {pattern.get("id") for pattern in patterns}
    component_ids = {component.get("id") for component in components}
    record_ids = [record.get("id") for record in records if isinstance(record, dict)]

    if len(records) != EXPECTED_TOTAL:
        errors.append(f"Expected exactly {EXPECTED_TOTAL} records; found {len(records)}.")

    duplicate_ids = sorted(item_id for item_id, count in Counter(record_ids).items() if count > 1)
    if duplicate_ids:
        errors.append(f"Duplicate record IDs: {duplicate_ids}")

    entity_counts = Counter(
        record.get("entityType") for record in records if isinstance(record, dict)
    )
    for entity_type, expected_count in EXPECTED_ENTITY_COUNTS.items():
        actual_count = entity_counts.get(entity_type, 0)
        if actual_count != expected_count:
            errors.append(
                f"Expected {expected_count} {entity_type} records; found {actual_count}."
            )
    invalid_entity_types = sorted(set(entity_counts) - set(EXPECTED_ENTITY_COUNTS), key=str)
    if invalid_entity_types:
        errors.append(f"Invalid entity types: {invalid_entity_types}")

    source_ids = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record[{index}] must be an object.")
            continue

        label = record.get("id") or f"record[{index}]"
        missing_fields = sorted(COMMON_FIELDS - record.keys())
        if missing_fields:
            errors.append(f"{label} missing common fields: {missing_fields}")

        for field in ("id", "name", "summary"):
            if not is_nonempty_string(record.get(field)):
                errors.append(f"{label}.{field} must be a non-empty string.")
        for field in ("useWhen", "avoidWhen", "designGuidance"):
            validate_string_list(errors, label, field, record.get(field))

        entity_type = record.get("entityType")
        definition = record.get("definition")
        required_definition_field = DEFINITION_FIELDS.get(entity_type)
        if not isinstance(definition, dict):
            errors.append(f"{label}.definition must be an object.")
        elif required_definition_field:
            if set(definition) != {required_definition_field}:
                errors.append(
                    f"{label}.definition must contain only {required_definition_field!r}."
                )
            required_value = definition.get(required_definition_field)
            if entity_type == "learning-expression":
                validate_string_list(
                    errors, f"{label}.definition", required_definition_field, required_value
                )
            elif not is_nonempty_string(required_value):
                errors.append(
                    f"{label}.definition.{required_definition_field} must be a non-empty string."
                )

        implementations = record.get("implementations")
        if not isinstance(implementations, list) or not implementations:
            errors.append(f"{label}.implementations must be a non-empty array.")
        else:
            for implementation_index, implementation in enumerate(implementations):
                implementation_label = f"{label}.implementations[{implementation_index}]"
                if not isinstance(implementation, dict):
                    errors.append(f"{implementation_label} must be an object.")
                    continue
                missing = {"kind", "ref", "role"} - implementation.keys()
                if missing:
                    errors.append(f"{implementation_label} missing fields: {sorted(missing)}")
                kind = implementation.get("kind")
                if kind not in IMPLEMENTATION_KINDS:
                    errors.append(f"{implementation_label}.kind is invalid: {kind!r}.")
                for field in ("ref", "role"):
                    if not is_nonempty_string(implementation.get(field)):
                        errors.append(f"{implementation_label}.{field} must be a non-empty string.")
                for field in ("platform", "note"):
                    if field in implementation and not is_nonempty_string(implementation[field]):
                        errors.append(f"{implementation_label}.{field} must be a non-empty string.")
                if kind == "component" and implementation.get("ref") not in component_ids:
                    errors.append(
                        f"{implementation_label} references unknown component {implementation.get('ref')!r}."
                    )

        platform_guidance = record.get("platformGuidance")
        if not isinstance(platform_guidance, dict):
            errors.append(f"{label}.platformGuidance must be an object.")
        elif any(not is_nonempty_string(key) or not is_nonempty_string(value) for key, value in platform_guidance.items()):
            errors.append(f"{label}.platformGuidance must map non-empty strings to non-empty strings.")

        related_records = record.get("relatedRecords")
        if not isinstance(related_records, list):
            errors.append(f"{label}.relatedRecords must be an array.")
        else:
            for related_index, relationship in enumerate(related_records):
                relationship_label = f"{label}.relatedRecords[{related_index}]"
                if not isinstance(relationship, dict) or set(relationship) != {"ref", "relationship"}:
                    errors.append(
                        f"{relationship_label} must contain only ref and relationship."
                    )
                    continue
                if relationship.get("ref") not in set(record_ids):
                    errors.append(
                        f"{relationship_label} references unknown Learning Design record {relationship.get('ref')!r}."
                    )
                if not is_nonempty_string(relationship.get("relationship")):
                    errors.append(f"{relationship_label}.relationship must be a non-empty string.")

        governance = record.get("governance")
        if not isinstance(governance, dict):
            errors.append(f"{label}.governance must be an object.")
        else:
            if set(governance) != set(GOVERNANCE_VALUES):
                errors.append(
                    f"{label}.governance must contain exactly {sorted(GOVERNANCE_VALUES)}."
                )
            for field, allowed_values in GOVERNANCE_VALUES.items():
                if governance.get(field) not in allowed_values:
                    errors.append(
                        f"{label}.governance.{field} has invalid value {governance.get(field)!r}."
                    )

        legacy = record.get("legacy")
        if not isinstance(legacy, dict) or set(legacy) != {"sourceId", "sourceUrl"}:
            errors.append(f"{label}.legacy must contain exactly sourceId and sourceUrl.")
        else:
            source_id = legacy.get("sourceId")
            source_ids.append(source_id)
            if source_id != record.get("id"):
                errors.append(f"{label}.legacy.sourceId must match its compatibility ID.")
            if source_id not in pattern_ids:
                errors.append(f"{label} maps to unknown pattern ID {source_id!r}.")
            expected_url = f"/patterns/index.html#{source_id}"
            if legacy.get("sourceUrl") != expected_url:
                errors.append(
                    f"{label}.legacy.sourceUrl must be {expected_url!r}; got {legacy.get('sourceUrl')!r}."
                )

    source_counts = Counter(source_ids)
    missing_pattern_ids = sorted(pattern_ids - set(source_ids))
    extra_pattern_ids = sorted(set(source_ids) - pattern_ids, key=str)
    repeated_pattern_ids = sorted(
        source_id for source_id, count in source_counts.items() if count != 1
    )
    if missing_pattern_ids:
        errors.append(f"Current pattern IDs not represented: {missing_pattern_ids}")
    if extra_pattern_ids:
        errors.append(f"Unknown legacy source IDs: {extra_pattern_ids}")
    if repeated_pattern_ids:
        errors.append(f"Legacy source IDs not represented exactly once: {repeated_pattern_ids}")

    model_text = json.dumps(records, ensure_ascii=False)
    introduced_terms = [
        name
        for name, pattern in EXTERNAL_METHODOLOGY_PATTERNS.items()
        if re.search(pattern, model_text, flags=re.IGNORECASE)
    ]
    if introduced_terms:
        errors.append(f"External-methodology terminology found: {introduced_terms}")

    validate_generated = "--generated" in sys.argv[1:]
    unknown_arguments = set(sys.argv[1:]) - {"--generated"}
    if unknown_arguments:
        errors.append(f"Unknown arguments: {sorted(unknown_arguments)}")
    if validate_generated:
        validate_generated_route(errors, records)

    if errors:
        print("Learning Design validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    generated_message = " Generated route, grouping and local references are valid." if validate_generated else ""
    print(
        "Learning Design model valid: 12 records "
        "(5 purposes, 5 structures, 2 expressions), with complete legacy and component references."
        + generated_message
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
