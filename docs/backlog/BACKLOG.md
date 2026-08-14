# Backlog

# Document Information

| Field | Value |
| --- | --- |
| Project | Atanor |
| Document | BACKLOG |
| Status | 🟢 Active |
| Version | 3.0 |
| Last Updated | 2026-08-14 |
| Audience | Contributors and Developers |

---

# Backlog Status

| Metric | Value |
| --- | ---: |
| Total Tasks | 38 |
| Pending | 1 |
| In Progress | 0 |
| Completed | 29 |
| Deferred | 3 |
| Cancelled | 5 |
| Blocked | 0 |

**Current Epic:** Epic K · MVP Requirement Workflow

**Current Task:** AT-038 — Automatic Requirement Resolution

---

# Backlog Governance

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
- User interfaces are implementations of application use cases, not architectural dependencies of the domain.
- Technology choices for user interfaces should be justified by concrete product requirements rather than introduced speculatively.
- Development should be driven by concrete user needs and validated MVP workflows rather than by speculative architecture.
- The domain and persistence model should remain flexible and minimal; new abstractions require concrete evidence.

---

# Completed Foundation

The initial foundation and source workflow are complete through **AT-016**.

## Epic A · Infrastructure

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-001 | Create initial repository structure | 🔴 | ✅ |
| AT-002 | Initialize backend project | 🔴 | ✅ |
| AT-003 | Initialize frontend project | 🔴 | ✅ |
| AT-004 | Configure initial Docker Compose | 🔴 | ❌ |
| AT-005 | Configure environment variables | 🔴 | ❌ |

AT-004 was cancelled because containerized infrastructure is not currently required. AT-005 was cancelled when configuration requirements were simplified and consolidated into backend configuration.

## Epic B · Backend

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-006 | Initialize FastAPI application | 🔴 | ✅ |
| AT-007 | Configure configuration system | 🔴 | ✅ |
| AT-008 | Configure logging | 🟡 | ✅ |
| AT-009 | Implement health endpoint | 🟡 | ✅ |

## Epic C · Persistence

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-010 | Configure persistence layer | 🔴 | ✅ |
| AT-011 | Define initial domain model | 🔴 | ✅ |
| AT-012 | Configure migrations | 🟡 | ✅ |

The domain model is intentionally minimal and extensible. New concepts are introduced only when concrete requirements justify them.

## Epic D · Product Interaction

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-013 | Reorganize product interaction roadmap | 🔴 | ✅ |
| AT-014 | Define first application use cases | 🔴 | ✅ |
| AT-015 | Build minimal CLI interface | 🟡 | ✅ |
| AT-016 | Validate first end-to-end user workflow | 🔴 | ✅ |

User interfaces remain replaceable implementations of application use cases.

---

# Deferred Development Quality Tooling

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-017 | Configure Ruff | 🟡 | ⏸ |
| AT-018 | Configure Pyright | 🟡 | ⏸ |
| AT-019 | Configure pre-commit hooks | 🟡 | ⏸ |
| AT-020 | Configure testing framework | 🟡 | ✅ |

AT-021 to AT-023 were cancelled/superseded by the workflow implemented through AT-015 and AT-016. Cancelled identifiers are retained and never reused.

---

# Epic G · Requirement Discovery

**Status: 🟢 Completed**

Objective: transform imported authoritative sources into explicit requirement candidates while preserving provenance. Semantic resolution and arbitrary-document completeness remain outside scope.

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-024 | Define requirement discovery use case | 🔴 | ✅ |
| AT-025 | Extract text from PDF sources | 🔴 | ✅ |
| AT-026 | Identify and normalize requirement candidates | 🔴 | ✅ |
| AT-027 | Persist discovered requirements | 🔴 | ✅ |
| AT-028 | Expose requirement inspection | 🟡 | ✅ |
| AT-029 | Validate requirement discovery end-to-end | 🔴 | ✅ |

AT-029 established the initial PDF workflow and confirmed that scanned PDFs without an extractable text layer remain unsupported.

---

# Epic H · Structured Requirement Discovery

**Status: 🟢 Completed**

