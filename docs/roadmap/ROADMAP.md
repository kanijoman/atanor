# Atanor Roadmap

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | ROADMAP                     |
| Status       | 🟢 Active                   |
| Version      | 0.7                         |
| Last Updated | 2026-08-14                  |
| Audience     | Contributors and Developers |

---

# Vision

Atanor aims to become a knowledge-driven learning platform capable of transforming examination requirements and authoritative sources into structured, traceable and adaptive learning experiences.

The initial MVP focuses on Spanish public administration competitive examinations.

---

# Development Strategy

Atanor follows an incremental delivery model. Infrastructure and supporting technologies are introduced only when they solve an existing problem.

The roadmap describes strategic direction. It does not enumerate implementation tasks or establish one-to-one correspondence with the backlog.

Development is guided by working software, small traceable changes, evidence-driven domain decisions, MVP alignment and real source material rather than hypothetical formats.

From the first user-visible MVP workflow onward, **product validation is the primary driver of development**. Technical quality remains fundamental, but technical decisions are justified by the user value, product capability or demonstrated engineering risk they address.

The preferred evolution loop is:

```text
User need
    ↓
Product behavior
    ↓
Minimal technical support
    ↓
Real validation
    ↓
Learning
    ↓
Refinement
```

The roadmap therefore evolves from validated product capabilities rather than from a predetermined architectural target.

---

# Product Evolution

## Stage 1 · Foundation

**Status: 🟢 Completed**

Established the technical, organizational and development foundations of Atanor.

## Stage 2 · Application & Source Foundation

**Status: 🟢 Completed**

Established the minimal source, persistence and application capabilities required to introduce authoritative source material.

Validated workflow:

```text
PDF source
    ↓
Import
    ↓
Persist
    ↓
Retrieve / List
```

## Stage 3 · Requirement Discovery

**Status: 🟢 Completed**

Validated deterministic extraction of structured requirement mentions from supported PDF formats.

```text
Source
    ↓
Document Structure Detection
    ↓
Requirement Mention
    ↓
Requirement
```

Real BOE and Junta de Castilla y León samples demonstrated different structures. Scanned PDFs remain outside the current extraction boundary.

## Stage 4 · Requirement Scope & Coverage

**Status: 🟢 Completed**

Validated the contextual knowledge layer between requirements and available knowledge.

```text
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Coverage
```

The model supports multiple contextual scopes, required depth and Knowledge Needs that may remain unfulfilled. Initial coverage is deliberately limited to `COVERED` and `MISSING`.

Coverage is an assessment result rather than a persistent domain entity at this stage.

The stage is covered by domain, persistence and real-sample regression tests.

## Stage 5 · First User-Validated MVP Workflow

**Status: 🟢 In Progress**

Turn the validated requirement-processing capabilities into an observable product experience and use the resulting user feedback to determine what Atanor needs next.

Current validated capability:

```text
Convocatoria
    ↓
Source
    ↓
Requirement Discovery
    ↓
Automatic Resolution
    ↓
User-Oriented Study Requirements
```

AT-041 is the next step: expose this output through the smallest meaningful application interface so that a real user can inspect and evaluate it.

The goal of this stage is **not** to complete the architecture or the learning platform. It is to establish whether Atanor's first user-visible output is useful and to let that evidence drive subsequent product and technical decisions.

Potential next capabilities after validation may include improving requirement quality, adding contextual information, identifying missing knowledge, constructing knowledge or beginning study interactions. Their priority must be determined by observed user needs rather than assumed in advance.

## Stage 6 · Knowledge Construction

**Status: ⚪ Future**

Build the capability to transform validated Knowledge Needs into reusable canonical Knowledge when product validation demonstrates that this is the next valuable step.

Potential capabilities include:

- identify suitable knowledge sources;
- acquire or ingest source material;
- extract candidate knowledge;
- validate knowledge against evidence;
- establish provenance;
- construct reusable canonical Knowledge;
- reuse existing Knowledge where it satisfies a need.

These capabilities remain intentionally provisional. The first implementation step should be derived from the user workflow validated in Stage 5 rather than from the complete Knowledge model anticipated today.

## Stage 7 · Knowledge Retrieval and Assistance

**Status: ⚪ Future**

Make structured knowledge usable through search and AI-assisted interaction, including grounded retrieval, source citation, explanations and uncertainty reporting, when these capabilities address validated user needs.

## Stage 8 · Learning Platform

**Status: ⚪ Future**

Transform validated knowledge capabilities into an adaptive learning environment, including learning paths, study sessions, questions, assessment, progress tracking and revision planning as product evidence establishes their priority.

## Stage 9 · Ecosystem Expansion

**Status: ⚪ Future**

Expand beyond the initial MVP once the core product has been validated. Possible directions include additional examination domains, integrations, analytics, collaboration and broader learning use cases.

---

# Long-Term Vision

Although the initial product targets Spanish public administration examinations, the underlying model should remain sufficiently general to support other knowledge-intensive domains.

The reusable conceptual direction is:

```text
Source
    ↓
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Evidence
    ↓
Canonical Knowledge
    ↓
Learning
```

This is a strategic direction rather than a fixed implementation contract. Concrete product validation may change the order, boundaries or representation of these capabilities.

---

# Living Document

This roadmap defines strategic direction. Implementation detail belongs in the backlog and relevant technical documentation.

The roadmap may evolve when new evidence invalidates assumptions or product validation changes priorities.
