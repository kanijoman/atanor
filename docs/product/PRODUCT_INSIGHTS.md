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

## AT-111 - Supported syllabus breadth

### Hypothesis

> **Before choosing the next topics to support, measure how much of the real syllabi Atanor can already prepare.**

### Method

`atanor study-support-report <pdf>...` runs call detection and programme discovery on a PDF without persisting anything and reports, per programme unit, whether study material exists. It was run over the four sample PDFs in `backend/tests/samples/`.

### Result (2026-10-07)

| Sample | Call detected | Programmes | Units | Supported |
| --- | --- | --- | --- | --- |
| BOE-A-2024-14098 | yes | 10 (annexes) | 348 | 21 (6%) |
| BOJA24-138-... | yes | 7 | 269 | 0 (0%) |
| OPOS_AYTO_LEON_INFORMATICA_B | **no** | 0 | 0 | n/a |
| Programa_Archiveros_0 | **no** | 0 | 0 | n/a |

Observations:

- Supported units are concentrated in six topics: Ley 19/2013 (4 units), Ley 39/2015 (5), protection of personal data (10), data modelling (2). No unit of the BOJA sample matches any supported topic.
- Two of the four samples are not recognised as calls by `call_discovery`, so the end-to-end flow produces no programme for them even though the programme-discovery strategies can parse them when given a call. A candidate importing either document would currently receive an error.
- The unsupported units form a long tail: 478 distinct titles, with the most frequent topic repeated only 8 times. The recurring ones are institutional law (Constitution, Cortes Generales, Poder Judicial, Gobierno y Administracion, Union Europea, acto administrativo, personal al servicio de las Administraciones, presupuesto de gasto, equality policies) and IT/office skills (TCP/IP, Windows, Word, Excel, Access, Outlook).

### Update after AT-112 to AT-114

Study material for Ley 19/2013 and Ley 39/2015 is now acquired article by article, and a candidate can import any convocatoria PDF. Importing the four samples confirmed that the OPOS Ayuntamiento de Leon and Archiveros documents are refused as not being a convocatoria, so the call-detection heuristic, not the study material, is the first limit a real candidate would meet. Two further findings came out of acquiring real BOE text: the article parser originally dropped paragraph text around inline links (a latent defect hidden by simple fixtures), and the `knowledge_sources` table had no migration. Both were fixed and guarded by tests.

### Consequence

Adding topics one at a time yields about 1-2 percentage points each on this sample, so breadth needs a repeatable mechanism (a topic registry fed by authoritative sources) rather than hand-written entries, and call detection must be fixed before more programmes become reachable. These findings guide AT-113 to AT-115.

## AT-115 - One model for requirements and programme units

Earlier entries in this document speak of requirements, requirement scopes and a binary covered/missing coverage. That model was built before programme discovery existed. Once candidates could import a convocatoria and browse its units, the requirement and the unit turned out to be the same thing, no unit ever needed more than one scope, and the requirement code was not on any product path. The two were unified: a programme unit is the requirement, it carries its own persisted knowledge need (also for units without material, which keeps "Atanor knows what it does not know"), and coverage is the single aspect-based summary plus a programme-level count. The older entries are kept as history of how the product was discovered.

## AT-118 - Faithful programme structure and the real scope of a unit

Keeping the complete official wording of each programme unit (previously only its first line was stored) exposed two things the truncation had hidden. First, programmes such as the Cuerpo General Auxiliar de la AGE annex have two blocks that restart numbering, so a candidate saw two different "unit 11" entries; blocks are now kept and units stay in document order. Second, the full wording of a unit is often much wider than the material that matches it: unit 11 of that programme asks for the Ley 39/2015 and the Ley 40/2015, the contentious-administrative appeal and the parties' capacity and representation, while the current material covers eight aspects of the Ley 39/2015 only, so its "8 of 8" coverage overstates what the unit requires. Matching topics from substrings of the whole wording also produced false positives (an employment-statute unit that merely mentions the Ley 19/2013), so a topic is now recognised from the leading statement. Aligning each topic's aspects with the unit's full scope is the next step (the normative material of the vertical slice).

## AT-119 (batch A) - Constitution topics for the Cuerpo General Auxiliar

Four topics of the Constitución Española (units 1 to 4 of the programme: principles and fundamental rights, Tribunal Constitucional, reform and Corona, Cortes Generales and Defensor del Pueblo, Poder Judicial) are now acquired from the BOE, with aspects taken from the official wording of each unit. The annex went from 3 to 7 of 28 units with material. Two findings: the article extractor assumed titled articles ("Artículo 1. Objeto.") and matched the page's navigation index, so it found nothing in the Constitution, whose articles are untitled headings; and a topic must check that a unit asks for everything the material covers, because the BOJA and Archiveros syllabi open with the same subject ("La Constitución Española de 1978") but list different subtopics. Those units stay unsupported rather than showing material designed for another scope. Every aspect-to-article mapping is still unreviewed and is checked against the live BOE by a `network` test.

## AT-119 (batch B) - Government, State administration and territorial organisation

Three more topics (units 5, 8 and 9 of the programme) were added, built from the Constitution, Ley 50/1997, Ley 40/2015 and Ley 7/1985. They needed two things the earlier topics did not: aspects drawing on articles of several laws (the removal of the Government is in the Constitution and in Ley 50/1997), now supported with per-law labels in the study text, and article titles read from the BOE instead of assumed (the Ley de Bases de Régimen Local has untitled article headings). The annex went from 7 to 10 of 28 units with material. The aspect-to-article mappings were built from the real article titles and all of them are checked against the live BOE. One known gap remains: unit 11 of the same programme asks for Ley 39/2015 and Ley 40/2015 and the contentious-administrative appeal, so its current Ley 39/2015 material still overstates what it covers.

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
