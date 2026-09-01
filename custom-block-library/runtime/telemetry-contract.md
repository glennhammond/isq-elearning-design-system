# ISQ Custom Block Telemetry Contract

Status: Candidate  
Contract version: 0.1.0

## Purpose

This contract separates learner interaction behaviour from xAPI transport. A component emits a neutral browser event. An ISQ xAPI adapter, when present in the same runtime context, translates that event into governed xAPI statements.

The component must not contain production LRS credentials or assume a particular course identifier.

## Knowledge Check event

Event name:

```text
isq:knowledge-check-answered
```

The event is dispatched from the component root using `CustomEvent` with `bubbles: true`.

Minimum `detail` payload:

```json
{
  "contractVersion": "0.1.0",
  "component": "isq-kc-single",
  "componentVersion": "0.1.0",
  "questionKey": "workplace-priority",
  "activityId": "https://example.isq.qld.edu.au/xapi/course/activity/question",
  "parentActivityId": "https://example.isq.qld.edu.au/xapi/course/activity",
  "groupingActivityId": "https://example.isq.qld.edu.au/xapi/course",
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

## xAPI mapping

The governed adapter should normally map a valid formative submission as follows:

- verb: `http://adlnet.gov/expapi/verbs/answered`
- object type: `http://adlnet.gov/expapi/activities/cmi.interaction`
- interaction type: supplied by the component contract
- object/activity ID: `activityId`
- result.response: serialised response identifier(s) according to xAPI interaction rules
- result.success: `success`
- result.completion: `true`
- result.score: optional only where the governance profile requires it
- result extension: attempt number where required by the ISQ profile
- context parent: `parentActivityId`
- context grouping: `groupingActivityId`

The adapter, not the component, owns actor resolution, registration handling, endpoint/authentication and network retry behaviour.

## Required configuration

For telemetry-enabled use, the course implementation supplies stable identifiers through data attributes or an adapter configuration layer. Canonical examples use placeholder ISQ-domain identifiers only.

A production implementation must not ship placeholder identifiers.

## Failure behaviour

Telemetry failure must not suppress learner feedback or prevent progression in a formative Knowledge Check. The adapter may log or queue a failure according to ISQ xAPI governance, but the component's interaction behaviour remains available.

Where telemetry is an explicit compliance/evidence requirement, the course-level design must define the failure state separately rather than altering the generic component contract silently.

## Privacy

The event contains interaction evidence only. It must not include learner identity, email address, raw SCORM learner data or LRS credentials. Those concerns belong to the governed telemetry adapter.
