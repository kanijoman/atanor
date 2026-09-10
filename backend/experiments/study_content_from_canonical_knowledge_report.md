# AT-084 — Candidate-facing study content experiment

## Objective

Test whether a concrete `KnowledgeNeed` plus authoritative canonical evidence can be transformed into useful candidate-facing study material without prematurely extending the production domain model.

## Experimental case

- Knowledge need: **Derecho de acceso a la información pública**
- Canonical source: **Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno**
- Evidence range: **articles 12–24**
- Source authority: **Boletín Oficial del Estado**

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

The experiment now checks coverage at a finer granularity than article references.

A small manual matrix defines the aspects that should be present for each experimental concept. The study artifact is then compared with that matrix and each concept is classified as:

- **COVERED** — all required aspects are represented;
- **PARTIAL** — some required aspects are represented and others are missing;
- **MISSING** — none of the required aspects are represented.

This matrix is deliberately experimental. It is not a production domain model and does not imply that semantic matching has been solved automatically.

### Expected result for the current artifact

The probe intentionally exposes incompleteness in several concepts. In particular:

- `access_limits` is **PARTIAL** because the synthesis captures justification, proportionality and case-specific application but does not enumerate the protected interests;
- `personal_data` is **PARTIAL** because it acknowledges the specific regime but does not fully explain the relevant distinction;
- `resolution` is **PARTIAL** because it covers notification, the one-month deadline, the possible extension and the silence rule, but does not cover all relevant guarantees such as reasoned denial, judicial challenge and the optional claim;
- `information_units` is **PARTIAL** because the candidate-facing text is too generic to demonstrate all required aspects;
- other concepts can reach **COVERED** under the current manual matrix.

The important result is not the exact count. It is that a concept can cite the correct article and still be materially incomplete for study purposes.

## Findings

### 1. Article-level completeness is insufficient

All target articles 12–24 are referenced by the artifact. This demonstrates complete article-level traceability for the selected range.

It does **not** demonstrate that the candidate-facing content covers the knowledge expressed by those articles.

### 2. Semantic aspects provide a useful validation mechanism

The manual `concept → required aspects` matrix exposes omissions that article-level checks cannot detect. This is a stronger experimental signal for future coverage validation.

### 3. Semantic matching remains unresolved

The experiment currently supplies the aspect mapping manually. Therefore it demonstrates the shape of the validation problem, not an automated solution.

A future automated matcher would need to establish that a piece of candidate-facing content actually expresses a required aspect. That is a semantic validation problem and should not yet be hidden behind a production abstraction.

### 4. Candidate-facing content remains distinct from Knowledge and evidence

The experiment continues to support the separation between:

- canonical evidence;
- reusable knowledge concepts;
- candidate-facing pedagogical presentation;
- coverage evaluation.

These concerns are related but not interchangeable.

### 5. The current production model still does not need to change

The experiment has now demonstrated a concrete validation need, but it has not demonstrated the minimum stable representation that should become part of the production domain.

In particular, it is still premature to introduce production entities such as `CoverageAspect`, `EvidenceFragment`, `StudyContent` or richer coverage states solely from this case.

The next step should test whether the same semantic-coverage pattern repeats across another independently selected `KnowledgeNeed`.

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

The smallest justified architectural conclusion is that future coverage work will likely need semantic validation below the article level. The experiment does not yet justify choosing its final representation, persistence model or matching technology.

## Next smallest product experiment

Repeat the same manual semantic-coverage procedure with a second real `KnowledgeNeed` from the same legal corpus, preferably one whose structure differs from the current procedural topic.

Success would mean that the aspect-based validation pattern is useful beyond this single case. Failure would be equally valuable evidence against prematurely promoting it to the production model.

## Conclusion

**EXPERIMENT STATUS: SEMANTIC COVERAGE HYPOTHESIS SUPPORTED — PRODUCTION MODEL EXTENSION DEFERRED**

AT-084 now demonstrates three distinct levels:

1. article-level traceability;
2. concept-level organisation;
3. aspect-level coverage validation.

The third level catches real omissions that the first two cannot. That is sufficient evidence to continue the investigation, but not sufficient evidence to freeze a new production abstraction.
