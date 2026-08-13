# Backlog

# Document Information

| Field        | Value |
| ------------ | ----- |
| Project      | Atanor |
| Document     | BACKLOG |
| Status       | 🟢 Active |
| Version      | 2.3 |
| Last Updated | 2026-08-13 |
| Audience     | Contributors and Developers |

---

# Backlog Status

| Metric      | Value |
| ----------- | ----: |
| Total Tasks |    33 |
| Pending     |     0 |
| In Progress |     1 |
| Completed   |    24 |
| Deferred    |     3 |
| Cancelled   |     5 |
| Blocked     |     0 |

**Current Epic:** Epic I · Requirement Scope & Knowledge Needs

**Current Task:** AT-033 · Define Requirement Scope and Knowledge Need

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

AT-004 was cancelled because containerized infrastructure is not currently required. AT-005 was cancelled when configuration requirements were simplified and consolidated into the backend configuration work.

## Epic B · Backend

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-006 | Initialize FastAPI application | 🔴 | ✅ |
| AT-007 | Implement configuration system | 🔴 | ✅ |
| AT-008 | Configure logging | 🟡 | ✅ |
| AT-009 | Implement health endpoint | 🟡 | ✅ |

## Epic C · Persistence

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-010 | Configure persistence layer | 🔴 | ✅ |
| AT-011 | Define initial domain model | 🔴 | ✅ |
| AT-012 | Configure migrations | 🟡 | ✅ |

The initial domain model remains intentionally minimal and extensible. It separates `Requirement`, knowledge coverage concepts, reusable `Knowledge`, and provenance through `Source`. New concepts are introduced only when concrete requirements justify them.

## Epic D · Product Interaction

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-013 | Reorganize product interaction roadmap | 🔴 | ✅ |
| AT-014 | Define first application use cases | 🔴 | ✅ |
| AT-015 | Build minimal CLI interface | 🟡 | ✅ |
| AT-016 | Validate first end-to-end user workflow | 🔴 | ✅ |

User interfaces remain replaceable implementations of application use cases. No permanent commitment to React, Qt, or another UI framework is made until concrete product requirements justify it.

---

# Deferred Development Quality Tooling

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-017 | Configure Ruff | 🟡 | ⏸ |
| AT-018 | Configure Pyright | 🟡 | ⏸ |
| AT-019 | Configure pre-commit hooks | 🟡 | ⏸ |

These identifiers are retained and will not be reused.

## AT-020 · Testing Framework

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-020 | Configure testing framework | 🟡 | ✅ |

## Superseded Application Workflow Tasks

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-021 | Integrate interface with application | 🔴 | ❌ |
| AT-022 | Expose first application workflow | 🟡 | ❌ |
| AT-023 | Verify end-to-end execution | 🔴 | ❌ |

These tasks were superseded by the workflow implemented through AT-015 and AT-016.

---

# Epic G · Requirement Discovery

**Status: 🟢 Completed**

## Objective

Transform an imported authoritative source into explicit requirement candidates while preserving provenance. The epic intentionally stops at validating the technical workflow and does not claim semantic requirement resolution or complete extraction from arbitrary convocatorias.

## Core Constraints

Different sources may use different document structures. A pattern observed in one BOE document is not a universal document rule. Requirement expressions such as `Constitución Española`, `Constitución`, and `Constitución de 1978` may refer to the same conceptual requirement; semantic equivalence and canonical resolution remain future concerns.

## Tasks

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-024 | Define requirement discovery use case | 🔴 | ✅ |
| AT-025 | Extract text from PDF sources | 🔴 | ✅ |
| AT-026 | Identify and normalize requirement candidates | 🔴 | ✅ |
| AT-027 | Persist discovered requirements | 🔴 | ✅ |
| AT-028 | Expose requirement inspection | 🟡 | ✅ |
| AT-029 | Validate requirement discovery end-to-end | 🔴 | ✅ |

### AT-029 · Validate Requirement Discovery End-to-End

**Status: Completed**

Validated the complete PDF discovery workflow against real samples. A text-based BOE PDF passed through extraction and candidate discovery, producing 440 numbered candidates. This validates the workflow but demonstrates that the initial numbered-line heuristic is intentionally broad and is not yet a semantic requirement extractor. A real Ayuntamiento de León PDF without an extractable text layer was also added as a regression sample and remains unsupported until a future text-acquisition mechanism such as OCR is justified.

AT-029 is deliberately limited to workflow validation. Extraction precision, semantic equivalence, provider-specific parsing and scanned-PDF support are future work.

---

# Epic H · Structured Requirement Discovery

**Status: 🟢 Completed**

## Objective

Improve requirement discovery from the broad candidate extraction validated in Epic G by using document structure and context from real convocatorias.

The BOE sample is the first structural reference, not a universal specification. Another BOE call, or a call from another provider, may use different organization or terminology.

## Core Constraints

- Do not assume that all convocatorias share one document structure.
- Treat observed structures as source-specific evidence, not domain rules.
- Prefer explicit deterministic structural signals over speculative NLP or semantic infrastructure.
- Provider-specific strategies are acceptable when justified by real samples.
- Preserve source expressions and provenance.
- Do not introduce canonical requirement resolution merely because equivalent expressions exist.
- Keep scanned-PDF/OCR support outside the immediate scope unless a concrete task demonstrates that it blocks the workflow.
- Use the minimum implementation necessary; future semantic analysis remains an option, not a current dependency.

