# Backlog

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | BACKLOG                     |
| Status       | 🟢 Active                   |
| Version      | 2.0                         |
| Last Updated | 2026-08-13                  |
| Audience     | Contributors and Developers |

---

# Purpose

This backlog defines the implementation plan for Atanor.

It is a technical planning tool that decomposes the project's strategic direction into implementable tasks.

The backlog is intentionally more detailed than the roadmap. There is no requirement for a one-to-one correspondence between roadmap milestones and backlog tasks.

Technical implementation details belong in the corresponding commits and Architecture Decision Records (ADRs), not in the backlog.

---

# Backlog Status

| Metric      | Value |
| ----------- | ----: |
| Total Tasks |    32 |
| Pending     |     3 |
| In Progress |     0 |
| Completed   |    21 |
| Deferred    |     3 |
| Cancelled   |     5 |
| Blocked     |     0 |

**Current Epic:** Epic H · Structured Requirement Discovery

**Next Task:** AT-030 · Define structured requirement sections

> These figures reflect the current task inventory. They should be updated whenever task status changes.

---

# Task Status

- ⬜ Pending
- 🟡 In Progress
- ✅ Completed
- ❌ Cancelled
- ⏸ Deferred
- ⛔ Blocked

---

# Priority

- 🔴 High
- 🟡 Medium
- 🟢 Low

---

# Backlog Governance

The backlog defines the implementation plan of the project, not its technical specification.

## Principles

- Task identifiers are unique and immutable once work has started.
- Once a task enters **In Progress**, its definition is considered frozen.
- Implementation details belong in commits and technical documentation.
- Additional work discovered during implementation must be evaluated as new work.
- Tasks may be cancelled if they no longer provide value or are considered premature.
- Cancelled task identifiers are never reused.
- Deferred tasks retain their identifiers and are not part of the active implementation sequence.
- Git history is the project's technical record; the backlog reflects planning and execution status.
- A single push should normally represent one isolated backlog task.
- Implemented functionality should be validated by automated tests whenever practical.
- Quality infrastructure may be brought forward when an active implementation task requires it.
- User interfaces are implementations of application use cases, not architectural dependencies of the domain.
- Technology choices for user interfaces should be justified by concrete product requirements rather than introduced speculatively.

---

# Completed Foundation

The initial foundation and source workflow are complete through **AT-016**.

## Epic A · Infrastructure

| ID     | Task                                | Priority | Status |
| ------ | ----------------------------------- | :------: | :------: |
| AT-001 | Create initial repository structure |    🔴    |    ✅   |
| AT-002 | Initialize backend project          |    🔴    |    ✅   |
| AT-003 | Initialize frontend project         |    🔴    |    ✅   |
| AT-004 | Configure initial Docker Compose    |    🔴    |    ❌   |
| AT-005 | Configure environment variables     |    🔴    |    ❌   |

AT-004 was cancelled because containerized infrastructure is not currently required. AT-005 was cancelled when configuration requirements were simplified and consolidated into the backend configuration work.

---

## Epic B · Backend

| ID     | Task                           | Priority | Status |
| ------ | ------------------------------ | :------: | :------: |
| AT-006 | Initialize FastAPI application |    🔴    |    ✅   |
| AT-007 | Implement configuration system |    🔴    |    ✅   |
| AT-008 | Configure logging              |    🟡    |    ✅   |
| AT-009 | Implement health endpoint      |    🟡    |    ✅   |

---

## Epic C · Persistence

| ID     | Task                        | Priority | Status |
| ------ | --------------------------- | :------: | :------: |
| AT-010 | Configure persistence layer |    🔴    |    ✅   |
| AT-011 | Define initial domain model |    🔴    |    ✅   |
| AT-012 | Configure migrations        |    🟡    |    ✅   |

### Current Domain-Model Direction

The conceptual work performed before implementing AT-010 and AT-011 established that the initial domain model should be a minimal, extensible foundation rather than a complete representation of the future Atanor knowledge system.

The current domain core consists of:

```text
Requirement
    └── Blueprint
            └── Knowledge Requirement
                    └── Knowledge
                            └── Source(s)
```

