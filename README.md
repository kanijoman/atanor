# Atanor

> **A knowledge-driven platform for public service examination preparation.**

Atanor is an open-source platform designed to transform examination requirements and authoritative sources into structured, traceable and reusable knowledge that can support effective learning.

The first MVP focuses on Spanish public administration examinations. The underlying model is intentionally broader so validated knowledge can eventually be reused across different examinations and other knowledge-intensive learning domains.

## Product Direction

Atanor aims to solve a problem traditionally addressed by preparation services: turning an official examination requirement into a justified knowledge scope and, eventually, an effective learning journey.

The current product direction is deliberately incremental. A user should be able to provide a supported `convocatoria`, obtain the relevant study requirements and programme structure, and progressively receive the knowledge needed to prepare it.

The current validated application flow is:

```text
Convocatoria PDF
    ↓
Source
    ↓
Document Processing
    ↓
Requirement Discovery
    ↓
Requirement Resolution
    ↓
Study Requirements
    ↓
Study Programme Discovery
    ↓
Study Programme Units
    ↓
Knowledge Need
    ↓
Knowledge Construction
    ↓
Candidate Study Material
```

## Current Status

Atanor currently supports:

- PDF source import and persistence;
- deterministic text extraction with page/order provenance;
- deterministic document structure analysis for the currently observed source families;
- requirement discovery and deterministic resolution;
- user-oriented study requirements;
- requirement scopes and knowledge needs;
- binary knowledge coverage (`COVERED` / `MISSING`);
- autonomous acquisition from an authoritative BOE source;
- deterministic relevant-content extraction;
- first reusable `Knowledge` construction;
- study-programme discovery for the current BOE, BOJA and Archiveros samples;
- persistence and retrieval of study programmes and programme units;
- a first end-to-end candidate study-material flow from a real programme point to persisted and retrievable material.

The first end-to-end material case uses a real BOE call point referring to Ley 19/2013. Atanor derives the narrower `Derecho de acceso a la información pública` knowledge need without modifying the original programme point.

These capabilities have been validated against four real PDF samples and focused product tests. Support is intentionally not presented as universal parsing of arbitrary official documents. Scanned/image-only PDFs remain outside the current extraction boundary.

## Product Principles

A few principles guide the current development stage:

- **Product validation drives development.**
- **Atanor should provide the knowledge required by the candidate rather than making the candidate responsible for finding and supplying it.**
- **External sources are evidence and raw material, not automatically validated knowledge.**
- **Important knowledge claims should remain traceable to supporting evidence.**
- **Uncertainty must remain explicit; unsupported knowledge is preferable to fabricated certainty.**
- **Architecture enables product evolution rather than dictating it.**
- **New abstractions, dependencies and infrastructure require concrete evidence.**
- **Experiments discover behavior; tests protect behavior once it is accepted.**
- **Development is incremental, pragmatic and maintainable.**

## Experiments and Tests

Exploratory work may live under `backend/experiments/` while it is actively useful for answering an unresolved question. Once an experiment's conclusions are incorporated into product behavior, tests or documentation, the exploratory artifact should normally be removed. Git history preserves the investigation.

Tests define behavior that Atanor has decided to preserve. The preferred development loop is:

```text
Hypothesis
    ↓
Experiment / mini-MVP
    ↓
Real validation
    ↓
Observation
    ↓
Validated requirement
    ↓
Test + implementation
```

## Documentation

Project documentation is organized by responsibility:

| Document | Purpose |
|---|---|
| `docs/foundations/FOUNDATIONS.md` | Product mission, vision and foundational principles. |
| `docs/roadmap/ROADMAP.md` | Strategic product direction and major stages. |
| `docs/backlog/BACKLOG.md` | Current product state and immediate priorities. |
| `docs/architecture/ARCHITECTURE.md` | Validated architecture and architectural decisions. |
| `docs/conventions/CONVENTIONS.md` | Development and engineering conventions. |
| `docs/technology/TECHNOLOGY.md` | Technology decisions. |
| `docs/migrations/MIGRATIONS.md` | Database migration strategy. |
| GitHub Issues | Concrete task definition, acceptance criteria, discussion and status. |

The backlog intentionally does not duplicate the detailed history of completed tasks. GitHub Issues and Git history provide the execution record.

## Development Workflow

New concrete work is normally tracked through a GitHub Issue using the `AT-XXX` identifier. Each task should be isolated, validated and traceable.

Commit messages use:

```text
AT-XXX Change description
```

The preferred workflow is:

```text
Product hypothesis / need
    ↓
GitHub Issue
    ↓
Minimal implementation
    ↓
Automated validation
    ↓
Real-product validation
    ↓
Issue closed
```

## Technology

The current backend stack is:

- Python 3.14
- uv
- FastAPI
- Pydantic
- Pydantic Settings
- Uvicorn
- SQLAlchemy
- Alembic
- SQLite

The project deliberately has no mandatory paid dependency and does not currently require Docker, PostgreSQL, vector databases, graph databases, external AI services or crawling infrastructure.

Technology choices remain subordinate to validated product requirements.

## Current Product Gap

The first candidate study-material vertical is now proven at the application level, but the candidate does not yet have a simple interface for selecting a programme point and reading its generated material.

The next mini-MVP should therefore expose this capability through the existing application interface before expanding the knowledge model or introducing additional infrastructure.

## Vision

Atanor is intended to become a knowledge platform capable of understanding, organizing and relating information so users can study more effectively while maintaining traceability to authoritative sources and making uncertainty explicit.
