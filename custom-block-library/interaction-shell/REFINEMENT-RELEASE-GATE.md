# Interaction Shell refinement — release gate

Status: **Candidate refinement implemented**  
Shell source: **0.1.0**  
Knowledge Check consuming version: **0.3.0 Candidate**  
Decision Point presentation baseline: **0.1.0 Candidate**  
Target Rise stylesheet: **1.1.0**

## Decision

The amended CP for Principals visual prototype establishes the preferred refined interaction language, but the course prototype is not the production authority. Its reusable visual decisions have been extracted into the governed ISQ Interaction Shell and mapped to existing ISQ design tokens.

## Implemented

- shared `.isq-interaction` anatomy;
- common dark-header treatment for Decision Point and Knowledge Check;
- common interaction-type label and title hierarchy;
- full-row native radio/checkbox response treatment;
- shared selected, hover and mobile states;
- shared action and feedback layout;
- shared progression/footer treatment;
- no side-highlight treatment;
- Knowledge Check Single and Sequence examples migrated to the shell;
- neutral Decision Point presentation example added;
- automated validator updated to enforce shell adoption.

## Explicit non-decisions

The following have **not** been copied from the CP prototype as universal authority:

- CP-specific wording or scenarios;
- provisional CP prototype colour values;
- course-specific one-attempt rules;
- Decision Point xAPI semantics;
- a universal requirement to gate progression;
- Reflection styling beyond the future response-component relationship.

## Required QA before stylesheet 1.1.0 release

1. Desktop visual review of Decision Point, Knowledge Check Single, Multiple response and Sequence.
2. 320px/mobile visual and interaction review.
3. Keyboard focus review, including selected options and progression controls.
4. 200% zoom/reflow review.
5. Confirm native radio/checkbox semantics remain intact.
6. Confirm feedback states remain distinguishable without colour alone.
7. Confirm no conflict with existing `.isq-option`, `.isq-options`, `.isq-decision-actions` or `.isq-decision-feedback` rules.
8. Confirm existing courses on 1.0.0 remain unaffected.
9. Build and publish immutable `isq-rise-components-v1.1.0.css` rather than modifying 1.0.0 in place.
10. Update the component catalogue and CP for Principals production baseline when 1.1.0 is released.

## Migration rule

- Existing published courses remain pinned to 1.0.0 unless deliberately upgraded.
- New governed Decision Points and Knowledge Checks should use Interaction Shell markup.
- During the candidate period, the shell source may be inlined/loaded only for controlled visual qualification.
- Once 1.1.0 is released, local shell CSS copies are prohibited.

## Governance enforcement

`validate_custom_block_library.py` now checks that:

- Knowledge Check declares the Interaction Shell as required;
- Single and Sequence examples consume the shell;
- the Decision Point reference example consumes the shell;
- required shell selectors exist;
- no side-highlight CSS is introduced;
- canonical shell/example source remains domain-neutral.