The model deliberately separates the need for knowledge (`Requirement`), its expected knowledge coverage (`Blueprint` and `KnowledgeRequirement`), reusable canonical knowledge (`Knowledge`), and information provenance (`Source`).

This is intentionally narrower than the broader domain hypothesis. Concepts such as knowledge assertions, evidence, learning paths, assessments, knowledge hierarchies, and other future extensions remain outside the initial implementation until concrete requirements justify them.

The domain model is expected to evolve organically. New concepts should be introduced as new entities or relationships when required rather than being anticipated as speculative fields or structures in the existing core.

### AT-012 Completion Note

AT-012 established Alembic as the controlled schema migration mechanism. The current persistence schema is represented by an initial migration, and future persistent schema changes must be introduced through explicit, reviewed migrations. The migration lifecycle is covered by automated tests, including upgrade and downgrade validation.

---

## Epic D · Product Interaction

The first user-facing work was intentionally technology-neutral. Atanor validated application behavior and user workflows before committing to a permanent UI framework.

| ID     | Task                                      | Priority | Status |
| ------ | ----------------------------------------- | :------: | :------: |
| AT-013 | Reorganize product interaction roadmap    |    🔴    |    ✅   |
| AT-014 | Define first application use cases        |    🔴    |    ✅   |
| AT-015 | Build minimal CLI interface               |    🟡    |    ✅   |
| AT-016 | Validate first end-to-end user workflow   |    🔴    |    ✅   |

### AT-013 Completion Note

AT-013 reviewed and reorganized the planned user-facing work so that product behavior and application use cases precede concrete UI technology. React, Qt, and other UI frameworks are deliberately deferred until validated requirements justify them. The backlog now treats the UI as a replaceable implementation of application use cases rather than a dependency of the domain.

### AT-014 Completion Note

AT-014 established the first application use case around the MVP entry point: importing an official examination call from a local PDF and representing it as a persisted `Source`. The implementation keeps the source as a reference to the external document rather than storing the document itself, and separates the application workflow from domain and persistence details. The slice includes PDF input validation, source persistence and retrieval, UTC timestamp handling, an Alembic migration, and automated tests including a synthetic PDF. PDF content extraction, requirement generation, external URLs and source discovery remain future work.

### AT-015 Completion Note

AT-015 added the first technology-neutral user interface adapter: a minimal Python standard-library CLI using `argparse`. The CLI exposes the `import-source` workflow and delegates to the existing application use case and persistence layer without introducing new framework dependencies. It includes automated tests for successful PDF import and invalid input handling. This validates the first practical interaction with Atanor while keeping the UI implementation replaceable.

### AT-016 Completion Note

AT-016 completed the first usable Source workflow end to end: a PDF can be imported, persisted, retrieved and listed through the CLI. Source identity is represented by a UUID and is deliberately separated from the external document locator, avoiding coupling entity identity to a local file path. The workflow is covered by automated application, persistence, migration and end-to-end tests using isolated temporary SQLite databases and synthetic PDFs. The local development database remains an ignored artifact and is not required by the test suite.

### UI Decoupling Direction

User interfaces must depend on application use cases rather than directly on domain persistence details. The concrete interface implementation should remain replaceable so that a CLI, desktop UI, web UI, or future alternative can evolve without coupling the domain model to a specific UI technology.

No permanent commitment to React, Qt, or another UI framework is made at this stage. Such a decision should follow demonstrated product requirements.

---

# Deferred Development Quality Tooling

The following tasks remain recorded but are intentionally deferred. They are not part of the active implementation sequence and should only be brought forward when a concrete development need justifies them.

| ID     | Task                         | Priority | Status |
| ------ | ---------------------------- | :------: | :------: |
| AT-017 | Configure Ruff               |    🟡    |    ⏸   |
| AT-018 | Configure Pyright            |    🟡    |    ⏸   |
| AT-019 | Configure pre-commit hooks   |    🟡    |    ⏸   |

These identifiers are retained and will not be reused.

---

## AT-020 · Testing Framework

