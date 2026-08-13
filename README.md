# Atanor

# Document Information

| Field        | Value                |
| ------------ | -------------------- |
| Project      | Atanor               |
| Document     | README               |
| Status       | 🟢 Active            |
| Version      | 0.5                  |
| Last Updated | 2026-08-13           |
| Audience     | Users and Developers |

> **A knowledge-driven platform for public service examination preparation.**

Atanor is an open-source platform designed to transform examination requirements and authoritative sources into structured, traceable and reusable knowledge that can support effective learning.

The first MVP focuses on Spanish public administration examinations. The underlying model is intentionally broader so that validated knowledge can eventually be reused across different examinations and other knowledge-intensive learning domains.

---

# Product Direction

Atanor aims to solve a problem traditionally addressed by preparation services: turning an official examination requirement into a justified knowledge scope and, eventually, an effective learning journey.

The current conceptual flow is:

```text
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Coverage
    ↓
Knowledge
    ↓
Learning Path
```

The current model deliberately separates what an examination context requires from whether the corresponding knowledge already exists. Knowledge construction and learning capabilities will be introduced incrementally as real requirements justify them.

---

# Current Status

The initial foundation and source workflow are complete. Requirement Discovery was validated through **AT-032**, and Requirement Scope, Knowledge Need and initial Coverage modeling were completed through **AT-035**.

Atanor currently has a validated vertical workflow for supported PDF sources:

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
Requirement mention
    ↓
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Coverage
```

The discovery and domain workflow is covered by automated tests and has been exercised with real PDF samples from different sources, including BOE and Junta de Castilla y León documents.

The current discovery implementation is intentionally deterministic and structure-aware. It does not claim to be a universal parser, semantic requirement resolver or OCR system. A scanned PDF sample from Ayuntamiento de León is retained as a regression case for the current absence of OCR support.

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

---

# Project Principles

Atanor is developed around a small set of core principles:

* **Knowledge is the core product asset.**
* **Requirements, scopes, needs and knowledge are distinct concepts.**
* **Canonical knowledge must remain reusable independently of a curriculum.**
* **Important knowledge claims should remain traceable to supporting evidence.**
* **Artificial Intelligence is a tool, not the product itself.**
* **Maintainability takes precedence over unnecessary complexity.**
* **Infrastructure is introduced only when it solves an existing problem.**
* **Development is iterative, incremental and pragmatic.**

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

Requirement Discovery is complete through **AT-032**. Requirement Scope & Coverage is complete through **AT-035**.

The next implementation task has intentionally not been fixed yet. The project is currently reevaluating the documentation and product direction before defining the next development step.

The next strategic capability is expected to involve **Knowledge Construction**, but its first implementation should be defined from the validated Requirement Scope and Knowledge Need model rather than assuming a complete Blueprint or corpus architecture in advance.

---

# Vision

Atanor is not intended to become another conversational chatbot.

Its purpose is to become a knowledge platform capable of understanding, organizing and relating information, allowing users to study more effectively while maintaining traceability to authoritative sources and making uncertainty explicit.
