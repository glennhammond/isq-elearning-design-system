#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "custom-block-library"
KC = LIB / "knowledge-check"
RUNTIME = LIB / "runtime"

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        errors.append(f"Could not read {path.relative_to(ROOT)}: {exc}")
        return ""


component_path = KC / "component.json"
try:
    component = json.loads(text(component_path))
except json.JSONDecodeError as exc:
    component = {}
    errors.append(f"component.json is invalid JSON: {exc}")

check(component.get("key") == "isq-kc", "Knowledge Check family key must be isq-kc.")
check(component.get("status") == "candidate", "Knowledge Check must remain candidate until external release evidence passes.")
check(component.get("version") in {"0.1.0", "0.2.0"}, "Knowledge Check candidate version is unexpected.")
variant_keys = {v.get("key") for v in component.get("variants", [])}
check({"isq-kc-single", "isq-kc-sequence"}.issubset(variant_keys), "Single and Sequence variants are required.")

controller = text(KC / "knowledge-check.js")
adapter = text(RUNTIME / "xapi-adapter.js")

check('isq:knowledge-check-answered' in controller, "Controller must emit the governed Knowledge Check event.")
check('activityName' in controller and 'activityDescription' in controller, "Controller event must expose governed activity metadata.")
check('XMLHttpRequest' not in controller and 'fetch(' not in controller, "Component controller must not contain xAPI transport.")
check('Authorization' not in controller and 'Basic ' not in controller, "Component controller must not contain credentials.")

check('ISQ_XAPI_RUNTIME' in adapter, "Adapter must delegate identity and transport to the shared runtime contract.")
check('correctResponsesPattern' in adapter, "Adapter must declare correctResponsesPattern.")
check('interactionType: "choice"' in adapter, "Adapter must map Knowledge Check to a choice interaction.")
check('completion: true' in adapter and 'success:' in adapter, "Adapter must record completion and measured success.")
check('[,]'.replace('[', '\\[') or True, "noop")
check('RESPONSE_DELIMITER = "[,]"' in adapter, "Multiple response encoding must use the governed [,] delimiter.")
check('Authorization' not in adapter and 'endpoint:' not in adapter and 'Basic ' not in adapter, "Adapter must not embed endpoint credentials or direct transport configuration.")

for relative in ["examples/single.html", "examples/sequence.html"]:
    source = text(KC / relative)
    check('data-isq-knowledge-check' in source, f"{relative} must identify the Knowledge Check component.")
    check('<fieldset' in source and '<legend' in source, f"{relative} must use semantic fieldset/legend grouping.")
    check('role="status"' in source and 'aria-live="polite"' in source, f"{relative} must expose dynamic feedback accessibly.")
    for attr in [
        'data-activity-id=',
        'data-activity-name=',
        'data-activity-description=',
        'data-parent-activity-id=',
        'data-grouping-activity-id=',
    ]:
        check(attr in source, f"{relative} is missing {attr[:-1]} telemetry metadata.")
    check('child-protection' not in source.lower(), f"{relative} contains Child Protection-specific content.")
    check('Authorization' not in source and 'Basic ' not in source, f"{relative} contains credential material.")

all_source = "\n".join(text(path) for path in [KC / "knowledge-check.js", RUNTIME / "xapi-adapter.js", KC / "examples/single.html", KC / "examples/sequence.html"])
for forbidden in ["lrs2.isq.qld.edu.au", "REDACTED_TEST_CREDENTIAL", "CP-T-", "principal-sarah", "tilly", "tom/"]:
    check(forbidden.lower() not in all_source.lower(), f"Canonical source contains forbidden course/test-specific token: {forbidden}")

if errors:
    print("Custom Block Library validation FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Custom Block Library validation PASSED")
print("- Knowledge Check family remains Candidate")
print("- Interaction and telemetry transport are separated")
print("- Neutral examples contain required accessibility and telemetry metadata")
print("- No embedded endpoint credentials or Child Protection-specific identifiers detected")
