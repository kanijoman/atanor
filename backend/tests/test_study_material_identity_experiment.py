from app.application.study_material import (
    derive_knowledge_needs_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import Knowledge, StudyProgrammeUnit


class InMemoryKnowledgeRepository:
    def __init__(self) -> None:
        self.items: dict = {}

    def save(self, knowledge: Knowledge) -> Knowledge:
        self.items[knowledge.id] = knowledge
        return knowledge

    def get_by_identity(self, identity_key: tuple[str, int]) -> Knowledge | None:
        return next(
            (
                knowledge
                for knowledge in self.items.values()
                if knowledge.identity_key == identity_key
            ),
            None,
        )


def test_same_knowledge_need_from_different_programme_units_reuses_material() -> None:
    first_unit = StudyProgrammeUnit(
        number=1,
        title="Derecho de acceso a la información pública",
        start_page=10,
        start_order=100,
        end_page=12,
        end_order=120,
    )
    second_unit = StudyProgrammeUnit(
        number=7,
        title="La Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información",
        start_page=40,
        start_order=400,
        end_page=42,
        end_order=420,
    )
    repository = InMemoryKnowledgeRepository()

    first_need = derive_knowledge_needs_for_programme_unit(first_unit)[0]
    second_need = derive_knowledge_needs_for_programme_unit(second_unit)[0]

    first_material = generate_study_material_for_programme_unit(
        first_unit,
        first_need,
        repository,
    )
    second_material = generate_study_material_for_programme_unit(
        second_unit,
        second_need,
        repository,
    )

    assert first_need.identity_key == second_need.identity_key
    assert first_need.id != second_need.id
    assert first_material is second_material
    assert first_material.title == second_material.title
    assert first_material.description == second_material.description
    assert first_material.sources == second_material.sources
    assert len(repository.items) == 1
