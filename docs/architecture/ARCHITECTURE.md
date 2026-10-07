# Atanor Architecture

# Document Information

| Field | Value |
|---|---|
| Project | Atanor |
| Document | ARCHITECTURE |
| Status | 🟢 Active |
| Version | 2.0 |
| Last Updated | 2026-10-07 |
| Audience | Contributors and Developers |

---

# Purpose

This document describes the conceptual and validated technical architecture of Atanor. The architecture supports transforming requirements and authoritative sources into structured, traceable and reusable knowledge while keeping domain concepts independent from implementation technology.

# Architectural Principles

- Domain concepts must not depend on interface technology.
- Application use cases orchestrate domain behavior and persistence.
- Sources and their representations are distinct from requirements and knowledge.
- External document structures must not become intrinsic domain structures.
- The official wording of a programme unit is preserved; the knowledge need derived from it never modifies it.
- Persistence technology is an implementation detail.
- New abstractions require validated product needs.
- Acquired source material is not automatically canonical Knowledge.
- Exploratory experiments may inspect implementation behavior without becoming product contracts.
- Candidate-facing claims such as study coverage must be explicit and traceable rather than inferred from textual coincidence.

# Current Validated Architecture

```text
PDF (uploaded or local)
    ↓
Source (identified by content hash)
    ↓
Text Extraction
    ↓
Document Structure Analysis
    ↓
Call detection
    ↓
Study Programme discovery (provider-specific strategies)
    ↓
Study Programme Unit  (the requirement as the convocatoria states it)
    ↓
Knowledge Need
    ↓
Study Material (curated or acquired from an authoritative source)  =  Knowledge
    ↓
Study Coverage Summary
```

The source workflow has been validated against real BOE and Junta de Andalucía samples. Call and programme discovery are deterministic and provider-specific. A programme unit is the requirement as the convocatoria states it: its official wording is preserved and never modified by the knowledge need derived from it.

AT-044 and AT-045 validated a deterministic document-structure analysis stage for supported text-based PDFs. The stage currently separates marker detection, local classification (`STRUCTURAL` / `ENUMERATION`) and hierarchy construction. This representation is an application processing result, not a new domain concept.

Study material is either curated by Atanor or acquired from an authoritative source. Acquired material is not proof that arbitrary acquired content is complete, semantically valid or canonical Knowledge; its provenance and review status are therefore explicit.

AT-096 and AT-112 established an explicit semantic coverage contract for candidate-facing study material. Partial coverage is represented through required, covered and pending aspects, derived from the material actually produced rather than inferred from raw text similarity.

# Architectural Layers

## Interface Layer

Provides adapters for application use cases. The current implementation uses a minimal standard-library CLI, a FastAPI HTTP API and a React web interface (`frontend/`). Interfaces expose validated application behavior without owning domain rules.

The HTTP API currently exposes:

| Endpoint | Purpose |
|---|---|
| `GET /`, `GET /health` | Application root and health check. |
| `GET /api/calls`, `/api/calls/{id}` | List and retrieve imported calls. |
| `POST /api/calls?filename=...` | Import the PDF sent as the request body (25 MB limit). 201 for a new call, 200 when the same content was imported before, 413 / 422 with an explanation when the file is too large, not a PDF, or contains no convocatoria. |
| `GET /api/calls/{id}/programmes` | Programmes belonging to a call. |
| `GET /api/study/programmes`, `/api/study/programmes/{id}` | Programmes and their units, including per-unit study-material availability and a programme-level summary (`units_total`, `units_with_material`). |
| `GET /api/study/units/{id}` | Study material, provenance (origin and review status) and semantic coverage summary (covered, pending and required aspects) for a unit. Answers 503 when acquired material cannot be retrieved right now. |

The web interface follows the candidate flow import (optional) → call → programme → unit → study material and checklist.

A `Source` is identified by the SHA-256 of its content (`content_hash`), so importing the same document again, from any path, returns the existing call. Uploaded PDFs are stored under `uploads/` as `<hash>.pdf`. Nothing is persisted for a document in which no call is discovered.

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
Call and programme discovery
```

The first three stages are deterministic and evidence-driven. AT-045 established that local context is sufficient for the currently observed distinction between meaningful structural markers and internal enumerations. The implementation must remain replaceable and must not be treated as a universal document parser.

Knowledge acquisition is one kind of material provider (see below). Retrieval and article extraction are replaceable implementation mechanisms; the domain does not assume BOE structure or a particular retrieval technology.

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

### Study material providers

`application/study_material/` holds a registry of supported topics (`registry.py`, one module per topic under `topics/`). Each topic declares how its programme unit titles are recognized, its required aspects, a coverage strategy and a **material provider**:

- `CuratedMaterial`: study text written by Atanor, stored as data under `content/`, citing reference sources. Used where open-domain knowledge has no authoritative text online (for example object-oriented programming, data modelling) or where the text needs expert review.
- `AcquiredNormativeMaterial`: study text assembled from the articles of an authoritative normative source (currently Ley 19/2013, Ley 39/2015, the Constitución Española, Ley 50/1997, Ley 40/2015, Ley 7/1985, the Estatuto Básico del Empleado Público, RDL 4/2000, Ley 47/2003 and Ley 29/1998, from the BOE) through `application/normative_source/`. Each required aspect maps explicitly to the articles that develop it (a topic can draw on several laws, and then every article is labelled with its law), and the result is persisted as `Knowledge` so later requests need no network.

Every topic exposes its **provenance** (`origin`: curated or acquired; `review_status`: unreviewed or reviewed) so the candidate can tell how the material was produced. Coverage is derived from the material actually produced: an aspect counts as covered only when the text has a section for it with substantive content, so aspects whose articles could not be acquired remain pending. If an acquiring provider cannot reach its source, the API reports the material as temporarily unavailable instead of inventing it.

## Domain Layer

The current validated model is:

```text
Source
    ↓
