# Atanor Roadmap

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | ROADMAP                     |
| Status       | 🟢 Active                   |
| Version      | 0.5                         |
| Last Updated | 2026-08-13                  |
| Audience     | Contributors and Developers |

---

# Vision

Atanor aims to become a knowledge-driven learning platform capable of transforming examination requirements and authoritative sources into structured, traceable and adaptive learning experiences.

The initial MVP focuses on preparation for Spanish public administration competitive examinations.

The long-term vision is broader: a reusable platform for knowledge-intensive learning domains where reliable sources, structured knowledge and personalized learning are valuable.

---

# Development Strategy

Atanor follows an incremental delivery model.

Infrastructure, frameworks and supporting technologies are introduced only when they solve an existing problem.

Every meaningful milestone should produce measurable product value while keeping the repository simple, maintainable and operational.

The roadmap describes strategic direction. It does not enumerate implementation tasks or establish one-to-one correspondence with the backlog.

---

# Roadmap Principles

Development is guided by:

- Deliver working software at every meaningful milestone.
- Introduce infrastructure only when necessary.
- Prefer small, atomic and traceable changes.
- Keep the architecture adaptable.
- Prioritize product capabilities over technology adoption.
- Validate important domain assumptions before committing to implementation.
- Keep the MVP aligned with the needs of the initial examination use case.
- Let real source material drive generalization instead of designing for hypothetical formats.

---

# Product Evolution

The roadmap is organized around product capabilities rather than technologies.

The order below describes the intended evolution. The exact implementation sequence may change as domain knowledge and validation results evolve.

---

# Stage 1 · Foundation

**Status: 🟢 Completed**

## Objective

Establish the technical, organizational and development foundations of Atanor.

## Outcome

- Repository structure established.
- Development conventions defined.
- Core documentation established.
- Development workflow agreed.
- Backend foundation initialized.
- Initial application executable.

---

# Stage 2 · Application & Source Foundation

**Status: 🟢 Completed**

## Objective

Establish the minimal domain, persistence and application capabilities required to introduce authoritative source material into Atanor.

## Outcome

Atanor established a validated source workflow:

```text
PDF source
    ↓
Import
    ↓
Persist
    ↓
Retrieve / List
```

The workflow is exposed through a minimal CLI and validated with isolated automated tests.

The stage deliberately stopped before requirement extraction, knowledge construction and learning features.

---

# Stage 3 · Requirement Discovery

**Status: 🟢 Completed**

## Objective

Transform imported authoritative source material into explicit, structured requirements that can become the entry point for subsequent knowledge construction.

## Validated Capability

```text
Source
    ↓
Document Structure Detection
    ↓
Requirement Mention
    ↓
Requirement
```

Requirement discovery does not assume a universal document structure. Real samples from BOE and Junta de Castilla y León demonstrated different structural conventions, including numbered entries and `Tema` entries.

The current implementation preserves source expressions, source identifiers and document locations. Structured identifiers are treated as text rather than being assigned semantic meaning.

## Outcome

Atanor can now:

- extract text from supported PDF sources;
- identify requirement mentions using deterministic structural rules;
- preserve source provenance and location;
- persist and inspect discovered requirements;
- validate the complete workflow end to end against real source material;
- keep unsupported scanned PDFs outside the current workflow boundary.

The implementation deliberately does not claim semantic requirement resolution, universal document parsing or OCR support.

A real Ayuntamiento de León PDF without an extractable text layer remains a regression sample for the current absence of OCR support.

The architecture also remains open to future provider- or document-specific discovery strategies, but no such abstraction has been introduced without sufficient evidence.

---

# Stage 4 · Knowledge Construction

**Status: 🔵 Next**

## Objective

Build the capability to transform requirements and authoritative sources into structured, reusable knowledge.

## Intended Capabilities

- scope discovery;
- Knowledge Blueprint construction;
- knowledge assessment;
- source identification and acquisition;
- extraction of candidate knowledge;
- coverage refinement;
- depth estimation;
- provenance and evidence;
- canonical knowledge construction.

The first implementation step should validate the transition from a real persisted requirement to a justified knowledge scope before introducing the complete Blueprint model.

---

# Stage 5 · Knowledge Retrieval and Assistance

**Status: ⚪ Future**

## Objective

Make structured knowledge usable through search and AI-assisted interaction.

## Potential Capabilities

- grounded retrieval;
- source-aware answers;
- source citation;
- explanations;
- knowledge exploration;
- gap and uncertainty reporting.

AI should operate over structured and traceable knowledge rather than becoming an opaque substitute for it.

---

# Stage 6 · Learning Platform

**Status: ⚪ Future**

## Objective

Transform the knowledge model into an adaptive learning environment.

## Potential Capabilities

- learning-path generation;
- personalized study sessions;
- question generation;
- assessment;
- progress tracking;
- weakness detection;
- revision planning;
- spaced repetition.

The learning path should be derived from required knowledge, dependencies and the learner's current state.

---

# Stage 7 · Ecosystem Expansion

**Status: ⚪ Future**

## Objective

Expand Atanor beyond the initial MVP once the core product has been validated.

## Potential Capabilities

- additional examination domains;
- external integrations;
- advanced analytics;
- collaboration;
- plugin architecture;
- additional knowledge sources;
- broader learning use cases.

The exact scope should depend on product validation and user feedback.

---

# Long-Term Vision

Although the initial product targets Spanish public administration examinations, the underlying model should remain sufficiently general to support other knowledge-intensive domains.

The reusable foundation is:

```text
Source
    ↓
Requirement
    ↓
Knowledge Scope
    ↓
Evidence
    ↓
Canonical Knowledge
    ↓
Learning
```

The product should not be architected around a single examination structure when a more general domain model is justified.

---

# Living Document

This roadmap defines strategic direction.

Implementation detail belongs in the backlog and in the relevant technical documentation.

The roadmap may evolve when new evidence invalidates assumptions or when product validation changes priorities.
