from pathlib import Path

import pytest
from support import FixtureSourceRetriever

from app.application.call_discovery import discover_call
from app.application.study_material.registry import find_topic_for_title
from app.application.study_material.topics import administrative_procedure_and_appeals, procedure
from app.domain.models import Knowledge, Source, StudyProgrammeUnit

SAMPLES = Path(__file__).parent / "samples"
TOPIC = administrative_procedure_and_appeals.TOPIC


@pytest.fixture(scope="module")
def unit_11() -> StudyProgrammeUnit:
    """Unit 11 of Bloque I, Annex I (Cuerpo General Auxiliar de la AGE)."""
    path = SAMPLES / "BOE-A-2024-14098.pdf"
    discovered = discover_call(Source(title=path.name, locator=str(path)))
    assert discovered is not None
    programme = next(p for p in discovered.programmes if p.identifier == "I")
    return next(u for u in programme.units if u.section.startswith("I.") and u.number == 11)


def _material() -> Knowledge:
    description = TOPIC.provider.description(FixtureSourceRetriever())
    return Knowledge(title=TOPIC.name, description=description, sources=TOPIC.provider.sources)


def test_the_real_unit_asks_for_laws_review_and_judicial_appeal(unit_11) -> None:
    assert "Régimen Jurídico del Sector Público" in unit_11.title
    assert "El recurso contencioso-administrativo" in unit_11.title
    assert "capacidad, legitimación, representación y defensa" in unit_11.title


def test_the_unit_is_recognised_by_the_topic_that_covers_its_whole_scope(unit_11) -> None:
    assert find_topic_for_title(unit_11.title) is TOPIC


def test_every_aspect_of_the_unit_is_covered_by_the_acquired_articles() -> None:
    knowledge = _material()

    assert TOPIC.covered_aspects(knowledge, TOPIC.required_aspects) == TOPIC.required_aspects
    assert len(TOPIC.required_aspects) == 6


def test_the_material_draws_on_the_three_laws_and_labels_each_article() -> None:
    text = _material().description

    cited = {source.locator.rsplit("=", 1)[1] for source in TOPIC.provider.sources}
    assert cited == {"BOE-A-2015-10565", "BOE-A-2015-10566", "BOE-A-1998-16718"}
    assert "Ley 39/2015, Artículo 106. Revisión de disposiciones y actos nulos." in text
    assert "Ley 40/2015, Artículo 3. Principios generales." in text
    assert "Ley 29/1998, Artículo 25." in text


def test_a_unit_that_asks_for_the_judicial_appeal_is_not_covered_by_the_law_alone() -> None:
    wording = (
        "Las Leyes del Procedimiento Administrativo Común de las Administraciones Públicas y del "
        "Régimen Jurídico del Sector Público. El procedimiento administrativo común y sus fases."
    )

    assert find_topic_for_title(wording) is None


def test_a_unit_that_asks_for_more_than_the_topic_covers_is_not_claimed(unit_11) -> None:
    wording = f"{unit_11.title} La responsabilidad patrimonial de las Administraciones Públicas."

    assert find_topic_for_title(wording) is None


def test_the_law_alone_keeps_its_own_narrower_topic() -> None:
    law_alone = "La Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común."

    assert find_topic_for_title(law_alone) is procedure.TOPIC


def test_the_narrower_topic_is_not_applied_to_a_wider_syllabus() -> None:
    wider = (
        "La Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las "
        "Administraciones Públicas. El recurso contencioso-administrativo."
    )

    assert find_topic_for_title(wider) is None
