# Learning Design model v0.1

`data/learning-design.json` is a parallel, non-rendering model for the future Learning Design catalogue. It conservatively transforms the 12 current records in `data/patterns.json` while leaving the existing Learning Patterns page, source data and URLs unchanged.

## Classification

The model classifies the records by their primary role:

- **5 learning-design purposes** describe the support, understanding, practice or transfer the learner needs: Explain a concept, Key message, Explanatory feedback, Reflection and Contextualise a resource.
- **5 experience structures** describe how learning is organised, sequenced, grouped or given flow: Section opener, Scenario stage, Ordered sequence, Comparison structure and Section summary.
- **2 learning expressions** describe established ISQ combinations of content, interaction and quality characteristics: Legislation or authority and Professional decision point.

These types are deliberately distinct. A purpose states why learning support is needed, a structure organises an experience, and an expression defines the essential characteristics of a recognised ISQ treatment.

## Implementations and compatibility

Implementation relationships point from a Learning Design record to a component, recipe, native capability or platform implementation. They describe possible ways to realise the intent; an implementation does not define or own the Learning Design record. Component references are validated against `data/components.json`, while platform guidance remains secondary.

Every record preserves its current pattern ID in both `id` and `legacy.sourceId`. Its compatibility URL remains `/patterns/index.html#<id>`. The parallel model complements the reconciliation manifest by providing the approved future 5/5/2 classification in a purpose-built record shape; it does not replace or drive the reconciliation manifest.

## Migration boundary

This version does not drive the generator or site because Phase 1 establishes and validates the information model before any visible migration. `data/patterns.json` remains the rendering source, so navigation, search, templates, generated HTML and existing `/patterns/` behavior remain unchanged.

The next migration phase can define how the approved model drives rendered Learning Design views, navigation and search while maintaining compatibility for existing pattern links.
