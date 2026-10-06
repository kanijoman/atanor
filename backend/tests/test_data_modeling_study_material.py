from app.application.study_material import (
    build_study_coverage_summary,
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import Knowledge, KnowledgeNeed, StudyProgrammeUnit
from support import InMemoryKnowledgeRepository


def real_data_modeling_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=12,
        title=(
            "Modelos de datos. Entidades, atributos y relaciones. "
            "Modelo relacional. Normalización."
        ),
        start_page=86779,
        start_order=1,
        end_page=86779,
        end_order=2,
    )


def test_derives_knowledge_need_for_real_data_modeling_programme_unit() -> None:
    programme_unit = real_data_modeling_programme_unit()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)

    assert len(needs) == 1
    assert needs[0].topic == "Modelado de datos"
    assert needs[0].depth == 1
    assert needs[0].identity_key == ("Modelado de datos", 1)


def test_generates_useful_data_modeling_study_material() -> None:
    programme_unit = real_data_modeling_programme_unit()
    need = derive_knowledge_needs_for_programme_unit(programme_unit)[0]
    repository = InMemoryKnowledgeRepository()

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        need,
        repository,
    )

    assert knowledge.title == "Modelado de datos"
    assert knowledge.identity_key == ("Modelado de datos", 1)
    assert knowledge.description is not None

    study_content = knowledge.description.casefold()
    assert "entidades" in study_content
    assert "atributos" in study_content
    assert "relaciones" in study_content
    assert "modelo relacional" in study_content
    assert "normalización" in study_content

    assert len(knowledge.sources) == 1
    assert knowledge.sources[0].title == (
        "ISO/IEC 19763-12:2015, Information technology — Metamodel framework "
        "for interoperability (MFI) — Part 12: Metamodel for information model registration"
    )
    assert knowledge.sources[0].locator == "https://www.iso.org/standard/61559.html"


def test_data_modeling_study_material_covers_required_aspects() -> None:
    programme_unit = real_data_modeling_programme_unit()
    need = derive_knowledge_needs_for_programme_unit(programme_unit)[0]
    repository = InMemoryKnowledgeRepository()

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        need,
        repository,
    )
    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)
    summary = build_study_coverage_summary(
        KnowledgeNeed(topic=need.topic, depth=need.depth),
        required_aspects,
        covered_aspects,
    )

    assert required_aspects == (
        "Entidades",
        "Atributos",
        "Relaciones",
        "Modelo relacional",
        "Normalización",
        "Metodologías y reglas de modelado",
    )
    assert covered_aspects == required_aspects
    assert summary.status == "covered"
    assert summary.covered_count == 6
    assert summary.required_count == 6
    assert summary.pending_aspects == ()
    assert summary.coverage_percentage == 100.0


def test_data_modeling_study_material_reports_partial_coverage() -> None:
    programme_unit = real_data_modeling_programme_unit()
    need = derive_knowledge_needs_for_programme_unit(programme_unit)[0]
    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = (
        "Entidades",
        "Atributos",
        "Relaciones",
        "Metodologías y reglas de modelado",
    )

    summary = build_study_coverage_summary(
        KnowledgeNeed(topic=need.topic, depth=need.depth),
        required_aspects,
        covered_aspects,
    )

    assert summary.status == "partial"
    assert summary.covered_count == 4
    assert summary.required_count == 6
    assert summary.pending_aspects == (
        "Modelo relacional",
        "Normalización",
    )
    assert summary.coverage_percentage == (4 / 6) * 100
