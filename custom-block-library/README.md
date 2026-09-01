# ISQ Custom Block Library

Status: Candidate foundation  
Phase: 02 — Knowledge Check canonicalisation  
Owner: ISQ eLearning design/development steward

## Purpose

The ISQ Custom Block Library is the governed production-implementation layer of the ISQ eLearning Design System. It is not a parallel design system and it is not a repository of copied course snippets.

A component enters this library only when it is reusable, educationally justified, accessible, technically reliable, maintainable, appropriately generalised and consistent with the ISQ eLearning Design System.

## System relationship

1. **ISQ eLearning Design System** — principles, tokens, typography, colour, spacing, interaction standards and reusable presentation primitives.
2. **ISQ Custom Block Library** — governed implementations of selected custom components that solve recurring eLearning interaction or presentation needs.
3. **ISQ xAPI governance layer** — telemetry vocabulary, activity identification, context hierarchy, actor resolution and statement rules.

The three layers operate as one system. A custom block must consume the design system rather than recreate it, and xAPI must remain an optional governed capability unless telemetry is intrinsic to the component's purpose.

## Lifecycle

- **experimental** — proof or exploration; no reuse promise.
- **candidate** — generalised, documented and under accessibility/runtime validation.
- **approved** — production reuse permitted within documented constraints.
- **deprecated** — existing implementations may remain; no new use.
- **retired** — unsupported and removed from the active catalogue.

## Versioning

Semantic versioning applies to governed component contracts.

- **major** — breaking markup, configuration, behaviour or telemetry contract change.
- **minor** — backwards-compatible capability or variant.
- **patch** — backwards-compatible defect, accessibility or documentation correction.

Course-specific copy, learner names, legislation, scenario identifiers and course IDs never form part of a canonical component contract.

## Required component record

Every candidate or approved component must document:

- canonical name and key
- version and lifecycle status
- purpose
- appropriate and inappropriate use
- learning rationale
- anatomy and content contract
- canonical HTML
- CSS dependencies
- JavaScript dependencies
- configurable data
- variants and states
- accessibility requirements
- keyboard behaviour
- responsive behaviour
- Rise-specific constraints
- xAPI capability and event contract
- failure behaviour
- implementation instructions
- neutral example content
- QA evidence and known limitations
- owner, review date and change history

## Runtime principle

The default architecture is hybrid:

- semantic HTML remains local to the Rise custom-code block;
- styling is supplied by the governed external ISQ Rise stylesheet;
- small component-specific behaviour may remain embedded for Rise reliability;
- substantial repeated runtime logic should have one canonical source and be inlined or bundled for deployment rather than independently edited in course blocks;
- telemetry is separated from interaction behaviour through a component event contract.

A component must continue to provide its learner-facing behaviour if telemetry is unavailable, unless the approved learning requirement explicitly says otherwise.

## Telemetry boundary

Canonical components do not contain LRS credentials, Child Protection identifiers or direct course-specific xAPI transport configuration.

Interactive components emit neutral browser events that a governed telemetry adapter may consume. The first event contract is documented in `runtime/telemetry-contract.md`.

## Phase 02 promotion scope

The first governed family is **Knowledge Check**:

- `isq-kc-single` — one formative question.
- `isq-kc-sequence` — a short sequence of formative questions using the same question contract.

Both are currently **candidate** rather than **approved** until Rise package QA and xAPI governance review are complete.

Presentation-only patterns such as Featured List remain part of the design-system component catalogue rather than being duplicated here.
