from uuid import UUID

import pytest

from app.application.study_material import (
    generate_access_to_public_information_material,
    generate_study_material_for_programme_unit,
    prepare_programme_unit_for_study,
)
from app.domain.models import (
    Call,
    KnowledgeNeed,
    Source,
    StudyProgramme,
    StudyProgrammeUnit,
)


class InMemoryKnowledgeRepository:
    def __init__(self) -> None:
        self.items = {}

    def save(self, knowledge):
        self.items[knowledge.id] = knowledge
        return knowledge

    def get_by_id(self, knowledge_id: UUID):
        return self.items.get(knowledge_id)


def real_access_to_public_information_programme() -> tuple[
    StudyProgramme, StudyProgrammeUnit
]:
    source = Source(
        title="Real examination call",
        locator="call.pdf",
    )
    call = Call(title="Real examination call", source_id=source.id)
    programme = StudyProgramme(
        call_id=call.id,
        identifier="I",
        title="Programa oficial",
        units=(
            StudyProgrammeUnit(
                number=1,
                title="Derecho de acceso a la información pública",
                start_page=10,
                start_order=100,
                end_page=12,
                end_order=120,
            ),
        ),
    )
    return programme, programme.units[0]


def test_generates_candidate_facing_material_for_access_to_public_information() -> None:
    need = KnowledgeNeed(
        topic="Derecho de acceso a la información pública",
        depth=1,
    )
    repository = InMemoryKnowledgeRepository()

    knowledge = generate_access_to_public_information_material(need, repository)

    assert knowledge.title == need.topic
    assert knowledge.description
    assert "1. Concepto y titulares" in knowledge.description
    assert "10. Recursos y reclamaciones" in knowledge.description
    assert "Artículo 12" in knowledge.description
    assert "(Artículos 23 y 24)" in knowledge.description


def test_candidate_facing_material_contains_explanations_and_relevant_concepts() -> None:
    need = KnowledgeNeed(
        topic="Derecho de acceso a la información pública",
        depth=1,
    )
    repository = InMemoryKnowledgeRepository()

    material = generate_access_to_public_information_material(need, repository)

    assert "información pública" in material.description.lower()
    assert "límites" in material.description.lower()
    assert "protección de datos" in material.description.lower()
    assert "solicitud" in material.description.lower()
    assert "inadmitir" in material.description.lower()
    assert "resolución" in material.description.lower()
    assert "reclamación" in material.description.lower()


def test_candidate_facing_material_retains_canonical_evidence_reference() -> None:
    need = KnowledgeNeed(
        topic="Derecho de acceso a la información pública",
        depth=1,
    )
    repository = InMemoryKnowledgeRepository()

    material = generate_access_to_public_information_material(need, repository)

    assert len(material.sources) == 1
    assert material.sources[0].title.startswith("Ley 19/2013")
    assert material.sources[0].locator == (
        "https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887"
    )


def test_generated_material_can_be_retrieved_after_persistence() -> None:
    need = KnowledgeNeed(
        topic="Derecho de acceso a la información pública",
        depth=1,
    )
    repository = InMemoryKnowledgeRepository()

    saved = generate_access_to_public_information_material(need, repository)
    retrieved = repository.get_by_id(saved.id)

    assert retrieved == saved
    assert retrieved is not None
    assert retrieved.description == saved.description


def test_generated_material_is_reproducible_for_the_same_knowledge_need() -> None:
    need = KnowledgeNeed(
        topic="Derecho de acceso a la información pública",
        depth=1,
    )
    first_repository = InMemoryKnowledgeRepository()
    second_repository = InMemoryKnowledgeRepository()

    first = generate_access_to_public_information_material(need, first_repository)
    second = generate_access_to_public_information_material(need, second_repository)

    assert first.title == second.title
    assert first.description == second.description
    assert first.sources == second.sources


def test_generates_material_from_a_programme_item_and_persists_it() -> None:
    programme, programme_unit = real_access_to_public_information_programme()
    need = KnowledgeNeed(
        topic=programme_unit.title,
        depth=1,
    )
    repository = InMemoryKnowledgeRepository()

    material = generate_study_material_for_programme_unit(
        programme_unit,
        need,
        repository,
    )

    assert programme.units[0] == programme_unit
    assert material.title == programme_unit.title
    assert repository.get_by_id(material.id) == material


def test_rejects_a_knowledge_need_that_does_not_match_the_programme_item() -> None:
    _, programme_unit = real_access_to_public_information_programme()
    need = KnowledgeNeed(
        topic="Unrelated topic",
        depth=1,
    )
    repository = InMemoryKnowledgeRepository()

    with pytest.raises(ValueError, match="does not match"):
        generate_study_material_for_programme_unit(
            programme_unit,
            need,
            repository,
        )


def test_prepares_study_material_from_a_programme_item_without_manual_knowledge_need() -> None:
    programme, programme_unit = real_access_to_public_information_programme()
    repository = InMemoryKnowledgeRepository()

    material = prepare_programme_unit_for_study(
        programme_unit,
        repository,
    )

    assert programme.units[0] == programme_unit
    assert material.title == programme_unit.title
    assert material.description
    assert repository.get_by_id(material.id) == material
