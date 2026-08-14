# Backlog

# Document Information

| Field | Value |
| --- | --- |
| Project | Atanor |
| Document | BACKLOG |
| Status | 🟢 Active |
| Version | 3.4 |
| Last Updated | 2026-08-14 |
| Audience | Contributors and Developers |

---

# Backlog Status

| Metric | Value |
| --- | ---: |
| Total Tasks | 41 |
| Pending | 0 |
| In Progress | 1 |
| Completed | 32 |
| Deferred | 3 |
| Cancelled | 5 |
| Blocked | 0 |

**Current Epic:** Epic K · MVP Requirement Workflow

**Current Task:** AT-041 — Validate the First Candidate Product Experience

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
- During the current early product stage, each task should be treated as a mini-MVP: a small, self-contained increment that provides value or produces actionable product knowledge.
- Future tasks are hypotheses, not commitments. Detailed future work should be defined only when evidence from the preceding iteration justifies it.
- Parallel development should be introduced only when the product direction is sufficiently stable to make independent work valuable.

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

Objective: iteratively discover and validate the smallest useful candidate experience. At this stage the backlog intentionally avoids predicting the complete product journey. Each task is a mini-MVP whose outcome determines the next hypothesis.

Atanor has two conceptual user profiles:

- **Candidate:** the primary product user and the focus of the MVP.
- **Curator:** the internal/expert role that may resolve ambiguities, fill knowledge gaps or validate information when automation cannot do so reliably.

Curator functionality is not a parallel MVP. Dedicated curator tooling should be introduced only when it is demonstrated to be necessary to provide, validate or scale the candidate experience.

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

**Status: Completed**

**Goal:** connect the existing requirement-discovery workflow with the automatic-resolution contract so that Atanor can process discovered candidates as a continuous product flow rather than exposing separate technical capabilities.

AT-039 implemented the minimum application-level orchestration required to connect discovery to automatic resolution. A discovered `RequirementMention` becomes a `RequirementCandidate`, which is passed to the existing domain resolver. The resulting `RequirementResolution` preserves provenance and represents either a successful automatic resolution or an unresolved case for internal follow-up.

The task deliberately did not expand the resolution algorithm. Discovery, persistence and workflow orchestration were separated into independent application modules during the task, replacing the former generic `application/requirement.py` module with focused modules for discovery, requirement operations and workflow orchestration.

The integration was validated against the available samples. Text-based BOE and Archiveros samples exercise the integrated flow; the Ayuntamiento de León scanned sample remains an explicit unsupported extraction case. The complete suite passes with **75 tests**.

#### AT-039 Completion Criterion

A supported convocatoria can flow from imported source through requirement discovery into automatic resolution without requiring a user-facing validation step. Resolved and unresolved outcomes are represented, provenance remains intact, and the behavior is covered by automated flow tests.

### AT-040 · Produce a User-Usable Requirement Set

**Status: Completed**

**Goal:** turn the internal discovery/resolution result into the first genuinely useful product output: a user can provide a supported convocatoria and Atanor returns the set of requirements that the user needs to study, without exposing discovery, resolution or curation mechanics.

#### AT-040 Scope

- Define the application-level output representing the requirements a user should study from a supported convocatoria.
- Consume resolved requirements produced by the AT-039 workflow.
- Keep unresolved cases internal; they must not become a user-facing validation task.
- Preserve source provenance so resulting study requirements remain traceable.
- Provide the minimum inspection/use-case interface needed to validate this output end-to-end.
- Add automated tests for the user-oriented flow using the existing real samples.
- Avoid introducing study planning, Knowledge generation, OCR, semantic AI or a permanent UI unless the concrete flow demonstrates that they are required.

#### Explicitly Outside AT-040

- User validation of discovered requirements.
- Expert/curator UI.
- OCR or scanned-PDF support.
- Advanced semantic matching or confidence scoring.
- Automatic generation of detailed Knowledge or study plans.
- Frontend implementation unless required to expose the use case for validation.

#### AT-040 Completion Criterion

Given a supported convocatoria, Atanor produces a user-oriented set of study requirements from the automatically resolved workflow, while unresolved/discrepant cases remain internal and the user is not asked to validate Atanor's extraction or matching decisions. The flow is covered by automated tests and can be inspected end-to-end through an existing application interface or the minimum interface required by the task.

AT-040 was validated with **82 passing tests**. The final implementation introduced `StudyRequirementSet` as a minimal application-level output and reused the existing `Requirement` model rather than introducing a speculative `StudyRequirement` domain entity. The requirement repository contract was extended with `list_by_source()` and kept as a single shared protocol rather than duplicating it in the workflow module.

