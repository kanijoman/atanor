# Backlog

# Document Information

| Field | Value |
| --- | --- |
| Project | Atanor |
| Document | BACKLOG |
| Status | 🟢 Active |
| Version | 3.8 |
| Last Updated | 2026-08-18 |
| Audience | Contributors and Developers |

---

# Backlog Status

| Metric | Value |
| --- | ---: |
| Total Tasks | 45 |
| Pending | 1 |
| In Progress | 0 |
| Completed | 37 |
| Deferred | 3 |
| Cancelled | 5 |
| Blocked | 0 |

**Current Epic:** Epic L · Knowledge Construction

**Current Task:** AT-046 · Integrate Document Structure Analysis into the Real Processing Pipeline

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
- Technology choices should be justified by concrete product requirements rather than introduced speculatively.
- Development should be driven by concrete user needs and validated MVP workflows rather than speculative architecture.
- The domain and persistence model should remain flexible and minimal; new abstractions require concrete evidence.
- During the current early product stage, each task is a mini-MVP: a small, self-contained increment that provides value or produces actionable product knowledge.
- Future tasks are hypotheses, not commitments. Detailed future work is defined only when evidence from the preceding iteration justifies it.
- Parallel development should be introduced only when the product direction is sufficiently stable to make independent work valuable.
- `experiments/` is used for exploratory product and technical investigation. Experiments may inspect, measure or compare behavior without becoming part of the product contract.
- Tests specify validated behavior and should remain agnostic of exploratory implementation details. Observations become tests only after they are accepted as product or engineering requirements.

---

# Historical Backlog

The following tasks are completed or deferred/cancelled. Their implementation details and technical decisions are preserved in Git history and the project documentation.

## Foundation · AT-001–AT-023

| ID | Task | Status |
| --- | --- | :---: |
| AT-001 | Create initial repository structure | ✅ |
| AT-002 | Initialize backend project | ✅ |
| AT-003 | Initialize frontend project | ✅ |
| AT-004 | Configure initial Docker Compose | ❌ |
| AT-005 | Configure environment variables | ❌ |
| AT-006 | Initialize FastAPI application | ✅ |
| AT-007 | Configure configuration system | ✅ |
| AT-008 | Configure logging | ✅ |
| AT-009 | Implement health endpoint | ✅ |
| AT-010 | Configure persistence layer | ✅ |
| AT-011 | Define initial domain model | ✅ |
| AT-012 | Configure migrations | ✅ |
| AT-013 | Reorganize product interaction roadmap | ✅ |
| AT-014 | Define first application use cases | ✅ |
| AT-015 | Build minimal CLI interface | ✅ |
| AT-016 | Validate first end-to-end user workflow | ✅ |
| AT-017 | Configure Ruff | ⏸ |
| AT-018 | Configure Pyright | ⏸ |
| AT-019 | Configure pre-commit hooks | ⏸ |
| AT-020 | Configure testing framework | ✅ |
| AT-021 | Superseded | ❌ |
| AT-022 | Superseded | ❌ |
| AT-023 | Superseded | ❌ |

AT-004 and AT-005 were cancelled. AT-017–AT-019 remain deferred. AT-021–AT-023 were cancelled/superseded by the validated workflow and their identifiers are retained.

## Epic G · Requirement Discovery · AT-024–AT-029

| ID | Task | Status |
| --- | --- | :---: |
| AT-024 | Define requirement discovery use case | ✅ |
| AT-025 | Extract text from PDF sources | ✅ |
| AT-026 | Identify and normalize requirement candidates | ✅ |
| AT-027 | Persist discovered requirements | ✅ |
| AT-028 | Expose requirement inspection | ✅ |
| AT-029 | Validate requirement discovery end-to-end | ✅ |

The initial PDF workflow was validated. Scanned PDFs without a meaningful text layer remain unsupported.

## Epic H · Structured Requirement Discovery · AT-030–AT-032

| ID | Task | Status |
| --- | --- | :---: |
| AT-030 | Define structured requirement sections | ✅ |
| AT-031 | Extract requirements from a known structured section | ✅ |
| AT-032 | Validate discovery against multiple real source structures | ✅ |

Real BOE, BOCyL and Ayuntamiento de León samples demonstrated that provider structures differ and that OCR should remain deferred until required.

## Epic I · Requirement Scope & Knowledge Needs · AT-033–AT-035

| ID | Task | Status |
| --- | --- | :---: |
| AT-033 | Define Requirement Scope and Knowledge Need | ✅ |
| AT-034 | Persist Requirement Scope and Knowledge Needs | ✅ |
| AT-035 | Evaluate Knowledge Coverage | ✅ |

The validated model distinguishes `RequirementScope`, `KnowledgeNeed`, `Knowledge` and derived binary `Coverage` (`COVERED` / `MISSING`).

## Epic J · Documentation Re-evaluation · AT-036

