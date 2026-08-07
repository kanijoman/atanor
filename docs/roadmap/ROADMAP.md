# Atanor Roadmap

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | ROADMAP                     |
| Status       | 🟢 Active                   |
| Version      | 0.2                         |
| Last Updated | 2026-08-07                  |
| Audience     | Contributors and Developers |

---

# Vision

Atanor aims to become an AI-powered knowledge platform capable of managing, organizing and retrieving structured knowledge while maintaining complete traceability to authoritative sources.

The initial MVP focuses on the preparation of Spanish General State Administration competitive examinations. However, the long-term vision is to evolve into a general-purpose knowledge platform that can be adapted to different domains requiring reliable knowledge management and AI-assisted learning.

---

# Development Strategy

Atanor follows an incremental delivery model.

Infrastructure, frameworks and supporting technologies are introduced only when they solve an existing problem. This **Just Enough Infrastructure** approach minimizes unnecessary complexity, reduces technical debt and allows the architecture to evolve naturally as new requirements emerge.

Every sprint should produce a measurable improvement to the project while keeping the repository simple, maintainable and fully operational.

---

# Roadmap Principles

Development is guided by the following principles:

* Deliver working software at every milestone.
* Introduce infrastructure only when necessary.
* Prefer small, atomic and traceable changes.
* Keep the architecture adaptable.
* Prioritize business capabilities over technology adoption.
* Continuously reduce technical debt instead of accumulating it.

---

# Product Evolution

The roadmap is organized around product capabilities rather than specific technologies.

Each milestone should deliver a complete and demonstrable improvement to the platform.

---

# Sprint 1 · Foundation

## Objective

Establish the technical and organizational foundations of the project.

## Expected Outcome

* Repository structure established.
* Development conventions defined.
* Project documentation created.
* Development workflow agreed.
* Backend and frontend projects initialized.
* Architecture prepared for future implementation.

---

# Sprint 2 · First Running System

## Objective

Deliver the first executable version of Atanor.

## Expected Outcome

* Backend application running.
* Frontend application running.
* Basic communication between frontend and backend.
* Health endpoint available.
* Local development environment operational.

This milestone establishes the first complete vertical slice of the application.

---

# Sprint 3 · Knowledge Core

## Objective

Implement the core domain model and document management capabilities.

## Expected Outcome

* Document storage.
* Document import pipeline.
* Knowledge organization.
* Source traceability.
* Initial persistence layer.
* First searchable knowledge base.

At the end of this sprint, Atanor should be capable of managing official documentation as structured knowledge.

---

# Sprint 4 · AI Assistant

## Objective

Enable AI-assisted interaction with the knowledge base.

## Expected Outcome

* Retrieval-Augmented Generation (RAG).
* Grounded question answering.
* Source citation.
* Context-aware conversations.
* AI-assisted explanations.

The assistant must always provide verifiable answers grounded in official documentation.

---

# Sprint 5 · Learning Platform

## Objective

Transform the knowledge base into an active learning environment.

## Expected Outcome

* Personalized study sessions.
* Quiz generation.
* Progress tracking.
* Learning analytics.
* Revision planning.
* Spaced repetition.

At this stage, Atanor becomes a complete study platform rather than a document repository.

---

# Sprint 6 · Ecosystem Expansion

## Objective

Expand the platform beyond the initial MVP.

## Potential Capabilities

* Additional examination domains.
* Plugin architecture.
* Knowledge graph extensions.
* Advanced analytics.
* Collaboration features.
* External integrations.

The exact scope of this sprint will depend on user feedback and the evolution of the MVP.

---

# Long-Term Vision

Although the first release targets Spanish public administration examinations, the architecture is intentionally domain-independent.

Future versions should support any knowledge-intensive domain requiring:

* Structured documentation.
* Source traceability.
* AI-assisted retrieval.
* Knowledge management.
* Personalized learning.

The objective is to build a reusable knowledge platform rather than a solution limited to a single use case.

---

# Living Document

This roadmap defines the strategic direction of the project.

Specific implementation details are maintained in the project backlog and may evolve throughout development.

Architectural decisions are documented independently and may change provided they remain aligned with the goals and principles described in this roadmap.
