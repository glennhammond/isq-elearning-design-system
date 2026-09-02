# ISQ Custom Block Telemetry Contract

Status: Candidate  
Contract version: 0.2.0

## Purpose

This contract separates learner interaction behaviour from xAPI identity, statement construction and transport. A component emits a neutral browser event. The governed adapter translates that event into a standards-aligned statement and delegates trusted identity plus secure delivery to an injected ISQ xAPI runtime.

The component and adapter must not contain production LRS credentials, hard-coded course-specific identifiers, reusable Basic authentication values or a direct production endpoint.

## Knowledge Check event

Event name:

```text
isq:knowledge-check-answered
```

The event is dispatched from the component root using `CustomEvent` with `bubbles: true`.

Telemetry-enabled instances supply stable course metadata. The minimum event payload is:

```json
{
  "contractVersion": "0.2.0",
  "component": "isq-kc-single",
  "componentVersion": "0.2.0",
  "questionKey": "workplace-priority",
  "activityId": "https://example.isq.qld.edu.au/xapi/demo/workplace-priority",
  "activityName": "Workplace priority knowledge check",
  "activityDescription": "Which action should come first?",
  "parentActivityId": "https://example.isq.qld.edu.au/xapi/demo/activity",
  "groupingActivityId": "https://example.isq.qld.edu.au/xapi/demo/course",
  "interactionType": "choice",
  "responseIds": ["urgent"],
  "correctResponseIds": ["urgent"],
  "success": true,
  "completion": true,
  "attemptNumber": 1,
  "choices": [
    {"id": "urgent", "label": "Address the safety issue first"},
    {"id": "routine", "label": "Complete routine administration first"}
  ]
}
```

Response and correct-response IDs are normalised to source choice order before the event is emitted. This gives deterministic multiple-response encoding.

## xAPI adapter mapping

`xapi-adapter.js` maps a valid formative submission as follows:

- verb: `http://adlnet.gov/expapi/verbs/answered`
- object type: `http://adlnet.gov/expapi/activities/cmi.interaction`
- interaction type: `choice`
- object/activity ID: `activityId`
- object name/description: supplied activity metadata using `en-AU`
- choices: stable IDs plus learner-facing labels
- correctResponsesPattern: IDs joined using the xAPI `[,]` delimiter
- result.response: selected IDs joined using `[,]`
- result.success: measured Boolean success
- result.completion: `true` because a valid response was submitted
- context parent: `parentActivityId`
- context grouping: `groupingActivityId`
- context registration: only when the runtime supplies a genuine registration
- statement ID: UUID generated before delivery so a transport implementation can use it as an idempotency key
- ISQ extensions: component key, component version and attempt number

The adapter does not create an Actor itself and does not send a network request directly.

## Shared runtime contract

For governed telemetry, the containing runtime exposes:

```js
window.ISQ_XAPI_RUNTIME = {
  async getActor() { /* return trusted xAPI Agent or null */ },
  async getRegistration() { /* optional genuine registration UUID or null */ },
  async sendStatement(statement, options) { /* secure governed transport */ }
};
```

`getActor()` must resolve a trusted learner identity according to ISQ xAPI governance. For governed learner evidence, anonymous fallback must not silently replace failed authenticated identity.

`sendStatement()` owns endpoint selection, authorisation, validation, retry, secure transport and operational logging. The component and adapter are transport-agnostic.

## Failure behaviour

Telemetry failure must not suppress formative feedback or prevent learner progression. The adapter emits `isq:telemetry-status` with one of:

- `unavailable`
- `identity-unavailable`
- `sent`
- `failed`

Those events are operational signals. They must not be presented as learning success/failure.

Where telemetry is itself an explicit compliance evidence requirement, the course implementation must define the failure policy separately. It must not silently change the generic Knowledge Check behaviour.

## Privacy and security

The component event contains interaction evidence, not learner identity. Identity is added only inside the governed adapter/runtime boundary.

No canonical source may contain:

- raw SCORM learner data in the component event;
- LRS credentials;
- reusable Basic Auth values;
- a production LRS endpoint;
- Child Protection or other course-specific activity identifiers.

## Governance status

The event-to-statement mapping is technically defined and source-validatable, but production approval still requires stored-LRS evidence from the approved ISQ runtime/transport. Current ISQ governance also distinguishes technical pattern proof from production approval; a technically proven statement shape is not, by itself, authorisation to deploy a browser credential model.
