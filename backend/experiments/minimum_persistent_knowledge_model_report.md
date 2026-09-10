# AT-085 — Minimum Persistent Knowledge Model

## Objective

Determine the minimum information Atanor would need to retain so that previously constructed knowledge can be reproduced later without relying on experiment-local definitions.

The experiment intentionally does not modify the production domain model.

## Cases

Two previously validated KnowledgeNeeds were used:

1. `Derecho de acceso a la información pública` — Ley 19/2013.
2. `Métodos HTTP y semántica de las peticiones` — RFC 9110.

The cases represent different canonical domains while using the same conceptual construction flow.

## Experimental protocol

```text
validated case
    ↓
persistent candidate state
    ↓
baseline reconstruction
    ↓
remove one candidate field
    ↓
reconstruct
    ↓
compare with baseline
```

A field is considered **required by this experiment** when removing it changes the reconstruction signature.

## Candidate persistent state

The experiment groups the state into four categories:

```text
IDENTITY
    KnowledgeNeed title

EVIDENCE
    source identifier
    source locator
    evidence locations

KNOWLEDGE
    candidate-facing study sections

VALIDATION
    required aspects
    covered aspects attached to study sections
```

Coverage status itself is not persisted. It is reconstructed from required aspects and the aspects associated with the constructed study sections.

## Results

Both cases reproduced successfully from the candidate state.

Removing any of the following changed the reconstruction result in both cases:

- `knowledge_need_title`
- `evidence`
- `study_sections`
- `required_aspects`

Therefore the experiment demonstrates that these four coarse-grained state groups cannot be discarded if Atanor must reproduce the current experimental result exactly.

## Important observations

### 1. Evidence needs a location, not only a source

Persisting only `RFC 9110` or `BOE-A-2013-12887` is insufficient to identify which part of the canonical source supports the constructed knowledge.

The minimum evidence representation therefore needs at least:

```text
source identity
source locator
relevant locations
```

The experiment does not yet define a production `Evidence` entity.

### 2. Raw canonical source content does not need to be persisted

The experiment can reproduce the relationship to canonical evidence from source identity, locator, and relevant locations. The source itself can remain externally retrievable.

This does not prove that caching or snapshots are unnecessary for the product. It only shows that raw source content is not required by this reconstruction experiment.

### 3. Candidate-facing knowledge is state, not merely provenance

Knowing the KnowledgeNeed and its evidence does not reproduce the constructed study material. Some representation of the constructed knowledge must be retained, or a deterministic reconstruction process must exist.

For the current experiment, the smallest demonstrated representation is the set of study sections containing:

- title;
- candidate-facing content;
- evidence locations;
- covered aspects.

Whether these sections belong to the production domain or are an application/presentation artifact remains open.

### 4. Coverage is derived

The experiment does not persist `COVERED` or `MISSING`. Those values are reconstructed from the retained aspect information.

This reinforces the previous decision that coverage should remain derived rather than becoming persisted state prematurely.

### 5. Manual semantic validation creates a persistence requirement

The current semantic matching process is manual. Consequently, the experiment retains `covered_aspects` with the constructed study sections so that the current validation result can be reproduced.

If Atanor later acquires a deterministic and trustworthy semantic-matching mechanism, this information may become derivable instead.

## Architectural decision

**No production domain change is justified by AT-085 yet.**

The experiment demonstrates a minimum **information set**, not yet a minimum production entity model.

The strongest current candidate for persistent state is:

```text
KnowledgeNeed
    ↓
Evidence references
    ↓
Constructed knowledge representation
```

with validation metadata retained only because the current semantic evaluation is manual.

## Remaining questions

1. Can `EvidenceReference` be minimally generalized across legal provisions, RFC sections, and other source structures without introducing source-specific abstractions?
2. Is candidate-facing `StudySection` actually domain state, or should it remain an application/content representation of `Knowledge`?
3. Which parts of the semantic aspect model belong to the KnowledgeNeed and which belong to the constructed knowledge?
4. Can the same persistent state reconstruct knowledge after the source has changed, or will Atanor eventually need source snapshots/versioning?

These questions should be answered by further evidence rather than by extending the domain model speculatively.

## Conclusion

AT-085 successfully moves the investigation from **"can the process be reproduced in an experiment?"** to **"what information must survive for the product to reproduce it later?"**.

The experiment supports three strong conclusions:

- Knowledge construction requires persistent provenance from a KnowledgeNeed to specific source locations.
- The constructed candidate-facing knowledge cannot be recovered from provenance alone.
- Coverage can remain derived, but the current manual semantic validation requires retaining the aspect mapping used to reproduce that result.

The next step should be a narrower modeling exploration of the `KnowledgeNeed → Evidence → constructed Knowledge` relationship before introducing production abstractions.
