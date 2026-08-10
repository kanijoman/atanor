# Foundations

> *The challenge of public service examinations is not the lack of information. It is the difficulty of transforming that information into reliable, relevant and learnable knowledge.*

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | FOUNDATIONS                 |
| Status       | 🟢 Active                   |
| Version      | 0.3                         |
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
- how the resulting knowledge should be organized into a coherent learning journey.

That refinement is a major part of the value traditionally provided by academic preparation services.

Atanor aims to make that process systematic, traceable and continuously maintainable.

---

# Mission

**Transform authoritative knowledge and explicit learning requirements into effective, verifiable and adaptive learning.**

Users should spend their time understanding, practicing and consolidating knowledge—not manually determining what they need to study, where to find it, or how it fits together.

---

# Vision

A user should be able to provide an official syllabus, examination notice, regulation, or other relevant documents and obtain a justified learning scope and a coherent learning journey.

Atanor should be able to construct and maintain that knowledge using:

- public and freely accessible sources;
- authoritative sources;
- documents provided by the user.

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
Canonical Knowledge
    ↓
Learning Path
```

The Knowledge Blueprint describes the proposed coverage, expected depth, evidence and confidence before the final knowledge corpus is built.

---

# What We Are

Atanor is a learning platform built around a structured, traceable knowledge model.

Its core capability is not merely storing documents or answering questions. It is transforming requirements and evidence into knowledge that can be organized, evaluated and learned.

---

# What We Are Not

Atanor is not:

- a traditional academy;
- a document repository;
- a specialized search engine;
- merely a chatbot;
- dependent on proprietary commercial study material.

AI may support many capabilities, but AI itself is not the product.

---

# Core Principles

## Knowledge Is the Primary Asset

The value of Atanor lies in how knowledge is represented, organized, related and maintained.

Documents are sources of knowledge, not necessarily the knowledge model itself.

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

The same knowledge may be required by multiple convocations, topics or learning paths.

Curriculum defines which knowledge is relevant in a particular context.

---

## Knowledge Must Be Verifiable

Knowledge should maintain traceability to the sources or evidence that support it.

The system should distinguish between:

- directly supported facts;
- user-provided requirements;
- inferred or proposed coverage;
- unresolved or unknown information.

Uncertainty must not be silently converted into certainty.

---

## Knowledge Is Modular

Knowledge should be represented as reusable and interconnected units rather than static manuals.

A knowledge unit may participate in multiple curricula, explanations, questions and learning paths.

---

## Sources and Knowledge Are Different

The source that establishes that something must be learned does not necessarily need to be the source that best explains it.

Atanor should therefore distinguish:

- curricular evidence;
- authoritative knowledge sources;
- explanatory or academic sources;
- user-provided material.

---

## Knowledge Evolves

Authoritative sources change, requirements change and the state of knowledge evolves.

Atanor must be able to update knowledge while preserving provenance and historical context where necessary.

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
Evidence
    ↓
Coverage Model
    ↓
Depth Model
    ↓
Canonical Knowledge
    ↓
Learning Path
```

The resulting study material becomes a generated view of the underlying knowledge model rather than the primary asset itself.

---

# Guiding Question

Every architectural, functional or technical decision should answer:

> **Does this decision help transform requirements and authoritative knowledge into a better, simpler and more effective learning experience?**

If the answer is no, it does not belong in Atanor.