Objective: improve discovery using deterministic document structure and real convocatoria evidence without assuming a universal provider format.

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-030 | Define structured requirement sections | 🔴 | ✅ |
| AT-031 | Extract requirements from a known structured section | 🔴 | ✅ |
| AT-032 | Validate discovery against multiple real source structures | 🟡 | ✅ |

The BOE, BOCyL and Ayuntamiento de León samples demonstrated that source structures differ and that scanned-PDF/OCR support should remain deferred until required by a concrete workflow.

---

# Epic I · Requirement Scope & Knowledge Needs

**Status: 🟢 Completed**

Objective: represent knowledge coverage required by a requirement in a contextual scope independently of whether corresponding knowledge exists.

| ID | Task | Priority | Status |
 | --- | --- | :---: | :---: |
| AT-033 | Define Requirement Scope and Knowledge Need | 🔴 | ✅ |
| AT-034 | Persist Requirement Scope and Knowledge Needs | 🔴 | ✅ |
| AT-035 | Evaluate Knowledge Coverage | 🔴 | ✅ |

The validated model distinguishes `RequirementScope`, `KnowledgeNeed`, available `Knowledge`, and derived `Coverage`. Coverage currently uses only `COVERED` and `MISSING`; richer semantics remain deferred until justified by concrete use cases. The superseded `Blueprint` / `KnowledgeRequirement` model was removed rather than retained in parallel.

---

# Epic J · Documentation Re-evaluation

**Status: 🟢 Completed**

## AT-036 · Re-evaluate and Update Project Documentation

Updated README, Foundations, Architecture and Roadmap documentation to reflect the validated model and MVP-oriented development strategy. Development conventions were separated from architecture because they represent project-wide practices. No documentation split was introduced without a concrete maintainability benefit.

---

# Epic K · MVP Requirement Workflow

**Status: 🟢 Active**

Objective: build the first product-oriented vertical slice of Atanor around a concrete user need: transform a supported convocatoria PDF into useful study requirements without transferring semantic validation work to the user. The product should resolve discovered requirements automatically where possible and surface only genuine discrepancies or unresolved cases for internal expert curation.

### AT-037 · Validate the First MVP Requirement Workflow

**Status: Completed**

Validated the complete workflow against real samples:

```text
PDF convocatoria
      ↓
Source import
      ↓
Text extraction
      ↓
Structured requirement discovery
      ↓
Requirement persistence
      ↓
Requirement retrieval
```

The BOE and BOCyL samples validate text-based workflows with different document structures. The Ayuntamiento de León scanned sample validates the explicit unsupported-text-layer behavior. Source provenance is preserved and the resulting Requirements survive persistence and retrieval.

AT-037 added integration coverage for the complete workflow. The complete test suite contains **64 passing tests**.

No OCR, semantic NLP, AI, generalized provider parser architecture or automatic scope/knowledge generation was introduced. These remain deferred until concrete product evidence requires them.

### AT-038 · Automatic Requirement Resolution

**Status: Pending**

**Goal:** transform discovered requirement candidates into reliable Requirements without requiring the user to determine whether Atanor's output is relevant or correctly identified.

Atanor should attempt to resolve discovered candidates automatically against the knowledge and requirement concepts already available to the system. The normal product path is automatic resolution. Expert intervention is an internal exception-handling and curation mechanism for genuine discrepancies or unresolved cases, not a user-facing validation workflow.

Initial conceptual flow:

```text
Imported convocatoria
        ↓
Discovered candidates
        ↓
Automatic resolution
        ↓
   ┌────┼──────────┐
   ↓    ↓          ↓
RESOLVED  DISCREPANCY  UNRESOLVED
   ↓         ↓             ↓
continue   expert       curation
              \          /
               ↓        ↓
             resolved result
```

The first implementation should remain deliberately small. It should establish the minimum contract required to distinguish confidently resolved candidates from cases that require further attention, without prematurely introducing semantic AI/NLP, complex confidence models or a permanent administration UI.

### AT-038 Scope

