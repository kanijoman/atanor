# Architecture

# Document Information

| Field               | Value                       |
| ------------------- | --------------------------- |
| Project             | Atanor                      |
| Document            | ARCHITECTURE                |
| Status              | 🟢 Active                   |
| Version             | 0.3                         |
| Last Updated        | 2026-08-10                  |
| Audience            | Contributors and Developers |
| Architecture Status | 🟡 Evolving                 |

---

# Purpose

This document defines the architectural principles and currently validated architectural direction of Atanor.

It intentionally avoids describing speculative implementation details or prematurely committing the project to frameworks, infrastructure or persistence technologies.

The architecture must evolve from the validated domain model.

Detailed implementation choices belong in the source code and Architecture Decision Records (ADR).

---

# Architectural Vision

Atanor is designed as a knowledge platform rather than a collection of independent features.

Its architecture must support the transformation of learning requirements and evidence into structured, traceable and reusable knowledge, and eventually into adaptive learning experiences.

The current conceptual flow is:

```text
Requirement
    ↓
Scope Discovery
    ↓
Knowledge Blueprint
    ↓
Canonical Knowledge
    ↓
Learning Path
```

This flow represents the current domain direction, not a finalized implementation architecture.

Business requirements and validated domain concepts drive architectural decisions—not frameworks, libraries or infrastructure.

---

# Architectural Principles

## Domain First

The domain model is the primary driver of the architecture.

Technical choices must support the domain rather than shape it.

The conceptual model must therefore be validated before selecting a persistence strategy or introducing application structures around it.

---

## Knowledge and Curriculum Are Distinct

Atanor must distinguish between:

- the knowledge that exists in the canonical knowledge model;
- the requirements imposed by a particular curriculum or examination;
- the scope of knowledge considered relevant to those requirements.

The same knowledge may be reused by multiple curricula.

A curriculum should therefore select and contextualize knowledge rather than own it.

---

## Scope Before Knowledge

A requirement does not necessarily define the complete knowledge that must be learned.

Atanor needs an intermediate scope-definition process capable of determining, with explicit evidence and confidence:

- candidate coverage;
- expected depth;
- relevant sources;
- curricular evidence;
- unresolved uncertainty.

The resulting Knowledge Blueprint is a conceptual boundary between a requirement and the canonical knowledge model.

This is a validated domain direction, but its final representation and persistence model remain open.

---

## Evidence and Provenance

The architecture must preserve the distinction between knowledge and the evidence supporting it.

Atanor should be able to distinguish, at least conceptually:

- authoritative source material;
- user-provided material;
- curricular evidence;
- inferred or proposed scope;
- unresolved information.

A source establishing that something should be learned does not necessarily need to be the source that best explains the knowledge.

The architecture should therefore allow multiple kinds of evidence and sources to participate without conflating their roles.

---

## Explicit Uncertainty

Atanor must not silently turn inference into fact.

The system should be able to represent that a conclusion is:

- directly supported;
- inferred from multiple sources;
- provided by the user;
- insufficiently supported;
- unknown.

This is especially important when determining coverage and expected depth from requirements that do not specify them explicitly.

---

## Incremental Evolution

Architecture grows together with the product.

New components are introduced only when they solve a real business or technical requirement.

Important domain assumptions should be validated through small experiments before becoming architectural commitments.

---

## Just Enough Architecture

The project avoids speculative design.

Architectural complexity should appear only when justified by the current stage of development.

In particular, the emerging Knowledge Blueprint and canonical knowledge model should not be translated prematurely into a large set of technical abstractions.

---

## Simplicity

Whenever multiple valid solutions exist, prefer the simplest one that satisfies the current requirements.

Avoid unnecessary abstractions and premature optimization.

Simplicity must not, however, erase important domain distinctions such as:

```text
Requirement ≠ Source ≠ Knowledge ≠ Evidence
```

---

## Low Coupling

System components should communicate through well-defined interfaces.

Implementation details should remain isolated whenever possible.

The knowledge domain should not become tightly coupled to a particular storage engine, AI provider or external source.

---

## High Cohesion

Each module should have a single, clearly defined responsibility.

Related functionality should remain together.

Boundaries should emerge from validated domain responsibilities rather than from technical fashion.

---

## Reversible Decisions

Architectural decisions should remain reversible whenever practical.

Replacing a framework or technology should require minimal impact on the rest of the system.

Domain concepts should not depend unnecessarily on infrastructure-specific representations.

---

# Current Architectural Direction

The current project stage has established the following conceptual direction:

```text
Learning / Examination Requirement
                ↓
         Scope Discovery
                ↓
       Knowledge Blueprint
                ↓
       Canonical Knowledge
                ↓
        Learning Experience
```

The Knowledge Blueprint is expected to capture, conceptually:

```text
Knowledge Scope
├── Coverage
├── Expected Depth
├── Evidence
├── Provenance
└── Confidence
```

Canonical knowledge is expected to be reusable across different requirements and curricula.

The exact structure of knowledge entities, assertions, relationships and dependencies is still being validated and is therefore not yet a finalized architectural contract.

---

# Current Architecture

At the current stage of the project, the following architectural decisions have been made:

* The repository is organized as a monorepo.
* Backend and frontend evolve independently.
* Project documentation is maintained alongside the source code.
* Architecture evolves incrementally.
* Infrastructure is introduced only when required.
* Technology decisions are documented separately.
* Significant architectural changes are recorded through ADRs.
* Domain modeling precedes persistence design.
* The conceptual distinction between requirements, scope, knowledge and evidence is part of the current architectural direction.

The internal application architecture is not yet finalized.

It will emerge from the validated domain model and the first functional capabilities.

---

# Deferred Decisions

The following architectural decisions remain intentionally deferred until sufficient evidence exists:

* Exact internal application structure.
* Module boundaries.
* Final Knowledge Blueprint representation.
* Exact canonical knowledge model.
* Persistence architecture and database technology.
* Retrieval architecture.
* AI integration strategy.
* Authentication.
* Deployment model.
* Scalability strategy.
* Observability.

In particular, persistence must not be selected merely because a relational model is familiar or because an earlier document hierarchy suggested one.

The persistence model should follow the validated domain model.

Deferring these decisions reduces unnecessary complexity and preserves architectural flexibility.

---

# Architecture Decision Records

Significant architectural decisions should be documented through Architecture Decision Records (ADR).

Each ADR should answer, at minimum:

* What decision was made?
* What problem does it solve?
* Which alternatives were considered?
* Why was this solution selected?
* What are the expected consequences?
* Which assumptions support the decision?

ADRs complement this document by preserving the historical context behind architectural evolution without turning this document into a detailed project journal.

---

# Architecture Evolution

Architecture is expected to evolve continuously throughout the project's lifetime.

This document should remain concise and stable.

Implementation details belong in the codebase.

Validated architectural decisions should be reflected here, while significant decisions and their historical reasoning should be recorded through ADRs.

Unvalidated hypotheses should remain explicitly identified as such until experiments or implementation provide sufficient evidence.
