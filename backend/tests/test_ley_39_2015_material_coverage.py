from support import InMemoryKnowledgeRepository

from app.application.study_material import (
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import StudyProgrammeUnit


def test_acquired_ley_39_2015_material_covers_every_required_aspect() -> None:
    programme_unit = StudyProgrammeUnit(
        number=11,
        title="Las Leyes del Procedimiento Administrativo Común de las Administraciones",
        start_page=16,
        start_order=830,
        end_page=16,
        end_order=834,
    )
    repository = InMemoryKnowledgeRepository()
    need = derive_knowledge_needs_for_programme_unit(programme_unit)[0]

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        need,
        repository,
    )

    covered_aspects = derive_covered_aspects(programme_unit, knowledge)

    assert len(covered_aspects) == 8
    assert covered_aspects == derive_required_aspects_for_programme_unit(programme_unit)
