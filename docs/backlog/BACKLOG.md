# Atanor Backlog

## Document Information

| Field | Value |
| --- | --- |
| Project | Atanor |
| Document | BACKLOG |
| Status | Active |
| Version | 6.0 |
| Last Updated | 2026-09-10 |
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
    ↓
Candidate Study Material
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
- First end-to-end candidate study-material vertical: a real programme point can derive a concrete `KnowledgeNeed`, generate candidate-facing material, persist it and retrieve it.

The first end-to-end material case is grounded in the real BOE call sample and derives the narrower knowledge need `Derecho de acceso a la información pública` from the broader programme wording referring to Ley 19/2013. The programme unit itself is preserved unchanged.

These capabilities are validated against the project's real PDF samples and focused product tests. They do not imply universal support for arbitrary official-document formats.

---

## Current Product Gap

The main unresolved question is now whether the validated application capabilities are exposed as a **usable candidate workflow** rather than only as internal operations and tests.

Atanor can already derive study material from a real programme point, but the candidate does not yet have a simple product interface for selecting a programme point and reading the resulting material.

The next work should therefore prioritize making the first study-material vertical directly usable, before expanding the knowledge model or introducing additional infrastructure.

---

## Immediate Priority

**Expose the first candidate study-material workflow through the existing application interface.**

The next task should allow a candidate to select a real study-programme unit and obtain its generated study material, while preserving the programme point and derived Knowledge Need as distinct concepts.

Concrete implementation and acceptance criteria are tracked in GitHub Issue **AT-087**.

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
| `backend/experiments/` | Exploratory investigations only while they are actively useful; completed experiments should be removed once their conclusions are captured by product code, tests or documentation. |
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

The project has completed the initial foundation, source workflow, requirement-discovery, requirement-scope, document-processing, knowledge-acquisition, knowledge-construction, study-programme and first candidate study-material validation iterations.

The detailed history of those iterations is intentionally not reproduced here. It remains available through Git history and the corresponding project documentation.

The current transition to GitHub Issues as the primary task-tracking mechanism was evaluated through **AT-080**.

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
