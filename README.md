# Atanor

# Document Information

| Field        | Value                |
| ------------ | -------------------- |
| Project      | Atanor               |
| Document     | README               |
| Status       | 🟢 Active            |
| Version      | 0.7                  |
| Last Updated | 2026-08-17           |
| Audience     | Users and Developers |

> **A knowledge-driven platform for public service examination preparation.**

Atanor is an open-source platform designed to transform examination requirements and authoritative sources into structured, traceable and reusable knowledge that can support effective learning.

The first MVP focuses on Spanish public administration examinations. The underlying model is intentionally broader so that validated knowledge can eventually be reused across different examinations and other knowledge-intensive learning domains.

---

# Product Direction

Atanor aims to solve a problem traditionally addressed by preparation services: turning an official examination requirement into a justified knowledge scope and, eventually, an effective learning journey.

The current validated product direction starts with a narrower promise: **a user provides a supported convocatoria and Atanor determines what the user needs to study without requiring the user to validate Atanor's discovery or resolution decisions.**

The validated requirement flow is:

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

AT-043 extended the product exploration beyond requirement discovery. Atanor can now acquire text from an authoritative BOE source and apply a deterministic relevance strategy to a `KnowledgeNeed` without requiring the candidate to provide the missing knowledge.

This does **not** mean that arbitrary source text is considered validated knowledge. External documents are treated as raw material; acquisition, relevant-content extraction and validated knowledge remain distinct steps.

---

# Current Status

The foundation, source workflow, requirement discovery, requirement resolution, user-oriented requirement projection and the first autonomous knowledge-acquisition experiment are complete through **AT-043**.

Atanor currently has two validated experimental flows:

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

and:

```text
Knowledge Need
    ↓
External source acquisition
    ↓
Raw extracted content
    ↓
Deterministic relevance extraction
    ↓
Candidate Knowledge
```

The second flow was validated experimentally against a real BOE sample. From approximately 328,000 extracted characters, the deterministic strategy selected approximately 2,000 characters containing multiple relevant formulations of the Constitution Española topic. The result demonstrates that autonomous acquisition and basic relevance filtering are viable, but it is not yet sufficient to claim semantic knowledge extraction.

The BOE experiment also demonstrated that source documents may contain substantially more information than the study programme itself, including administrative, eligibility and procedural information. Such information may become valuable product functionality, but it is intentionally outside the current MVP scope.

Different BOE and other official-document templates must not be assumed to share a universal structure. The current deterministic strategy is therefore an experiment, not a general-purpose BOE parser.

---

# Product Development Principle: Atanor Must Provide Knowledge

A core product constraint has now been established:

> **Atanor must provide the knowledge required by the candidate; it must not make the candidate responsible for finding and supplying that knowledge.**

A candidate may eventually benefit from curator intervention when automation cannot reliably resolve a gap, but candidate-supplied knowledge is not the intended default workflow.

This principle guides future Knowledge Construction work. Atanor may use authoritative sources, deterministic extraction, AI or other mechanisms, but it must distinguish between:

```text
Source material
    ↓
Acquired information
    ↓
Relevant information
    ↓
Validated knowledge
```

Atanor must not claim `COVERED` merely because a source contains a textual match. Saying **"I don't know"** is preferable to presenting invented, incomplete or insufficiently supported knowledge as fact.

---

# Experiments and Tests

Atanor now deliberately distinguishes **experiments** from **tests**.

### Experiments

Experiments are exploratory tools used to inspect, measure and understand product behavior. They may print output, compare strategies, process real documents and evolve rapidly. They are not product contracts.

They live under:

```text
backend/experiments/
```

For example, AT-043 introduced `inspect_boe_knowledge.py` to inspect the actual content produced by the deterministic BOE knowledge-extraction strategy.

### Tests

Tests define behavior that Atanor has already decided to preserve. They should remain deterministic, self-contained and agnostic of exploratory implementation details.

The intended development loop is:

```text
Experiment
    ↓
Observation
    ↓
Product insight
    ↓
Requirement / decision
    ↓
Test
    ↓
Implementation
```

This separation allows Atanor to investigate uncertain product questions without prematurely turning hypotheses into permanent technical contracts.

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
* **Atanor must provide knowledge rather than delegating knowledge acquisition to the candidate.**
* **Uncertainty must be explicit; unsupported knowledge is preferable to fabricated certainty.**
* **External sources are evidence and raw material, not automatically validated knowledge.**
* **Experiments are used to discover product behavior; tests protect behavior once it is decided.**
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

AT-043 demonstrated that Atanor can begin constructing knowledge autonomously from an authoritative external source, but also established that raw source extraction is not equivalent to validated knowledge.

The next product direction should therefore focus on improving the reliability and generality of the transition from **source material → relevant information → knowledge**, while avoiding assumptions about a single document template. The next mini-MVP should be selected from evidence produced by experiments rather than from a predetermined technical roadmap.

Potential future directions include document-structure discovery, more robust relevance extraction, source diversification and semantic knowledge construction. None is currently a commitment.

---

# Vision

Atanor is not intended to become another conversational chatbot.

Its purpose is to become a knowledge platform capable of understanding, organizing and relating information, allowing users to study more effectively while maintaining traceability to authoritative sources and making uncertainty explicit.
