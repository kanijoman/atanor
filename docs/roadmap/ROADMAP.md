# Atanor Roadmap

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | ROADMAP                     |
| Status       | 🟢 Active                   |
| Version      | 0.3                         |
| Last Updated | 2026-08-10                  |
| Audience     | Contributors and Developers |

---

# Vision

Atanor aims to become a knowledge-driven learning platform capable of transforming examination requirements and authoritative sources into structured, traceable and adaptive learning experiences.

The initial MVP focuses on preparation for Spanish General State Administration competitive examinations.

The long-term vision is broader: a reusable platform for knowledge-intensive learning domains where reliable sources, structured knowledge and personalized learning are valuable.

---

# Development Strategy

Atanor follows an incremental delivery model.

Infrastructure, frameworks and supporting technologies are introduced only when they solve an existing problem.

Every milestone should produce a measurable improvement while keeping the repository simple, maintainable and operational.

The roadmap describes strategic direction. It does not attempt to enumerate implementation tasks or establish one-to-one correspondence with the backlog.

---

# Roadmap Principles

Development is guided by:

- Deliver working software at every meaningful milestone.
- Introduce infrastructure only when necessary.
- Prefer small, atomic and traceable changes.
- Keep the architecture adaptable.
- Prioritize product capabilities over technology adoption.
- Validate important domain assumptions before committing to implementation.
- Continuously reduce technical debt.
- Keep the MVP aligned with the needs of the initial examination use case.

---

# Product Evolution

The roadmap is organized around capabilities rather than technologies.

The order below describes the intended evolution of the product. The exact implementation sequence may change as domain knowledge and validation results evolve.

---

# Stage 1 · Foundation

## Objective

Establish the technical, organizational and development foundations of Atanor.

## Outcome

- Repository structure established.
- Development conventions defined.
- Core documentation established.
- Development workflow agreed.
- Backend and frontend foundations initialized.
- Initial application executable.

---

# Stage 2 · Knowledge Foundation

## Objective

Establish the conceptual and technical foundation required to represent Atanor's knowledge domain.

## Outcome

Atanor should be able to distinguish, at a minimum:

- examination requirements;
- knowledge scope;
- candidate coverage;
- expected depth;
- knowledge entities;
- knowledge assertions;
- sources and evidence;
- relationships and dependencies.

A key goal of this stage is to validate the Knowledge Blueprint concept before committing to a detailed persistence model.

---

# Stage 3 · Knowledge Construction

## Objective

Build the capability to transform requirements and sources into structured knowledge.

## Outcome

Atanor should progressively support:

- requirement analysis;
- scope discovery;
- source identification;
- extraction of candidate knowledge;
- coverage refinement;
- depth estimation;
- provenance and evidence;
- canonical knowledge construction.

Public and freely accessible sources and user-provided documents must be sufficient to construct the knowledge base. Commercial material may be used only when explicitly provided by the user.

---

# Stage 4 · Knowledge Retrieval and Assistance

## Objective

Make structured knowledge usable through search and AI-assisted interaction.

## Potential capabilities

- grounded retrieval;
- source-aware answers;
- source citation;
- explanations;
- knowledge exploration;
- gap and uncertainty reporting.

AI should operate over structured and traceable knowledge rather than becoming an opaque substitute for it.

---

# Stage 5 · Learning Platform

## Objective

Transform the knowledge model into an adaptive learning environment.

## Potential capabilities

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

# Stage 6 · Ecosystem Expansion

## Objective

Expand Atanor beyond the initial MVP once the core product has been validated.

## Potential capabilities

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
Requirements
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