Call
    ↓
Study Programme
    ↓
Study Programme Unit  (= the requirement)
    ↓
Knowledge Need
    ↓
Knowledge
    ↓
Coverage
```

Document structure remains outside this model. Structural markers, classifications, hierarchy levels, parent relationships and continuation text are processing information used by call and programme discovery; they are not domain entities.

### Source

A document the candidate provides, identified by the SHA-256 of its content so the same document is never imported twice.

### Call

The examination opportunity a source describes.

### Study Programme and Study Programme Unit

A call contains one or more study programmes, each made of units. A unit is the requirement as the convocatoria states it: its complete official wording (continuation lines joined, gazette page headers and footers removed), its position in the document and, when the programme is divided into blocks that restart numbering, the name of its block (`section`). Units are kept in document order, not ordered by number. Earlier stages modelled requirements and requirement scopes as separate entities; they were merged into the unit (AT-115) because no product flow needed more than one scope per requirement and the unit already carried the requirement's provenance.

### Knowledge Need

Represents the knowledge a programme unit demands. Every unit has one, derived without modifying its wording: supported units get the topic Atanor can prepare material for, any other unit keeps its official wording as the topic. It is valid even when corresponding Knowledge does not exist, and it records which Knowledge, if any, satisfies it.

### Knowledge

Represents reusable knowledge that may satisfy one or more Knowledge Needs. The definitive canonical Knowledge model remains intentionally limited until concrete requirements justify further design.

### Coverage

Represents the result of comparing a Knowledge Need with available Knowledge. Coverage is derived and is not an independent persisted entity. A need without Knowledge is missing; for a unit with study material, coverage is expressed through required aspects as described below. At programme level, coverage is the number of units that have study material.

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

The persistence layer uses SQLAlchemy with SQLite and Alembic. Persistence must not make domain concepts dependent on SQLAlchemy or SQLite-specific behavior. Knowledge needs are persisted with the programme unit they belong to, and link to the Knowledge that satisfies them.

The current structural-analysis representation is not persisted. Persistence should be introduced only if a downstream workflow demonstrates a concrete need for structural-tree storage, repeatability or auditability.

Candidate-facing coverage summaries are currently derived from application-level contracts and are not independently persisted.

# Call and Programme Discovery

Call and programme discovery are validated capabilities rather than a universal document parser.

```text
Source
    ↓
Document Structure Detection
    ↓
Call detection
    ↓
Programme discovery strategy (BOE, BOJA, Archiveros layouts)
    ↓
Study Programme Units
```

A unit usually lists several subjects ("La Ley X. El recurso Y. ..."). A study topic is recognised from the unit's leading statement (its first sentence), so a later mention of another law does not make the unit that law. The rest of the wording is kept as the unit's official scope. A topic whose material is designed around a concrete scope also requires the wording to ask for exactly what the material covers (`states_subject_with_scope`): every subtopic the material covers must be asked for, and every statement of the wording must be accounted for by the topic. A syllabus that opens with the same subject but lists other subtopics, or asks for more than the material covers, is not presented as covered.

Real samples demonstrate different document structures. The current implementation recognizes only the minimum deterministic structures justified by those samples. `Tema` identifiers and other structured identifiers are preserved as text and are not assigned semantic meaning.

The current validated structural representation preserves raw marker information, marker classification, hierarchy level, parent relationship and continuation text. `STRUCTURAL` and `ENUMERATION` are processing classifications; they do not imply domain semantics beyond the validated hierarchy behavior.

Scanned PDFs remain outside the supported extraction boundary; OCR is future work.

Two units with similar wording are not assumed to be the same requirement. Semantic entity resolution is not currently implemented.

# Knowledge Acquisition Boundary

AT-043 established the first autonomous acquisition experiment and AT-113 brought acquisition into the product for the first normative topics. Its architecture intentionally separates:

```text
Knowledge Need
      ↓
Authoritative source (catalog entry)
      ↓
Retrieved source content
      ↓
Article extraction
      ↓
Study material (Knowledge) with explicit aspect-to-article mapping
```

The implementation currently covers two BOE laws with a deterministic article extractor. The earlier local-PDF acquisition prototype with literal line matching was retired once article-level acquisition replaced it. This is evidence for the architecture of the workflow, not a commitment to BOE-only acquisition.

Provider-specific document structures must remain outside the domain model. Different BOE documents, and different providers, may expose different layouts or levels of structure. A source adapter may exploit known structure when evidence justifies it, but the domain must continue to represent `Source`, `KnowledgeNeed` and `Knowledge` independently.

Acquired content may contain material that is not part of what a candidate needs. Therefore the following distinction must remain explicit:

```text
Source Material
      ≠
Relevant Content
      ≠
Validated / Canonical Knowledge
```

Semantic validation, completeness assessment, richer provenance, freshness and quality scoring remain future capabilities until a concrete candidate-facing workflow requires them.

# Knowledge Need Boundary

The current validated progression is:

```text
Study Programme Unit (requirement)
    ↓
Knowledge Need
    ↓
Knowledge
    ↓
Coverage
```

Acquisition and curation extend the implementation around `KnowledgeNeed` without changing this domain boundary.

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

- interpreting a programme unit into several finer needs automatically;
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
