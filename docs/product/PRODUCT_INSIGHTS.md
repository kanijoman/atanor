# Atanor Product Insights

This document records product discoveries, validated hypotheses, and potential future capabilities identified during iterative validation.

These entries are **not backlog commitments**. An insight becomes a backlog item only when a future mini-MVP is explicitly selected to validate or implement it.

## Product principles

### Candidate first

The MVP is focused on providing value to the candidate. Curator capabilities are introduced only when the product requires them.

### Product-led development

Each iteration is a small, self-contained mini-MVP. A mini-MVP establishes a concrete product hypothesis, implements the minimum needed to test it, and uses the evidence to decide the next iteration.

At the current maturity of Atanor, future backlog items are hypotheses rather than commitments. Large blocks of anticipated work should not be planned prematurely because doing so creates unnecessary rework as the product is discovered.

### Knowledge honesty

Atanor must be explicit about the availability and limitations of its knowledge.

> **Atanor must never present unknown, partial, or uncertain knowledge as complete and reliable.**

During the current product-discovery phase, the minimum distinction is whether knowledge is available or unavailable for a `KnowledgeNeed`. More detailed states such as partial coverage, uncertainty, or freshness should only be introduced when a concrete product need justifies them.

A truthful "I don't know" is a valid and preferable product outcome when Atanor lacks sufficient knowledge to support a candidate reliably.

### Knowledge ownership

Atanor is responsible for providing the knowledge required by the candidate. The candidate must **never** be responsible for obtaining missing information and supplying it to Atanor as part of the normal study workflow.

Knowledge gaps are therefore a product responsibility, not a candidate task. Atanor should attempt to resolve them through its own acquisition mechanisms. When automatic acquisition is insufficient, a curator may provide or validate source material so that Atanor can ingest and incorporate the required knowledge.

This principle does not prescribe a particular acquisition technology. Search, public-source retrieval, document ingestion, AI-assisted extraction, or other mechanisms may be evaluated pragmatically as the product evolves.

### Experiments and tests

Exploratory experiments and product tests have different responsibilities.

- `experiments/` is for investigation, inspection, comparison and measurement. Experiments may expose implementation details and produce observations that are not yet product requirements.
- `tests/` specify validated behavior. Tests should remain deterministic and agnostic of exploratory implementation details.
- An observation from an experiment becomes a test expectation only after the product or engineering decision is accepted as part of the contract.

This separation allows Atanor to explore uncertain product behavior without prematurely freezing it into the test suite.

## Validated discoveries

### AT-041 — Candidate entry point

The first candidate-oriented validation established the minimum flow for providing a local PDF convocatoria and extracting study requirements from it.

The important product insight was that the convocatoria itself can be used as the initial source of study requirements. At this stage Atanor does not need a pre-existing knowledge base to identify the candidate's requirements.

### BOE experiment

The BOE sample demonstrated that a real convocatoria contains substantially more information than the study programme. Automatic extraction therefore produces information that may be useful but is not necessarily a study requirement.

Potential future capabilities include identifying and exposing non-study information such as candidate eligibility requirements, application conditions, merit requirements, deadlines, and other convocatoria metadata. These capabilities remain deliberately deferred while the MVP focuses on the simplest candidate value path.

The experiment also reinforced that BOE documents must not be treated as having one universal template. Different sections and programme formulations can coexist in the same source, so provider-specific structure is an implementation concern rather than a domain assumption.

### Knowledge availability mini-MVP

The knowledge-oriented experiment established that a study requirement can contain one or more knowledge needs and that a knowledge need may either be associated with available Atanor knowledge or remain explicitly unresolved.

This validates an important product property: Atanor can represent what it knows and, equally importantly, what it does not know without pretending that unavailable knowledge exists.

The implementation was validated through persistence and end-to-end tests, including both available and unavailable knowledge cases. The migration contract was updated accordingly and the full test suite is green.

The mini-MVP is therefore considered **closed**.

## Current product boundary

At this point Atanor can:

1. ingest a textual PDF convocatoria;
2. identify candidate study requirements;
3. represent knowledge needs for those requirements;
4. represent whether knowledge is currently available for a need;
5. evaluate study coverage from the knowledge currently represented by Atanor;
6. autonomously acquire source material for a concrete knowledge need through a minimal external-source strategy;
7. extract a first deterministic subset of potentially relevant content from acquired source material.

The current system does **not** yet provide the candidate with a complete study experience, nor does acquisition automatically imply that the resulting material is validated canonical knowledge. Knowledge coverage is currently a validated domain capability rather than a complete candidate-facing knowledge supply workflow.

This boundary is intentional. AT-043 established the first autonomous knowledge-acquisition capability and identified the next product gap: distinguishing relevant content from incidental references and eventually validating or structuring that content as trustworthy knowledge.

## AT-043 — Knowledge Acquisition Prototype

### Hypothesis

> **Atanor can acquire a first useful piece of knowledge for a `KnowledgeNeed` through its own acquisition mechanism, making the resulting knowledge available for study coverage without requiring the candidate to supply it.**

### Result

AT-043 validated the acquisition part of the hypothesis with a BOE-backed experiment and a deterministic extraction strategy. For `Constitución Española`, approximately 328,116 source characters were reduced to 1,991 extracted characters. The extracted material contained several genuinely relevant programme formulations, while also including incidental references to the Constitution.

The result therefore validates:

- autonomous source acquisition without candidate intervention;
- deterministic first-stage relevance filtering;
- preservation of the distinction between source material and knowledge;
- the usefulness of real-source experiments for discovering the next product gap.

It does **not** yet validate semantic completeness, factual validation, canonical knowledge construction, or a universal BOE parsing strategy.

AT-043 is considered **closed** with **89 passing tests** and no regressions.

## Potential future capabilities

These items have emerged from experiments but are intentionally not scheduled until a concrete mini-MVP requires them:

- distinguish study-programme content from other convocatoria information;
- identify candidate eligibility and application requirements before study planning;
- detect document structure without assuming a universal BOE or provider template;
- improve relevance extraction beyond literal topic matching;
- represent partial, uncertain, outdated, or insufficient knowledge;
- automatically acquire, populate, or validate knowledge using external sources and/or NLP/ML techniques;
- curator workflows for resolving ambiguity and filling knowledge gaps;
- richer knowledge provenance, freshness, and quality information;
- automatic refresh and maintenance of acquired knowledge.

These are product opportunities, not implementation commitments.

## Working principle

During the current product-discovery phase:

> **Product insight is recorded; implementation is deferred until a concrete mini-MVP hypothesis requires it.**
