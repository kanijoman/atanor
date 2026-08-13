# Atanor Architecture

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | ARCHITECTURE                |
| Status       | 🟢 Active                   |
| Version      | 0.6                         |
| Last Updated | 2026-08-13                  |
| Audience     | Contributors and Developers |

---

# Purpose

This document describes the conceptual and validated technical architecture of Atanor.

The architecture exists to support the product objective of transforming requirements and authoritative sources into structured, traceable and reusable knowledge.

The architecture should remain as simple as possible while preserving important domain distinctions.

---

# Architectural Principles

- Domain concepts must not depend on interface technology.
- Application use cases orchestrate domain behavior and persistence without exposing persistence details to interfaces.
- Sources and their representations are distinct from the requirements and knowledge they support.
- External document structures must not become intrinsic domain structures.
- Requirement expressions found in sources must remain distinguishable from canonical requirements.
- Persistence technology is an implementation detail of the domain model.
- New abstractions should be introduced when validated requirements justify them, not for hypothetical future formats or capabilities.

---

# Current Validated Architecture

The source-to-requirement workflow is now validated for supported PDF sources:

```text
PDF Source
    ↓
Import
    ↓
Persist Source
    ↓
Text Extraction
    ↓
Structured Requirement Discovery
    ↓
Requirement Mention
    ↓
Requirement
    ↓
Persist / Inspect
```

The workflow has been validated against real PDF samples from different sources, including BOE and Junta de Castilla y León documents.

The current CLI is an adapter for application use cases rather than part of the domain architecture.

---

# Architectural Layers

## Interface Layer

Provides user- or system-facing adapters for application use cases.

The current implementation uses a minimal standard-library CLI. A future web, desktop or other interface may replace or complement it without changing the domain model.

Interfaces should not directly manipulate persistence entities or database sessions when an application use case can provide the required behavior.

---

## Application Layer

Contains use cases that orchestrate application behavior.

The application layer is responsible for coordinating:

- input validation relevant to the use case;
- domain operations;
- persistence operations;
- transaction boundaries where required;
- application-level output;
- document text extraction and structured requirement discovery.

Source- and format-specific parsing rules belong here or in dedicated application/integration components, not in domain concepts.

---

## Domain Layer

Contains the business concepts and relationships that represent Atanor's knowledge domain.

The current model is intentionally minimal. It includes concepts such as:

```text
Source
    ↓
Requirement Mention
    ↓
Requirement
```

The distinction between a discovered source expression and a persisted requirement is intentional. Requirement provenance is mandatory through `source_id`.

The model is expected to evolve as real product requirements are validated.

Concepts such as evidence, knowledge assertions, learning paths, assessments and richer knowledge hierarchies remain future extensions until concrete requirements justify them.

---

## Persistence Layer

Provides storage implementations for the domain and application layers.

The current implementation uses SQLAlchemy with SQLite and Alembic migrations.

The persistence layer must not make domain concepts dependent on SQLAlchemy or SQLite-specific behavior.

---

# Source and Requirement Discovery

Requirement Discovery is a validated application capability rather than a universal document parser:

```text
Source
    ↓
Document Structure Detection
    ↓
Requirement Mention
    ↓
Requirement
```

## Source Structure Is Not Domain Structure

A source may be a PDF from the BOE, a document from another public authority, or a user-provided document. Real samples have demonstrated that different sources can use different structures.

The current implementation recognizes the minimum deterministic structures justified by the validated samples. These include numbered entries under a `Programa` context and `Tema` entries such as:

```text
Tema 1.– ...
Tema IV.– ...
Tema A.– ...
```

The identifier is preserved as text. It is not converted to a number or interpreted semantically.

Sources from the same provider may share a pattern, but no universal document structure should be assumed. A provider- or document-specific strategy may become appropriate if additional real samples justify it, but no such abstraction is currently part of the architecture.

Scanned PDFs are currently outside the supported extraction boundary; OCR is a future capability.

## Requirement Expression Is Not Requirement Identity

A source may contain expressions such as:

```text
Constitución Española
Constitución
Constitución de España
Constitución de 1978
```

These expressions may refer to the same canonical requirement.

Architecturally, the distinction is:

```text
Source
    ↓
Requirement Expression / Mention
    ↓
Canonical Requirement
```

The original expression, provenance and source location must remain traceable even when several expressions are eventually associated with the same requirement.

The current implementation does not perform semantic entity resolution. It should not introduce a general semantic resolution subsystem until real requirements justify it.

---

# Requirement Discovery Boundary

Requirement Discovery is intentionally limited to identifying and representing requirements.

It does not yet construct the complete knowledge scope.

The intended conceptual progression is:

```text
Source
    ↓
Requirement
    ↓
Scope Discovery
    ↓
Knowledge Blueprint
    ↓
Knowledge Assessment
    ↓
Candidate Knowledge
    ↓
Evidence & Validation
    ↓
Canonical Knowledge
    ↓
Learning Path
```

Each step should be introduced only when the preceding capability provides sufficient evidence about the domain.

---

# Persistence and Identity

Domain entity identity is independent of external document locators.

For sources, the persisted entity has its own identity while the external document locator identifies where the source originated. A local file path is therefore not used as the source's canonical identity.

Requirements currently require `source_id`, making provenance explicit and mandatory. A textual expression in a document is evidence about a requirement, not necessarily the identity of that requirement.

---

# Evolution Strategy

Atanor uses an evidence-driven architectural evolution strategy.

The architecture deliberately supports future growth without implementing future infrastructure prematurely.

Examples of currently deferred capabilities include:

- advanced source discovery;
- semantic requirement resolution;
- OCR for scanned documents;
- Knowledge Blueprint construction;
- richer evidence models;
- graph or vector persistence;
- external AI services;
- web UI;
- multi-user infrastructure.

These capabilities may become appropriate later, but each should be introduced in response to a concrete product requirement.

---

# Architectural Decision Rule

When several technically valid solutions exist, prefer the solution that:

1. preserves the important domain distinction;
2. introduces the least unnecessary complexity;
3. can be validated with the current requirements;
4. keeps future replacement possible without speculative abstraction.

The guiding question is:

> **Does this architectural decision help Atanor transform requirements and authoritative sources into better, simpler and more traceable knowledge?**
