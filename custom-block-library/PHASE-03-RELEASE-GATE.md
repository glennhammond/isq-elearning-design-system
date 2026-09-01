# Phase 03 — Controlled Rise Validation + xAPI Adapter + Knowledge Check 1.0 Release Gate

Status: **Phase complete — release gate HOLD**  
Current family version: **0.2.0 Candidate**  
Target release: **1.0.0 Approved**

## Executive decision

Phase 03 has completed the implementation and evidence preparation that can be performed in the governed source repository. The Knowledge Check family is **not promoted to 1.0.0 Approved** because several release gates require evidence from an actual published Articulate Rise package, assistive-technology testing and stored statements delivered through an approved ISQ xAPI runtime/transport.

This HOLD is a governance success, not an incomplete architecture decision. Approval is evidence-based.

## Implemented in this phase

### 1. Governed xAPI adapter boundary

`runtime/xapi-adapter.js` now translates the neutral `isq:knowledge-check-answered` event into the governed choice-interaction statement shape.

It provides:

- `answered` verb;
- `cmi.interaction` Activity type;
- `choice` interaction type;
- stable declared choices;
- deterministic `[,]` multiple-response encoding;
- `correctResponsesPattern`;
- `result.response`;
- measured `result.success`;
- `result.completion: true` after a valid submission;
- parent and grouping context;
- registration only when supplied by the runtime;
- statement UUID generated before delivery;
- component key/version and attempt-number extensions.

The adapter contains **no endpoint, browser credential, SCORM discovery or direct network transport**.

### 2. Shared runtime contract

The adapter delegates trusted identity and delivery to:

```js
window.ISQ_XAPI_RUNTIME = {
  async getActor() {},
  async getRegistration() {},
  async sendStatement(statement, options) {}
};
```

This creates the maintainability boundary required by the library without pretending that moving a reusable credential into a shared JavaScript file would secure it.

### 3. Identity failure policy

Governed learner evidence is not emitted with an invented anonymous Actor when trusted identity cannot be resolved. The adapter reports `identity-unavailable` operationally and leaves the formative interaction unaffected.

This aligns the reusable component with the Child Protection governance rule that authenticated evidence should not silently degrade into anonymous evidence.

### 4. Formative failure isolation

Telemetry remains non-blocking. Correct/incorrect learning feedback is produced by the component before telemetry delivery is attempted. A transport or identity failure therefore cannot convert a learning answer into a UI error or prevent the learner continuing.

### 5. Stronger activity metadata contract

Telemetry-enabled Knowledge Checks now provide:

- activity ID;
- activity name;
- optional activity description;
- parent activity ID;
- grouping activity ID.

Course-specific identifiers remain configuration, never canonical component code.

### 6. Deterministic response ordering

Single and multiple responses are normalised to the order of the declared choices before the event is emitted. This gives stable xAPI response and correct-response serialisation rather than relying on incidental click order.

### 7. Automated repository QA

`validate_custom_block_library.py` now checks the governed source for:

- component family/variant integrity;
- component/telemetry separation;
- required accessibility primitives in neutral examples;
- required telemetry metadata;
- absence of embedded endpoint credentials;
- absence of Child Protection-specific identifiers/content in canonical implementation source;
- governed `[,]` response delimiter;
- expected xAPI mapping fields.

`.github/workflows/custom-block-library.yml` runs this validator for relevant branches and pull requests.

## Relationship to current ISQ xAPI governance

Phase 03 is deliberately compatible with the established governance evidence:

- Object = direct interaction;
- Parent = direct containing activity;
- Grouping = broader course/experience;
- `en-AU` for ISQ-authored language maps;
- `answered` for a submitted choice interaction;
- actual response and measured success;
- genuine registration only when one exists;
- distinct statements for distinct attempts;
- no browser credential as a production design.

The existing governance library records single-choice Pattern P002 as technically PROVEN and multiple-response P004 as CANDIDATE. The reusable Knowledge Check family supports both through one component contract, so the family cannot claim complete telemetry qualification until the multiple-response path is also verified in stored LRS evidence.

## Release-gate matrix