## Tasks

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-030 | Define structured requirement sections | 🔴 | ✅ |
| AT-031 | Extract requirements from a known structured section | 🔴 | ✅ |
| AT-032 | Validate discovery against multiple real source structures | 🟡 | ✅ |

### AT-030 · Define Structured Requirement Sections

**Status: Completed**

Introduced the first source-specific structured context using the `Programa` section observed in the real BOE sample. Numbered candidates are considered only while inside that context. Matching is case-insensitive and supports the observed numbered-heading variants.

The implementation deliberately does not treat `Programa` as a universal document concept. Other structures such as `Temario` may require a different strategy in the future. No semantic analysis or generalized parser framework was introduced.

### AT-031 · Extract Requirements from a Known Structured Section

**Status: Completed**

Connected structured discovery with the application-level requirement workflow. Discovered `RequirementMention` instances can be converted into persisted `Requirement` entities while preserving the mandatory `source_id` provenance.

The task deliberately does not introduce semantic canonicalization, deduplication, or additional document structures.

### AT-032 · Validate Discovery Against Multiple Real Source Structures

**Status: Completed**

Validated structured discovery against multiple real convocatorias, including the BOE sample and a Junta de Castilla y León BOCyL sample. The latter uses `Tema` entries and demonstrated that structured numbering cannot safely be assumed to be Arabic numeric identifiers. The implementation therefore preserves the original structured expression and treats the `Tema` identifier as textual, allowing formats such as Arabic numbers, Roman numerals or letters without assigning semantic meaning to them.

The samples also provide evidence that document structure may vary by issuing body or document format. An organism-specific abstraction remains a possible future evolution, but current evidence is insufficient to justify introducing one. No such abstraction has been added.

The Ayuntamiento de León scanned PDF remains unsupported and continues to serve as a regression sample for the absence of an extractable text layer.

---

# Epic I · Requirement Scope & Knowledge Needs

**Status: 🟡 In Progress**

## Objective

Establish and validate the domain model required to express the knowledge coverage demanded by a requirement within a specific examination context, independently of whether the required knowledge already exists in Atanor.

The milestone focuses on the conceptual relationship between:

```text
Requirement
    │
    │ appears in
    ▼
Examination Context
    │
    │ defines
    ▼
Requirement Scope
    │
    │ expresses
    ▼
Knowledge Needs
    │
    │ compared with
    ▼
Knowledge Corpus
    │
    ▼
Coverage
```

The distinction between required knowledge and available knowledge must remain explicit. A Knowledge Need may exist even when the corresponding knowledge is not yet present in Atanor.

## Core Constraints

- A requirement may have multiple contextual scopes.
- A scope belongs to a requirement in a specific examination context.
- Different examination contexts may define different scopes for the same requirement.
- A scope may express different levels of required depth or granularity.
- A Knowledge Need represents required knowledge independently of its current availability.
- The same knowledge may satisfy multiple Knowledge Needs.
- Knowledge availability must not alter the Requirement Scope.
- Coverage is initially a derived result rather than an independent persisted entity.
- Do not introduce automatic semantic resolution, OCR, AI-generated scopes, automatic source discovery, or canonical Knowledge construction in this milestone.
- Do not commit to a definitive persistence model for Knowledge Scope before the domain concepts are validated.

## Tasks

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-033 | Define Requirement Scope and Knowledge Need | 🔴 | 🟡 |

### AT-033 · Define Requirement Scope and Knowledge Need

**Status: In Progress**

Establish the conceptual model, domain invariants and validation cases required to represent the knowledge coverage demanded by a requirement within an examination context.

The task must validate the following representative cases:

1. The same requirement with the same scope.
2. The same requirement with different scopes.
3. The same knowledge with different required depths.
4. A Knowledge Need for which no corresponding knowledge currently exists.

The task should establish the distinction between Requirement Scope, Knowledge Need and current knowledge availability without prematurely defining the definitive `Knowledge` persistence model.

## Explicitly Outside This Epic

- Automatic semantic resolution of requirements.
- Automatic scope generation.
- OCR.
- AI-generated scopes.
- Construction of the canonical Knowledge model.
- Automatic source discovery.
- Knowledge acquisition.
- User assessment.
- Question generation.
- Coverage optimization.
- Definitive Knowledge persistence design.

## Completion Criterion

The epic is complete when Atanor can unambiguously represent:

> Given a requirement in an examination context, what knowledge coverage is required, independently of whether that knowledge currently exists in Atanor?

The validated domain model and its automated tests must precede durable Requirement Scope or Knowledge persistence work.

## Anticipated Follow-up Work

The following work is intentionally not yet committed to the active backlog and must be defined from the validated outcome of AT-033:

- Requirement Scope persistence.
- Knowledge coverage evaluation.

---

# Domain Model Direction

Requirement Discovery preserves the distinction between:

```text
Source expression / mention
        ↓
Candidate / structured requirement
        ↓
Canonical Requirement (future)
```

Epic I extends this direction with the distinction between a requirement's contextual scope and the knowledge required by that scope:

```text
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

The canonical Knowledge model remains intentionally undefined until the requirement, scope and knowledge-need concepts have been sufficiently validated.

---

# Active Backlog Summary

AT-033 is currently the only active implementation task. No additional persistence or knowledge-construction tasks are committed until its domain validation is complete.
