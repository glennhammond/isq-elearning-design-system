# ISQ Learning 2027 reconciliation

`data/reconciliation-manifest.json` is a non-rendering evidence and governance layer between the current catalogue and the proposed ISQ Learning 2027 architecture. It represents every current source record: **23 components** from `data/components.json` and **12 learning patterns** from `data/patterns.json`.

The manifest does not drive the generator or site. It does not change rendered HTML, navigation, URLs, source records, visible status labels, CSS, production assets or deployment.

## Reconciliation model

The model keeps six dimensions separate:

- **Entity type** identifies what an item is: foundation, primitive, component, recipe, learning-design purpose, structural pattern, learning expression, platform implementation or legacy treatment.
- **Maturity** records confidence and readiness: Experimental, Candidate, Validated or Approved.
- **Reuse scope** identifies the intended boundary of reuse: ISQ-wide, Platform, Course-family or Course-specific.
- **Support state** records lifecycle support: Active, Legacy, Deprecated or Retired.
- **Implementation state** records how completely the proposal is implemented.
- **Evidence state** records the strength of supporting proof.

Implementation state and evidence state are proof metadata. They support governance decisions but are not primary user-facing status labels. The existing site status field remains unchanged until a later migration.

Each reconciliation record preserves its current catalogue identity and status, proposes values across these dimensions, describes its ISQ role and Rise implementation, records production evidence, and identifies discrepancies or unresolved decisions.

## Approved decisions

- Key Message is a recipe composed from Callout and typography, not an independent UI component.
- Legislation Panel is a learning expression and recipe built primarily from Split Card and typography, not an independent canonical component.
- Generic Tabs remains Candidate and Partial until extracted and independently validated. Harm Tabs remains a Course-specific, Validated platform implementation and evidence for future generic Tabs.
- Role Split remains Candidate. A shared implementation exists, but audited production comparisons currently bypass it.
- Self-assessment remains a Course-specific, Candidate platform implementation and is not promoted to canonical component status.
- Course Feedback remains Experimental while data handling, privacy, storage and submission behaviour are unresolved.
- Divider remains Experimental and requires variant rationalisation.
- Editorial Reflection remains a legacy treatment and must not be developed for new work.
- Card Grid remains a single record while the possible separation of Grid as a layout primitive and Card as an independent component is unresolved.
- Footer Band remains unchanged while its overlap with generic `.isq-band` primitives is unresolved.

## Learning Patterns future classification

The current Learning Patterns page and URLs remain unchanged. The manifest records provisional future primary roles only:

- Structural patterns: Section opener, Scenario stage, Process, Comparison and Section summary.
- Learning-design purposes: Explanation, Key message, Feedback, Reflection and Resource.
- Learning expressions: Legislation or authority and Decision point.

Records may include secondary classifications where a single role does not express the full relationship.

## Rise Design System v1.0 target

The manifest records a non-rendering consolidation objective for Panel, Button, Callout, Accordion, Video Frame, Section Opener, Split Card, Resource Card, Process, Scenario Stage and Decision Point. Meta Tags and existing production foundation APIs requiring formal documentation support that target. Tabs, Role Split, Card / Grid and Footer Band / generic Band remain in the candidate queue.

The target set does not claim that every listed item is already production-approved.

## Remaining work

Future governance work includes resolving Card / Grid and Footer Band / generic Band architecture, extracting and validating generic Tabs, reconciling Role Split with production comparisons, documenting foundation APIs, and resolving the Course Feedback data path. Older audit prose also retains earlier 21/11 release counts and should be reconciled later against the current 23/12 source counts.
