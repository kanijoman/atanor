# Backlog

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | BACKLOG                     |
| Status       | 🟢 Active                   |
| Version      | 1.0                         |
| Last Updated | 2026-08-11                  |
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
| Pending     |    10 |
| In Progress |     0 |
| Completed   |    11 |
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

## Epic D · Frontend

| ID     | Task                         | Priority | Status |
| ------ | ---------------------------- | :------: | :------: |
| AT-013 | Initialize React application |    🔴    |    ⬜   |
| AT-014 | Configure routing            |    🟡    |    ⬜   |
| AT-015 | Create application layout    |    🟡    |    ⬜   |

---

## Epic E · Quality

| ID     | Task                         | Priority | Status |
| ------ | ---------------------------- | :------: | :------: |
| AT-016 | Configure Ruff              |    🟡    |    ⬜   |
| AT-017 | Configure Pyright            |    🟡    |    ⬜   |
| AT-018 | Configure pre-commit hooks  |    🟡    |    ⬜   |
| AT-019 | Configure testing framework |    🟡    |    ✅   |

### AT-019 Execution Note

AT-019 was brought forward because AT-010 required automated persistence tests. The task established the minimum project-wide testing foundation required before further persistence behavior is implemented.

---

## Epic F · First Running System

| ID     | Task                                   | Priority | Status |
| ------ | -------------------------------------- | :------: | :------: |
| AT-020 | Connect frontend and backend           |    🔴    |    ⬜   |
| AT-021 | Implement API client                   |    🟡    |    ⬜   |
| AT-022 | Display backend status in the frontend |    🟡    |    ⬜   |
| AT-023 | Verify end-to-end execution            |    🔴    |    ⬜   |

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
