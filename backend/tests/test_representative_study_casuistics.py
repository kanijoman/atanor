from app.application.study_material import (
    build_study_coverage_summary,
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import StudyProgrammeUnit
from app.infrastructure.knowledge_repository import InMemoryKnowledgeRepository


def real_data_modelling_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=1,
        title=(
            "Modelado de datos, metodologías y reglas. Entidades, atributos y relaciones."
        ),
        start_page=1,
        start_order=1,
        end_page=1,
        end_order=2,
    )


def test_data_modelling_casuistic_represents_structured_technical_concepts() -> None:
    programme_unit = real_data_modelling_programme_unit()
    repository = InMemoryKnowledgeRepository()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    assert len(needs) == 1
    assert needs[0].topic == "Modelado de datos"
    assert needs[0].depth == 1
    assert needs[0].identity_key == (
        "Modelado de datos",
        1,
    )

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        needs[0],
        repository,
    )

    assert knowledge.title == needs[0].topic
    assert knowledge.identity_key == needs[0].identity_key
    assert knowledge.description
    assert len(knowledge.sources) >= 1
    assert repository.get_by_identity(needs[0].identity_key) is knowledge

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)

    assert required_aspects == (
        "Entidades",
        "Atributos",
        "Relaciones",
        "Metodologías y reglas de modelado",
    )
    assert covered_aspects == required_aspects


def test_data_modelling_study_content_explains_required_technical_concepts() -> None:
    programme_unit = real_data_modelling_programme_unit()
    repository = InMemoryKnowledgeRepository()
    need = derive_knowledge_needs_for_programme_unit(programme_unit)[0]

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        need,
        repository,
    )

    content = knowledge.description.casefold()

    assert "entidad" in content
    assert "tipo de entidad" in content

    assert "atributo" in content
    assert "propiedad" in content

    assert "relación" in content
    assert "cardinalidad" in content

    assert "metodología" in content
    assert "regla" in content
    assert "consistencia" in content