**AT-036 · Re-evaluate and Update Project Documentation — ✅ Completed**

Project documentation was aligned with the validated domain model and MVP-oriented development strategy. Development conventions remain separate from architecture.

---

# Epic K · MVP Requirement Workflow · AT-037–AT-043

**Status: 🟢 Completed**

Objective: iteratively validate the smallest useful candidate experience. The candidate is the primary product user; curator activity remains an internal mechanism and is not a parallel MVP.

### AT-037 · Validate the First MVP Requirement Workflow — ✅

Validated the flow `PDF convocatoria → Source import → text extraction → structured discovery → persistence → retrieval` against real samples.

### AT-038 · Automatic Requirement Resolution — ✅

Established deterministic resolution: exactly one match resolves; no match or multiple matches remain `UNRESOLVED`. No semantic AI/NLP, OCR, confidence scoring or user-facing validation was introduced.

### AT-039 · Integrate Requirement Discovery with Automatic Resolution — ✅

Connected discovery and deterministic resolution into one application workflow while preserving provenance and unresolved outcomes.

### AT-040 · Produce a User-Usable Requirement Set — ✅

Introduced the minimal application-level `StudyRequirementSet`, reusing `Requirement` rather than adding a speculative domain entity. Unresolved cases remain internal.

### AT-041 · Validate the First Candidate Product Experience — ✅

Confirmed that a candidate can obtain a useful study-requirement result without understanding or validating Atanor's internal decisions.

### AT-042 · Validate Knowledge Coverage for a Candidate Requirement — ✅

Validated contextual `KnowledgeNeed`s and binary knowledge coverage while deliberately avoiding semantic matching, partial coverage and candidate-managed knowledge input.

### AT-043 · Knowledge Acquisition Prototype — ✅

Validated autonomous acquisition from an authoritative BOE source and deterministic relevance extraction. The experiment reduced approximately 328k source characters to 1,991 characters for `Constitución Española`, but the result still contained incidental references. Therefore acquisition and first-stage relevance filtering were validated, not semantic knowledge validation or canonical Knowledge construction.

AT-043 established `experiments/` as an exploratory area and confirmed that provider-specific structure must remain an implementation concern rather than a domain assumption. The suite reached 89 passing tests with no regressions.

---

# Epic L · Knowledge Construction

**Status: 🟢 Active**

Objective: progressively transform acquired authoritative source material into trustworthy, reusable knowledge while keeping document structure, acquisition and extraction strategies outside the domain model.

### AT-044 · Validate Document Structural Analysis — ✅ Completed

**Goal:** establish a useful first-stage structural analyzer for heterogeneous text-based documents without attempting universal or perfect document interpretation.

AT-044 validated deterministic structural marker detection and contextual hierarchy construction against the BOE, BOJA and Archiveros samples. The analyzer recognizes heterogeneous marker families (`numeric`, `roman`, `letter`, `topic`) and builds useful hierarchy for the observed structures.

The iteration explicitly accepts that the analyzer is heuristic rather than complete. In particular, internal enumerations such as `1`, `2`, `c`, `d` must not incorrectly become top-level document sections, while explicit nested markers and new top-level sequences must reset hierarchy context correctly. These behaviors are covered by `tests/test_document_structure.py`.

The Ayuntamiento de León sample remains `IMAGE_ONLY_OR_EMPTY` and structural analysis is skipped upstream; OCR is still outside scope.

AT-044 is closed. No further structural sophistication is planned unless a regression or a concrete product workflow demonstrates the need.

### AT-045 · Validate Contextual Hierarchy Inference — ✅ Completed

**Goal:** determine whether local structural context materially improves the separation between meaningful sections and internal enumerations across the existing real documents.

AT-045 used the four current PDF samples as an isolated experiment and classified extracted markers as `STRUCTURAL` or `ENUMERATION` before hierarchy construction. The experiment established that the distinction is useful and can be implemented with a small deterministic rule set based on local sequence and hierarchy context.

Validated behaviors include:

- simple numeric sequences can represent internal enumerations rather than new sections;
- numeric and letter markers can participate in the same local enumeration;
- an enumeration may begin after a nested structural marker;
- an explicit nested structural marker terminates the previous enumeration context;
- a new top-level sequence does not inherit a previous nested enumeration context;
- raw marker information and continuation text remain preserved;
- image-only documents remain outside structural analysis.

The behavior is covered by `tests/test_document_structure.py`. The experiment reached **9/9 focused tests and 99/99 tests in the complete suite** with no regressions.

The experiment deliberately did not introduce OCR, AI/NLP, confidence scoring, universal parsing or a new domain model. Its conclusion is that the next justified step is not more exploratory hierarchy sophistication, but integration of the validated structural analysis into the real application processing path.

AT-045 is closed.

### AT-046 · Integrate Document Structure Analysis into the Real Processing Pipeline — 🔴 Pending

