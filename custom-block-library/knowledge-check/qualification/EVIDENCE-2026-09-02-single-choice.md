# Knowledge Check single-choice xAPI qualification evidence — 2 September 2026

Status: **PASS — stored LRS evidence confirmed**

## Environment

- Articulate Rise custom-code block
- SCORM 2004 published runtime
- Connect & Learn test environment
- Veracity LRS test endpoint
- Component: `isq-kc-single`
- Component version: `0.2.0`

## Proven chain

The self-contained qualification bundle successfully demonstrated:

1. Knowledge Check interaction event emitted;
2. authenticated learner resolved via SCORM 2004 on the first attempt;
3. governed `answered` xAPI statement constructed;
4. statement transported to the Veracity test LRS;
5. Veracity returned HTTP 204;
6. both statements were subsequently confirmed as stored in the LRS.

## Stored statements

### Attempt 1 — incorrect

- Statement ID: `60e4a979-13f6-4f83-8cb6-fcab72cd7d10`
- Response: `option-a`
- Success: `false`
- Completion: `true`
- Attempt number: `1`

### Attempt 2 — correct retry

- Statement ID: `141b30ae-7441-4cd0-a01f-9900909951e9`
- Response: `option-b`
- Success: `true`
- Completion: `true`
- Attempt number: `2`

## Statement structure verified

The qualification run confirmed:

- authenticated learner Agent from SCORM 2004;
- verb `http://adlnet.gov/expapi/verbs/answered`;
- Object type `cmi.interaction`;
- `interactionType: choice`;
- stable declared choices;
- `correctResponsesPattern`;
- actual `result.response`;
- measured `result.success`;
- `result.completion: true`;
- Parent and Grouping context activities;
- component key, component version and attempt-number extensions;
- unique statement UUID per submitted attempt.

## Architecture finding

Rise custom-code blocks are iframe-isolated. The successful qualification used the component, event listener/xAPI adapter and test runtime within the same custom-code iframe. A DOM `CustomEvent` emitted in one Rise custom-code iframe cannot be relied upon to reach an adapter listening in a different iframe.

This must be treated as a deployment constraint for the governed library. Shared infrastructure may still have one canonical source, but each telemetry-enabled component iframe must load or contain the runtime/adapter code required in that iframe.

## Release-gate effect

The following Phase 03 gates can now be marked **PASS**:

- Published Rise functional behaviour — Single Knowledge Check
- Single-choice xAPI statement semantics through the new adapter
- SCORM 2004 learner resolution
- Rise → adapter → transport → Veracity end-to-end delivery
- Incorrect attempt recorded separately from successful retry
- Stored-LRS verification for the single-choice path

This evidence does **not** by itself promote the entire Knowledge Check family to `1.0.0 Approved`. Multiple-response stored-LRS qualification, accessibility/device evidence and governance review remain separate gates.
