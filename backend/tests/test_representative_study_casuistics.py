from app.application.study_material import (
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import KnowledgeNeed, StudyProgrammeUnit


class InMemoryKnowledgeRepository:
    def __init__(self) -> None:
        self.items = {}

    def save(self, knowledge):
        self.items[knowledge.id] = knowledge
        return knowledge

    def get_by_identity(self, identity_key: tuple[str, int]):
        return next(
            (
                knowledge
                for knowledge in self.items.values()
                if knowledge.identity_key == identity_key
            ),
            None,
        )


def real_ley_39_2015_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=1,
        title=(
            "La Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo "
            "Común de las Administraciones Públicas. Objeto y ámbito de aplicación"
        ),
        start_page=1,
        start_order=1,
        end_page=1,
        end_order=2,
    )


def test_ley_39_2015_casuistic_exercises_partial_coverage() -> None:
    programme_unit = real_ley_39_2015_programme_unit()
    repository = InMemoryKnowledgeRepository()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    assert len(needs) == 1
    assert needs[0].topic == "Procedimiento administrativo común"
    assert needs[0].depth == 1
    assert needs[0].identity_key == (
        "Procedimiento administrativo común",
        1,
    )

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        needs[0],
        repository,
    )

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)

    assert len(required_aspects) == 8
    assert covered_aspects == required_aspects[:2]
    assert covered_aspects != required_aspects
