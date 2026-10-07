# Atanor Backlog

## Document Information

| Field | Value |
| --- | --- |
| Project | Atanor |
| Document | BACKLOG |
| Status | Active |
| Version | 9.0 |
| Last Updated | 2026-10-07 |
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
Source (identified by content hash)
    ↓
Document Processing
    ↓
Call and Study Programme Discovery
    ↓
Study Programme Units (the requirements)
    ↓
Knowledge Need
    ↓
Study Material (curated or acquired)
    ↓
Candidate Study Material
    ↓
Study Coverage
```

The current implementation supports heterogeneous text-based PDF structures through source-specific application strategies. Scanned/image-only PDFs remain outside the current extraction boundary.

### Validated capabilities

- PDF source import and persistence.
- Deterministic document text extraction with page/order provenance.
- Document structure analysis for the currently observed source families.
- Call detection and provider-specific study-programme discovery; a programme unit is the requirement as the convocatoria states it.
- A persisted knowledge need for every programme unit, valid even without material, linked to the knowledge that satisfies it.
- Programme-level coverage: how many units of an imported programme have study material.
- Deterministic study-programme discovery for the current BOE, BOJA and Archiveros samples.
- Persistence and retrieval of discovered study programmes and units.
- Candidate-facing study material for sixteen topics: Ley 19/2013, Ley 39/2015 and ten topics of the Constitución Española and related laws (principles and fundamental rights, Tribunal Constitucional and Corona, Cortes Generales and Defensor del Pueblo, Poder Judicial, Gobierno, Administración General del Estado, organización territorial, personal funcionario, derechos y deberes de los funcionarios, presupuesto del Estado) acquired from the BOE article by article, and four curated topics (personal data protection, electronic identity and signature, object-oriented programming, data modelling).
- Explicit material provenance (origin: curated or acquired; review status) shown to the candidate.
- Bring-your-own convocatoria: a candidate can upload a PDF through the web interface; sources are identified by content hash, so repeated uploads are idempotent, and documents that are not a convocatoria are refused with an explanation.
- Candidate-facing study-material availability in programme listings, so supported units are directly actionable and unsupported units are identifiable without probing a failing endpoint.
- Candidate-facing semantic study-coverage summaries showing covered and pending aspects for supported units.
- Actionable study-aspect checklist in the candidate interface, backed by explicitly exposed required aspects (AT-105).

The current candidate study flow preserves the official programme wording while exposing Atanor's derived `KnowledgeNeed`, candidate-facing study material and explicit semantic coverage information.

AT-104 validated representative study-content casuistics across legal and technical domains. The experiments established an explicit distinction between programme scope, study requirements, study material and coverage. Coverage is only meaningful when study requirements are independently defined and supported by substantive evidence in the material. The object-oriented programming case also demonstrated that coverage detection must tolerate natural wording differences rather than depend on exact phrase matching.

Coverage is an explicit aspect contract derived from the material actually produced: an aspect is covered only when the material has a section for it with substantive content. For Ley 39/2015 each of the 8 required aspects maps to the BOE articles that develop it, so coverage is 8 of 8 when acquisition succeeds and drops for any aspect whose articles are missing. The aspect-to-article mappings are still pending expert review.

These capabilities are validated against the project's real PDF samples and focused product tests. They do not imply universal support for arbitrary official-document formats or universal semantic coverage.

---

## Current Product Gap

The first candidate-facing study loop is now usable end-to-end for the supported programme units:

```text
Call
  ↓
Programme
  ↓
Programme Unit
  ↓
Study Material
  ↓
Coverage Feedback
```

The main product gap is no longer basic access to study material. It is **breadth and usefulness of preparation**: only a small deterministic subset of the imported syllabus is currently supported, and the material itself remains deliberately minimal.

The next step should therefore be selected from the highest-value candidate problem demonstrated by the current product, rather than extending coverage or architecture by default.

---

## Immediate Priority

**Re-evaluate the next increment from the evidence gathered by AT-111 to AT-114.**

Measured on the four real samples (`atanor study-support-report`), 11% of the BOE units (13 of 28 in the Cuerpo General Auxiliar annex), 0% of the BOJA units and none of the other two documents are supported, and two of the four samples are not recognised as a convocatoria at all. The candidates for the next increment are:

- **Breadth through the registry and the acquired provider**: the highest-frequency unsupported topics are institutional law (Constitution, Cortes Generales, Poder Judicial, Gobierno y Administracion, Union Europea, acto administrativo, personal al servicio de las Administraciones) and IT/office skills. Law topics reuse the BOE acquisition mechanism; IT topics need curated or expert-reviewed material.
- **Recognising more call formats**: the OPOS Ayuntamiento de Leon and Archiveros documents are refused as convocatorias. Fixing detection makes more candidate documents usable.
- **Expert review of material**: curated topics and every aspect-to-article mapping are `unreviewed`; a minimal way to record review would turn provenance into trust.

The next increment must produce an observable candidate-facing improvement and be justified by this evidence rather than extending the architecture by default.

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
| `docs/foundation/FOUNDATIONS.md` | Product mission, vision and foundational principles. |
| `docs/roadmap/ROADMAP.md` | Strategic product direction and major stages; not individual tasks. |
| `docs/backlog/BACKLOG.md` | Current product state, active hypothesis and immediate priorities. |
| GitHub Issues | Concrete tasks, acceptance criteria, discussion and execution status. |
| `docs/architecture/ARCHITECTURE.md` | Validated architecture, domain/application boundaries and architectural decisions. |
| `docs/conventions/CONVENTIONS.md` | Engineering and development practices. |
| `docs/architecture/TECHNOLOGY.md` | Adopted, deferred and rejected technology choices. |
| `docs/architecture/MIGRATIONS.md` | Database migration strategy and conventions. |
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

AT-096 extended the candidate study-material vertical to Ley 39/2015 and introduced explicit semantic coverage feedback. AT-097 exposed material availability directly in the programme listing. Both are now closed after real candidate-facing validation.

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
