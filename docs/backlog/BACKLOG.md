# Backlog

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | BACKLOG                     |
| Status       | 🟢 Active                   |
| Version      | 0.3                         |
| Last Updated | 2026-08-10                  |
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
| Pending     |    14 |
| In Progress |     0 |
| Completed   |     7 |
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
| AT-010 | Configure persistence layer |    🔴    |    ⬜   |
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

This is a domain hypothesis, not yet a finalized persistence design.

AT-010 should therefore be evaluated against the validated domain model rather than assuming that the initial `Document → Chapter → Topic → Epigraph` hierarchy is the final model.

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
| AT-019 | Configure testing framework |    🟡    |    ⬜   |

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

Before implementation of a durable knowledge model, the domain should establish:

1. What constitutes a requirement.
2. How a requirement defines or references a scope.
3. How candidate coverage is discovered.
4. How expected depth is represented.
5. How knowledge entities and assertions are distinguished.
6. How evidence and provenance are represented.
7. How the same knowledge can be reused across multiple curricula.
8. How uncertainty and confidence are represented.
9. How learning paths are derived from required knowledge.

Only after these concepts are sufficiently validated should the persistence model be finalized.

---

# Living Document

This backlog evolves together with the project.

Tasks may be added, cancelled or reprioritized as development progresses, provided such changes remain aligned with the roadmap, foundations and development conventions.

The objective is to maintain a backlog that is concise, accurate and focused on delivering incremental value.
