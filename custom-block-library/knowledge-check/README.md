# Knowledge Check

Family key: `isq-kc`  
Version: `0.1.0`  
Status: **Candidate**  
Variants: `isq-kc-single`, `isq-kc-sequence`

## Purpose

Use a Knowledge Check when the learner should retrieve, discriminate or apply knowledge and the response has an objectively defensible correct answer. The feedback should improve understanding or future performance, not merely report correctness.

Do not use this component for personal reflection, confidence ratings or self-report. Those belong to the Reflection family. Do not use it as a substitute for a scenario Decision Point where the educational value lies in contextual judgement and consequences rather than a simple correct answer.

## Variants

### Knowledge Check — Single

One formative question with immediate explanatory feedback.

Use when one decision or retrieval prompt is sufficient and a multi-question container would add unnecessary interaction cost.

### Knowledge Check — Sequence

A short set of questions using the same question contract. Each question remains an independent interaction and may emit its own telemetry event.

Use when several tightly related questions form one coherent practice sequence. Do not turn long quizzes into a custom sequence when the native Rise quiz is more appropriate.

Sequence navigation is deliberately non-blocking. The component may encourage progression with a Next question action, but formative practice should not rely on inaccessible or brittle UI locking unless the learning requirement genuinely needs gating.

## Anatomy

Each question contains:

1. a clear prompt;
2. a semantic `fieldset` and `legend`;
3. native radio buttons or checkboxes;
4. one primary Check answer action;
5. an associated live feedback region;
6. optional next-question navigation;
7. optional telemetry identifiers supplied by the course implementation.

## Content contract

Required per question:

- `data-question-key` — stable local key within the component instance;
- answer inputs with stable `value` identifiers;
- `data-correct-responses` — comma-separated correct response IDs;
- `data-correct-feedback` — explanatory feedback for a correct response;
- `data-incorrect-feedback` — explanatory feedback for an incorrect response.

Required learner-facing content:

- prompt;
- meaningful legend;
- concise response labels;
- feedback that explains the reasoning.

For telemetry-enabled implementations also provide stable, governed:

- `data-activity-id`;
- `data-parent-activity-id`;
- `data-grouping-activity-id`.

Never reuse the demonstration IDs in production.

## HTML and CSS

The component consumes the existing ISQ Rise design system stylesheet. Phase 02 deliberately introduces no new visual styling because the mature shared classes already provide the required question options, buttons, feedback states, layout and accessible focus treatment.

Current dependencies include:

- `.isq-block`
- `.isq-panel`
- `.isq-content`
- `.isq-options`
- `.isq-option`
- `.isq-decision-actions`
- `.isq-decision-feedback`
- `.isq-callout`
- `.isq-button`
- `.isq-visually-hidden`

This is intentional reuse, not inheritance from Child Protection semantics.

## JavaScript architecture

`knowledge-check.js` is the canonical interaction controller.

The controller owns only learner-facing interaction behaviour:

- validation;
- answer evaluation;
- attempt count for the current runtime instance;
- feedback state;
- optional sequence navigation;
- emission of the neutral `isq:knowledge-check-answered` event.

It does **not** resolve learner identity, discover SCORM APIs, authenticate with an LRS, create xAPI statements or retry network requests.

During Candidate validation, the neutral HTML examples and canonical controller remain separate source artefacts so that controller changes cannot silently diverge across copied examples. For a controlled Rise test, paste the selected example into one custom-code block and inline the exact current contents of `knowledge-check.js` immediately before the closing `</section>` tag.

Once the component passes the Phase 03 Rise and accessibility gates, release preparation should generate immutable, copy-ready Rise bundles from these canonical sources. Generated bundles must never become an independently edited source of truth.

## xAPI capability

Telemetry is optional.

When a valid response is checked, the component emits:

```text
isq:knowledge-check-answered
```

See `../runtime/telemetry-contract.md` for the payload and xAPI mapping.

A course-level ISQ telemetry adapter may listen for the event and construct the governed xAPI statement. If there is no adapter, the Knowledge Check still works normally.

No LRS credential, SCORM learner lookup or course-specific xAPI identifier belongs in the canonical controller.

## Accessibility contract

Release requires all of the following:

- semantic fieldset/legend grouping;
- native radio/checkbox operation;
- visible keyboard focus;
- meaningful control labels;
- feedback associated with the question using `aria-describedby`;
- dynamic feedback exposed through `role="status"` and `aria-live="polite"`;
- correct/incorrect meaning communicated in text, not colour alone;
- no keyboard trap;
- mobile touch targets remain usable;
- content remains understandable at 200% zoom and enlarged text;
- no essential behaviour depends on motion;
- sequence focus movement is predictable and only occurs after an explicit navigation action.

## Candidate Rise validation workflow

For the controlled Phase 03 test implementation:

1. choose `examples/single.html` or `examples/sequence.html`;
2. paste the example into one Rise custom-code block;
3. inline the exact governed contents of `knowledge-check.js` at the marked location;
4. replace the neutral demonstration copy as required for the test;
5. replace demonstration response identifiers with stable local identifiers;
6. supply governed activity, parent and grouping IDs if telemetry is being tested;
7. do not add an LRS credential or direct xAPI transport to the component;
8. verify the course uses the approved external ISQ Rise stylesheet version;
9. test the published package, not only the Rise authoring preview.

If telemetry is required, add the approved ISQ telemetry adapter at course/runtime level according to xAPI governance. Phase 02 deliberately does not invent or ship production xAPI transport before that architecture is reviewed.

## QA gate before Approved

`0.1.0` remains Candidate until the following evidence exists:

- source/static validation passes;
- published Rise desktop behaviour passes;
- published Rise mobile behaviour passes at 320px and representative phone width;
- keyboard-only pass;
- screen-reader semantics/feedback pass;
- 200% zoom/text resize pass;
- no telemetry present: interaction still passes;
- telemetry adapter present: event payload and xAPI statement mapping pass;
- failure-to-send test confirms formative feedback/progression is unaffected;
- xAPI architecture reviewed by the relevant ISQ xAPI stakeholder.

Only after those gates should the family be promoted from `candidate` to `approved` and released as `1.0.0`.

## Change history

### 0.1.0 — Candidate foundation

- Extracted the reusable question/evaluation behaviour from Child Protection implementations.
- Removed Child Protection wording, legislation, scenario names and activity IDs.
- Removed embedded xAPI transport and learner-resolution responsibilities.
- Established Single and Sequence variants on one question contract.
- Added neutral telemetry event contract.
- Retained existing shared ISQ design-system CSS primitives rather than introducing duplicate component styling.
