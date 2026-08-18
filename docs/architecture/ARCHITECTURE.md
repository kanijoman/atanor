# Atanor Architecture

# Document Information

| Field | Value |
|---|---|
| Project | Atanor |
| Document | ARCHITECTURE |
| Status | 🟢 Active |
| Version | 0.8 |
| Last Updated | 2026-08-18 |
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
- Acquired source material is not automatically canonical Knowledge.
- Exploratory experiments may inspect implementation behavior without becoming product contracts.

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
Knowledge Acquisition
    ↓
Source Material
    ↓
Relevant Content
    ↓
Knowledge
    ↓
Coverage
```

The source workflow has been validated against real BOE and Junta de Castilla y León samples. Requirement Scope, Knowledge Need and initial Coverage have been validated through domain and persistence tests. AT-043 additionally validated a minimal autonomous acquisition and deterministic relevance-extraction path using a BOE sample.

The acquisition/extraction path is currently a prototype. It must not be interpreted as proof that arbitrary acquired material is complete, semantically valid or canonical Knowledge.

# Architectural Layers

## Interface Layer

Provides adapters for application use cases. The current implementation uses a minimal standard-library CLI. A future interface may replace or complement it without changing the domain model.

## Application Layer

Contains use cases that coordinate validation, domain operations, persistence, transactions and document processing. Source- and format-specific parsing belongs here or in dedicated integration components, not in domain concepts.

The current application flow distinguishes three stages during knowledge acquisition:

```text
Knowledge Need
    ↓
Acquisition strategy
    ↓
Source material
    ↓
Extraction strategy
    ↓
Relevant content / candidate Knowledge
```

Acquisition and extraction strategies are replaceable implementation mechanisms. The domain does not assume BOE structure, a particular retrieval technology or a particular extraction algorithm.

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

An external document or extracted text is not automatically equivalent to canonical Knowledge. This distinction is particularly important after AT-043: the BOE experiment demonstrated useful relevant context but also incidental references.

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

# Knowledge Acquisition and Extraction Boundary

AT-043 established the first application-level knowledge acquisition path. Its architecture intentionally separates:

```text
Knowledge Need
      ↓
Acquisition
      ↓
External Source Material
      ↓
Relevance Extraction
      ↓
Candidate Knowledge
```

The first implementation uses the BOE as an experimental source and a deterministic literal/context extraction strategy. This is evidence for the architecture of the workflow, not a commitment to BOE-only acquisition or literal matching as the final solution.

Provider-specific document structures must remain outside the domain model. Different BOE documents, and different providers, may expose different layouts or levels of structure. A source adapter may exploit known structure when evidence justifies it, but the domain must continue to represent `Source`, `KnowledgeNeed` and `Knowledge` independently.

The current extraction strategy may return relevant context mixed with incidental references. Therefore the following distinction must remain explicit:

```text
Source Material
      ≠
Relevant Content
      ≠
Validated / Canonical Knowledge
```

Semantic validation, completeness assessment, richer provenance, freshness and quality scoring remain future capabilities until a concrete candidate-facing workflow requires them.

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

The acquisition prototype extends the implementation around `KnowledgeNeed` without changing this domain boundary.

This layer deliberately does not construct the complete knowledge corpus. The following remain outside the current architecture:

- semantic scope discovery;
- automatic interpretation of requirement meaning;
- OCR;
- semantic knowledge matching;
- partial or depth-aware coverage calculation;
- complete canonical Knowledge construction;
- learning paths and assessments.

A richer Knowledge Blueprint may become useful later if future requirements need confidence, evidence requirements, alternative interpretations or unresolved inference. It is not currently required as an independent domain entity.

# Experiments and Tests

Exploratory experiments are kept separate from automated tests:

```text
experiments/
    ↓
observe / measure / compare
    ↓
product or engineering insight
    ↓
validated requirement
    ↓
tests/
```

Experiments may expose raw extracted content, sizes, intermediate representations or other implementation details. Tests should verify only behavior that has become part of the accepted contract. This allows uncertain acquisition and extraction approaches to evolve without creating brittle regression expectations.

# Evolution Strategy

Atanor uses evidence-driven architectural evolution. Deferred capabilities include advanced source discovery, semantic requirement resolution, OCR, richer Knowledge Blueprint semantics, canonical Knowledge construction, richer evidence models, semantic coverage, graph or vector persistence, external AI services, web UI and multi-user infrastructure.

Each capability should be introduced only in response to a concrete product requirement.

# Architectural Decision Rule

When several technically valid solutions exist, prefer the solution that preserves important domain distinctions, introduces the least unnecessary complexity, can be validated with current requirements and keeps future replacement possible without speculative abstraction.

> **Does this architectural decision help Atanor transform requirements and authoritative sources into better, simpler and more traceable knowledge?**