The task exposed no debt requiring a standalone cleanup task before continuing MVP work.

### AT-041 · Validate the First Candidate Product Experience

**Status: In Progress**

**Goal:** validate the first genuinely useful candidate interaction rather than prematurely selecting a complete UI, API or future workflow. The task is a product experiment: determine the minimum interaction through which a candidate can provide a supported convocatoria and obtain a useful answer to the question **"What do I need to study?"**.

#### AT-041 Product Hypothesis

A candidate should be able to provide a real convocatoria and receive a clear, useful and sufficiently reliable representation of the study requirements derived from it, without being asked to understand or validate Atanor's internal discovery, resolution or curation process.

#### AT-041 Scope

- Define the candidate who participates in this first product validation.
- Define the minimum input required from that candidate.
- Define the minimum result that could constitute a useful first product outcome.
- Define what information makes that result useful and trustworthy.
- Define the product behavior that is deliberately outside the experiment.
- Select the smallest interface capable of exercising the experiment meaningfully only after the product interaction is defined.
- Use manual/internal curation when necessary during development; do not build dedicated curator functionality unless the experiment demonstrates that it is required.
- Validate the result using at least one realistic convocatoria and explicit product-value criteria.

#### AT-041 Explicitly Outside

- Designing the complete Candidate Journey.
- Defining the final product UI or frontend architecture.
- Building a dedicated curator application.
- Making the candidate responsible for semantic validation.
- Study planning, progress tracking, tests or adaptive learning.
- OCR or scanned-PDF support unless the experiment proves it necessary.
- Advanced ML/NLP, confidence scoring or semantic matching unless the experiment demonstrates that the current approach cannot provide sufficient value.
- Predicting or scheduling detailed future tasks beyond what the experiment's evidence justifies.

#### AT-041 Validation Model

During development, the candidate result may be inspected by the product developer or another expert to identify omissions, false positives, ambiguities and usability problems. This is a **development validation mechanism**, not part of the intended mature candidate experience.

The mature product should instead provide the candidate with a sufficiently reliable result directly. Candidate validation of Atanor's semantic decisions is not considered part of the target product experience.

#### AT-041 Completion Criterion

AT-041 is complete when we have a working, minimal candidate-facing interaction and enough evidence to determine whether the resulting answer to **"What do I need to study?"** provides real value. The implementation should be the smallest practical mechanism capable of producing that evidence. The outcome of AT-041 will determine the next mini-MVP rather than committing the project to a predefined AT-042 implementation.

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
| TD-010 | Resolution result persistence | AT-039 produced in-memory resolutions; AT-040 still derives the user-oriented set during the application call. Durable resolution decisions are not yet stored. | Repeatability, auditability, asynchronous processing or internal curation becomes a concrete requirement. |
| TD-011 | Resolution algorithm sophistication | Current matching is intentionally deterministic and minimal. | Real user-oriented output demonstrates unacceptable unresolved/ambiguous rates. |
| TD-012 | Application workflow contract | Discovery, requirement operations and workflow orchestration are now separated, but their APIs are still small and may evolve rapidly during MVP work. | Repeated consumers, external API exposure or increasing workflow complexity. |

**Debt triage after AT-040:** no item requires a standalone debt-resolution task before AT-041. TD-010 remains intentionally deferred because durable resolution state has no demonstrated MVP requirement yet. TD-011 remains deferred until real output quality provides evidence that deterministic matching is insufficient. TD-012 should be monitored as the workflow crosses an application-interface boundary in AT-041. The repository-contract duplication identified during AT-040 was resolved within the task and does not remain as debt.

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
User-oriented study requirement set
  ↓
Requirement Scope
  ↓
Knowledge Need
  ↓
Available Knowledge
  ↓
Derived Coverage
```

Requirement discovery preserves source expressions and provenance. Automatic resolution is now an application-level step. The user-oriented requirement set is a minimal application output and does not yet justify a separate domain entity. Further domain changes should be driven by the candidate experiment and its evidence.

---

# Active Backlog Summary

The foundation, requirement discovery, structured discovery, requirement scope/knowledge-need modeling, coverage evaluation, documentation re-evaluation, first real-sample workflow, automatic requirement resolution and user-oriented requirement projection are complete. **AT-040 is complete with 82 passing tests.**

The active work is **AT-041 — Validate the First Candidate Product Experience**. It is intentionally defined as a mini-MVP experiment. No subsequent implementation task is committed until the evidence produced by AT-041 justifies the next step.
