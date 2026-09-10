from uuid import UUID

from app.application.study_material import (
    generate_access_to_public_information_material,
)
from app.domain.models import KnowledgeNeed


class InMemoryKnowledgeRepository:
    def __init__(self) -> None:
        self.items = {}

    def save(self, knowledge):
        self.items[knowledge.id] = knowledge
        return knowledge

    def get_by_id(self, knowledge_id: UUID):
        return self.items.get(knowledge_id)


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
    assert "Artículo 24" in knowledge.description


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