AT-020 was brought forward because AT-010 required automated persistence tests. It established the minimum project-wide testing foundation required before further persistence behavior was implemented.

| ID     | Task                         | Priority | Status |
| ------ | ---------------------------- | :------: | :------: |
| AT-020 | Configure testing framework |    🟡    |    ✅   |

---

# Superseded Application Workflow Tasks

The following tasks were part of the original First Running System plan. The application workflow was brought forward and implemented through AT-015 and AT-016, so these tasks no longer provide independent value.

| ID     | Task                                   | Priority | Status |
| ------ | -------------------------------------- | :------: | :------: |
| AT-021 | Integrate interface with application   |    🔴    |    ❌   |
| AT-022 | Expose first application workflow      |    🟡    |    ❌   |
| AT-023 | Verify end-to-end execution            |    🔴    |    ❌   |

### Cancellation Reason

- **AT-021** was superseded by the application/interface integration delivered through AT-015.
- **AT-022** was superseded by the first exposed application workflow delivered through AT-015.
- **AT-023** was superseded by the end-to-end validation delivered through AT-016.

The identifiers remain recorded to preserve planning history and are never reused.

---

# Epic G · Requirement Discovery

**Status: 🟢 Completed**

## Objective

Transform an imported authoritative source into explicit, structured requirement candidates that can be evaluated and used as the entry point for subsequent knowledge construction.

The epic intentionally stops at validating the workflow:

```text
Source
  ↓
Requirement Discovery
  ↓
Requirement candidates
```

It does not claim semantic requirement resolution or complete extraction of all requirements from arbitrary convocatorias.

## Core Constraints

### Source structures are not universal

Different sources may use different document structures. Sources originating from the same provider may share a useful pattern, while sources from different providers may not.

Requirement discovery should therefore allow source- or format-specific extraction strategies without making any single document structure intrinsic to the domain model.

The initial implementation remains simple and deterministic. Generalized parser frameworks should only be introduced when real sources demonstrate a need for them.

### Requirement expressions are not canonical requirements

A source may express the same requirement in different ways, for example:

```text
Constitución Española
Constitución
Constitución de España
Constitución de 1978
```

Requirement discovery must distinguish the original expression found in the source from the normalized requirement it represents.

The original expression and its source location remain traceable. General semantic equivalence and canonical resolution are intentionally outside this epic.

## Tasks

| ID | Task | Priority | Status |
| ------ | --------------------------------------------- | :------: | :------: |
| AT-024 | Define requirement discovery use case          |    🔴    |    ✅   |
| AT-025 | Extract text from PDF sources                  |    🔴    |    ✅   |
| AT-026 | Identify and normalize requirement candidates |    🔴    |    ✅   |
| AT-027 | Persist discovered requirements                |    🔴    |    ✅   |
| AT-028 | Expose requirement inspection                  |    🟡    |    ✅   |
| AT-029 | Validate requirement discovery end-to-end      |    🔴    |    ✅   |

### AT-024 · Define Requirement Discovery Use Case

**Status: Completed**

Defined and implemented the application-level workflow that transforms a source into requirement mentions while keeping extraction strategy separate from the canonical domain concept. Requirement mentions remain application-level data and are not persisted separately at this stage.

### AT-025 · Extract Text from PDF Sources

**Status: Completed**

Implemented isolated, testable text extraction for supported PDF sources using `pypdf`. The extractor validates the source locator, file existence and PDF type, then extracts page content in document order. Tests use self-contained synthetic PDFs and cover multi-page ordering and invalid input.

### AT-026 · Identify and Normalize Requirement Candidates

**Status: Completed**

Implemented a first deterministic candidate-detection pass over extracted text. Numbered lines are identified as requirement mentions while preserving their original expression, source identity and line-based locator. Normalization is deliberately limited to basic whitespace cleanup. No semantic equivalence, canonical requirement resolution, generalized parser framework or persistence model was introduced.

### AT-027 · Persist Discovered Requirements

**Status: Completed**

