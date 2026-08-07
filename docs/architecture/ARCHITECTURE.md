# Architecture

# Document Information

| Field               | Value                       |
| ------------------- | --------------------------- |
| Project             | Atanor                      |
| Document            | ARCHITECTURE                |
| Status              | 🟢 Active                   |
| Version             | 0.2                         |
| Last Updated        | 2026-08-07                  |
| Audience            | Contributors and Developers |
| Architecture Status | 🟡 Evolving                 |

---

# Purpose

This document defines the architectural principles that guide the evolution of Atanor.

It intentionally avoids describing speculative designs or future components. Instead, it records the architectural decisions that influence the project at its current stage.

Detailed implementation choices belong to the source code and Architecture Decision Records (ADR).

---

# Architectural Vision

Atanor is designed as a knowledge platform rather than a collection of independent features.

The architecture is expected to evolve together with the domain while preserving a stable set of guiding principles.

Business requirements drive architectural decisions—not frameworks, libraries or infrastructure.

---

# Architectural Principles

## Domain First

The domain model is the primary driver of the architecture.

Technical choices must support the domain rather than shape it.

---

## Incremental Evolution

Architecture grows together with the product.

New components are introduced only when they solve a real business or technical requirement.

---

## Just Enough Architecture

The project avoids speculative design.

Architectural complexity should appear only when justified by the current stage of development.

---

## Simplicity

Whenever multiple valid solutions exist, prefer the simplest one that satisfies the current requirements.

Avoid unnecessary abstractions and premature optimization.

---

## Low Coupling

System components should communicate through well-defined interfaces.

Implementation details should remain isolated whenever possible.

---

## High Cohesion

Each module should have a single, clearly defined responsibility.

Related functionality should remain together.

---

## Reversible Decisions

Architectural decisions should remain reversible whenever practical.

Replacing a framework or technology should require minimal impact on the rest of the system.

---

# Current Architecture

At the current stage of the project, only the following architectural decisions have been made:

* The repository is organized as a monorepo.
* Backend and frontend evolve independently.
* Project documentation is maintained alongside the source code.
* Architecture evolves incrementally.
* Infrastructure is introduced only when required.
* Technology decisions are documented separately.
* Significant architectural changes are recorded through ADRs.

No internal application architecture has been defined yet.

It will emerge as the first functional components of the system are implemented.

---

# Deferred Decisions

The following architectural decisions have intentionally been deferred until they become necessary:

* Internal application structure.
* Module boundaries.
* Persistence architecture.
* Authentication.
* AI integration.
* Retrieval architecture.
* Deployment model.
* Scalability strategy.
* Observability.

Deferring these decisions reduces unnecessary complexity and allows the architecture to remain aligned with the evolving product.

---

# Architecture Decision Records

Significant architectural decisions should be documented through Architecture Decision Records (ADR).

Each ADR should answer, at minimum:

* What decision was made?
* What problem does it solve?
* Which alternatives were considered?
* Why was this solution selected?
* What are the expected consequences?

ADRs complement this document by preserving the historical context behind architectural evolution without changing its guiding principles.

---

# Architecture Evolution

Architecture is expected to evolve continuously throughout the project's lifetime.

This document should remain concise and stable.

Implementation details belong in the codebase, while significant architectural changes should be reflected through ADRs rather than by continuously rewriting this document.