- Define the minimum domain/application contract for automatic requirement resolution.
- Resolve candidates against known concepts where a deterministic resolution is sufficiently reliable.
- Preserve the original source expression and provenance.
- Represent unresolved or discrepant candidates without exposing the internal process as a required user workflow.
- Make expert review possible as an internal curation path when automatic resolution is insufficient.
- Ensure a successful curation decision can improve future automatic resolution rather than repeatedly resolving identical candidates.
- Validate the behavior with automated tests, starting from concrete resolution cases.

### Explicitly Outside AT-038

- User-facing requirement validation or approval workflows.
- Semantic AI/NLP or LLM-based resolution.
- A sophisticated statistical confidence/scoring system.
- OCR.
- Automatic scope generation beyond what concrete resolution cases require.
- Automatic Knowledge Need generation.
- Knowledge construction or acquisition.
- Permanent administration UI.
- Generalized provider parsing.
- Rich coverage semantics.

### AT-038 Completion Criterion

A discovered requirement candidate can be automatically resolved when the current knowledge is sufficient, while unresolved or conflicting cases are represented for internal expert curation. The original provenance is preserved, the automated path is covered by tests, and the design permits later improvements to resolution mechanisms without changing the user-facing product contract.

---

# Known Technical Debt & Deferred Concerns

These items are tracked deliberately but do not currently block MVP-oriented work. They become implementation tasks only when their cost, risk or product value justifies them.

| ID | Concern | Current Decision | Trigger for Re-evaluation |
| --- | --- | --- | --- |
| TD-001 | Static type checking | Keep AT-018 deferred. | Type-related regressions or increasing cross-layer complexity. |
| TD-002 | Automated linting / pre-commit | Keep AT-017 and AT-019 deferred. | Growing codebase, CI adoption or additional contributors. |
| TD-003 | Requirement/Source identifier consistency | `Requirement` currently uses `int`, while `Source` uses `UUID`. | A concrete persistence/API requirement or broader identity refactor. |
| TD-004 | `RequirementScope` builder identity semantics | Review whether modifying a persisted scope must preserve or replace its identity. | The builder is used in a workflow that mutates/replaces persisted scopes. |
| TD-005 | Error and edge-case coverage | Expand incrementally alongside product workflows. | A concrete failure mode is discovered or a workflow becomes user-facing. |
| TD-006 | CLI inspection completeness | Existing CLI is sufficient for current development validation. | CLI becomes a primary user workflow or manual inspection becomes a bottleneck. |
| TD-007 | Scanned PDF / OCR support | Explicitly unsupported; Ayuntamiento de León remains a regression case. | A real MVP workflow requires scanned convocatorias. |
| TD-008 | Richer Knowledge Coverage | Keep `COVERED/MISSING`; defer `PARTIAL`, depth-aware and semantic matching. | An open-domain use case demonstrates binary coverage is insufficient. |
| TD-009 | Generalized provider-specific parsing | Current strategies are driven by observed real samples. | More source formats require repeated structural adaptations. |

AT-037 did not introduce a new debt item. Its real-sample validation strengthens the evidence behind TD-007 and TD-009, but neither currently justifies implementation. No debt item is being promoted prematurely.

---

# Domain Model Direction

The current direction remains intentionally minimal:

```text
Source
  ↓
Requirement discovery
  ↓
Requirement
  ↓
Requirement Scope
  ↓
Knowledge Need
  ↓
Available Knowledge
  ↓
Derived Coverage
```

Requirement discovery preserves source expressions and provenance. Automatic semantic resolution is now the next MVP concern. The Knowledge model should evolve only when a concrete workflow requires it.

---

# Active Backlog Summary

The foundation, requirement discovery, structured discovery, requirement scope/knowledge-need modeling, coverage evaluation, documentation re-evaluation and first real-sample requirement workflow are complete. AT-037 validated the first MVP requirement vertical slice with 64 passing tests.

The next implementation step is **AT-038 — Automatic Requirement Resolution**. This moves Atanor from merely producing discovered Requirements to automatically determining what those requirements represent, while keeping expert curation as an internal fallback for discrepancies and unresolved cases. The user remains outside this validation process and should ultimately receive the resulting study requirements directly.
