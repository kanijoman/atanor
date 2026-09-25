from app.application.study_material import (
    derive_knowledge_needs_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import Knowledge, StudyProgrammeUnit


class InMemoryKnowledgeRepository:
    def __init__(self) -> None:
        self.knowledge: Knowledge | None = None

    def save(self, knowledge: Knowledge) -> Knowledge:
        self.knowledge = knowledge
        return knowledge

    def get_by_identity(self, identity_key: tuple[str, int]) -> Knowledge | None:
        if self.knowledge is not None and self.knowledge.identity_key == identity_key:
            return self.knowledge
        return None


def real_personal_data_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=7,
        title=(
            "La protección de datos personales y su régimen jurídico: "
            "principios, derechos y obligaciones. Derechos digitales."
        ),
        start_page=86778,
        start_order=3,
        end_page=86778,
        end_order=4,
    )


def test_derives_knowledge_need_for_real_personal_data_programme_unit() -> None:
    programme_unit = real_personal_data_programme_unit()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)

    assert len(needs) == 1
    assert needs[0].topic == "Protección de datos personales"
    assert needs[0].depth == 1
    assert needs[0].identity_key == ("Protección de datos personales", 1)


def test_generates_personal_data_study_material_with_canonical_sources() -> None:
    programme_unit = real_personal_data_programme_unit()
    need = derive_knowledge_needs_for_programme_unit(programme_unit)[0]
    repository = InMemoryKnowledgeRepository()

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        need,
        repository,
    )

    assert knowledge.title == "Protección de datos personales"
    assert knowledge.identity_key == ("Protección de datos personales", 1)
    assert knowledge.description is not None
    assert "Principios del tratamiento" in knowledge.description
    assert "Derechos de las personas" in knowledge.description
    assert "Obligaciones y responsabilidad" in knowledge.description

    assert len(knowledge.sources) == 2
    assert knowledge.sources[0].title == (
        "Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016"
    )
    assert knowledge.sources[0].locator == (
        "https://eur-lex.europa.eu/eli/reg/2016/679/oj/spa"
    )
    assert knowledge.sources[1].title == (
        "Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales "
        "y garantía de los derechos digitales"
    )
    assert knowledge.sources[1].locator == (
        "https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673"
    )
