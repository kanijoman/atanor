# Foundations

> *The challenge of public service examinations is not the lack of information. It is the difficulty of transforming that information into reliable, relevant and learnable knowledge.*

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | FOUNDATIONS                 |
| Status       | 🟢 Active                   |
| Version      | 0.4                         |
| Last Updated | 2026-08-10                  |
| Audience     | Contributors and Developers |

---

# Why This Project Exists

Atanor was created to solve a specific problem in knowledge-intensive learning, initially public service examinations.

A competitive examination does not normally provide everything a candidate needs to learn. Its requirements often define a subject or source without specifying the complete knowledge coverage, the appropriate level of detail, or the best explanatory sources.

The difficult part is therefore not only finding information.

It is determining:

- what knowledge is required;
- how deeply it must be understood;
- which sources should support it;
- how different sources relate to each other;
- how the required knowledge should be organized into a coherent learning journey.

That refinement is a major part of the value traditionally provided by academic preparation services.

Atanor aims to make that process systematic, traceable and maintainable without depending structurally on proprietary study material.

---

# Mission

**Transform authoritative knowledge and explicit learning requirements into effective, verifiable and adaptive learning.**

Users should spend their time understanding, practicing and consolidating knowledge—not manually determining what they need to study, where to find it, or how it fits together.

---

# Vision

A user should be able to provide an official syllabus, examination notice, regulation, or other relevant documents and obtain a justified learning scope and a coherent learning journey.

Atanor should construct and refine the required knowledge using:

- public and freely accessible sources;
- authoritative sources;
- documents provided by the user;
- knowledge already accumulated and validated in the canonical corpus.

Paid third-party material must never be a structural dependency of the platform.

The platform should make uncertainty explicit rather than presenting unsupported assumptions as facts.

---

# The Core Product Problem

A requirement such as:

> "Operating Systems"

does not, by itself, determine:

- which concepts must be covered;
- how those concepts should be decomposed;
- how much detail is appropriate;
- which sources should be used;
- which parts are explicitly required and which are inferred from the domain.

Atanor therefore needs an intermediate process between a requirement and canonical knowledge.

Conceptually:

```text
Requirement
    ↓
Scope Discovery
    ↓
Knowledge Blueprint
    ↓
Knowledge Assessment
    ↓
Source Discovery / Acquisition
    ↓
Knowledge Candidates
    ↓
Evidence & Validation
    ↓
Canonical Knowledge
    ↓
Learning Path
```

This flow is iterative rather than strictly linear.

The Knowledge Blueprint defines the proposed coverage, expected depth, evidence needs and confidence. It also acts as the specification used to evaluate existing knowledge and determine whether new acquisition or refinement is necessary.

---

# The Canonical Knowledge Corpus

Atanor does not assume the existence of a complete corpus before the system can operate.

The canonical knowledge corpus is a **cumulative asset built progressively and on demand**.

When a new requirement is introduced, Atanor should first evaluate whether the existing canonical knowledge is sufficient. If it is, the system should reuse it. If it is incomplete or insufficient for the current requirement, Atanor may acquire additional source material, extract candidate knowledge, validate it and extend the corpus.

Conceptually:

```text
Requirement
     ↓
Knowledge Blueprint
     ↓
Existing Canonical Knowledge
     │
     ├── Sufficient ───────→ Reuse
     │
     ├── Insufficient ─────→ Extend / Revalidate
     │
     └── Missing ──────────→ Acquire
                                  ↓
                         Candidate Knowledge
                                  ↓
                         Evidence & Validation
                                  ↓
                         Canonical Knowledge
```

The corpus is therefore **demand-driven rather than continuously maintained for its own sake**.

Atanor does not need to proactively re-evaluate the entire corpus on a permanent schedule. Knowledge is re-evaluated when a real requirement provides a reason to do so, such as a new curriculum, a different expected depth, insufficient evidence, or a relevant source change discovered during use.

This keeps acquisition and maintenance aligned with actual product needs.

---

# What We Are

Atanor is a learning platform built around a structured, traceable knowledge model.

Its core capability is not merely storing documents or answering questions. It is transforming requirements, evidence and source material into knowledge that can be organized, evaluated, reused and learned.

The canonical knowledge corpus is one of the primary product assets, but it is not a static repository of documents. It is a reusable representation of validated knowledge that grows through real learning requirements.

---

# What We Are Not

Atanor is not:

