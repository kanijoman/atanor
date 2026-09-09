# Candidate Study Programme Real-Data Validation

## Purpose

This report records the evidence produced by the real-data experiment for AT-081.7.

The experiment evaluates whether the current Atanor domain model can represent a candidate-oriented study programme by relating official programme units to knowledge needs and distinguishing covered and missing knowledge.

It is a bounded validation experiment. It does not introduce new domain mechanisms, semantic matching, AI, persistence, API or UI behavior.

## Important limitation

The current requirement-discovery pipeline produces `RequirementMention` objects but does not yet construct `RequirementScope` and `KnowledgeNeed` objects from those mentions. The experiment therefore builds a minimal in-memory structural probe containing a scope and one knowledge need for structurally matching real mentions.

Consequently, the experiment validates that the existing candidate-study projection and domain model can represent the relationship, but it does **not** validate an end-to-end pipeline that derives real scopes and knowledge needs from discovered requirements.

Coverage is also not available from the current real-document pipeline, so all probe needs are reported as missing. This is a pipeline capability gap, not evidence that the underlying knowledge is absent.

## Sample results

### BOE — `BOE-A-2024-14098.pdf`

| Programme | Units | Structural matches | Mapped units | Unmapped units |
| --- | ---: | ---: | ---: | ---: |
| I | 28 | 67 | 28/28 | 0 |
| II | 8 | 23 | 8/8 | 0 |
| III | 45 | 101 | 45/45 | 0 |
| IV | 17 | 42 | 17/17 | 0 |
| V | 33 | 67 | 33/33 | 0 |
| VI | 25 | 59 | 25/25 | 0 |
| VII | 58 | 96 | 58/58 | 0 |
| VIII | 35 | 84 | 35/35 | 0 |
| IX | 57 | 110 | 57/57 | 0 |
| X | 57 | 102 | 53/57 | 4 |

Result: strong structural validation. Nine programmes map all discovered units; Programme X has four unmapped units and remains representable without requiring a model change.

### BOJA — `BOJA24-138-00046-48048-01_00304998.pdf`

| Programme | Units | Structural matches | Mapped units | Unmapped units |
| --- | ---: | ---: | ---: | ---: |
| II.1 | 30 | 30 | 30/30 | 0 |
| II.A | 39 | 41 | 39/39 | 0 |
| II.B | 40 | 42 | 40/40 | 0 |
| II.C | 40 | 40 | 40/40 | 0 |
| II.D | 40 | 40 | 40/40 | 0 |
| II.E | 40 | 40 | 40/40 | 0 |
| II.F | 40 | 40 | 40/40 | 0 |

Result: excellent structural validation. Every discovered programme unit can be represented by the candidate-study projection.

### Archiveros — `Programa_Archiveros_0.pdf`

| Programme | Units | Structural matches | Mapped units | Unmapped units |
| --- | ---: | ---: | ---: | ---: |
| I | 25 | 1 | 1/25 | 24 |

Result: negative validation for the current deterministic title-based matching approach. The sample remains structurally discoverable, but the current matching strategy cannot reliably relate most of its units to requirement mentions. This is a matching limitation, not evidence of a domain-model incompatibility.

### León — `OPOS_AYTO_LEON_INFORMATICA_B.pdf`

| Programmes discovered | Requirement mentions | Candidate-study validation |
| ---: | ---: | --- |
| 0 | 0 | Not reachable |

Result: negative validation at the document-processing boundary. The PDF is a scanned/image-only document, so the current text-extraction pipeline cannot discover its programme or requirements. OCR/image-document processing is required before this sample can participate in downstream validation.

## Interpretation

The experiment provides sufficient evidence to close the AT-081.7 validation with **GO, with explicit debt**:

- The existing domain model and candidate-study projection are structurally compatible with real programme data.
- BOE and BOJA provide strong positive evidence across multiple programmes and units.
- Unmapped units are representable and do not force a new domain abstraction.
- Archiveros exposes a deterministic matching limitation that should remain explicit rather than being hidden by semantic guessing.
- León is a valid negative test for the current text-extraction boundary because it is scanned/image-only. OCR should be treated as separate future work.
- Real `RequirementScope` / `KnowledgeNeed` construction from the requirement pipeline is still missing and should be tracked as separate work if required by the next candidate-facing workflow.
- Real knowledge coverage is not yet available in this experiment and should not be inferred from the probe.

No domain-model change is justified by this experiment.

## Reproducibility

The executable experiment is:

`backend/experiments/candidate_study_programme_real_data.py`

Run from `backend` with:

```text
uv run python .\\experiments\\candidate_study_programme_real_data.py
```

The report records the observed output from the validation run so future work can continue from the same evidence without repeating the exploratory reasoning.
