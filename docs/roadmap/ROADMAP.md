# Atanor Roadmap

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | ROADMAP                     |
| Status       | 🟢 Active                   |
| Version      | 0.9                         |
| Last Updated | 2026-09-03                  |
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

Exploratory work follows a complementary loop:

```text
Hypothesis
    ↓
Experiment
    ↓
Observation
    ↓
Product insight
    ↓
Validated requirement
    ↓
Implementation / test
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

**Status: 🟢 Completed**

Turned the validated requirement-processing capabilities into an observable product experience and used real-sample evidence to determine what Atanor needs next.

Validated capability:

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

The candidate experience is intentionally minimal. Atanor does not ask the candidate to understand or validate internal semantic decisions.

The stage also established an important product principle: Atanor, rather than the candidate, owns the responsibility for supplying knowledge required for study.

## Future Capability · Eligibility and Opportunity Discovery

**Status: ⚪ Future / Product Direction Identified**

Atanor should eventually be able to determine which selection processes are relevant to a candidate based on the candidate's capabilities and circumstances, rather than requiring the candidate to start from a known convocatoria.

A candidate may provide relevant information such as:

- nationality or other legally relevant personal conditions;
- educational qualifications and training;
- professional experience;
- seniority or previous public-service status;
- other capabilities or circumstances required by a selection process.

The capability should support both directions of discovery:

```text
Known Convocatoria
    ↓
Requirements
    ↓
Candidate Profile
    ↓
Eligibility Assessment
```

and:

```text
Candidate Profile
    ↓
Relevant Requirements
    ↓
Matching Selection Processes
    ↓
Relevant Convocatorias
```

Eligibility must explicitly distinguish at least three outcomes:

```text
ELIGIBLE
    Known information satisfies the relevant requirements.

NOT ELIGIBLE
    Known information contradicts at least one relevant requirement.

UNDETERMINED
    Available information is insufficient to establish eligibility.
```

Eligibility conclusions should remain traceable to the requirements extracted from authoritative sources. Atanor should not turn missing information or uncertain interpretation into a definitive eligibility decision.

When a compatible process is identified, eligibility should become a natural entry point into the existing preparation flow:

```text
Candidate Profile
    ↓
Eligible Selection Process
    ↓
Requirements
    ↓
Programme
    ↓
Knowledge Needs
    ↓
Preparation
```

This capability is deliberately documented as a product direction rather than an implementation commitment. It must not yet drive the creation of domain entities, persistence structures or candidate-profile infrastructure until concrete user validation establishes their need.

## Stage 6 · Knowledge Construction

**Status: 🟢 Prototype Validated / Next Increment Pending**

Build the capability to transform validated Knowledge Needs into reusable knowledge when product validation demonstrates that this is the next valuable step.

AT-043 established the first autonomous acquisition and extraction path:

```text
Knowledge Need
    ↓
Knowledge Acquisition
    ↓
External Source Material
    ↓
Relevant Content
    ↓
Candidate Knowledge
```

The BOE experiment demonstrated that a deterministic strategy can substantially reduce a real source to potentially relevant context. It did not yet establish semantic completeness, canonical knowledge validation or a universal source template.

Potential capabilities include:

- identify suitable knowledge sources;
- acquire or ingest source material;
- detect source/document structure without embedding provider assumptions in the domain;
- extract candidate knowledge;
- distinguish relevant content from incidental references;
- validate knowledge against evidence;
- establish provenance;
- construct reusable canonical Knowledge;
- reuse existing Knowledge where it satisfies a need.

These capabilities remain intentionally provisional. The next implementation step should be derived from the evidence of AT-043 rather than from the complete Knowledge model anticipated today.

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

Eligibility and opportunity discovery add another entry point to this model:

```text
Candidate Capabilities
    ↓
Requirement Matching
    ↓
Eligible Opportunities
    ↓
Selection Process
    ↓
Knowledge Needs
    ↓
Learning
```

This is a strategic direction rather than a fixed implementation contract. Concrete product validation may change the order, boundaries or representation of these capabilities.

---

# Living Document

This roadmap defines strategic direction. Implementation detail belongs in the backlog and relevant technical documentation.

The roadmap may evolve when new evidence invalidates assumptions or product validation changes priorities.
