#!/usr/bin/env python3
"""Validate the non-rendering reconciliation manifest against current sources."""

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "data" / "reconciliation-manifest.json"
COMPONENTS_PATH = ROOT / "data" / "components.json"
PATTERNS_PATH = ROOT / "data" / "patterns.json"

EXPECTED_COUNTS = {"component": 23, "pattern": 12}
REMOVED_FIELDS = {"arti" "factRelationship", "canonical" "Reference"}
REMOVED_TERMS = {
    "arti" "fact-canonical-candidate",
    "unresolved-" "boundary",
    "not-a-canonical-" "component",
    "not-a-canonical-" "candidate",
    "isq-pattern-" "expression",
}
EXPECTED_VOCABULARY = {
    "proposedEntityType": {
        "foundation",
        "primitive",
        "component",
        "recipe",
        "learning-design-purpose",
        "structural-pattern",
        "learning-expression",
        "platform-implementation",
        "legacy-treatment",
    },
    "proposedMaturity": {"experimental", "candidate", "validated", "approved"},
    "reuseScope": {"isq-wide", "platform", "course-family", "course-specific"},
    "supportState": {"active", "legacy", "deprecated", "retired"},
    "implementationState": {"specified", "partial", "implemented", "production-verified"},
    "evidenceState": {"inferred", "documented", "tested", "audited"},
}
REQUIRED_FIELDS = {
    "reconciliationKey",
    "currentId",
    "currentName",
    "sourceType",
    "currentCategory",
    "currentStatus",
    "proposedEntityType",
    "proposedMaturity",
    "reuseScope",
    "supportState",
    "implementationState",
    "evidenceState",
    "isqRelationship",
    "riseImplementation",
    "productionEvidence",
    "discrepancies",
    "decisionStatus",
}
NESTED_FIELDS = {
    "isqRelationship": {"classification", "expressionReference", "notes"},
    "riseImplementation": {"type", "reference", "state"},
    "productionEvidence": {"state", "notes"},
}


def load_json(path):
    def reject_duplicate_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            result[key] = value
        return result

    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def find_removed_fields(value, location="manifest"):
    findings = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_location = f"{location}.{key}"
            if key in REMOVED_FIELDS:
                findings.append(child_location)
            findings.extend(find_removed_fields(child, child_location))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_removed_fields(child, f"{location}[{index}]"))
    return findings


