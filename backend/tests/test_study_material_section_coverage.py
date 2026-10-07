import pytest
from support import InMemoryKnowledgeRepository

from app.application.study_material import (
    MaterialOrigin,
    ReviewStatus,
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_material_provenance,
    derive_required_aspects_for_programme_unit,
    generate_material_for_need,
)
from app.application.study_material.coverage import aspects_covered_by_sections
from app.domain.models import Knowledge, StudyProgrammeUnit

SECTION_BODY = " ".join(["contenido"] * 20)
REQUIRED = ("Concepto y alcance", "Límites del derecho")


def _knowledge(description: str) -> Knowledge:
    return Knowledge(title="Tema", description=description)


def test_aspect_is_covered_when_its_section_has_substantive_content() -> None:
    text = f"1. Concepto y alcance\n{SECTION_BODY}\n\n2. Límites del derecho\n{SECTION_BODY}"

    assert aspects_covered_by_sections(_knowledge(text), REQUIRED) == REQUIRED


def test_aspect_without_a_section_stays_pending() -> None:
    text = f"1. Concepto y alcance\n{SECTION_BODY}"

    assert aspects_covered_by_sections(_knowledge(text), REQUIRED) == ("Concepto y alcance",)


def test_section_with_only_a_few_words_is_not_evidence_of_coverage() -> None:
    text = f"1. Concepto y alcance\n{SECTION_BODY}\n\n2. Límites del derecho\nSe verá más adelante."

    assert aspects_covered_by_sections(_knowledge(text), REQUIRED) == ("Concepto y alcance",)


def test_heading_may_be_a_shorter_form_of_the_aspect() -> None:
    text = f"1. Concepto y titulares\n{SECTION_BODY}"
    aspects = ("Concepto y titulares del derecho de acceso",)

    assert aspects_covered_by_sections(_knowledge(text), aspects) == aspects


def _unit(title: str) -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=1, title=title, start_page=1, start_order=1, end_page=1, end_order=2
    )


SECTION_COVERED_UNITS = [
    "La Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública",
    "Identidad y firma electrónica. El DNI electrónico",
    "La protección de datos personales y su régimen jurídico",
    "Modelado de datos. Entidades, atributos y relaciones",
]


@pytest.mark.parametrize("title", SECTION_COVERED_UNITS)
def test_curated_material_covers_every_required_aspect_through_its_sections(title: str) -> None:
    unit = _unit(title)
    need = derive_knowledge_needs_for_programme_unit(unit)[0]
    knowledge = generate_material_for_need(need, InMemoryKnowledgeRepository())

    required = derive_required_aspects_for_programme_unit(unit)

    assert derive_covered_aspects(unit, knowledge) == required


def test_removing_a_section_from_curated_material_lowers_coverage() -> None:
    unit = _unit("Modelado de datos. Entidades, atributos y relaciones")
    need = derive_knowledge_needs_for_programme_unit(unit)[0]
    knowledge = generate_material_for_need(need, InMemoryKnowledgeRepository())
    truncated = Knowledge(
        title=knowledge.title,
        description=knowledge.description.split("4. Modelo relacional")[0],
        sources=knowledge.sources,
    )

    covered = derive_covered_aspects(unit, truncated)

    assert covered == ("Entidades", "Atributos", "Relaciones")


def test_current_study_material_is_labelled_as_curated_and_unreviewed() -> None:
    provenance = derive_material_provenance(
        _unit("Modelado de datos. Entidades, atributos y relaciones")
    )

    assert provenance.origin is MaterialOrigin.CURATED
    assert provenance.review_status is ReviewStatus.UNREVIEWED