**Hypothesis:** the structural analysis validated in AT-044/AT-045 becomes materially useful only when it is a real application capability consumed by the processing workflow, rather than an isolated experiment.

**Goal:** promote the minimum validated structural-analysis behavior into the application pipeline so that text extracted from a supported PDF can be transformed into an inspectable structured representation before downstream requirement/knowledge extraction.

**Mini-MVP scope:**

- Reuse the existing PDF text-extraction path; do not redesign source import or persistence.
- Introduce the smallest application-level structural-analysis component justified by AT-045.
- Keep marker extraction, classification and hierarchy inference as explicit processing stages where that separation improves testability.
- Preserve raw marker data, marker classification, hierarchy level, parent relationship and continuation text in the processing result.
- Feed the resulting structural representation into the next downstream processing stage without yet changing the domain model for `Requirement`, `KnowledgeNeed` or `Knowledge`.
- Provide a minimal application/CLI inspection path so the real pipeline can be observed on the existing BOE, BOJA and Archiveros samples.
- Preserve the current image-only behavior: scanned PDFs remain unsupported and must not trigger OCR implicitly.
- Add focused unit tests for the production structural-analysis component and at least one application-level integration test proving that extracted PDF text reaches the structural representation.
- Run the complete regression suite before closing the task.

**Explicitly outside AT-046:**

- OCR or scanned-PDF support.
- AI/NLP or external AI services.
- New semantic document models in the domain layer.
- Universal document parsing.
- Automatic canonical Knowledge construction.
- Candidate-facing UI.
- Persistence of the full structural tree unless a concrete downstream requirement demonstrates that it is necessary.
- Additional hierarchy heuristics not supported by the AT-045 evidence.

**Completion criterion:**

A supported text-based PDF can pass through the real application processing path and produce the validated structural representation, observable through a minimal inspection path and covered by focused tests plus the complete regression suite. The existing requirement/knowledge domain behavior remains unchanged. If implementation reveals that a new abstraction is required, its necessity must be demonstrated by the concrete pipeline rather than introduced speculatively.

---

# Known Technical Debt & Deferred Concerns

| ID | Concern | Current Decision | Trigger for Re-evaluation |
| --- | --- | --- | --- |
| TD-001 | Static type checking | Keep AT-018 deferred. | Type-related regressions or increasing cross-layer complexity. |
| TD-002 | Automated linting / pre-commit | Keep AT-017 and AT-019 deferred. | Growing codebase, CI adoption or additional contributors. |
| TD-003 | Requirement/Source identifier consistency | `Requirement` uses `int`; `Source` uses `UUID`. | Concrete persistence/API requirement or broader identity refactor. |
| TD-004 | `RequirementScope` builder identity semantics | Review when persisted scope mutation is required. | A workflow mutates/replaces persisted scopes. |
| TD-005 | Error and edge-case coverage | Expand incrementally with product workflows. | Concrete failure mode or user-facing workflow. |
| TD-006 | CLI inspection completeness | Sufficient for current development validation. | CLI becomes primary user workflow or manual inspection bottleneck. |
| TD-007 | Scanned PDF / OCR support | Explicitly unsupported; León sample remains a regression case. | A real MVP workflow requires scanned convocatorias. |
| TD-008 | Richer Knowledge Coverage | Keep binary `COVERED/MISSING`. | An open-domain use case demonstrates insufficiency. |
| TD-009 | Generalized provider-specific parsing | Use evidence-driven strategies; do not assume a universal template. | More formats require repeated structural adaptations. |
| TD-010 | Resolution result persistence | Current resolutions are application-level results. | Repeatability, auditability, asynchronous processing or curation becomes concrete. |
| TD-011 | Resolution algorithm sophistication | Keep deterministic and minimal. | User-oriented output demonstrates unacceptable unresolved/ambiguous rates. |
| TD-012 | Knowledge extraction quality | Current extraction may include incidental references and is not semantically complete. | Candidate-facing knowledge requires trustworthy, structured or complete knowledge. |
| TD-013 | Knowledge provenance and quality metadata | Rich freshness/evidence/confidence semantics deferred. | Acquired knowledge is presented directly to candidates or maintained over time. |

No debt item currently requires a standalone cleanup task before AT-046.

---

# Active Backlog Summary

The foundation, requirement discovery, structured discovery, requirement scope/knowledge-need modeling, coverage evaluation, documentation re-evaluation, first candidate workflow, automatic requirement resolution, user-oriented requirement projection, candidate validation, knowledge coverage validation, knowledge acquisition prototype, structural document analysis and contextual hierarchy inference are complete.

**Current status: 37 completed tasks, 1 pending, 3 deferred, 5 cancelled, 0 in progress.**

AT-045 is closed after validating the `STRUCTURAL / ENUMERATION` distinction with 99/99 tests passing. **AT-046 is now the active mini-MVP**, selected directly from that evidence: promote the validated structural analysis into the real application processing pipeline, keeping the implementation minimal and the domain model unchanged.
