# Technology

## Document Information

| Field        | Value      |
| ------------ | ---------- |
| Project      | Atanor     |
| Document     | Technology |
| Status       | 🟢 Active  |
| Version      | 0.4        |
| Last Updated | 2026-08-11 |
| Audience     | Developers |

---

## 1. Purpose

This document defines the technological decisions and constraints that guide Atanor development.

Technology is subordinate to the domain and product requirements. Atanor should introduce infrastructure only when it solves an existing problem and should avoid speculative technologies and unnecessary complexity.

This document records adopted technologies as well as relevant deferred options.

---

## 2. Technology Principles

### 2.1 Pragmatism First

Technology must solve a concrete problem.

A technology should not be introduced merely because it is common, fashionable or potentially useful in the future.

The simplest technology that adequately satisfies the current requirement should be preferred.

### 2.2 No Mandatory Paid Dependencies

Atanor's core functionality must not depend on paid third-party software, libraries, APIs, platforms or infrastructure.

The project must be capable of being developed, executed and tested using freely available software.

When a third-party dependency is required, open-source and freely available alternatives should be preferred when they adequately satisfy the project's requirements.

Paid services may be considered as optional integrations in the future, but they must never be a mandatory dependency of the core platform.

### 2.3 Open Source and Self-Hostable Infrastructure

Whenever infrastructure is required, Atanor should prefer technologies that are:

* freely available;
* open source;
* locally executable;
* self-hostable;
* supported by the Python ecosystem.

This reduces vendor lock-in and keeps the core platform independently deployable.

### 2.4 Avoid Premature Infrastructure

Infrastructure must be introduced incrementally.

Atanor should not introduce:

* distributed systems;
* managed cloud services;
* vector databases;
* graph databases;
* external AI services;
* crawling services;
* container orchestration;

unless a validated product requirement demonstrates that they are necessary.

---

## 3. Adopted Technology

### 3.1 Backend

| Technology        | Status     | Purpose                         |
| ----------------- | ---------- | ------------------------------- |
| Python 3.14       | 🟢 Adopted | Backend language                |
| FastAPI           | 🟢 Adopted | HTTP API framework              |
| Pydantic          | 🟢 Adopted | Data validation and API schemas |
| Pydantic Settings | 🟢 Adopted | Application configuration       |
| Uvicorn           | 🟢 Adopted | ASGI application server         |

Python is the backend implementation language. The project targets Python 3.14.

---

### 3.2 Dependency Management

| Technology | Status     | Purpose                                      |
| ---------- | ---------- | -------------------------------------------- |
| uv         | 🟢 Adopted | Python dependency and environment management |

Dependencies must be declared explicitly in `pyproject.toml`.

---

### 3.3 Persistence

| Technology | Status     | Purpose                      |
| ---------- | ---------- | ---------------------------- |
| SQLAlchemy | 🟢 Adopted | Relational persistence layer |
| SQLite     | 🟢 Adopted | Initial database engine      |
| Alembic    | 🟢 Adopted | Database schema migrations   |

Atanor uses a relational persistence model for the current knowledge domain.

SQLite is the initial database engine because the current requirements only require local relational persistence and do not justify the operational complexity of a database server.

SQLAlchemy provides an abstraction between the application domain and the database implementation.

The persistence layer must not make the domain model dependent on SQLAlchemy-specific implementation details.

Alembic provides explicit, versioned database schema migrations. Persistent schema changes must be introduced through reviewed migrations rather than relying on implicit schema mutation.

---

## 4. Deferred Technologies

Deferred technologies are not rejected. They are simply not justified by the current requirements.

### 4.1 PostgreSQL

**Status:** 🟡 Deferred

PostgreSQL may replace or complement SQLite when Atanor requires capabilities that justify a server-based relational database, such as:

* concurrent multi-user workloads;
* production deployment requirements;
* operational or scalability requirements;
* database capabilities not adequately provided by SQLite.

The adoption of PostgreSQL must be driven by a concrete requirement rather than anticipation.

---

### 4.2 Graph Database

**Status:** 🟡 Deferred

Atanor's knowledge domain has graph-like relationships, but this does not currently justify a graph database.

The validated model can be represented using a relational database.

A graph database should only be considered if real query or domain requirements demonstrate that the relational model is insufficient.

---

### 4.3 Vector Database

**Status:** 🟡 Deferred

No vector database is currently required.

Semantic search, embeddings or retrieval mechanisms may be introduced later if validated product requirements require them.

---

### 4.4 Artificial Intelligence Services

**Status:** 🟡 Deferred

AI is not a mandatory infrastructure dependency of Atanor.

The platform must be capable of building and maintaining its canonical knowledge using public sources and user-provided material without requiring a paid AI provider.

AI capabilities may be introduced later as implementation tools for specific product capabilities.

---

### 4.5 External Crawling or Data Acquisition Services

**Status:** 🟡 Deferred

Atanor should initially rely on freely accessible sources and user-provided material.

Commercial crawling, scraping or data acquisition services are not part of the core architecture.

---

### 4.6 Containerization

**Status:** 🟡 Deferred

Docker and Docker Compose are not currently required.

Containerization should only be introduced when it solves a concrete development, testing or deployment problem.

---

## 5. Current Technology Stack

The current backend stack is therefore:

```text
Python 3.14
    │
    ├── FastAPI
    ├── Pydantic
    ├── Pydantic Settings
    ├── Uvicorn
    │
    └── SQLAlchemy
            │
            ├── Alembic
            │
            ▼
         SQLite
```

The stack deliberately contains no mandatory paid service or proprietary infrastructure.

---

## 6. Technology Selection Process

A technology should be adopted when:

1. a concrete requirement exists;
2. the current implementation cannot adequately satisfy it;
3. the proposed technology provides a clear benefit;
4. its operational and maintenance cost is justified;
5. a freely available or open-source option is preferred when suitable.

Before introducing significant infrastructure, the project should evaluate whether the requirement can be satisfied by the existing stack.

---

## 7. Evolution

Technology decisions are not permanent.

A deferred technology may become adopted when a concrete requirement justifies it.

Likewise, an adopted technology may be replaced if it no longer provides sufficient value.

Changes should be documented when they materially affect the architecture, development workflow or operational requirements.
