# Phase 03 — Controlled Rise Validation + xAPI Adapter + Knowledge Check 1.0 Release Gate

Status: **Phase complete — release gate HOLD**  
Current family version: **0.2.0 Candidate**  
Target release: **1.0.0 Approved**

## Executive decision

Phase 03 has completed the implementation and repository-side qualification architecture for the first governed Knowledge Check family. The release remains on **HOLD for 1.0.0 Approved**, but the most important end-to-end single-choice telemetry path has now been proven in the actual ISQ environment.

On 2 September 2026 a self-contained qualification bundle was run through the published Rise → SCORM 2004 → Connect & Learn → Veracity path. The component resolved the authenticated learner through SCORM 2004, emitted distinct incorrect and correct attempts, constructed governed xAPI statements, received HTTP 204 from Veracity for both PUT requests, and both statement IDs were subsequently confirmed as stored in the LRS.

The remaining gates are multiple-response stored-LRS verification, accessibility/device qualification, failure-mode qualification, production transport governance and stakeholder review. Approval remains evidence-based.

## Implemented in this phase

### 1. Governed xAPI adapter boundary

`runtime/xapi-adapter.js` translates the neutral `isq:knowledge-check-answered` event into the governed choice-interaction statement shape.

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

The canonical adapter contains **no endpoint, browser credential, SCORM discovery or direct network transport**.

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

### 3. Rise iframe deployment constraint

Controlled qualification confirmed an important Rise constraint: a custom-code block runs inside its own iframe. A DOM `CustomEvent` emitted by a component does not cross into a different custom-code block iframe.

Therefore an xAPI-enabled component deployment must ensure that the interaction controller, adapter and runtime are available within the same iframe/runtime context. The governed source may remain modular in the repository, but Rise deployment must either:

- inline/bundle the governed runtime and adapter into the component block; or
- load governed external scripts from within that same component iframe.

A course-level listener in a separate Rise custom-code block is not a valid architecture for ordinary DOM-event communication.

### 4. Identity failure policy

Governed learner evidence is not emitted with an invented anonymous Actor when trusted identity cannot be resolved. The adapter reports `identity-unavailable` operationally and leaves the formative interaction unaffected.

### 5. Formative failure isolation

Telemetry remains non-blocking. Correct/incorrect learning feedback is produced by the component before telemetry delivery is attempted. A transport or identity failure therefore cannot convert a learning answer into a UI error or prevent the learner continuing.

### 6. Stronger activity metadata contract

Telemetry-enabled Knowledge Checks provide:

- activity ID;
- activity name;
- optional activity description;
- parent activity ID;
- grouping activity ID.

Course-specific identifiers remain configuration, never canonical component code.

### 7. Deterministic response ordering

Single and multiple responses are normalised to the order of the declared choices before the event is emitted. This gives stable xAPI response and correct-response serialisation rather than relying on incidental click order.

### 8. Automated repository QA

`validate_custom_block_library.py` checks the governed source for:

- component family/variant integrity;
- component/telemetry separation;
- required accessibility primitives in neutral examples;
- required telemetry metadata;
- absence of embedded endpoint credentials;
- absence of Child Protection-specific identifiers/content in canonical implementation source;
- governed `[,]` response delimiter;
- expected xAPI mapping fields.

`.github/workflows/custom-block-library.yml` runs this validator for relevant branches and pull requests.

## Controlled qualification evidence — 2 September 2026

### Environment

- Articulate Rise custom-code block
- published through SCORM 2004
- Connect & Learn test/development environment
- authenticated learner resolved through SCORM 2004
- controlled Veracity test endpoint
- self-contained qualification bundle so component, adapter and runtime share one Rise iframe

### Single-choice incorrect attempt — PASS

Stored statement ID:

```text
60e4a979-13f6-4f83-8cb6-fcab72cd7d10
```

Verified evidence:

- Actor resolved through SCORM 2004 on attempt 1;
- verb `answered`;
- Object = direct Knowledge Check interaction;
- `interactionType: choice`;
- declared choices and `correctResponsesPattern` present;
- `result.response: option-a`;
- `result.success: false`;
- `result.completion: true`;
- Parent and Grouping present;
- component key/version and attempt number present;
- HTTP 204 returned by Veracity;
- statement confirmed stored in Veracity.

### Single-choice correct retry — PASS

Stored statement ID:

```text
141b30ae-7441-4cd0-a01f-9900909951e9
```

Verified evidence:

