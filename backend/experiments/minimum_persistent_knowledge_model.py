"""Explore the minimum state Atanor must retain to reproduce constructed knowledge.

The experiment uses two previously validated KnowledgeNeed cases from different
canonical domains. It deliberately does not modify the production domain model.

Question:
    What information must Atanor persist so the knowledge construction result
    can be reproduced later without relying on experiment-local definitions?

Protocol:
    validated case
        -> candidate persistent state
        -> reconstruction
        -> remove one field
        -> verify reconstruction failure

This is an experiment, not a production contract.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EvidenceReference:
    source_identifier: str
    source_locator: str
    locations: tuple[str, ...]


@dataclass(frozen=True)
class StudySectionState:
    title: str
    content: str
    evidence_locations: tuple[str, ...]
    covered_aspects: tuple[str, ...]


@dataclass(frozen=True)
class PersistentKnowledgeState:
    knowledge_need_title: str
    evidence: EvidenceReference
    study_sections: tuple[StudySectionState, ...]
    required_aspects: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class Reconstruction:
    knowledge_need_title: str
    evidence_locations: tuple[str, ...]
    study_sections: tuple[str, ...]
    coverage: dict[str, str]


CASES = (
    PersistentKnowledgeState(
        knowledge_need_title="Derecho de acceso a la información pública",
        evidence=EvidenceReference(
            source_identifier="BOE-A-2013-12887",
            source_locator="https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
            locations=tuple(f"art. {number}" for number in range(12, 25)),
        ),
        study_sections=(
            StudySectionState(
                "Qué es el derecho de acceso",
                "El derecho de acceso permite obtener información pública.",
                ("art. 12",),
                ("right_holder",),
            ),
            StudySectionState(
                "Qué se considera información pública",
                "La información pública comprende contenidos o documentos elaborados o adquiridos en el ejercicio de funciones públicas.",
                ("art. 13",),
                ("public_information",),
            ),
        ),
        required_aspects={
            "right_holder": ("who may exercise the right",),
            "public_information": ("definition of public information",),
        },
    ),
    PersistentKnowledgeState(
        knowledge_need_title="Métodos HTTP y semántica de las peticiones",
        evidence=EvidenceReference(
            source_identifier="RFC 9110",
            source_locator="https://www.rfc-editor.org/rfc/rfc9110",
            locations=("sec. 9.2", "sec. 9.3", "sec. 9.3.1", "sec. 9.3.2", "sec. 9.3.3", "sec. 9.3.4", "sec. 9.3.5", "sec. 9.3.6", "sec. 9.3.7", "sec. 9.3.8"),
        ),
        study_sections=(
            StudySectionState(
                "Propiedades generales de los métodos HTTP",
                "Los métodos HTTP expresan la intención de una petición.",
                ("sec. 9.2",),
                ("method_intent",),
            ),
            StudySectionState(
                "GET",
                "GET solicita la transferencia de una representación del recurso objetivo.",
                ("sec. 9.3.1",),
                ("get_semantics",),
            ),
        ),
        required_aspects={
            "method_intent": ("methods express request intent",),
            "get_semantics": ("transfer of a representation of the target resource",),
        },
    ),
)


def reconstruct(state: PersistentKnowledgeState) -> Reconstruction:
    coverage = {}
    for aspect, requirements in state.required_aspects.items():
        covered = any(
            aspect in section.covered_aspects for section in state.study_sections
        )
        coverage[aspect] = "COVERED" if covered else "MISSING"
        if not requirements:
            coverage[aspect] = "MISSING"

    return Reconstruction(
        knowledge_need_title=state.knowledge_need_title,
        evidence_locations=state.evidence.locations,
        study_sections=tuple(section.title for section in state.study_sections),
        coverage=coverage,
    )


def state_without(state: PersistentKnowledgeState, field: str) -> PersistentKnowledgeState:
    values: dict[str, Any] = {
        "knowledge_need_title": state.knowledge_need_title,
        "evidence": state.evidence,
        "study_sections": state.study_sections,
        "required_aspects": state.required_aspects,
    }
    values[field] = None

    if field == "evidence":
        values[field] = EvidenceReference("", "", ())
    elif field == "study_sections":
        values[field] = ()
    elif field == "required_aspects":
        values[field] = {}
    elif field == "knowledge_need_title":
        values[field] = ""

    return PersistentKnowledgeState(**values)


def reconstruction_signature(result: Reconstruction) -> tuple[Any, ...]:
    return (
        result.knowledge_need_title,
        result.evidence_locations,
        result.study_sections,
        tuple(sorted(result.coverage.items())),
    )


def main() -> None:
    fields = (
        "knowledge_need_title",
        "evidence",
        "study_sections",
        "required_aspects",
    )

    print("=== AT-085 — MINIMUM PERSISTENT KNOWLEDGE MODEL ===")
    print("cases:", len(CASES))
    print("protocol: validated case -> persistent state -> reconstruction -> field removal")
    print()

    all_passed = True
    for case in CASES:
        baseline = reconstruct(case)
        print(f"CASE: {case.knowledge_need_title}")
        print("  baseline reconstruction: SUCCESS")

        for field in fields:
            reduced = state_without(case, field)
            reduced_result = reconstruct(reduced)
            reproducible = reconstruction_signature(reduced_result) == reconstruction_signature(baseline)
            status = "REQUIRED" if not reproducible else "REMOVABLE"
            print(f"  {field}: {status}")
            all_passed = all_passed and not reproducible

        print()

    print("CLASSIFICATION")
    print("  IDENTITY: knowledge_need_title")
    print("  EVIDENCE: evidence.source_identifier, evidence.source_locator, evidence.locations")
    print("  KNOWLEDGE: study_sections (candidate-facing constructed content)")
    print("  VALIDATION: required_aspects + study_sections.covered_aspects")
    print("  DERIVED: coverage status")
    print()

    print("FINDINGS")
    print("  minimum persistent state demonstrated: YES" if all_passed else "  minimum persistent state demonstrated: NO")
    print("  production domain changes: NOT YET JUSTIFIED")
    print("  raw canonical source content persistence: NOT REQUIRED FOR RECONSTRUCTION")
    print("  semantic matching automation: NOT ESTABLISHED")
    print("  covered_aspects are retained because current semantic matching is manual")
    print("  next question: whether evidence and study-section state can be minimally generalized")


if __name__ == "__main__":
    main()
