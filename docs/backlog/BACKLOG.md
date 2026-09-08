# Atanor Backlog

## Document Information

| Field | Value |
| --- | --- |
| Project | Atanor |
| Document | BACKLOG |
| Status | Active |
| Version | 5.0 |
| Last Updated | 2026-09-08 |
| Audience | Contributors and Developers |

---

## Purpose

`BACKLOG.md` is the project's **operational product backlog**. It communicates where Atanor is, what has been validated, and what should be considered next.

It is intentionally not a historical task ledger. Concrete task definition and execution tracking are managed through GitHub Issues; implementation history is preserved by Git.

---

## Current Product State

Atanor is an early-stage product focused first on Spanish public administration examinations.

The current validated application flow is:

```text
Convocatoria PDF
    ↓
Source
    ↓
Document Processing
    ↓
Requirement Discovery
    ↓
Requirement Resolution
    ↓
Study Requirements
    ↓
Study Programme Discovery
    ↓
Study Programme Units
    ↓
Knowledge Need
    ↓
Knowledge Construction
```

The current implementation supports heterogeneous text-based PDF structures through source-specific application strategies. Scanned/image-only PDFs remain outside the current extraction boundary.

### Validated capabilities

- PDF source import and persistence.
- Deterministic document text extraction with page/order provenance.
- Document structure analysis for the currently observed source families.
- Requirement discovery and deterministic requirement resolution.
- User-oriented study requirement projection.
- Requirement scopes and knowledge needs.
- Binary knowledge coverage assessment (`COVERED` / `MISSING`).
- Autonomous acquisition from an authoritative BOE source.
- Deterministic relevant-content extraction for acquired material.
- First reusable `Knowledge` construction workflow.
- Deterministic study-programme discovery for the current BOE, BOJA and Archiveros samples.
- Persistence and retrieval of discovered study programmes and units.

These capabilities are validated against the project's four real PDF samples. They do not imply universal support for arbitrary official-document formats.

---

## Current Product Gap

The main unresolved question is no longer whether Atanor can process isolated technical stages. The key question is whether these capabilities can be composed into a **useful preparation experience for an actual candidate**.

In particular, Atanor must demonstrate that a candidate can move from an official examination call to a trustworthy, usable study scope and then to the knowledge required to prepare it.

The next work should therefore prioritize product value and validation over additional infrastructure or speculative architecture.

---

## Immediate Priority

**Define and validate the next candidate-facing mini-MVP from the capabilities now available.**

The next task should establish a concrete user workflow that uses the validated requirement and study-programme capabilities and exposes the smallest meaningful preparation result.

The precise implementation should be defined in a GitHub Issue after the product hypothesis is selected.

---

## Working Model

Each new task follows this general loop:

```text
Product hypothesis / need
        ↓
GitHub Issue
        ↓
Minimal implementation
        ↓
Automated validation
        ↓
Real-product validation
        ↓
Learning
        ↓
Next Issue / refinement
```

A task is considered a mini-MVP when it provides user value, materially improves a validated workflow, produces actionable product knowledge, or provides technical capability demonstrably required by the current experiment.

Future work is intentionally treated as hypotheses rather than commitments.

---

## Documentation Responsibilities

| Artifact | Responsibility |
| --- | --- |
| `README.md` | Project introduction, current high-level capability and contributor orientation. |
| `docs/foundations/FOUNDATIONS.md` | Product mission, vision and foundational principles. |
| `docs/roadmap/ROADMAP.md` | Strategic product direction and major stages; not individual tasks. |
| `docs/backlog/BACKLOG.md` | Current product state, active hypothesis and immediate priorities. |
| GitHub Issues | Concrete tasks, acceptance criteria, discussion and execution status. |
| `docs/architecture/ARCHITECTURE.md` | Validated architecture, domain/application boundaries and architectural decisions. |
| `docs/conventions/CONVENTIONS.md` | Engineering and development practices. |
| `docs/technology/TECHNOLOGY.md` | Adopted, deferred and rejected technology choices. |
| `docs/migrations/MIGRATIONS.md` | Database migration strategy and conventions. |
| `backend/experiments/` | Exploratory investigations and evidence that has not necessarily become a product contract. |
| Git history | Actual implementation history and technical change record. |

Documentation should be updated only when the information belongs to that document and its maintenance cost is justified.

---

## GitHub Issues Workflow

New concrete tasks should normally be created as GitHub Issues using the `AT-XXX` identifier in the title.

An Issue should contain enough information to establish:

- the problem or hypothesis;
- the intended outcome;
- relevant scope and explicit non-goals;
- acceptance criteria when they can be defined in advance.

Implementation details discovered during development do not need to be copied into this backlog. They belong in code, commits, experiments or technical documentation as appropriate.

When a task is completed, its Issue is closed after validation. If new work is discovered, create a separate Issue rather than silently expanding the original scope.

Commits continue to use:

```text
AT-XXX Change description
```

This preserves traceability between product task, implementation and Git history without requiring the repository backlog to duplicate the Issue history.

---

## Historical Context

The project has completed the initial foundation, source workflow, requirement-discovery, requirement-scope, document-processing, knowledge-acquisition, knowledge-construction and study-programme validation iterations.

The detailed history of those iterations is intentionally not reproduced here. It remains available through Git history, experiments and the corresponding project documentation.

The current transition to GitHub Issues as the primary task-tracking mechanism is itself being evaluated through **AT-080**.

---

## Backlog Governance

- Keep this document short and operational.
- Do not duplicate the detailed history of completed tasks.
- Do not use the backlog as a technical specification.
- Do not predefine a long sequence of speculative implementation tasks.
- Prefer one isolated task per GitHub Issue.
- Keep task scope stable once implementation starts.
- Validate behavior with automated tests whenever practical.
- Validate product-facing work against real user value, not only technical correctness.
- Introduce new abstractions, dependencies or infrastructure only when justified by concrete evidence.
- Preserve uncertainty explicitly; unresolved product questions should become hypotheses or experiments rather than hidden assumptions.
