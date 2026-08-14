# Backlog

# Document Information

| Field | Value |
| --- | --- |
| Project | Atanor |
| Document | BACKLOG |
| Status | 🟢 Active |
| Version | 3.1 |
| Last Updated | 2026-08-14 |
| Audience | Contributors and Developers |

---

# Backlog Status

| Metric | Value |
| --- | ---: |
| Total Tasks | 39 |
| Pending | 1 |
| In Progress | 1 |
| Completed | 30 |
| Deferred | 3 |
| Cancelled | 5 |
| Blocked | 0 |

**Current Epic:** Epic K · MVP Requirement Workflow

**Current Task:** AT-039 — Integrate Requirement Discovery with Automatic Resolution

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

AT-037 added integration coverage for the complete workflow and established the sample-based flow tests used to identify subsequent product gaps.

### AT-038 · Automatic Requirement Resolution

**Status: Completed**

**Goal:** transform discovered requirement candidates into reliable Requirements without requiring the user to determine whether Atanor's output is relevant or correctly identified.

AT-038 established the minimum automatic resolution contract. A candidate is resolved only when exactly one deterministic match is available; no match or multiple matches produce `UNRESOLVED`. The candidate's original source provenance is preserved.

The implementation deliberately does not introduce semantic AI/NLP, confidence scoring, OCR, user-facing validation or a permanent curation UI. Expert curation remains an internal future mechanism for genuine unresolved or discrepant cases.

Automated tests cover both component behavior and product-oriented resolution flows using the available real samples. The suite now contains **71 passing tests**.

### AT-039 · Integrate Requirement Discovery with Automatic Resolution

**Status: In Progress**

**Goal:** connect the existing requirement-discovery workflow with the automatic-resolution contract so that Atanor can process discovered candidates as a continuous product flow rather than exposing separate technical capabilities.

The task is intentionally focused on integration, not on improving the resolution algorithm. The existing discovery pipeline should produce candidates with provenance, and the resolution step should consume those candidates and produce resolved or unresolved outcomes without requiring user validation.

Target flow:

```text
Convocatoria PDF
      ↓
Source import
      ↓
Text extraction
      ↓
Requirement discovery
      ↓
Requirement candidates
      ↓
Automatic resolution
      ↓
┌───────────────┬────────────────┐
│               │                │
RESOLVED     UNRESOLVED      DISCREPANCY
│               │                │
continue       internal        internal
               curation        curation
```

### AT-039 Scope

- Connect discovered requirement candidates to the automatic resolver.
- Preserve candidate source provenance through the integrated flow.
- Define the minimum application-level orchestration required by the workflow.
- Add integration/flow tests covering successful and unresolved paths.
- Use the existing BOE, BOCyL and Ayuntamiento de León samples where the current extraction capabilities permit.
- Make the current unsupported scanned-PDF behavior explicit rather than solving OCR prematurely.

### Explicitly Outside AT-039

- Improving PDF extraction quality.
- OCR.
- Semantic NLP, LLM or fuzzy matching.
- Confidence/scoring systems.
- Automatic scope or Knowledge Need generation.
- Expert administration UI.
- Persistent curation history.
- Knowledge acquisition or content generation.

### AT-039 Completion Criterion

A supported convocatoria can flow from imported source through requirement discovery into automatic resolution without requiring a user-facing validation step. Resolved candidates continue through the workflow, unresolved candidates are represented for later internal curation, provenance remains intact, and the complete behavior is covered by automated flow tests.

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

AT-038 did not introduce a new debt item. The resolution contract instead provides a concrete boundary for future semantic-resolution improvements.

---

# Domain Model Direction

The current direction remains intentionally minimal:

```text
Source
  ↓
Requirement discovery
  ↓
Requirement candidate
  ↓
Automatic resolution
  ↓
Requirement / unresolved case
  ↓
Requirement Scope
  ↓
Knowledge Need
  ↓
Available Knowledge
  ↓
Derived Coverage
```

Requirement discovery preserves source expressions and provenance. Automatic resolution now forms the next application-level step. The Knowledge model should evolve only when a concrete workflow requires it.

---

# Active Backlog Summary

The foundation, requirement discovery, structured discovery, requirement scope/knowledge-need modeling, coverage evaluation, documentation re-evaluation, first real-sample workflow and automatic requirement resolution contract are complete. AT-038 is validated with **71 passing tests**.

The active implementation step is **AT-039 — Integrate Requirement Discovery with Automatic Resolution**. This connects the existing source/discovery workflow to automatic resolution so that Atanor begins behaving as a product pipeline rather than as a collection of independently validated capabilities. The user remains outside the validation process and should ultimately receive the resulting study requirements directly.
