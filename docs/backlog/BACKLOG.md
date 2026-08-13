# Backlog

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | BACKLOG                     |
| Status       | 🟢 Active                   |
| Version      | 2.1                         |
| Last Updated | 2026-08-13                  |
| Audience     | Contributors and Developers |

---

# Backlog Status

| Metric      | Value |
| ----------- | ----: |
| Total Tasks |    32 |
| Pending     |     2 |
| In Progress |     0 |
| Completed   |    22 |
| Deferred    |     3 |
| Cancelled   |     5 |
| Blocked     |     0 |

**Current Epic:** Epic H · Structured Requirement Discovery

**Next Task:** AT-031 · Extract requirements from a known structured section

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

**Status: 🔵 Active**

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
| AT-031 | Extract requirements from a known structured section | 🔴 | ⬜ |
| AT-032 | Validate discovery against multiple real source structures | 🟡 | ⬜ |

### AT-030 · Define Structured Requirement Sections

**Status: Completed**

Introduced the first source-specific structured context using the `Programa` section observed in the real BOE sample. Numbered candidates are considered only while inside that context. Matching is case-insensitive and supports the observed numbered-heading variants.

The implementation deliberately does not treat `Programa` as a universal document concept. Other structures such as `Temario` may require a different strategy in the future. No semantic analysis or generalized parser framework was introduced.

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

Requirements discovered from sources currently require a `source_id`, making provenance explicit and mandatory. Semantic entity resolution remains a future capability and should only be introduced when real source examples demonstrate that deterministic normalization is insufficient.

---

# Active Backlog Summary

| ID | Task | Priority | Status |
| --- | --- | :---: | :---: |
| AT-031 | Extract requirements from a known structured section | 🔴 | ⬜ |
| AT-032 | Validate discovery against multiple real source structures | 🟡 | ⬜ |

The next implementation step is **AT-031**. Its scope should remain limited to converting candidates from the known structured context into application-level requirement mentions and, where justified by the existing workflow, persisting them. It should not introduce semantic canonicalization or support additional document structures unless concrete evidence requires it.
