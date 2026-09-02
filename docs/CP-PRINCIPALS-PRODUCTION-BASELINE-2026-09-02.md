# CP for Principals 2027 — production baseline

Date frozen: **2 September 2026**  
Purpose: prevent Custom Block Library qualification work from blocking design/development of the Child Protection for Principals and Board Directors course.

## 1. Styling authority

Use the current immutable ISQ Rise production stylesheet:

```html
<link rel="stylesheet" type="text/css" href="https://xapistorage28032026.blob.core.windows.net/xapitestcourses/css/isq-rise-components-v1.0.0.css" />
```

**Authority:** `isq-rise-components-v1.0.0.css`.

Do not fork local CSS into individual course blocks where an existing design-system class already provides the required presentation or state. New CSS should enter the shared design-system process rather than becoming CP-specific styling unless the requirement is genuinely course-specific.

## 2. Component authority

### Approved existing design-system patterns

Components already recorded as approved/core/foundation in the ISQ eLearning Design System remain available for production use within their documented constraints. Their catalogue records and production CSS remain the authority.

Examples already present in the governed catalogue include Panel, Button, Callout, Meta tags, Card grid, Accordion and Tabs. Course use should follow the catalogue's stated appropriate/inappropriate use and accessibility requirements.

### Knowledge Check family

Current governed family:

- family: `isq-kc`
- Single: `isq-kc-single`
- Sequence: `isq-kc-sequence`
- current version: **0.2.0 Candidate**
- target: **1.0.0 Approved**

Qualification status at baseline freeze:

- Single-choice learner interaction: PASS
- Multiple-response learner interaction: PASS functionally
- Sequence learner interaction: PASS functionally
- repeated-instance/collision test: PASS functionally
- no-xAPI mode: PASS functionally
- Single-choice Rise → SCORM 2004 → Veracity xAPI: **PASS end to end**
- Single-choice incorrect + correct retry stored as separate Veracity statements: **PASS**
- multiple-response stored-LRS qualification: pending
- keyboard/screen-reader/mobile/zoom formal qualification: pending
- stakeholder/governance release review: pending

**Production decision for CP for Principals:** the outstanding Knowledge Check 1.0 release gate must not block course structure, visual design or use of unrelated approved components. Where a Knowledge Check is required before 1.0 approval, retain it as a controlled implementation candidate and avoid treating it as a final immutable release asset until the remaining gate closes.

## 3. xAPI architecture authority

The technically proven controlled path is:

```text
Rise custom-code iframe
  → interaction controller
  → neutral component event
  → xAPI adapter
  → trusted SCORM 2004 learner resolution
  → controlled transport
  → Veracity
```

Important Rise constraint: separate custom-code blocks run in separate iframe documents. Ordinary DOM `CustomEvent` communication does not cross those iframe boundaries. An xAPI-enabled component therefore needs its controller, adapter and runtime available within the same iframe, either bundled/inlined or loaded as governed scripts into that iframe.

Canonical reusable components must not contain production LRS credentials.

## 4. Media asset authority

The current eLearning Design System repository does **not** contain a governed reusable course-media asset pack equivalent to the component/CSS library. Its `assets/` directory currently serves reference-site CSS, JavaScript and icons rather than an authoritative CP course-media library.

Therefore for CP for Principals:

- course-specific photography, video, illustration and legal/source media remain course/source assets;
- do not assume Child Protection for Teachers imagery is automatically canonical for Principals;
- reuse only assets whose rights, accessibility treatment, crop/quality and instructional purpose remain appropriate;
- follow the ISQ imagery guidance/taxonomy for new selections;
- keep course media references separate from reusable component code;
- any genuinely reusable ISQ media asset library should be established as a separate governed workstream rather than improvised inside this component release.

## 5. What can proceed immediately in CP for Principals

The following work is unblocked by the Custom Block Library release gate:

- Rise course architecture and section build;
- approved course copy implementation;
- hero/header and general visual treatment;
- typography, colour, spacing and panel/layout work using the production stylesheet;
- approved/core/foundation catalogue components;
- image selection and media preparation under the ISQ imagery guidance;
- accessibility-first content structure;
- scenario/content presentation that does not depend on an unapproved custom interaction;
- xAPI activity-ID planning and context hierarchy.

## 6. What remains controlled

Do not represent the following as fully approved until the relevant gate closes:

- Knowledge Check `1.0.0` release;
- multiple-response xAPI production qualification;
- production-secure xAPI transport/authentication model;
- any new component family extracted from Child Protection;
- a canonical reusable ISQ course-media asset pack.

## Baseline decision

**CP for Principals design/development should proceed now.**

The Custom Block Library is a supporting platform workstream, not a prerequisite for completing the course. Future approved component releases can replace controlled candidates without reopening the course's visual/design-system foundation.
