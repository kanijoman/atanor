# Atanor Product Insights

This document records product discoveries, domain observations, and potential future capabilities identified during iterative validation.

These entries are **not backlog commitments**. An insight becomes a backlog item only when a future mini-MVP is explicitly selected to validate or implement it.

## Convocation documents contain multiple information domains

A Spanish public-sector exam call is not necessarily a study programme. A BOE call may contain several categories of information relevant to a candidate, including:

- eligibility and access requirements;
- selection process and exercises;
- study programme and topics;
- merits and scoring criteria;
- application deadlines and administrative instructions;
- other call-specific information.

The current PDF discovery strategy can surface candidates from several of these categories, but it does not yet classify them semantically.

### Potential future capability: candidate eligibility

Atanor could eventually analyse the eligibility requirements of a call before asking the candidate to start studying. Examples include required education level, nationality, age, functional capacity, or other call-specific conditions.

This could provide an important early product interaction:

> **Can I apply for this call?**

Only after establishing eligibility would Atanor need to guide the candidate through the selection process and study requirements.

This is considered a **potential future product capability**, not a current implementation task.

### Potential future capability: call structure classification

Atanor may eventually distinguish study requirements from other structured information in a call, such as eligibility requirements, selection criteria, merits, and administrative information.

The BOE validation experiment demonstrated that the current discovery strategy can produce both useful study-related candidates and unrelated structured candidates. This should not be treated as an extraction defect until a product requirement establishes which categories Atanor must provide to the candidate.

## Knowledge honesty

Atanor must be explicit about the availability and limitations of its knowledge.

> **Atanor must never present unknown, partial, or uncertain knowledge as complete and reliable.**

During the current product-discovery phase, the minimum distinction is whether knowledge is available or unavailable for a `KnowledgeNeed`. More detailed states such as partial coverage, uncertainty, or freshness should only be introduced when a concrete product need justifies them.

A truthful "I don't know" is a valid and preferable product outcome when Atanor lacks sufficient knowledge to support a candidate reliably.

## Working principle

During the current product-discovery phase:

> **Product insight is recorded; implementation is deferred until a concrete mini-MVP hypothesis requires it.**

This prevents exploratory findings from prematurely expanding the backlog or constraining the architecture.
