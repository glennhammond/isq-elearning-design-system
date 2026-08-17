# 0001: ISQ Learning system boundary

- Status: Accepted
- Date: 2026-08-17

## Context

ISQ Learning 2027 requires documentation and repository architecture that can be understood, governed and maintained on their own terms. References to external systems, methodology provenance or intellectual-property relationships create dependencies that are outside the purpose of this repository.

## Decision

ISQ Learning 2027 documentation is self-contained.

This repository defines only ISQ principles, learning purposes, learning expressions, structures, components, implementations, evidence, production standards and governance. It must not document external methodology or intellectual-property provenance.

Relationships to external systems are managed outside this repository. They are not represented through documentation fields, identifiers, architecture layers or cross-references here.

## Consequences

- Readers can interpret the ISQ Learning system without access to external documentation.
- Reconciliation records and governance documents use only ISQ-defined concepts and identifiers.
- External-system relationships require a separate, externally managed record if they are needed.
- Repository validation must reject boundary-specific fields and terminology that do not belong to the ISQ-only model.
