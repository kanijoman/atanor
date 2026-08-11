# Backlog

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | BACKLOG                     |
| Status       | 🟢 Active                   |
| Version      | 0.7                         |
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
| Pending     |    12 |
| In Progress |     1 |
| Completed   |     8 |
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
| ------ | ----------------------------------- | :------: | :----: |
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
| AT-010 | Configure persistence layer |    🔴    |    🟡   |
| AT-011 | Define initial domain model |    🔴    |    ⬜   |
| AT-012 | Configure migrations        |    🟡    |    ⬜   |

### Current Domain-Model Direction

The conceptual work performed before implementing AT-010 has shown that persistence should not be designed directly from the initial document hierarchy.

The current domain hypothesis distinguishes, at minimum:

```text
Curriculum
    Requirement
    Scope Definition
    Knowledge Blueprint

Knowledge
    Knowledge Entity
    Knowledge Assertion
    Relationships
    Dependencies

Provenance
    Source
    Evidence

Learning
    Learning Path
    Assessment
```

The initial persistence implementation is intentionally narrower than this full domain hypothesis. It is based on the validated concepts required for the first persistence slice and should evolve only when concrete requirements justify it.

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

The conceptual validation performed before AT-010 established the minimum concepts required for the initial persistence slice:

1. What constitutes a requirement.
2. How a requirement is represented by a blueprint.
3. How expected knowledge coverage and depth are associated with a blueprint.
4. How canonical knowledge can be reused across blueprints.
5. How sources and evidence provide provenance.

Further concepts such as candidate knowledge, assertions, learning paths and assessments remain outside the initial persistence implementation until concrete requirements justify their persistence model.

---

# Living Document

This backlog evolves together with the project.

Tasks may be added, cancelled or reprioritized as development progresses, provided such changes remain aligned with the roadmap, foundations and development conventions.

The objective is to maintain a backlog that is concise, accurate and focused on delivering incremental value.
