# ISQ Custom Block Library

Status: Governed candidate foundation  
Current focus: Interaction Shell refinement + Knowledge Check qualification  
Owner: ISQ eLearning design/development steward

## Purpose

The ISQ Custom Block Library is the governed production-implementation layer of the ISQ eLearning Design System. It is not a parallel design system and it is not a repository of copied course snippets.

A component enters this library only when it is reusable, educationally justified, accessible, technically reliable, maintainable, appropriately generalised and consistent with the ISQ eLearning Design System.

## System relationship

1. **ISQ eLearning Design System** — principles, tokens, typography, colour, spacing, interaction standards and reusable presentation primitives.
2. **ISQ Custom Block Library** — governed implementations of selected custom components that solve recurring eLearning interaction or presentation needs.
3. **ISQ xAPI governance layer** — telemetry vocabulary, activity identification, context hierarchy, actor resolution and statement rules.

The three layers operate as one system. A custom block must consume the design system rather than recreate it, and xAPI must remain an optional governed capability unless telemetry is intrinsic to the component's purpose.

## Shared Interaction Shell

Governed learner-response components must consume the shared **ISQ Interaction Shell** rather than developing independent visual treatments.

Current shell consumers:

- Knowledge Check — Single;
- Knowledge Check — Sequence / multiple-response variants;
- Decision Point presentation baseline;
- future learner-response Reflection components where semantically appropriate.

The shell governs shared presentation such as interaction header, type label, prompt hierarchy, response rows, actions, feedback and progression. Component-specific code owns learning semantics and behaviour.

Governance rule:

> All governed ISQ question, decision and response components must consume the canonical ISQ Interaction Shell. Component-specific CSS must not recreate header, response-option, primary-action, feedback or progression styling without an approved exception.

See `interaction-shell/README.md`.

## Lifecycle

- **experimental** — proof or exploration; no reuse promise.
- **candidate** — generalised, documented and under accessibility/runtime validation.
- **approved** — production reuse permitted within documented constraints.
- **deprecated** — existing implementations may remain; no new use.
- **retired** — unsupported and removed from the active catalogue.

## Versioning

Semantic versioning applies to governed component contracts.

- **major** — breaking markup, configuration, behaviour or telemetry contract change.
- **minor** — backwards-compatible capability, variant or governed presentation-anatomy refinement.
- **patch** — backwards-compatible defect, accessibility or documentation correction.

Course-specific copy, learner names, legislation, scenario identifiers and course IDs never form part of a canonical component contract.

## Required component record

Every candidate or approved component must document:

- canonical name and key;
- version and lifecycle status;
- purpose;
- appropriate and inappropriate use;
- learning rationale;
- anatomy and content contract;
- Interaction Shell dependency where applicable;
- canonical HTML;
- CSS dependencies;
- JavaScript dependencies;
- configurable data;
- variants and states;
- accessibility requirements;
- keyboard behaviour;
- responsive behaviour;
- Rise-specific constraints;
- xAPI capability and event contract;
- failure behaviour;
- implementation instructions;
- neutral example content;
- QA evidence and known limitations;
- owner, review date and change history.

## Runtime principle

The default architecture is hybrid:

- semantic HTML remains local to the Rise custom-code block;
- styling is supplied by the governed external ISQ Rise stylesheet;
- small component-specific behaviour may remain embedded for Rise reliability;
- substantial repeated runtime logic should have one canonical source and be inlined or bundled for deployment rather than independently edited in course blocks;
- telemetry is separated from interaction behaviour through a component event contract;
- Rise iframe boundaries are treated explicitly: event listeners/adapters required by a component must exist in the same runtime context or use a separately governed cross-frame mechanism.

A component must continue to provide its learner-facing behaviour if telemetry is unavailable, unless the approved learning requirement explicitly says otherwise.

## Telemetry boundary

Canonical components do not contain LRS credentials, Child Protection identifiers or direct course-specific xAPI transport configuration.

Interactive components emit neutral browser events that a governed telemetry adapter may consume within the appropriate Rise runtime context. The Knowledge Check contract is documented in `runtime/telemetry-contract.md`.

## Current governed component work

### Knowledge Check

- family version: **0.3.0 Candidate**;
- Single and Sequence variants share one question contract;
- single-choice Rise → SCORM 2004 → xAPI → Veracity path has stored-LRS evidence;
- remaining 1.0 gates include multiple-response stored-LRS evidence, accessibility qualification and governance review;
- presentation now consumes the Interaction Shell.

### Decision Point

- presentation baseline: **0.1.0 Candidate**;
- consumes the Interaction Shell;
- behaviour/xAPI semantics are not yet promoted as a fully governed reusable component.

Presentation-only patterns such as Featured List remain part of the design-system component catalogue rather than being duplicated in the Custom Block Library.
