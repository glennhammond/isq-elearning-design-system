# Decision Point

Status: **Candidate presentation baseline**  
Version: **0.1.0**  
Interaction Shell: **0.1.0 required**

## Purpose

A Decision Point asks the learner to make a consequential judgement in context and then provides response-specific feedback. It is not interchangeable with a factual Knowledge Check even where both use native choice controls.

This record currently governs the shared presentation baseline and anatomy only. Decision Point behaviour, xAPI semantics and scenario/progression rules require their own evidence before the component can be promoted as a fully governed reusable component.

## Required visual architecture

Decision Points must consume the canonical ISQ Interaction Shell:

- `.isq-interaction`
- `.isq-interaction--decision`
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

Decision Point-specific code must not duplicate shell styling.

## Learning distinction from Knowledge Check

Use a Decision Point when the educational value lies in contextual judgement, consequences, professional reasoning or the learner's next action in a scenario.

Use a Knowledge Check when the learner is retrieving or applying knowledge against an objectively defensible correct response without scenario progression being the central learning mechanism.

## Accessibility baseline

- native radio/checkbox controls;
- semantic fieldset and legend;
- visible focus;
- text feedback rather than colour-only correctness;
- dynamic feedback announced appropriately;
- no disabled progression until a requirement genuinely warrants gating;
- progression must not strand keyboard or screen-reader users;
- mobile/touch behaviour must preserve complete option labels.

## Evidence source

The initial refined presentation was extracted from the amended `CP_Principals_2027_Visual_Component_Family_v0.1.html` prototype. The course-specific wording, legal content, learner names and scenario logic are not canonical.
