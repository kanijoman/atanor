from support import InMemoryKnowledgeRepository

from app.application.study_material import (
    build_study_coverage_summary,
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import StudyProgrammeUnit


def real_object_oriented_programming_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=4,
        title=(
            "Diseño y programación orientada a objetos. Elementos y componentes "
            "software: objetos, clases, herencia, métodos, sobrecarga. Ventajas "
            "e inconvenientes. Patrones de diseño y lenguaje de modelado unificado "
            "(UML)."
        ),
        start_page=86778,
        start_order=1,
        end_page=86778,
        end_order=2,
    )


def test_derives_knowledge_need_for_real_object_oriented_programming_programme_unit() -> None:
    programme_unit = real_object_oriented_programming_programme_unit()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)

    assert len(needs) == 1
    assert needs[0].topic == "Programación orientada a objetos"
    assert needs[0].depth == 1
    assert needs[0].identity_key == ("Programación orientada a objetos", 1)


def test_generates_useful_object_oriented_programming_study_material() -> None:
    programme_unit = real_object_oriented_programming_programme_unit()
    need = derive_knowledge_needs_for_programme_unit(programme_unit)[0]
    repository = InMemoryKnowledgeRepository()

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        need,
        repository,
    )

    assert knowledge.title == "Programación orientada a objetos"
    assert knowledge.identity_key == ("Programación orientada a objetos", 1)
    assert knowledge.description is not None

    study_content = knowledge.description.casefold()
    assert "clases" in study_content
    assert "objetos" in study_content
    assert "encapsulación" in study_content
    assert "herencia" in study_content
    assert "polimorfismo" in study_content

    assert len(knowledge.sources) == 1
    assert knowledge.sources[0].title == "Python Documentation, Classes"
    assert knowledge.sources[0].locator == "https://docs.python.org/3/tutorial/classes.html"


def test_object_oriented_programming_study_material_reports_partial_coverage() -> None:
    programme_unit = real_object_oriented_programming_programme_unit()
    need = derive_knowledge_needs_for_programme_unit(programme_unit)[0]
    repository = InMemoryKnowledgeRepository()
    knowledge = generate_study_material_for_programme_unit(programme_unit, need, repository)

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)

    summary = build_study_coverage_summary(
        need,
        required_aspects,
        covered_aspects,
    )

    assert required_aspects == (
        "Objetos y clases",
        "Herencia",
        "Métodos",
        "Sobrecarga",
        "Ventajas e inconvenientes de la programación orientada a objetos",
        "Patrones de diseño",
        "Lenguaje de modelado unificado (UML)",
    )
    assert covered_aspects == required_aspects
    assert summary.status == "covered"
    assert summary.covered_count == 7
    assert summary.required_count == 7
    assert summary.pending_aspects == ()
    assert summary.coverage_percentage == 100.0
