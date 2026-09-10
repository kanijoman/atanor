# AT-084 — Candidate-facing study content experiment

## Objective

Test whether a concrete `KnowledgeNeed` plus authoritative canonical evidence can be transformed into useful candidate-facing study material without prematurely extending the production domain model.

The experiment now also tests whether semantic coverage validation is repeatable across independently selected `KnowledgeNeed` instances.

## Experimental corpus

Both cases use the consolidated **Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno**, published by the **Boletín Oficial del Estado**.

The canonical source is deliberately kept constant so that the experiment isolates variation in the `KnowledgeNeed`, rather than mixing source-authority and topic effects.

## Iteration 1: candidate-facing structure

The first probe established a useful candidate-facing structure:

```text
Canonical evidence
        ↓
Candidate-facing synthesis
        ↓
Exam-oriented points
```

The artifact is intentionally authored in the experiment. It groups the legal provisions into concepts and procedures rather than reproducing the legal text.

The first probe also demonstrated that article references are useful for traceability but insufficient to establish learning coverage.

## Iteration 2: semantic coverage probe

The experiment checks coverage at a finer granularity than article references.

A small manual matrix defines the aspects that should be present for each experimental concept. The study artifact is then compared with that matrix and each concept is classified as:

- **COVERED** — all required aspects are represented;
- **PARTIAL** — some required aspects are represented and others are missing;
- **MISSING** — none of the required aspects are represented.

This matrix is deliberately experimental. It is not a production domain model and does not imply that semantic matching has been solved automatically.

For the first case, **Derecho de acceso a la información pública** (articles 12–24), the probe exposed incompleteness in several concepts. In particular, limits, personal-data handling, resolution and information units were only partially represented by the candidate-facing artifact.

The important result was not the exact count. It was that a concept can cite the correct article and still be materially incomplete for study purposes.

## Iteration 3: repeatability probe

The same protocol has now been applied to a second real `KnowledgeNeed` from the same legal corpus:

- Knowledge need: **Principios y obligaciones generales de publicidad activa**
- Evidence range: **articles 5–11**, including article 6 bis
- Topic shape: publication duties, publication quality, institutional and planning information, legal and economic information, compliance control, the Transparency Portal and technical principles

The second case is intentionally different from the first. The first case is primarily procedural and concerns the exercise of an individual right; the second concerns an organisation's proactive transparency obligations and contains lists, classifications and technical requirements.

The experiment uses the same protocol:

```text
KnowledgeNeed
      ↓
Canonical evidence
      ↓
Candidate-facing study content
      ↓
Manual required-aspects matrix
      ↓
Semantic coverage
```

The second case is designed to answer five questions:

1. Does the aspect-based validation mechanism remain useful outside the first procedural topic?
2. Can it still distinguish `COVERED`, `PARTIAL` and `MISSING`?
3. Are required aspects meaningful units independently of article boundaries?
4. Does the same conceptual shape recur even when the knowledge structure changes?
5. Is there now enough evidence to justify a minimal production abstraction?

### Experimental design

The implementation keeps the aspect matrices inside the experiment. The production domain remains unchanged.

Each case contains:

- a `KnowledgeNeed` description;
- canonical evidence articles;
- candidate-facing sections;
- a manual `concept → required aspects` matrix;
- a manual `concept → covered aspects` mapping;
- the same deterministic semantic-coverage evaluator.

This deliberately separates **repeatability of the validation protocol** from **automation of semantic matching**. The former can be tested now; the latter remains unresolved.

### Execution status

The repeatability implementation is committed, but its execution has not yet been validated in this environment. The repository-side experiment must be run against the canonical BOE source before recording the final repeatability finding.

Therefore this iteration must not yet be interpreted as evidence that the hypothesis has succeeded. The code currently establishes the experimental protocol and the second case; the next step is to execute it and inspect the actual output.

## Findings so far

### 1. Article-level completeness is insufficient

The first case demonstrated that referencing every target article does not establish that the candidate-facing content covers the knowledge expressed by those articles.

### 2. Semantic aspects provide a useful validation mechanism

The first case showed that the manual `concept → required aspects` matrix can expose omissions that article-level checks cannot detect.

### 3. Semantic matching remains unresolved

Both cases currently supply the aspect mapping manually. The experiment demonstrates the shape of the validation problem, not an automated solution.

### 4. Candidate-facing content remains distinct from Knowledge and evidence

The experiment continues to support the separation between:

- canonical evidence;
- reusable knowledge concepts;
- candidate-facing pedagogical presentation;
- coverage evaluation.

These concerns are related but not interchangeable.

### 5. Production architecture remains deliberately unchanged

No production entity has been introduced for coverage aspects, evidence fragments or study content.

The current evidence is not sufficient to freeze a representation, persistence model or semantic-matching technology.

## Candidate-facing value

The product value is becoming clearer:

```text
Knowledge Need
      ↓
Study Content
      ↓
Coverage
   /       \
covered   missing
```

Atanor should eventually be able to tell the candidate not only *what to study*, but also which relevant aspects are still missing from the material.

This is a stronger product proposition than simply attaching official sources to study notes.

## Architectural decision

**No production domain-model extension yet.**

The smallest justified architectural conclusion remains that future coverage work will likely need semantic validation below the article level. The repeatability experiment must first be executed before deciding whether the aspect structure is stable enough to generalise.

## Next smallest product experiment

Execute the updated experiment against the canonical BOE source and compare both cases.

If the same validation protocol remains useful, identify the smallest common abstraction shared by both cases. If it does not, keep the mechanism experimental and investigate which parts are topic-specific.

Only after that evidence should a production coverage abstraction be considered.

## Conclusion

**EXPERIMENT STATUS: REPEATABILITY PROBE IMPLEMENTED — EXECUTION PENDING**

AT-084 currently demonstrates three levels worth preserving as hypotheses:

1. article-level traceability;
2. concept-level organisation;
3. aspect-level coverage validation.

The next decision should be driven by the second real KnowledgeNeed execution rather than by architectural preference.
