# Backlog

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | BACKLOG                     |
| Status       | 🟢 Active                   |
| Version      | 1.4                         |
| Last Updated | 2026-08-12                  |
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
| Total Tasks |    23 |
| Pending     |     6 |
| In Progress |     0 |
| Completed   |    15 |
| Cancelled   |     2 |
| Blocked     |     0 |

**Current Sprint:** Sprint 1 · Foundation

> These figures reflect the current task inventory. They should be updated whenever task status changes.

---

# Task Status

- ⬜ Pending
- 🟡 In Progress
- ✅ Completed
- ❌ Cancelled
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
- If cancelled work becomes necessary again, a new task must be created with a new identifier.
- Git history is the project's technical record; the backlog reflects planning and execution status.
- A single push should normally represent one isolated backlog task.
- Implemented functionality should be validated by automated tests whenever practical.
- Quality infrastructure may be brought forward when an active implementation task requires it.
- User interfaces are implementations of application use cases, not architectural dependencies of the domain.
- Technology choices for user interfaces should be justified by concrete product requirements rather than introduced speculatively.

---

# Sprint 1 · Foundation

## Epic A · Infrastructure

| ID     | Task                                | Priority | Status |
| ------ | ----------------------------------- | :------: | :------: |
| AT-001 | Create initial repository structure |    🔴    |    ✅   |
| AT-002 | Initialize backend project          |    🔴    |    ✅   |
| AT-003 | Initialize frontend project         |    🔴    |    ✅   |
| AT-004 | Configure initial Docker Compose    |    🔴    |    ❌   |
| AT-005 | Configure environment variables     |    🔴    |    ❌   |

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

The first user-facing work is intentionally technology-neutral. Atanor should validate application behavior and user workflows before committing to a permanent UI framework.

| ID     | Task                                      | Priority | Status |
| ------ | ----------------------------------------- | :------: | :------: |
| AT-013 | Reorganize product interaction roadmap   |    🔴    |    ✅   |
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

## Epic E · Quality

| ID     | Task                         | Priority | Status |
| ------ | ---------------------------- | :------: | :------: |
| AT-017 | Configure Ruff              |    🟡    |    ⬜   |
| AT-018 | Configure Pyright            |    🟡    |    ⬜   |
| AT-019 | Configure pre-commit hooks  |    🟡    |    ⬜   |
| AT-020 | Configure testing framework |    🟡    |    ✅   |

### AT-020 Execution Note

This task was brought forward because AT-010 required automated persistence tests. It established the minimum project-wide testing foundation required before further persistence behavior is implemented.

---

## Epic F · First Running System

| ID     | Task                                   | Priority | Status |
| ------ | -------------------------------------- | :------: | :------: |
| AT-021 | Integrate interface with application  |    🔴    |    ⬜   |
| AT-022 | Expose first application workflow      |    🟡    |    ⬜   |
| AT-023 | Verify end-to-end execution            |    🔴    |    ⬜   |

These tasks deliberately describe observable product behavior rather than prescribing a frontend framework. The concrete UI technology remains a future decision driven by the validated interaction requirements.

---

# Domain Model Validation Before Persistence

The backlog intentionally does not add speculative persistence tasks for the emerging Knowledge Blueprint and canonical knowledge model.

AT-010 and AT-011 established the initial persistence and domain foundations through small, validated increments. The initial domain slice demonstrates that a requirement can define a blueprint, a blueprint can require reusable knowledge, and knowledge can be associated with one or more sources.

Further concepts such as knowledge assertions, evidence, learning paths and assessments remain outside the initial implementation until concrete requirements justify their persistence model.

---

# Living Document

This backlog evolves together with the project.

Tasks may be added, cancelled or reprioritized as development progresses, provided such changes remain aligned with the roadmap, foundations and development conventions.

The objective is to maintain a backlog that is concise, accurate and focused on delivering incremental value.
