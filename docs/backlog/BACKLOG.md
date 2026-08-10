# Backlog

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | BACKLOG                     |
| Status       | 🟢 Active                   |
| Version      | 0.2                         |
| Last Updated | 2026-08-10                  |
| Audience     | Contributors and Developers |

---

# Purpose

This backlog defines the implementation plan for Atanor.

It represents the current development roadmap and tracks the progress of implementation tasks.

The backlog is a planning tool rather than a technical specification. Technical implementation details belong in the corresponding commits and Architecture Decision Records (ADRs).

---

# Backlog Status

| Metric      | Value |
| ----------- | ----: |
| Total Tasks |    23 |
| Pending     |    15 |
| In Progress |     0 |
| Completed   |     6 |
| Cancelled   |     2 |
| Blocked     |     0 |

**Current Sprint:** Sprint 1 · Foundation

---

# Task Status

* ⬜ Pending
* 🟡 In Progress
* ✅ Completed
* ❌ Cancelled
* ⛔ Blocked

---

# Priority

* 🔴 High
* 🟡 Medium
* 🟢 Low

---

# Backlog Governance

The backlog defines the implementation plan of the project, not its technical specification.

## Principles

* Task identifiers are unique and immutable once work has started.
* Once a task enters the **In Progress** state, its definition is considered frozen.
* Implementation details belong in commits, not in the backlog.
* Additional work discovered during implementation must be planned as a new task.
* Tasks may be cancelled if they no longer provide value or are considered premature.
* Cancelled task identifiers are never reused.
* If the work becomes necessary again, a new task must be created with a new identifier.
* Git history is the project's technical record; the backlog reflects planning and execution status.

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
| ------ | ------------------------------ | :------: | :----: |
| AT-006 | Initialize FastAPI application |    🔴    |    ✅   |
| AT-007 | Implement configuration system |    🔴    |    ✅   |
| AT-008 | Configure logging              |    🟡    |    ✅   |
| AT-009 | Implement health endpoint      |    🟡    |    ⬜   |

---

## Epic C · Persistence

| ID     | Task                        | Priority | Status |
| ------ | --------------------------- | :------: | :----: |
| AT-010 | Configure persistence layer |    🔴    |    ⬜   |
| AT-011 | Define initial domain model |    🔴    |    ⬜   |
| AT-012 | Configure migrations        |    🟡    |    ⬜   |

---

## Epic D · Frontend

| ID     | Task                         | Priority | Status |
| ------ | ---------------------------- | :------: | :----: |
| AT-013 | Initialize React application |    🔴    |    ⬜   |
| AT-014 | Configure routing            |    🟡    |    ⬜   |
| AT-015 | Create application layout    |    🟡    |    ⬜   |

---

## Epic E · Quality

| ID     | Task                        | Priority | Status |
| ------ | --------------------------- | :------: | :----: |
| AT-016 | Configure Ruff              |    🟡    |    ⬜   |
| AT-017 | Configure Pyright           |    🟡    |    ⬜   |
| AT-018 | Configure pre-commit hooks  |    🟡    |    ⬜   |
| AT-019 | Configure testing framework |    🟡    |    ⬜   |

---

## Epic F · First Running System

| ID     | Task                                   | Priority | Status |
| ------ | -------------------------------------- | :------: | :----: |
| AT-020 | Connect frontend and backend           |    🔴    |    ⬜   |
| AT-021 | Implement API client                   |    🟡    |    ⬜   |
| AT-022 | Display backend status in the frontend |    🟡    |    ⬜   |
| AT-023 | Verify end-to-end execution            |    🔴    |    ⬜   |

---

# Living Document

This backlog evolves together with the project.

Tasks may be added, cancelled or reprioritized as development progresses, provided such changes remain aligned with the project's roadmap and guiding principles.

The objective is to maintain a backlog that is concise, accurate and focused on delivering incremental value.
