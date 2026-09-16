from app.application.study_material import (
    derive_knowledge_needs_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import Knowledge, StudyProgrammeUnit


class InMemoryKnowledgeRepository:
    def __init__(self) -> None:
        self.knowledge: dict[tuple[str, int], Knowledge] = {}

    def save(self, knowledge: Knowledge) -> Knowledge:
        if knowledge.identity_key is not None:
            self.knowledge[knowledge.identity_key] = knowledge
        return knowledge

    def get_by_identity(self, identity_key: tuple[str, int]) -> Knowledge | None:
        return self.knowledge.get(identity_key)


def test_current_ley_39_2015_material_covers_two_of_eight_required_aspects() -> None:
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

    required_aspects = (
        "Objeto y finalidad del procedimiento administrativo común",
        "Ámbito subjetivo de aplicación",
        "Interesados, capacidad, representación y derechos",
        "Actividad administrativa, plazos y medios electrónicos",
        "Actos administrativos: requisitos, eficacia e invalidez",
        "Procedimiento administrativo común y sus fases",
        "Procedimientos sancionador y de responsabilidad patrimonial",
        "Revisión de actos, recursos, iniciativa legislativa y potestad reglamentaria",
    )
    covered_aspects = (
        aspect
        for aspect in required_aspects
        if aspect in knowledge.description
    )

    assert tuple(covered_aspects) == required_aspects[:2]