- same authenticated learner resolved through SCORM 2004;
- separate statement UUID from the incorrect attempt;
- `result.response: option-b`;
- `result.success: true`;
- `result.completion: true`;
- attempt number advanced to 2;
- Parent and Grouping retained;
- HTTP 204 returned by Veracity;
- statement confirmed stored in Veracity.

### Evidence decision

The reusable single-choice Knowledge Check path is now **technically proven end to end through the Phase 03 adapter/runtime architecture**. Single-choice xAPI is no longer a release blocker.

## Relationship to current ISQ xAPI governance

Phase 03 is compatible with the established governance direction:

- Object = direct interaction;
- Parent = direct containing activity;
- Grouping = broader course/experience;
- `en-AU` for ISQ-authored language maps;
- `answered` for a submitted choice interaction;
- actual response and measured success;
- genuine registration only when one exists;
- distinct statements for distinct attempts;
- no browser credential as a production design.

The existing governance library records single-choice Pattern P002 as technically PROVEN and multiple-response P004 as CANDIDATE. The Phase 03 qualification now independently re-proves the single-choice path through the reusable component architecture. Multiple-response still requires stored-LRS verification before the family can claim complete telemetry qualification.

## Release-gate matrix

| Gate | Current state | Decision |
| --- | --- | --- |
| Architecture/component contract | PASS | Complete |
| Domain generalisation | PASS | No CP-specific canonical content/IDs |
| CSS duplication | PASS | Existing shared design-system CSS reused |
| JS responsibility separation | PASS | Interaction, adapter and transport boundaries defined |
| Rise iframe architecture | PASS | Same-iframe deployment requirement proven and documented |
| Static/source validation | PASS when CI green | Automated validator added |
| Published Rise desktop functional behaviour | PASS — initial | Single, multiple-response UI, sequence, duplicate-instance and no-xAPI interaction cases exercised successfully |
| Single-choice stored-LRS semantics | **PASS** | Incorrect + correct retry confirmed stored in Veracity |
| Multiple-response stored-LRS semantics | PENDING | Controlled stored-LRS verification required |
| Browser credential security | PASS by design | No credential/endpoint in canonical component or adapter |
| Controlled test transport | **PASS** | Rise → SCORM 2004 → Veracity proven |
| Production transport | EXTERNAL DEPENDENCY | Approved runtime/proxy/short-lived model still required |
| Published Rise mobile / 320px | PENDING | Manual/runtime evidence required |
| Keyboard-only | PENDING | Manual/runtime evidence required |
| Screen reader | PENDING | Assistive-technology evidence required |
| 200% zoom / text resize | PENDING | Manual/runtime evidence required |
| No-xAPI behaviour | **PASS — functional** | Learner interaction confirmed working without telemetry configuration |
| Repeated instances / collision | **PASS — functional** | Two components in one runtime worked independently |
| Failed-xAPI behaviour | Architecture PASS | Controlled runtime fault test still required |
| xAPI stakeholder review | PENDING | Review architecture/evidence with Julian |

## Exact remaining controlled validation procedure

### A. Multiple-response xAPI qualification

Run the checkbox multiple-response Knowledge Check using the same self-contained qualification architecture and retain at least:

1. one incorrect stored statement;
2. one correct stored statement;
3. confirmation that response and `correctResponsesPattern` use deterministic `[,]` ordering.

### B. Accessibility/runtime matrix

Verify the approved candidate in the published package for:

- keyboard only;
- screen reader labels, grouping and status feedback;
- narrow mobile width including 320 CSS px;
- representative phone viewport;
- 200% browser zoom/text enlargement;
- focus after sequence navigation;
- validation warning with no answer;
- no keyboard trap;
- visible focus;
- sufficient touch targets.

### C. Failure qualification

Demonstrate that:

- unresolved actor prevents governed learner evidence but does not block feedback;
- unavailable/failed transport does not block learner feedback or progression;
- missing telemetry metadata creates no governed statement;
- no-selection creates no governed statement.

### D. Governance review

Review with the relevant ISQ xAPI stakeholder:

- same-iframe Rise deployment boundary;
- Actor resolution contract;
- Object/Parent/Grouping hierarchy;
- component/version/attempt extensions;
- registration behaviour;
- controlled-test direct browser transport versus approved production transport.

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

Phase 03 remains **complete with a HOLD release decision**, but the HOLD is now narrow rather than architectural.

The single-choice Knowledge Check has passed end-to-end Rise/SCORM/LRS qualification. Remaining work is multiple-response evidence, accessibility/failure qualification and governance approval. These outstanding gates should not block unrelated Child Protection for Principals design and development using the frozen production baseline documented separately.
