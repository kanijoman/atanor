# Atanor

# Document Information

| Field        | Value                |
| ------------ | -------------------- |
| Project      | Atanor               |
| Document     | README               |
| Status       | 🟢 Active            |
| Version      | 0.4                  |
| Last Updated | 2026-08-13           |
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

The initial foundation and source workflow are complete through **AT-016**. Requirement Discovery has subsequently been implemented and validated through **AT-032**.

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
Requirement mentions
    ↓
Requirement
    ↓
Persist / Inspect
```

The workflow is implemented through an application layer, exposed through a minimal CLI and covered by automated tests. The discovery workflow has been validated against real PDF samples from different sources, including BOE and Junta de Castilla y León documents.

The current discovery implementation is intentionally deterministic and structure-aware. It does not claim to be a universal parser, semantic requirement resolver or OCR system. A scanned PDF sample from Ayuntamiento de León is retained as a regression case for the current absence of OCR support.

---

# Requirement Discovery

Requirement discovery distinguishes the expression found in a source from the requirement it may represent.

The original expression, source and location remain traceable. Semantic equivalence between different expressions is deliberately outside the current implementation scope.

Document structures may vary between sources. Real samples have already demonstrated different structural conventions, including numbered entries and `Tema` entries. The current implementation preserves structured expressions without assigning semantic meaning to their numbering, allowing textual identifiers such as Arabic numbers, Roman numerals or letters.

The implementation uses the minimum deterministic structure necessary for the currently validated source formats. A future organism- or document-specific strategy may become appropriate if additional real samples provide sufficient evidence, but no such abstraction is currently required.

More general semantic matching, generalized parser infrastructure and OCR will only be introduced when real product requirements demonstrate a need for them.

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

Requirement Discovery is complete through **AT-032**. The next development step has not yet been fixed. It will be defined after evaluating the next workflow from discovered requirements toward knowledge scope and construction.

The next stage of the roadmap is **Knowledge Construction**, but implementation should first validate what information and intermediate concepts are actually required to transform a real requirement into a justified knowledge scope. The project should continue to let real source material and domain evidence drive generalization.

---

# Vision

Atanor is not intended to become another conversational chatbot.

Its purpose is to become a knowledge platform capable of understanding, organizing and relating information, allowing users to study more effectively while maintaining traceability to authoritative sources and making uncertainty explicit.
