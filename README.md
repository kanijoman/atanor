# Atanor

# Document Information

| Field        | Value                |
| ------------ | -------------------- |
| Project      | Atanor               |
| Document     | README               |
| Status       | 🟢 Active            |
| Version      | 0.3                  |
| Last Updated | 2026-08-12           |
| Audience     | Users and Developers |

> **A knowledge-driven platform for public service examination preparation.**

Atanor is an open-source platform designed to transform examination requirements and authoritative sources into structured, traceable and reusable knowledge that can support effective learning.

The first MVP focuses on Spanish public administration examinations. The underlying model is intentionally broader so that validated knowledge can eventually be reused across different examinations and other knowledge-intensive learning domains.

---

# Product Direction

Atanor aims to solve a problem traditionally addressed by preparation services: turning an official examination requirement into a justified scope of knowledge and, eventually, an effective learning journey.

The intended product flow is:

```text
Requirement
    ↓
Scope Discovery
    ↓
Knowledge Blueprint
    ↓
Knowledge Assessment
    ↓
Source Discovery / Acquisition
    ↓
Canonical Knowledge
    ↓
Learning Path
```

The canonical knowledge corpus is built progressively and on demand. Atanor does not require a complete global corpus before it can serve a new requirement.

---

# Current Status

The initial foundation is complete through **AT-016**.

Atanor currently has a validated first application workflow for PDF sources:

```text
PDF source
    ↓
Import
    ↓
Persist
    ↓
Retrieve / List
```

The workflow is implemented through an application layer, exposed through a minimal CLI and covered by isolated automated tests.

The next development stage is **Requirement Discovery**. Its objective is to transform imported authoritative source material into structured requirements without assuming that all sources share the same document structure or terminology.

The immediate target is:

```text
Source
    ↓
Requirement Discovery
    ↓
Requirement
```

Knowledge Blueprint construction and later learning capabilities remain outside the current implementation scope.

---

# Requirement Discovery

Requirement discovery must distinguish the expression found in a source from the canonical requirement it represents.

For example, different source expressions such as:

```text
Constitución Española
Constitución
Constitución de España
Constitución de 1978
```

may refer to the same requirement.

The original expression and its source location must remain traceable even when different expressions are associated with the same requirement.

Likewise, document structures may vary between sources. Sources from the same provider may share patterns, while sources from different providers may require different extraction strategies. The domain model must not depend on one specific document layout.

The initial implementation will remain deliberately simple and deterministic. More general semantic matching or parser infrastructure will only be introduced when real sources demonstrate a need for it.

---

# Project Principles

Atanor is developed around a small set of core principles:

* **Knowledge is the core product asset.**
* **Requirements and source expressions are not the same thing.**
* **Canonical knowledge must remain reusable independently of a curriculum.**
* **Every important knowledge claim should remain traceable to supporting evidence.**
* **Artificial Intelligence is a tool, not the product itself.**
* **Maintainability takes precedence over unnecessary complexity.**
* **Infrastructure is introduced only when it solves an existing problem.**
* **Development is iterative, incremental and pragmatic.**

---

# Development Philosophy

Atanor follows a pragmatic and incremental development process.

The project introduces infrastructure only when it solves an existing problem. Technologies, frameworks and project structure are incorporated as they become necessary, avoiding speculative design and unnecessary complexity.

Development follows modern software engineering practices, including:

* Clean Code
* SOLID principles
* DRY
* Pragmatic design
* Test-Driven Development whenever it provides clear value

Each backlog task should represent one isolated logical change, and each push should normally correspond to one backlog task.

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

The next active epic is **Requirement Discovery**:

1. Define the requirement discovery use case.
2. Extract text from supported PDF sources.
3. Identify and normalize requirement candidates.
4. Persist discovered requirements.
5. Expose minimal requirement inspection.
6. Validate the complete workflow end to end.

The sequence may evolve if real source material exposes new domain constraints, but the project should avoid speculative infrastructure and abstractions.

---

# Vision

Atanor is not intended to become another conversational chatbot.

Its purpose is to become a knowledge platform capable of understanding, organizing and relating information, allowing users to study more effectively while maintaining traceability to authoritative sources and making uncertainty explicit.