def main():
    errors = []
    try:
        components = load_json(COMPONENTS_PATH)
        patterns = load_json(PATTERNS_PATH)
        manifest = load_json(MANIFEST_PATH)
    except (json.JSONDecodeError, ValueError) as error:
        print(f"Reconciliation validation failed:\n- {error}", file=sys.stderr)
        return 1
    records = manifest.get("records", [])

    removed_fields = find_removed_fields(manifest)
    if removed_fields:
        errors.append(f"Removed reconciliation fields remain: {removed_fields}")
    manifest_text = json.dumps(manifest).lower()
    remaining_removed_terms = sorted(term for term in REMOVED_TERMS if term in manifest_text)
    if remaining_removed_terms:
        errors.append(f"Removed reconciliation terminology remains: {remaining_removed_terms}")

    vocabulary = manifest.get("vocabulary", {})
    for field, expected_values in EXPECTED_VOCABULARY.items():
        actual_values = vocabulary.get(field)
        if not isinstance(actual_values, list) or set(actual_values) != expected_values:
            errors.append(
                f"vocabulary.{field} must contain exactly {sorted(expected_values)}; got {actual_values!r}."
            )

    sources = {
        "component": {item["id"] for item in components},
        "pattern": {item["id"] for item in patterns},
    }

    for source_type, expected in EXPECTED_COUNTS.items():
        source_count = len(sources[source_type])
        if source_count != expected:
            errors.append(f"Current {source_type} source has {source_count} IDs; expected {expected}.")

        declared_key = f"{source_type}s"
        declared_count = manifest.get("expectedCounts", {}).get(declared_key)
        if declared_count != expected:
            errors.append(f"Manifest expectedCounts.{declared_key} is {declared_count!r}; expected {expected}.")

        represented = [record.get("currentId") for record in records if record.get("sourceType") == source_type]
        counts = Counter(represented)
        duplicates = sorted(item_id for item_id, count in counts.items() if count != 1)
        if duplicates:
            errors.append(f"{source_type.title()} IDs not represented exactly once: {duplicates}")
        missing = sorted(sources[source_type] - set(represented))
        extra = sorted(set(represented) - sources[source_type])
        if missing:
            errors.append(f"Missing {source_type} IDs: {missing}")
        if extra:
            errors.append(f"Unknown {source_type} IDs: {extra}")
        if len(represented) != expected:
            errors.append(f"Manifest has {len(represented)} {source_type} records; expected {expected}.")

    keys = [record.get("reconciliationKey") for record in records]
    duplicate_keys = sorted(key for key, count in Counter(keys).items() if count > 1)
    if duplicate_keys:
        errors.append(f"Duplicate reconciliation keys: {duplicate_keys}")
    if None in keys:
        errors.append("At least one record has no reconciliationKey.")

    for index, record in enumerate(records):
        label = record.get("reconciliationKey", f"record[{index}]")
        missing_fields = sorted(REQUIRED_FIELDS - record.keys())
        if missing_fields:
            errors.append(f"{label} missing fields: {missing_fields}")
        for field, required in NESTED_FIELDS.items():
            value = record.get(field)
            if not isinstance(value, dict):
                errors.append(f"{label}.{field} must be an object.")
                continue
            missing_nested = sorted(required - value.keys())
            if missing_nested:
                errors.append(f"{label}.{field} missing fields: {missing_nested}")
        if not isinstance(record.get("discrepancies"), list):
            errors.append(f"{label}.discrepancies must be an array.")

        source_type = record.get("sourceType")
        current_id = record.get("currentId")
        if source_type not in sources:
            errors.append(f"{label} has invalid sourceType {source_type!r}.")
        elif current_id not in sources[source_type]:
            errors.append(f"{label} references missing source ID {current_id!r}.")

        for field in ("proposedEntityType", "proposedMaturity", "reuseScope", "supportState", "implementationState", "evidenceState"):
            if record.get(field) not in vocabulary.get(field, []):
                errors.append(f"{label}.{field} has value outside the declared vocabulary: {record.get(field)!r}.")

        secondary = record.get("crosswalkClassifications", [])
        invalid_secondary = sorted(set(secondary) - set(vocabulary.get("proposedEntityType", [])))
        if invalid_secondary:
            errors.append(f"{label}.crosswalkClassifications contains invalid entity types: {invalid_secondary}")

    declared_total = manifest.get("expectedCounts", {}).get("total")
    if declared_total != sum(EXPECTED_COUNTS.values()) or len(records) != declared_total:
        errors.append(f"Total count mismatch: declared={declared_total!r}, records={len(records)}, expected=35.")

    target = manifest.get("riseDesignSystemV1Target")
    if not isinstance(target, dict):
        errors.append("Manifest must define riseDesignSystemV1Target.")
    else:
        target_references = list(target.get("components", []))
        supporting = target.get("supportingPrimitivesAndFoundations", {})
        target_references.extend(supporting.get("componentIds", []))
        for queue_item in target.get("candidateQueue", []):
            target_references.extend(queue_item.get("componentIds", []))
        duplicate_target_references = sorted(
            component_id for component_id, count in Counter(target_references).items() if count > 1
        )
        if duplicate_target_references:
            errors.append(f"Duplicate v1.0 target component references: {duplicate_target_references}")
        missing_target_references = sorted(set(target_references) - sources["component"])
        if missing_target_references:
            errors.append(f"Unknown v1.0 target component IDs: {missing_target_references}")

    if errors:
        print("Reconciliation validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Reconciliation manifest valid: 23 components, 12 patterns, 35 unique keys.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