| Gate | Current state | Decision |
| --- | --- | --- |
| Architecture/component contract | PASS | Complete |
| Domain generalisation | PASS | No CP-specific canonical content/IDs |
| CSS duplication | PASS | Existing shared design-system CSS reused |
| JS responsibility separation | PASS | Interaction, adapter and transport boundaries defined |
| Static/source validation | PASS when CI green | Automated validator added |
| Single-choice statement semantics | Strong prior evidence | Existing P002 governance evidence supports shape; re-verify through new adapter |
| Multiple-response statement semantics | PENDING | P004 stored-LRS verification required |
| Browser credential security | PASS by design | No credential/endpoint in component or adapter |
| Production transport | EXTERNAL DEPENDENCY | Approved runtime/proxy/short-lived model required |
| Published Rise desktop | PENDING | Manual/runtime evidence required |
| Published Rise mobile / 320px | PENDING | Manual/runtime evidence required |
| Keyboard-only | PENDING | Manual/runtime evidence required |
| Screen reader | PENDING | Assistive-technology evidence required |
| 200% zoom / text resize | PENDING | Manual/runtime evidence required |
| No-xAPI behaviour | Architecture PASS | Confirm once in published Rise package |
| Failed-xAPI behaviour | Architecture PASS | Confirm through runtime fault test |
| xAPI stakeholder review | PENDING | Review architecture/evidence with Julian |

## Exact controlled validation procedure

### A. Neutral Rise test course

Create one neutral Rise test lesson containing:

1. Knowledge Check — Single, radio choice;
2. Knowledge Check — Single, checkbox multiple response;
3. Knowledge Check — Sequence with two questions;
4. one duplicate instance to prove IDs/names do not conflict;
5. one instance with telemetry metadata omitted to prove no-xAPI mode.

Do not use Child Protection wording or identifiers.

### B. Publish context

Publish using the same Rise → SCORM 2004 → Connect & Learn development path used for current ISQ xAPI qualification where possible. Validate the **published package**, not only Rise authoring preview.

### C. Accessibility/runtime matrix

For every variant verify:

- mouse/pointer;
- keyboard only;
- screen reader with labels, grouping and status feedback;
- narrow mobile width including 320 CSS px;
- representative phone viewport;
- 200% browser zoom/text enlargement;
- focus after Next question;
- validation warning with no answer;
- incorrect answer then retry;
- correct answer;
- repeated component instances;
- no telemetry runtime;
- runtime identity unavailable;
- transport failure;
- transport success.

### D. LRS evidence

For each valid answer path retain a sanitised stored statement and verify:

- statement ID is stable/unique;
- Actor is the intended authenticated learner;
- verb is `answered`;
- Object is the direct Knowledge Check Activity;
- `interactionType` is `choice`;
- declared choices use stable IDs;
- `correctResponsesPattern` is present;
- single response is encoded correctly;
- multiple responses use `[,]` deterministically;
- `success` reflects the submitted attempt;
- `completion` is true for a valid submitted response;
- parent/grouping are correct;
- registration is present only if genuine;
- attempt number is correct;
- retries do not duplicate a statement through transport replay.

### E. Negative evidence

Verify that **no governed learner statement** is created for:

- component load;
- no selection;
- navigation alone;
- missing telemetry metadata;
- unresolved trusted learner identity.

## Promotion rule

Promote to **Knowledge Check 1.0.0 Approved** only when:

1. repository CI is green;
2. published-Rise accessibility/runtime matrix passes;
3. single- and multiple-choice adapter statements are verified in stored LRS evidence;
4. failure isolation is demonstrated;
5. the secure runtime/transport boundary is approved for the intended environment;
6. xAPI governance review is complete;
7. no open severity-high accessibility or telemetry defects remain.

At promotion:

- change component status from `candidate` to `approved`;
- release `1.0.0`;
- retain immutable source/release hash;
- add the family to the generated interactive catalogue;
- record qualification evidence and environment;
- do not modify a released 1.0.0 asset in place.

## Phase outcome

Phase 03 is therefore **complete with a HOLD release decision**.

The architecture and reusable source are ready for the controlled environment. The remaining evidence cannot be truthfully manufactured inside the repository. This is the intended operation of the governance model: code can become a release candidate through engineering work; it becomes Approved only through evidence.
