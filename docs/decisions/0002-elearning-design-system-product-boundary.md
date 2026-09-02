# ADR 0002: eLearning Design System product boundary

- **Status:** Accepted
- **Date:** 3 September 2026
- **Decision owner:** Glenn Hammond

## Context

The current governed reference implementation is named the ISQ eLearning Design System, while two older repositories also use variants of the broader eLearning Design System name. The work now encompasses more than an ISQ-branded catalogue: it includes learning-design principles, experience patterns, course composition, accessibility, platform guidance, reusable custom components, xAPI governance and quality assurance.

ISQ remains the first substantial implementation and evidence base. It should not define the boundary of the complete product.

## Decision

The canonical product is the **eLearning Design System**.

The system will contain a reusable core and explicit implementation layers:

1. principles and learning-design frameworks;
2. foundations and design tokens;
3. components and interaction states;
4. course-composition patterns;
5. media and imagery guidance;
6. accessibility and quality requirements;
7. platform implementations, including Rise, Storyline, Moodle and standalone web;
8. telemetry and xAPI governance;
9. branded themes, beginning with ISQ;
10. course applications and production evidence.

ISQ is a branded theme, implementation and course-application context within the eLearning Design System. Existing `.isq-` CSS classes, ISQ tokens, approved visual treatments and ISQ-specific documentation remain valid within that implementation layer.

## Authority boundaries

- Approved course documents remain the authority for controlled learner-facing copy.
- Figma will provide the visual and course-composition design authority.
- Governed source code and structured system data will provide the implementation authority.
- Published Rise, LMS and LRS testing will provide runtime evidence.
- A Figma prototype does not establish accessible or production-ready behaviour by itself.
- Course-specific legislation, policy, learner data, identifiers and credentials do not belong in reusable core components.

## Repository consequence

The current `glennhammond/isq-elearning-design-system` repository is the strongest technical baseline and will become the canonical eLearning Design System repository after consolidation.

The repository will not be renamed until:

- active custom-block pull requests have reached their appropriate review gates;
- useful legacy material has been classified and preserved;
- the existing `glennhammond/eLearning-design-system` name has been freed safely;
- GitHub-to-Vercel integration and deployment aliases have a verified migration plan.

## Design consequence

The system can remain comprehensive and unified without making every component brand-specific. Core anatomy and behaviour may support multiple themes, while the ISQ implementation retains the styling, content constraints and platform decisions required for ISQ work.
