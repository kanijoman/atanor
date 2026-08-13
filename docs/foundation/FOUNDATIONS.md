# Foundations

> *The challenge of public service examinations is not the lack of information. It is the difficulty of transforming that information into reliable, relevant and learnable knowledge.*

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | FOUNDATIONS                 |
| Status       | 🟢 Active                   |
| Version      | 0.5                         |
| Last Updated | 2026-08-13                  |
| Audience     | Contributors and Developers |

---

# Why This Project Exists

Atanor was created to solve a specific problem in knowledge-intensive learning, initially public service examinations.

An examination requirement often identifies an area or source without specifying the complete knowledge coverage, the appropriate level of detail, or the best explanatory sources.

The difficult part is therefore not only finding information. It is determining what knowledge is required, how deeply it must be understood, which sources should support it and how the resulting knowledge should be organized into a coherent learning journey.

Atanor aims to make that process systematic, traceable and maintainable without depending structurally on proprietary study material.

---

# Mission

**Transform authoritative knowledge and explicit learning requirements into effective, verifiable and adaptive learning.**

Users should spend their time understanding, practicing and consolidating knowledge—not manually determining what they need to study, where to find it, or how it fits together.

---

# Vision

A user should be able to provide an official syllabus, examination notice, regulation, or other relevant document and obtain a justified learning scope and, eventually, a coherent learning journey.

Atanor should construct and refine the required knowledge using public and freely accessible sources, authoritative sources, documents provided by the user and knowledge already accumulated and validated in the canonical corpus.

Paid third-party material must never be a structural dependency of the platform. The platform should make uncertainty explicit rather than presenting unsupported assumptions as facts.

---

# The Core Product Problem

A requirement such as:

> "Operating Systems"

does not, by itself, determine which concepts must be covered, how they should be decomposed, how much detail is appropriate or which sources should be used.

The current validated intermediate model is deliberately smaller than the long-term vision:

```text
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Coverage
    ↓
Knowledge
```

A Requirement Scope expresses the contextual knowledge coverage required by a requirement. A Knowledge Need represents a unit of that required coverage and remains valid even when corresponding Knowledge is not yet available.

The initial Coverage model is deliberately limited to `COVERED` and `MISSING`.

This model is a validated foundation for future knowledge construction. It does not assume that a complete Knowledge Blueprint, semantic matching system or global corpus already exists.

---

# The Canonical Knowledge Corpus

Atanor does not assume the existence of a complete corpus before the system can operate.

The canonical knowledge corpus is a cumulative asset built progressively and on demand.

When a new requirement is introduced, Atanor should eventually evaluate whether existing canonical knowledge is sufficient. If it is incomplete or insufficient for the current requirement, Atanor may acquire additional source material, extract candidate knowledge, validate it and extend the corpus.

Conceptually:

```text
Requirement Scope
       ↓
Knowledge Need
       ↓
Existing Knowledge
       │
       ├── Covered ───────→ Reuse
       └── Missing ───────→ Construct / Acquire
                                  ↓
                         Evidence & Validation
                                  ↓
                         Canonical Knowledge
```

The corpus is therefore demand-driven rather than continuously maintained for its own sake.

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

## Requirements Do Not Define the Whole Knowledge Model

A requirement identifies an expected area or source of knowledge. It does not necessarily define its complete coverage or depth.

Atanor therefore distinguishes:

```text
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Coverage + Depth
    ↓
Knowledge
```

## Knowledge Is Independent of Curriculum

Canonical knowledge must not belong to a single examination or syllabus. The same knowledge may be required by multiple curricula, topics or learning paths.

## Scope and Needs Are Independent of Availability

A Requirement Scope describes what is required in context. A Knowledge Need describes required coverage regardless of whether the corresponding knowledge exists.

Adding Knowledge may change Coverage without changing the requirement context or its needs.

## Knowledge Is Built on Demand

Real requirements should drive knowledge construction. A new requirement may reuse existing knowledge, expose a gap, require deeper treatment, trigger source discovery or require revalidation.

## Sources and Knowledge Are Different

The source that establishes that something must be learned does not necessarily need to be the source that best explains it. Atanor should distinguish curricular evidence, authoritative knowledge sources, explanatory sources and user-provided material.

## Knowledge Must Be Verifiable

Knowledge should maintain traceability to the sources or evidence that support it. The system should distinguish directly supported facts, user-provided requirements, inferred or proposed coverage and unresolved information.

## Knowledge Is Modular

Knowledge should be represented as reusable and interconnected units rather than static manuals. A knowledge unit may participate in multiple curricula, explanations, questions and learning paths.

## Learning Must Be Guided

Users should never face an empty page wondering what to study next. The platform should eventually construct a learning path from required knowledge, dependencies and the learner's current state.

## Learning Means Mastery

Completing a topic does not mean mastering it. Progress should ultimately be measured through demonstrated understanding rather than the amount of content consumed.

## Learning Must Adapt to the User

The learning experience should adapt to prior knowledge, available time, progress and demonstrated weaknesses.

---

# Value Proposition

Traditional preparation services provide a refined interpretation of a syllabus, study material and a predefined learning plan.

Atanor aims to make that refinement dynamic and traceable.

The current validated foundation is:

```text
Requirement
    ↓
Requirement Scope
    ↓
Knowledge Need
    ↓
Coverage
```

Future capabilities may extend this toward knowledge construction, evidence and validation, canonical knowledge and learning paths. Those capabilities should be introduced only when concrete product requirements justify them.

---

# Guiding Question

Every architectural, functional or technical decision should answer:

> **Does this decision help transform requirements and authoritative knowledge into a better, simpler and more effective learning experience?**

If the answer is no, it does not belong in Atanor.
