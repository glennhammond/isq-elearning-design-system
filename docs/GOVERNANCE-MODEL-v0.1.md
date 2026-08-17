# ISQ Learning governance model v0.1

Status: proposal

This document proposes a multidimensional governance model for ISQ Learning 2027. It avoids forcing architecture, readiness, reuse, support and proof into one status label.

## Entity type: What is it?

Entity type describes the role an item plays in the system:

- **Foundation** — a base design decision or API, such as tokens, typography or spacing.
- **Primitive** — a small reusable building block used to compose larger entities.
- **Component** — a reusable interface unit with a defined contract.
- **Recipe** — a purposeful composition of existing foundations, primitives or components.
- **Learning-design purpose** — the learning need or instructional intent being served.
- **Structural pattern** — a repeatable arrangement that organises learning content or flow.
- **Learning expression** — an ISQ-specific expression of learning intent through structure, content and components.
- **Platform implementation** — a platform-bound implementation of another entity or purpose.
- **Legacy treatment** — an existing treatment retained for compatibility but not intended for new work.

An entity has one primary type. Secondary classifications may be recorded where needed, but they must not obscure the primary role.

## Maturity: How ready and trusted is it?

- **Experimental** — exploratory and expected to change; wider reuse is not yet recommended.
- **Candidate** — proposed for broader use but still requires validation or consolidation.
- **Validated** — supported by sufficient implementation and evidence for its stated scope.
- **Approved** — accepted as part of the governed system for its stated scope.

Maturity does not imply reuse scope or support state. `Core` and `Stable` are not maturity states in this model.

## Reuse scope: Where may it be reused?

- **ISQ-wide** — intended for use across ISQ Learning products and platforms.
- **Platform** — reusable within a specific delivery platform.
- **Course-family** — reusable within a related family of courses.
- **Course-specific** — limited to one course context unless later reassessed.

## Support state: What lifecycle support does it receive?

- **Active** — maintained and available within its stated maturity and reuse scope.
- **Legacy** — retained for existing material but not developed for new work.
- **Deprecated** — scheduled for replacement or removal; new use is discouraged.
- **Retired** — no longer supported or available for use.

## Proof metadata

Implementation state and evidence state are supporting proof metadata, not primary user-facing status labels.

Implementation state describes whether an entity is specified, partially implemented, implemented or production-verified. Evidence state describes whether support is inferred, documented, tested or audited. These dimensions help reviewers understand why a maturity decision was made without conflating implementation presence with approval.

## Current-site transition

The existing site status field remains unchanged until a later migration. During the reconciliation phase, the non-rendering manifest records proposed governance values alongside the current source status. No proposed value changes visible catalogue labels, navigation, URLs or rendered documentation.

## Decision principles

- Record each governance dimension independently.
- Require the reuse scope to match the available evidence.
- Treat a course-specific implementation as evidence, not automatic proof of a generic component.
- Distinguish a learning purpose or expression from the component or recipe used to realise it.
- Preserve unresolved architecture choices explicitly until reviewed.
- Change visible catalogue status only through a separately approved migration.