Persisted discovered requirements using the existing domain and SQLAlchemy persistence patterns. Each discovered requirement retains a mandatory `source_id`, preserving end-to-end provenance. The implementation intentionally does not persist requirement mentions separately and does not perform semantic deduplication or identity resolution.

### AT-028 · Expose Requirement Inspection

**Status: Completed**

Added minimal CLI inspection for discovered requirements, including the empty-result case and persisted synthetic requirements. The CLI delegates to the application and persistence layers without coupling the domain to the interface.

### AT-029 · Validate Requirement Discovery End-to-End

**Status: Completed**

Validated the complete PDF discovery workflow against real samples. A text-based BOE PDF successfully passed through PDF extraction and candidate discovery, producing 440 numbered candidates. This confirms the technical workflow but also demonstrates that the initial numbered-line heuristic is intentionally broad and must not yet be treated as a semantic requirement extractor. A real Ayuntamiento de León PDF without an extractable text layer was also added as a regression sample and remains unsupported until a future text-acquisition mechanism such as OCR is justified.

AT-029 deliberately stops at workflow validation. Improving extraction precision, resolving semantic equivalence, parsing provider-specific structures, and supporting scanned PDFs are future work rather than completion criteria for this task.

---

# Epic H · Structured Requirement Discovery

**Status: 🔵 Active**

## Objective

Improve requirement discovery from the broad candidate extraction validated in Epic G by using the document structure and context of real convocatorias.

The immediate goal is not semantic entity resolution. It is to distinguish likely knowledge-bearing sections from general administrative text and to preserve the structure needed for later requirement modeling.

The epic starts from evidence gathered in AT-029: a real BOE document can be extracted end to end, but a simple numbered-line detector produced 440 candidates across the full document.

## Core Constraints

- Do not assume that all convocatorias share one document structure.
- Prefer explicit, deterministic structural signals over speculative NLP or semantic infrastructure.
- Provider-specific strategies are acceptable when justified by real samples.
- Preserve source expressions and provenance.
- Do not introduce canonical requirement resolution merely because equivalent expressions exist; that remains a separate concern until concrete examples require it.
- Keep scanned-PDF/OCR support outside the immediate scope unless a concrete next task demonstrates that it blocks the product workflow.

## Initial Tasks

| ID | Task | Priority | Status |
| ------ | --------------------------------------------- | :------: | :------: |
| AT-030 | Define structured requirement sections        |    🔴    |    ⬜   |
| AT-031 | Extract requirements from a known structured section |    🔴    |    ⬜   |
| AT-032 | Validate discovery against multiple real source structures |    🟡    |    ⬜   |

These tasks are intentionally small. Further decomposition should be driven by the evidence obtained from the real samples rather than by anticipating every possible convocatoria format.

---

# Domain Model Direction After Requirement Discovery

Requirement Discovery preserves the distinction between:

```text
Source expression / mention
        ↓
Candidate / structured requirement
        ↓
Canonical Requirement (future)
```

Different source expressions may refer to the same requirement. Source expression, provenance and location must remain traceable even when the canonical requirement is shared.

Requirements discovered from sources currently require a `source_id`, making provenance explicit and mandatory. Future requirement creation mechanisms should define their origin explicitly rather than weakening this traceability with an implicit optional source.

Semantic entity resolution should remain a future capability and should only be introduced when real source examples demonstrate that deterministic normalization is insufficient.

---

# Future Direction

The next stages remain intentionally evidence-driven:

```text
Source
    ↓
Structured Requirement Discovery
    ↓
Requirement
    ↓
Scope Discovery
    ↓
Knowledge Blueprint
    ↓
Knowledge Assessment
    ↓
Canonical Knowledge
```

The implementation should continue to move one validated slice at a time. No permanent UI framework, OCR subsystem, generalized parser framework or semantic matching infrastructure should be introduced without a concrete product need.

---

# Living Document

This backlog evolves together with the project.

Tasks may be added, cancelled, deferred or reprioritized as development progresses, provided such changes remain aligned with the roadmap, foundations and development conventions.

The objective is to maintain a backlog that is concise, accurate and focused on delivering incremental value.
