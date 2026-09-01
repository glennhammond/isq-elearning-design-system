# Phase 02 — Knowledge Check canonicalisation

Status: **Complete to Candidate review gate**  
Release decision: **Do not promote to Approved yet**

## Objective

Establish the first governed custom-component family by extracting the mature formative question behaviour proven in Child Protection, removing domain-specific content and xAPI transport, and defining a reusable implementation contract.

## Evidence assessed

The phase used the current Child Protection implementations as evidence, principally:

- Staff Code quick-check candidate v2.1-xAPI;
- Tilly scenario questions 5–8 v2.1-xAPI;
- the shared ISQ Rise stylesheet and decision-interaction utilities;
- the self-assessment/Likert xAPI candidate as contrasting evidence for Reflection semantics;
- the existing ISQ eLearning Design System repository and catalogue architecture.

## Decisions made

### 1. Knowledge Check is a learning-purpose family, not a visual pattern

A Knowledge Check has an objectively defensible correct response and immediate explanatory feedback. Self-report and confidence prompts are excluded even where their UI is visually similar.

### 2. Single and Sequence share one question contract

`isq-kc-single` and `isq-kc-sequence` are variants of one family. This prevents duplicated controllers, styling and telemetry logic.

### 3. Existing shared CSS is reused

No new component CSS is introduced in Phase 02. The existing `.isq-options`, `.isq-option`, `.isq-decision-actions`, `.isq-decision-feedback`, button, callout, panel and accessibility utilities already provide the required presentation layer.

This avoids a second styling authority and reduces maintenance debt.

### 4. Interaction and telemetry are separated

The canonical controller evaluates the answer, manages feedback/progression and emits a neutral event. It does not resolve the learner, authenticate, submit to an LRS or contain course-specific identifiers.

This removes the largest duplication found in the source implementations: repeated SCORM discovery, actor construction, xAPI transport and course-specific statement configuration inside each learner component.

### 5. Rise uses a hybrid deployment architecture

The external shared CSS remains the styling authority. Component-specific controller code may be inlined into the deployed Rise block from one governed canonical source rather than depending on a second external script request.

This is a deliberate reliability choice, not an endorsement of independently maintained embedded scripts.

### 6. Telemetry failure is non-blocking for formative practice

The generic Knowledge Check must still provide feedback and progression when xAPI is unavailable. If a future course requires telemetry as evidence of compliance, that is a course-level requirement and failure policy rather than a hidden change to the reusable component.

## Phase deliverables

- `custom-block-library/README.md` — architecture, lifecycle, versioning and governance foundation.
- `custom-block-library/runtime/telemetry-contract.md` — neutral component-event contract and governed xAPI boundary.
- `custom-block-library/knowledge-check/component.json` — machine-readable family specification.
- `custom-block-library/knowledge-check/README.md` — implementation, learning, accessibility, Rise and QA guidance.
- `custom-block-library/knowledge-check/knowledge-check.js` — canonical interaction controller.
- `custom-block-library/knowledge-check/examples/single.html` — neutral Single source example.
- `custom-block-library/knowledge-check/examples/sequence.html` — neutral Sequence source example.

## Source improvements achieved

Compared with the Child Protection source implementations, the canonical candidate now:

- contains no Child Protection wording, legislation or scenario logic;
- contains no Child Protection course/activity identifiers;
- contains no LRS endpoint or credential;
- contains no SCORM actor-discovery code;
- does not duplicate xAPI transport logic;
- distinguishes objectively assessed Knowledge Checks from Reflection/self-report;
- uses one shared controller for Single and Sequence variants;
- exposes telemetry through a stable, versioned neutral event contract;
- continues functioning when telemetry is absent;
- reuses existing ISQ design-system CSS rather than introducing local styles.

## Static review findings

The canonical controller is intentionally small and scoped to `[data-isq-knowledge-check]`. It uses native form controls and buttons and contains no parent-page DOM assumptions. The event payload contains no learner identity or credential material.

No new CSS has been added, so Phase 02 does not create token or selector duplication.

## Outstanding release evidence

The following are **approval gates**, not unfinished architecture:

| Gate | Status | Required evidence |
| --- | --- | --- |
| Source/schema review | Ready | Peer review of component contract and controller |
| Published Rise desktop | Pending | Interaction and layout pass |
| Published Rise mobile | Pending | 320px + representative phone pass |
| Keyboard-only | Pending | Complete operability and focus pass |
| Screen reader | Pending | Grouping, labels and feedback announcement pass |
| 200% zoom/text resize | Pending | No loss of content or operation |
| No-xAPI mode | Architecture pass | Confirm in published package |
| Telemetry event payload | Ready for adapter test | Validate emitted contract |
| xAPI statement mapping | Pending | ISQ telemetry adapter + LRS test |
| xAPI governance review | Pending | Review with ISQ xAPI stakeholder |

## Promotion rule

Do not label this family `Approved` or release it as `1.0.0` until all relevant QA gates pass.

The correct status at the end of Phase 02 is therefore:

**Knowledge Check family v0.1.0 — Candidate, architecture complete, ready for controlled Rise + xAPI validation.**

## Recommended Phase 03

Run controlled validation of Knowledge Check Single and Sequence in a neutral Rise test course, connect the event contract to the governed ISQ xAPI adapter, complete accessibility/device QA, resolve any defects, and promote the family to `1.0.0 Approved` only if the evidence supports promotion.

In parallel, begin extraction analysis for Reflection/Likert as the next family, but do not promote it until the Knowledge Check release pipeline has been proven end to end.
