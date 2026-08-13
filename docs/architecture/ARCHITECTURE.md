# Atanor Architecture

# Document Information

| Field | Value |
|---|---|
| Project | Atanor |
| Document | ARCHITECTURE |
| Status | 🟢 Active |
| Version | 0.7 |
| Last Updated | 2026-08-13 |
| Audience | Contributors and Developers |

---

# Purpose

This document describes the conceptual and validated technical architecture of Atanor. The architecture supports transforming requirements and authoritative sources into structured, traceable and reusable knowledge while keeping domain concepts independent from implementation technology.

# Architectural Principles

- Domain concepts must not depend on interface technology.
- Application use cases orchestrate domain behavior and persistence.
- Sources and their representations are distinct from requirements and knowledge.
- External document structures must not become intrinsic domain structures.
- Requirement expressions remain distinguishable from canonical requirements.
- Persistence technology is an implementation detail.
- New abstractions require validated product needs.

# Current Validated Architecture

```text
PDF Source
    ↓
Import
    ↓
Persist Source
    ↓
Text Extraction
    ↓
Requirement Discovery
    ↓
Requirement Mention
    ↓
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Coverage
```

The source workflow has been validated against real BOE and Junta de Castilla y León samples. Requirement Scope, Knowledge Need and initial Coverage have been validated through domain and persistence tests.

# Architectural Layers

## Interface Layer

Provides adapters for application use cases. The current implementation uses a minimal standard-library CLI. A future interface may replace or complement it without changing the domain model.

## Application Layer

Contains use cases that coordinate validation, domain operations, persistence, transactions and document processing. Source- and format-specific parsing belongs here or in dedicated integration components, not in domain concepts.

## Domain Layer

The current validated model is:

```text
Source
    ↓
Requirement Mention
    ↓
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Knowledge
    ↓
Coverage
```

### Requirement

Represents a requirement in the application domain. Provenance remains explicit through its source relationship.

### Requirement Scope

Represents the knowledge coverage required by a requirement in a specific contextual examination setting. A requirement may have multiple scopes.

### Knowledge Need

Represents a unit of knowledge coverage required by a scope. It is valid even when corresponding Knowledge does not exist.

### Knowledge

Represents reusable knowledge that may satisfy one or more Knowledge Needs. The definitive canonical Knowledge model remains intentionally limited until concrete requirements justify further design.

### Coverage

Represents the result of comparing a Knowledge Need with available Knowledge. The initial model supports only `COVERED` and `MISSING`. Coverage is derived and is not an independent persisted entity. Adding Knowledge may change Coverage without changing the Requirement Scope or Knowledge Need.

Semantic matching, partial coverage and depth-aware coverage are not currently implemented.

## Persistence Layer

The persistence layer uses SQLAlchemy with SQLite and Alembic. Persistence must not make domain concepts dependent on SQLAlchemy or SQLite-specific behavior. Requirement scopes and knowledge needs are persisted as part of the requirement aggregate.

# Source and Requirement Discovery

Requirement Discovery is a validated capability rather than a universal document parser.

```text
Source
    ↓
Document Structure Detection
    ↓
Requirement Mention
    ↓
Requirement
```

Real samples demonstrate different document structures. The current implementation recognizes only the minimum deterministic structures justified by those samples. `Tema` identifiers and other structured identifiers are preserved as text and are not assigned semantic meaning.

Scanned PDFs remain outside the supported extraction boundary; OCR is future work.

Requirement expression is not requirement identity. Semantic entity resolution is not currently implemented.

# Requirement Scope Boundary

The current validated progression is:

```text
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Coverage
```

This layer deliberately does not construct the complete knowledge corpus. The following remain outside the current architecture:

- semantic scope discovery;
- automatic interpretation of requirement meaning;
- OCR;
- semantic knowledge matching;
- partial or depth-aware coverage calculation;
- complete canonical Knowledge construction;
- learning paths and assessments.

A richer Knowledge Blueprint may become useful later if future requirements need confidence, evidence requirements, alternative interpretations or unresolved inference. It is not currently required as an independent domain entity.

# Evolution Strategy

Atanor uses evidence-driven architectural evolution. Deferred capabilities include advanced source discovery, semantic requirement resolution, OCR, richer Knowledge Blueprint semantics, canonical Knowledge construction, richer evidence models, semantic coverage, graph or vector persistence, external AI services, web UI and multi-user infrastructure.

Each capability should be introduced only in response to a concrete product requirement.

# Architectural Decision Rule

When several technically valid solutions exist, prefer the solution that preserves important domain distinctions, introduces the least unnecessary complexity, can be validated with current requirements and keeps future replacement possible without speculative abstraction.

> **Does this architectural decision help Atanor transform requirements and authoritative sources into better, simpler and more traceable knowledge?**
