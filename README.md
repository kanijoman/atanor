# Atanor

# Document Information

| Field        | Value                |
| ------------ | -------------------- |
| Project      | Atanor               |
| Document     | README               |
| Status       | 🟢 Active            |
| Version      | 0.6                  |
| Last Updated | 2026-08-14           |
| Audience     | Users and Developers |

> **A knowledge-driven platform for public service examination preparation.**

Atanor is an open-source platform designed to transform examination requirements and authoritative sources into structured, traceable and reusable knowledge that can support effective learning.

The first MVP focuses on Spanish public administration examinations. The underlying model is intentionally broader so that validated knowledge can eventually be reused across different examinations and other knowledge-intensive learning domains.

---

# Product Direction

Atanor aims to solve a problem traditionally addressed by preparation services: turning an official examination requirement into a justified knowledge scope and, eventually, an effective learning journey.

The current validated product direction starts with a narrower promise: **a user provides a supported convocatoria and Atanor determines what the user needs to study without requiring the user to validate Atanor's discovery or resolution decisions.**

The current validated flow is:

```text
Convocatoria
    ↓
Source
    ↓
Requirement Discovery
    ↓
Automatic Resolution
    ↓
User-Oriented Study Requirements
```

This is the first product-oriented vertical slice. The next step is to expose this result through a minimal application interface and validate whether it is genuinely useful to a real user.

The broader knowledge and learning model remains a direction rather than a fixed implementation sequence.

---

# Current Status

The foundation, source workflow, requirement discovery, requirement resolution and user-oriented requirement projection are complete through **AT-040**.

Atanor currently has a validated application workflow for supported PDF sources:

```text
PDF source
    ↓
Import
    ↓
Persist
    ↓
Text extraction
    ↓
Structured requirement discovery
    ↓
Automatic resolution
    ↓
User-oriented study requirements
```

The workflow is covered by automated tests and has been exercised with real PDF samples from different sources, including BOE and Junta de Castilla y León documents.

The discovery implementation is intentionally deterministic and structure-aware. It does not claim to be a universal parser, semantic requirement resolver or OCR system. A scanned PDF sample from Ayuntamiento de León is retained as a regression case for the current absence of OCR support.

AT-041 is the next step: expose the current result through the smallest meaningful application interface so that product value can be evaluated directly rather than only through automated tests.

---

# Current Domain Model

Atanor currently distinguishes:

- **Requirement** — the requirement represented in the application domain;
- **Requirement Scope** — the contextual knowledge coverage required by a requirement in a specific examination context;
- **Knowledge Need** — a unit of knowledge coverage required by a scope, independently of whether corresponding knowledge already exists;
- **Knowledge** — reusable knowledge that may satisfy one or more needs;
- **Coverage** — the result of comparing a knowledge need with available knowledge.

The initial coverage model is intentionally limited to:

```text
COVERED
MISSING
```

A need may therefore exist without available knowledge. Richer states such as partial coverage or semantic matching remain future possibilities and are not assumed by the current model.

The `StudyRequirementSet` introduced at the application layer is deliberately a product-oriented output rather than a new domain entity. It currently reuses `Requirement` directly.

---

# Project Principles

Atanor is developed around a small set of core principles:

* **Product validation drives development.**
* **Technical decisions must support a concrete user need, product capability or demonstrated engineering risk.**
* **Architecture enables product evolution; it does not dictate the roadmap.**
* **Requirements, scopes, needs and knowledge are distinct concepts.**
* **Canonical knowledge must remain reusable independently of a curriculum.**
* **Important knowledge claims should remain traceable to supporting evidence.**
* **Artificial Intelligence is a tool, not the product itself.**
* **Maintainability takes precedence over unnecessary complexity.**
* **Infrastructure is introduced only when it solves an existing problem.**
* **Development is iterative, incremental and pragmatic.**

Technical quality remains fundamental: product-driven development does not mean accepting fragile or unmaintainable implementations. The goal is to build the minimum sound technical foundation needed to validate and evolve the product safely.

---

# Technology

The currently adopted backend stack is:

* Python 3.14
* uv
* FastAPI
* Pydantic
* Pydantic Settings
* Uvicorn
* SQLAlchemy
* Alembic
* SQLite

The project deliberately has no mandatory paid dependency and no requirement for Docker, PostgreSQL, vector databases, graph databases, external AI services or crawling infrastructure at this stage.

Technology decisions remain subordinate to validated product requirements.

---

# Documentation

The main project documentation can be found under the `docs/` directory.

| Document | Description |
|---|---|
| **FOUNDATIONS.md** | Product mission, vision and foundational principles. |
| **ROADMAP.md** | Strategic product evolution and major development stages. |
| **BACKLOG.md** | Current implementation tasks and execution status. |
| **ARCHITECTURE.md** | Conceptual and validated technical architecture. |
| **TECHNOLOGY.md** | Adopted and deferred technology decisions. |
| **CONVENTIONS.md** | Development conventions and engineering practices. |
| **MIGRATIONS.md** | Database migration strategy and conventions. |

---

# Current Development Sequence

The first user-oriented requirement output is complete through **AT-040**.

**AT-041 — Expose the User-Oriented Requirement Workflow** is the next implementation task. Its purpose is to make the current capability reachable through a minimal application interface and validate it from the user's perspective.

The next product direction after AT-041 will be determined from that validation. Knowledge Construction remains a strategic possibility, but it is no longer assumed to be the immediate next capability: product evidence should determine whether the next priority is improving requirement quality, adding contextual information, constructing knowledge, or beginning study interactions.

---

# Vision

Atanor is not intended to become another conversational chatbot.

Its purpose is to become a knowledge platform capable of understanding, organizing and relating information, allowing users to study more effectively while maintaining traceability to authoritative sources and making uncertainty explicit.
