# Atanor Architecture

# Document Information

| Field | Value |
|---|---|
| Project | Atanor |
| Document | ARCHITECTURE |
| Status | 🟢 Active |
| Version | 1.0 |
| Last Updated | 2026-09-17 |
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
- Candidate-facing claims such as study coverage must be explicit and traceable rather than inferred from textual coincidence.

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
Document Structure Analysis
    ↓
Requirement Discovery / Knowledge Extraction
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
    ↓
Candidate Study Material
    ↓
Study Coverage Feedback
```

The source workflow has been validated against real BOE and Junta de Castilla y León samples. Requirement Scope, Knowledge Need and initial Coverage have been validated through domain and persistence tests. AT-043 additionally validated a minimal autonomous acquisition and deterministic relevance-extraction path using a BOE sample.

AT-044 and AT-045 validated a deterministic document-structure analysis stage for supported text-based PDFs. The stage currently separates marker detection, local classification (`STRUCTURAL` / `ENUMERATION`) and hierarchy construction. This representation is an application processing result, not a new domain concept.

The acquisition/extraction path is currently a prototype. It must not be interpreted as proof that arbitrary acquired material is complete, semantically valid or canonical Knowledge.

AT-096 subsequently validated an explicit semantic coverage contract for candidate-facing study material. Partial coverage is represented through required, covered and pending aspects rather than inferred from raw text similarity.

# Architectural Layers

## Interface Layer

Provides adapters for application use cases. The current implementation uses a minimal standard-library CLI and a web interface. Interfaces expose validated application behavior without owning domain rules.

## Application Layer

Contains use cases that coordinate validation, domain operations, persistence, transactions and document processing. Source- and format-specific parsing belongs here or in dedicated integration components, not in domain concepts.

The document-processing path now has an explicit structural-analysis boundary:

```text
Extracted Text
    ↓
Marker Detection
    ↓
Marker Classification
    ↓
Hierarchy Construction
    ↓
Structured Document Representation
    ↓
Downstream Requirement / Knowledge Extraction
```

The first three stages are deterministic and evidence-driven. AT-045 established that local context is sufficient for the currently observed distinction between meaningful structural markers and internal enumerations. The implementation must remain replaceable and must not be treated as a universal document parser.

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

Candidate-facing study preparation currently adds a deterministic material and coverage projection:

```text
Programme Unit
    ↓
Knowledge Need
    ↓
Candidate Study Material
    ↓
Required Aspects
    ↓
Covered Aspects
    ↓
Pending Aspects
    ↓
Study Coverage Summary
```

This is currently implemented at the application level for validated study-material verticals. It is not yet a generic semantic matching engine.

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

Document structure remains outside this model. Structural markers, classifications, hierarchy levels, parent relationships and continuation text are processing information used to improve downstream extraction; they are not currently domain entities.

### Requirement

Represents a requirement in the application domain. Provenance remains explicit through its source relationship.

### Requirement Scope

Represents the knowledge coverage required by a requirement in a specific contextual examination setting. A requirement may have multiple scopes.

### Knowledge Need

Represents a unit of knowledge coverage required by a scope. It is valid even when corresponding Knowledge does not exist.

### Knowledge

Represents reusable knowledge that may satisfy one or more Knowledge Needs. The definitive canonical Knowledge model remains intentionally limited until concrete requirements justify further design.

### Coverage

Represents the result of comparing a Knowledge Need with available Knowledge. Coverage is derived and is not an independent persisted entity.

For the current candidate-facing study-material vertical, useful partial coverage is represented explicitly by a deterministic set of required semantic aspects. The application derives which aspects are covered by the validated study material and builds a typed summary containing:

- coverage status (`missing`, `partial` or `covered`);
- covered aspect count;
- required aspect count;
- coverage percentage;
- covered aspects;
- pending aspects.

The candidate-facing summary is therefore an explicit product contract. It must not be inferred by substring matching, article-count coincidence or the mere existence of a `Knowledge` instance.

This semantic aspect mechanism has been validated across Ley 19/2013 and Ley 39/2015 verticals. It remains deterministic and vertical-specific until broader evidence justifies a generic semantic matching abstraction.

## Persistence Layer

The persistence layer uses SQLAlchemy with SQLite and Alembic. Persistence must not make domain concepts dependent on SQLAlchemy or SQLite-specific behavior. Requirement scopes and knowledge needs are persisted as part of the requirement aggregate.

The current structural-analysis representation is not persisted. Persistence should be introduced only if a downstream workflow demonstrates a concrete need for structural-tree storage, repeatability or auditability.

Candidate-facing coverage summaries are currently derived from application-level contracts and are not independently persisted.

# Source and Requirement Discovery

Requirement Discovery is a validated capability rather than a universal document parser.

```text
Source
    ↓
Document Structure Detection
    ↓
Marker Classification
    ↓
Hierarchy Construction
    ↓
Requirement Mention
    ↓
Requirement
```

Real samples demonstrate different document structures. The current implementation recognizes only the minimum deterministic structures justified by those samples. `Tema` identifiers and other structured identifiers are preserved as text and are not assigned semantic meaning.

The current validated structural representation preserves raw marker information, marker classification, hierarchy level, parent relationship and continuation text. `STRUCTURAL` and `ENUMERATION` are processing classifications; they do not imply domain semantics beyond the validated hierarchy behavior.

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

The candidate-facing study-material vertical extends the progression with derived preparation feedback:

```text
Knowledge Need
    ↓
Candidate Study Material
    ↓
Explicit Semantic Coverage
    ↓
Candidate Feedback
```

The following remain outside the current architecture:

- semantic scope discovery;
- automatic interpretation of arbitrary requirement meaning;
- OCR;
- generic semantic knowledge matching;
- automatic coverage assessment for arbitrary topics;
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

AT-045 demonstrated this transition explicitly: the structural distinction was first evaluated in `experiments/`, then accepted behaviors were encoded in focused tests. The experiment itself remains exploratory; the validated behavior is now an input to the real application pipeline.

AT-096 followed the same pattern for candidate-facing semantic coverage: an explicit aspect model was tested first, then exposed through the API and web interface once the behavior was validated with a real Ley 39/2015 study unit.

Experiments may expose raw extracted content, sizes, intermediate representations or other implementation details. Tests should verify only behavior that has become part of the accepted contract. This allows uncertain acquisition and extraction approaches to evolve without creating brittle regression expectations.

# Evolution Strategy

Atanor uses evidence-driven architectural evolution. Deferred capabilities include advanced source discovery, semantic requirement resolution, OCR, richer Knowledge Blueprint semantics, canonical Knowledge construction, richer evidence models, generic semantic coverage, graph or vector persistence, external AI services and multi-user infrastructure.

The current web interface is intentionally minimal. Further frontend architecture should be introduced only when a concrete candidate workflow requires it.

Each capability should be introduced only in response to a concrete product requirement.

# Architectural Decision Rule

When several technically valid solutions exist, prefer the solution that preserves important domain distinctions, introduces the least unnecessary complexity, can be validated with current requirements and keeps future replacement possible without speculative abstraction.

> **Does this architectural decision help Atanor transform requirements and authoritative sources into better, simpler and more traceable knowledge?**
