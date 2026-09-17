# Atanor Roadmap

## Document Information

| Field | Value |
| --- | --- |
| Project | Atanor |
| Document | ROADMAP |
| Status | Active |
| Version | 1.1 |
| Last Updated | 2026-09-17 |
| Audience | Contributors and Developers |

---

## Vision

Atanor aims to become a knowledge-driven learning platform capable of transforming examination requirements and authoritative sources into structured, traceable and adaptive learning experiences.

The initial product focuses on Spanish public administration competitive examinations.

---

## Development Strategy

The roadmap defines **strategic product direction**, not implementation tasks.

Atanor follows an evidence-driven, incremental model:

```text
User need / product hypothesis
        ↓
Minimal experiment or mini-MVP
        ↓
Real validation
        ↓
Learning
        ↓
Next validated capability
```

Technical quality remains fundamental, but technical work is subordinate to validated product needs and demonstrated engineering risks.

Future stages are directional. Their order, scope and implementation may change as product evidence accumulates.

---

## Product Evolution

### Stage 1 · Foundation

**Status: Completed**

Established the technical and development foundations of Atanor, including the backend, persistence, testing and minimal application infrastructure.

### Stage 2 · Source and Requirement Foundation

**Status: Completed**

Established the ability to import authoritative PDF sources, process their text and discover structured examination requirements.

Validated direction:

```text
PDF Source
    ↓
Source
    ↓
Document Processing
    ↓
Requirement Discovery
    ↓
Requirement
```

Real official-document samples demonstrated that source structures differ. Scanned/image-only PDFs remain outside the current extraction boundary.

### Stage 3 · Requirement Context and Candidate Study Scope

**Status: Completed**

Established the contextual layer needed to turn requirements into study-oriented knowledge needs.

```text
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Coverage
```

The initial coverage model distinguished only `COVERED` and `MISSING`. Later candidate-facing validation demonstrated that useful coverage feedback requires explicit semantic aspects when partial coverage matters.

### Stage 4 · Document Structure and Programme Discovery

**Status: Validated / Implemented**

Validated deterministic document-structure analysis and source-specific study-programme discovery against the current BOE, BOJA and Archiveros samples.

The current application can normalize heterogeneous programme structures into:

```text
Source
    ↓
Source-specific structure detection
    ↓
Study Programme
    ↓
Study Programme Units
```

The implementation deliberately keeps provider-specific structure in the application layer and does not assume a universal official-document format.

### Stage 5 · Knowledge Acquisition and Construction

**Status: Prototype Validated / Implemented**

Validated the first path from a `KnowledgeNeed` to reusable `Knowledge` through authoritative source acquisition and deterministic relevance extraction.

```text
Knowledge Need
    ↓
Knowledge Acquisition
    ↓
Source Material
    ↓
Relevant Content
    ↓
Knowledge Construction
    ↓
Knowledge
```

The current capability demonstrates acquisition, relevance extraction and first knowledge construction, but does not yet establish semantic completeness, universal source support or fully validated canonical knowledge.

### Stage 6 · Candidate Preparation MVP

**Status: Initial Candidate Loop Validated**

The first meaningful candidate preparation loop is now usable through the web application for supported programme units.

Validated flow:

```text
Convocatoria
    ↓
Study Programme
    ↓
Programme Unit
    ↓
Knowledge Need
    ↓
Candidate Study Material
    ↓
Study Coverage Feedback
```

The current experience includes:

- programme-level visibility of whether study material is available;
- direct navigation to supported study units;
- candidate-facing material grounded in canonical legal sources;
- explicit semantic coverage feedback showing covered and pending aspects.

The first coverage vertical spans Ley 19/2013 and Ley 39/2015. This demonstrates the end-to-end candidate interaction, but not broad syllabus coverage or pedagogically complete material.

The next objective within this stage should be selected from evidence about the highest-value remaining candidate problem, rather than assumed in advance.

### Future Capability · Eligibility and Opportunity Discovery

**Status: Future Product Direction**

Atanor should eventually be able to determine which selection processes are relevant to a candidate, including both starting from a known convocatoria and discovering opportunities from a candidate profile.

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

Eligibility should distinguish at least:

```text
ELIGIBLE
NOT ELIGIBLE
UNDETERMINED
```

This remains a product direction rather than an implementation commitment.

### Future Capability · Knowledge Retrieval and Assistance

**Status: Future**

Make validated knowledge usable through search and grounded AI-assisted interaction, including citations, explanations and explicit uncertainty when these capabilities address validated user needs.

### Future Capability · Adaptive Learning

**Status: Future**

Evolve validated knowledge into an adaptive learning environment with study sessions, questions, assessment, progress tracking and revision planning when product evidence establishes the need.

### Future Capability · Ecosystem Expansion

**Status: Future**

Expand beyond the initial examination domain once the core candidate experience has been validated. Possible directions include additional examination domains, integrations, analytics, collaboration and broader knowledge-intensive learning use cases.

---

## Long-Term Conceptual Direction

The reusable conceptual model remains:

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

Candidate preparation adds an explicit candidate-facing layer:

```text
Knowledge Need
    ↓
Candidate Study Material
    ↓
Semantic Coverage Feedback
    ↓
Study
```

Eligibility and opportunity discovery provide an additional entry point:

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

These models describe direction, not fixed technical contracts.

---

## Living Roadmap

The roadmap should change when product evidence changes the project's priorities or invalidates an assumption.

Implementation details and concrete tasks belong in GitHub Issues, while validated architectural decisions belong in `ARCHITECTURE.md`.
