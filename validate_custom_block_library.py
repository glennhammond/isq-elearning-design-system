#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "custom-block-library"
KC = LIB / "knowledge-check"
DP = LIB / "decision-point"
SHELL = LIB / "interaction-shell"
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
check(component.get("version") in {"0.1.0", "0.2.0", "0.3.0"}, "Knowledge Check candidate version is unexpected.")
variant_keys = {v.get("key") for v in component.get("variants", [])}
check({"isq-kc-single", "isq-kc-sequence"}.issubset(variant_keys), "Single and Sequence variants are required.")

shell_contract = component.get("interactionShell") or {}
check(shell_contract.get("required") is True, "Knowledge Check must require the governed Interaction Shell.")
check(shell_contract.get("modifier") == "isq-interaction--knowledge-check", "Knowledge Check must use the knowledge-check Interaction Shell modifier.")

shell_css = text(SHELL / "interaction-shell.css")
for selector in [
    ".isq-interaction",
    ".isq-interaction__header",
    ".isq-interaction__type",
    ".isq-interaction__title",
    ".isq-interaction__body",
    ".isq-interaction__options",
    ".isq-interaction__option",
    ".isq-interaction__actions",
    ".isq-interaction__feedback",
    ".isq-interaction__progression",
]:
    check(selector in shell_css, f"Interaction Shell is missing required selector {selector}.")

check("border-left" not in shell_css, "Interaction Shell must not introduce side-highlight styling.")
check("child protection" not in shell_css.lower(), "Interaction Shell CSS must remain domain-neutral.")

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
check('RESPONSE_DELIMITER = "[,]"' in adapter, "Multiple response encoding must use the governed [,] delimiter.")
check('Authorization' not in adapter and 'endpoint:' not in adapter and 'Basic ' not in adapter, "Adapter must not embed endpoint credentials or direct transport configuration.")

for relative in ["examples/single.html", "examples/sequence.html"]:
    source = text(KC / relative)
    check('data-isq-knowledge-check' in source, f"{relative} must identify the Knowledge Check component.")
    check('isq-interaction' in source and 'isq-interaction--knowledge-check' in source, f"{relative} must consume the governed Interaction Shell.")
    check('isq-interaction__header' in source and 'isq-interaction__option' in source, f"{relative} must use canonical Interaction Shell anatomy.")
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

# Decision Point is currently a presentation baseline, but its visual anatomy is governed now.
decision_example = text(DP / "examples/neutral-decision-point.html")
check('isq-interaction--decision' in decision_example, "Decision Point example must consume the Decision Point shell modifier.")
check('isq-interaction__header' in decision_example and 'isq-interaction__option' in decision_example, "Decision Point example must use canonical Interaction Shell anatomy.")
check('<fieldset' in decision_example and '<legend' in decision_example, "Decision Point example must preserve semantic option grouping.")
check('child protection' not in decision_example.lower(), "Decision Point canonical example must remain domain-neutral.")

all_source = "\n".join(text(path) for path in [
    KC / "knowledge-check.js",
    RUNTIME / "xapi-adapter.js",
    KC / "examples/single.html",
    KC / "examples/sequence.html",
    SHELL / "interaction-shell.css",
    DP / "examples/neutral-decision-point.html",
])
for forbidden in ["lrs2.isq.qld.edu.au", "REDACTED_TEST_CREDENTIAL", "CP-T-", "principal-sarah", "tilly", "tom/"]:
    check(forbidden.lower() not in all_source.lower(), f"Canonical source contains forbidden course/test-specific token: {forbidden}")

if errors:
    print("Custom Block Library validation FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Custom Block Library validation PASSED")
print("- Knowledge Check family remains Candidate")
print("- Knowledge Check and Decision Point consume the governed Interaction Shell")
print("- Interaction and telemetry transport are separated")
print("- Neutral examples contain required accessibility and telemetry metadata")
print("- No side-highlight styling, embedded endpoint credentials or Child Protection-specific identifiers detected")