- a traditional academy;
- a document repository;
- a specialized search engine;
- merely a chatbot;
- dependent on proprietary commercial study material;
- a system that requires a permanently maintained global corpus before it can serve users.

AI may support many capabilities, but AI itself is not the product.

---

# Core Principles

## Knowledge Is the Primary Asset

The value of Atanor lies in how knowledge is represented, organized, related, verified and maintained.

Documents are sources of knowledge, not necessarily the knowledge model itself.

The canonical corpus should be reusable independently of any particular curriculum.

---

## Requirements Do Not Define the Whole Knowledge Model

A requirement identifies an expected area or source of knowledge.

It does not necessarily define its complete coverage or depth.

Atanor must therefore distinguish:

```text
Requirement
    ↓
Scope
    ↓
Coverage + Depth
    ↓
Knowledge
```

---

## Knowledge Is Independent of Curriculum

Canonical knowledge must not belong to a single examination or syllabus.

The same knowledge may be required by multiple curricula, topics or learning paths.

Curriculum defines which knowledge is relevant in a particular context.

---

## The Blueprint Defines the Required Knowledge Scope

The Knowledge Blueprint is the bridge between an external requirement and the reusable knowledge corpus.

It should conceptually capture:

- candidate coverage;
- expected depth;
- evidence requirements;
- provenance;
- confidence;
- unresolved gaps.

The Blueprint is not merely a table of contents. It is also the specification against which existing knowledge is assessed.

---

## Knowledge Is Built on Demand

Atanor should not require a complete knowledge corpus before serving users.

Real requirements drive knowledge construction.

A new requirement may:

- reuse existing knowledge;
- expose a gap in existing knowledge;
- require deeper treatment;
- trigger source discovery;
- require revalidation of existing knowledge.

This creates a cumulative knowledge asset without imposing permanent, global maintenance as a product requirement.

---

## Sources and Knowledge Are Different

The source that establishes that something must be learned does not necessarily need to be the source that best explains it.

Atanor should distinguish:

- curricular evidence;
- authoritative knowledge sources;
- explanatory or academic sources;
- user-provided material.

A source can therefore contribute to scope discovery, knowledge construction, or both.

---

## Knowledge Must Be Verifiable

Knowledge should maintain traceability to the sources or evidence that support it.

The system should distinguish between:

- directly supported facts;
- user-provided requirements;
- inferred or proposed coverage;
- insufficiently supported knowledge;
- unresolved or unknown information.

Uncertainty must not be silently converted into certainty.

---

## Knowledge Is Modular

Knowledge should be represented as reusable and interconnected units rather than static manuals.

A knowledge unit may participate in multiple curricula, explanations, questions and learning paths.

---

## Knowledge Evolves Through Use

Authoritative sources change, requirements change and the required depth of knowledge changes.

Atanor should be able to update knowledge while preserving provenance and historical context where necessary.

However, continuous global re-evaluation is not a product requirement.

Knowledge should normally be re-evaluated when a concrete requirement creates a reason to do so.

---

## Learning Must Be Guided

Users should never face an empty page wondering what to study next.

The platform should construct a learning path from:

```text
Required Knowledge
        +
Knowledge Dependencies
        +
User Knowledge State
        ↓
Learning Path
```

---

## Learning Means Mastery

Completing a topic does not mean mastering it.

Progress should ultimately be measured through demonstrated understanding rather than the amount of content consumed.

---

## Learning Must Adapt to the User

The learning experience should adapt to prior knowledge, available time, progress and demonstrated weaknesses.

---

# Value Proposition

Traditional preparation services provide a refined interpretation of a syllabus, study material and a predefined learning plan.

Atanor aims to make that refinement dynamic and traceable.

Instead of treating a syllabus as a static table of contents, Atanor aims to construct:

```text
Requirement
    ↓
Scope Discovery
    ↓
Knowledge Blueprint
    ↓
Knowledge Assessment
    ↓
Source Discovery / Acquisition
    ↓
Canonical Knowledge
    ↓
Learning Path
```

The resulting study material becomes a generated view of the underlying knowledge model rather than the primary asset itself.

The accumulated corpus improves the efficiency of future requirements because previously validated knowledge can be reused rather than reconstructed.

---

# Guiding Question

Every architectural, functional or technical decision should answer:

> **Does this decision help transform requirements and authoritative knowledge into a better, simpler and more effective learning experience?**

If the answer is no, it does not belong in Atanor.
