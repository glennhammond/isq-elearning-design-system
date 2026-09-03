# ISQ Interaction Shell

Status: **Candidate foundation**  
Source version: **0.1.0**  
Intended stylesheet release: **ISQ Rise components 1.1.0**

## Purpose

The Interaction Shell is the shared presentation layer for governed ISQ learner-response components. It prevents Knowledge Checks, Decision Points and later Reflection interactions from evolving as separate visual systems.

It is a design-system dependency, not a learner component in its own right.

## Visual evidence

The initial refinement direction was extracted from the amended `CP_Principals_2027_Visual_Component_Family_v0.1.html` prototype. That prototype remains course evidence only; Child Protection wording, story logic, legal content and course-specific identifiers are not part of the canonical shell.

The reusable characteristics promoted from that prototype are:

- dark ISQ header band;
- small uppercase interaction-type label;
- prominent white interaction title;
- restrained white body surface;
- generous, full-row native radio/checkbox choices;
- clear checked, hover and focus states;
- one visually dominant response action;
- feedback below the response action;
- separate progression/footer region where progression exists;
- restrained borders/radii using ISQ tokens;
- mobile stacking without changing interaction meaning.

The prototype's provisional colour values are **not** copied as design-system authority. Canonical implementation uses existing validated ISQ tokens such as `--isq-blue-dark`, `--isq-border`, `--isq-ice` and the existing typography tokens.

## Components that must consume this shell

The governed target family is:

- Decision Point;
- Knowledge Check — Single;
- Knowledge Check — Multiple response;
- Knowledge Check — Sequence;
- Reflection interactions where a learner response is required, subject to later semantic review.

Presentation-only reflections do not automatically require the shell.

## Governance rule

> All governed ISQ question, decision and response components must consume the canonical ISQ Interaction Shell. Component-specific CSS must not recreate header, response-option, primary-action, feedback or progression styling without an approved exception.

This rule is intended to ensure that future visual refinements propagate across the interaction family rather than being manually copied between components.

## Canonical anatomy

- `.isq-interaction`
- `.isq-interaction__header`
- `.isq-interaction__type`
- `.isq-interaction__title`
- `.isq-interaction__body`
- `.isq-interaction__instruction`
- `.isq-interaction__options`
- `.isq-interaction__option`
- `.isq-interaction__actions`
- `.isq-interaction__feedback`
- `.isq-interaction__progression`
- `.isq-interaction__progression-state`

Semantic modifiers:

- `.isq-interaction--decision`
- `.isq-interaction--knowledge-check`
- `.isq-interaction--reflection`

Semantic modifiers do not create competing colour schemes. The interaction-type label communicates function; visual family resemblance is intentional.

## Accessibility requirements

The shell does not replace semantic HTML. Components using it must still:

- use native radio/checkbox controls;
- group response options with `fieldset` and `legend` where appropriate;
- preserve visible focus;
- provide text labels for state and feedback;
- expose dynamic feedback appropriately;
- not rely on colour alone;
- retain usable touch targets;
- remain usable at narrow widths and enlarged text;
- avoid essential motion.

## CSS architecture

`interaction-shell.css` is the candidate source fragment. It must be incorporated into the next immutable production Rise stylesheet release rather than maintained as a long-term second stylesheet.

Target release approach:

- leave `isq-rise-components-v1.0.0.css` unchanged;
- integrate and QA this source fragment;
- publish an immutable `isq-rise-components-v1.1.0.css` when approved;
- migrate new governed interaction markup to the shell;
- retain compatibility classes only for a defined migration period.

## Behaviour boundary

The Interaction Shell owns presentation only. It must not own:

- answer evaluation;
- Decision Point branching;
- sequence logic;
- xAPI statement construction;
- SCORM learner resolution;
- transport to an LRS.

Those responsibilities remain in their governed component/runtime layers.

## Change history

### 0.1.0 — Candidate

- Extracted the refined interaction presentation from the amended CP for Principals visual prototype.
- Replaced provisional prototype colours with validated ISQ design-system tokens.
- Established a common anatomy for Decision Point and Knowledge Check families.
- Added a backwards-compatible bridge for current `.isq-decision` markup.
