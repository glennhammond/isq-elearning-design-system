# Knowledge Check

Family key: `isq-kc`  
Version: `0.3.0`  
Status: **Candidate**  
Variants: `isq-kc-single`, `isq-kc-sequence`

## Purpose

Use a Knowledge Check when the learner should retrieve, discriminate or apply knowledge and the response has an objectively defensible correct answer. Feedback should improve understanding or future performance rather than merely report correctness.

Do not use this component for personal reflection, confidence ratings or self-report. Do not use it as a substitute for a scenario Decision Point where the educational value lies in contextual judgement and consequences.

## Variants

### Knowledge Check — Single

One formative question with immediate explanatory feedback.

### Knowledge Check — Sequence

A short set of questions using the same question contract. Each question remains an independent interaction and may emit its own telemetry event.

Sequence navigation is deliberately non-blocking. Formative practice should not rely on brittle UI locking unless the learning requirement genuinely requires gating.

## Interaction Shell

From `0.3.0`, all Knowledge Check variants consume the governed **ISQ Interaction Shell**.

Required presentation classes include:

- `.isq-interaction`
- `.isq-interaction--knowledge-check`
- `.isq-interaction__header`
- `.isq-interaction__type`
- `.isq-interaction__title`
- `.isq-interaction__body`
- `.isq-interaction__instruction`
- `.isq-interaction__options`
- `.isq-interaction__option`
- `.isq-interaction__actions`
- `.isq-interaction__feedback`
- `.isq-interaction__progression` where progression exists

The shell is shared with Decision Point rather than recreated locally. This is intentional: refinements to header hierarchy, response rows, action treatment, feedback spacing, progression, mobile behaviour or focus presentation should propagate across the interaction family.

See `../interaction-shell/README.md` and `../interaction-shell/interaction-shell.css`.

## Anatomy

Each question contains:

1. interaction-type label and clear prompt;
2. supporting instruction where required;
3. semantic `fieldset` and `legend`;
4. native radio buttons or checkboxes;
5. one primary Check answer action;
6. associated live feedback;
7. optional next-question/progression navigation;
8. optional telemetry identifiers supplied by the course implementation.

## Content contract

Required per question:

- `data-question-key`;
- stable response `value` identifiers;
- `data-correct-responses`;
- `data-correct-feedback`;
- `data-incorrect-feedback`.

For telemetry-enabled use also provide governed:

- `data-activity-id`;
- `data-activity-name`;
- optional `data-activity-description`;
- `data-parent-activity-id`;
- `data-grouping-activity-id`.

Never reuse demonstration IDs in production.

## CSS architecture

Knowledge Check must not introduce local CSS for interaction header, response rows, actions, feedback or progression. Those concerns belong to the shared Interaction Shell.

The current shell is Candidate source pending integration into the next immutable Rise stylesheet release. `isq-rise-components-v1.0.0.css` must remain unchanged. The intended next stylesheet is `isq-rise-components-v1.1.0.css` after shell QA and release approval.

## JavaScript architecture

`knowledge-check.js` remains the canonical interaction controller. The visual refinement does **not** change the component's behavioural/xAPI responsibilities.

The controller owns:

- validation;
- answer evaluation;
- runtime attempt count;
- feedback state;
- optional sequence navigation;
- emission of `isq:knowledge-check-answered`.

It does not own learner identity, SCORM discovery, xAPI statement construction or LRS transport.

## xAPI capability

Telemetry is optional. When a valid response is checked the component emits:

```text
isq:knowledge-check-answered
```

The governed xAPI adapter constructs the statement and delegates identity/transport to `window.ISQ_XAPI_RUNTIME` within the same Rise iframe/runtime context.

The interaction continues to work if telemetry is unavailable.

## Accessibility contract

Release requires:

- semantic fieldset/legend grouping;
- native radio/checkbox operation;
- visible keyboard focus;
- meaningful control labels;
- feedback associated with the question and announced appropriately;
- correctness conveyed in text, not colour alone;
- no keyboard trap;
- usable mobile touch targets;
- 200% zoom/text-resize usability;
- no essential dependence on motion;
- predictable Sequence focus movement.

## Candidate Rise validation workflow

1. choose the relevant example;
2. use the governed Interaction Shell candidate source during shell qualification;
3. inline the current governed `knowledge-check.js` controller for the controlled Rise test;
4. replace neutral demonstration content and IDs;
5. supply governed activity metadata if telemetry is being tested;
6. never add an LRS credential to canonical component source;
7. validate the published package, not only Rise authoring preview.

## QA gate before Approved

The family remains Candidate until the relevant gates pass, including:

- repository/static QA;
- Interaction Shell visual regression across Single, Multiple response and Sequence;
- keyboard-only published-Rise pass;
- screen-reader pass;
- mobile/320px pass;
- 200% zoom/text-resize pass;
- no-telemetry behaviour;
- xAPI statement qualification;
- xAPI governance review.

## Change history

### 0.3.0 — Interaction Shell refinement

- Adopted the governed ISQ Interaction Shell extracted from the amended CP for Principals visual prototype.
- Replaced the earlier tinted-panel Knowledge Check presentation with the shared dark-header, full-row response and restrained progression grammar.
- Kept all Knowledge Check learning and xAPI semantics separate from presentation.
- Added visual-regression requirements across Knowledge Check variants.

### 0.2.0 — xAPI candidate refinement

- Strengthened activity metadata and response-ordering contracts.
- Added governed adapter/runtime separation and controlled qualification evidence.

### 0.1.0 — Candidate foundation

- Extracted reusable question/evaluation behaviour from Child Protection source implementations.
- Removed course-specific wording, legislation, scenario names and activity IDs.
- Established Single and Sequence variants on one question contract.
