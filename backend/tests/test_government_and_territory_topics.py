from pathlib import Path

import pytest
from support import FixtureSourceRetriever

from app.application.call_discovery import discover_call
from app.application.study_material.registry import find_topic_for_title
from app.application.study_material.topics import (
    constitution,
    government,
    state_administration,
    territorial_organisation,
)
from app.application.study_programmes import discover_programmes
from app.domain.models import Call, Knowledge, Source, StudyProgrammeUnit

SAMPLES = Path(__file__).parent / "samples"
BATCH_B = [government, state_administration, territorial_organisation]


@pytest.fixture(scope="module")
def auxiliar_units() -> list[StudyProgrammeUnit]:
    """Bloque I of Annex I (Cuerpo General Auxiliar de la AGE), in document order."""
    path = SAMPLES / "BOE-A-2024-14098.pdf"
    discovered = discover_call(Source(title=path.name, locator=str(path)))
    assert discovered is not None
    programme = next(p for p in discovered.programmes if p.identifier == "I")
    return [unit for unit in programme.units if unit.section.startswith("I.")]


def _material(module) -> Knowledge:
    topic = module.TOPIC
    description = topic.provider.description(FixtureSourceRetriever())
    return Knowledge(title=topic.name, description=description, sources=topic.provider.sources)


@pytest.mark.parametrize("module", BATCH_B, ids=lambda m: m.__name__.split(".")[-1])
def test_every_aspect_is_covered_by_the_acquired_articles(module) -> None:
    topic = module.TOPIC

    knowledge = _material(module)

    assert topic.covered_aspects(knowledge, topic.required_aspects) == topic.required_aspects


@pytest.mark.parametrize(
    ("module", "locators"),
    [
        (
            government,
            {"BOE-A-1978-31229", "BOE-A-1997-25336"},
        ),
        (state_administration, {"BOE-A-2015-10566"}),
        (
            territorial_organisation,
            {"BOE-A-1978-31229", "BOE-A-1985-5392"},
        ),
    ],
    ids=["government", "state_administration", "territorial_organisation"],
)
def test_material_cites_every_law_it_draws_from(module, locators) -> None:
    cited = {source.locator.rsplit("=", 1)[1] for source in module.TOPIC.provider.sources}

    assert cited == locators


def test_articles_are_labelled_with_their_law_when_a_topic_mixes_laws() -> None:
    text = _material(government).description

    assert "Constitución Española, Artículo 99." in text
    assert "Ley 50/1997, Artículo 5. Del Consejo de Ministros." in text


def test_articles_are_not_labelled_when_a_topic_uses_one_law() -> None:
    text = _material(state_administration).description

    assert "  Artículo 61. Los Ministros." in text
    assert "Ley 40/2015, Artículo" not in text
    assert "Constitución Española, Artículo" not in _material(constitution).description


def test_the_territorial_topic_reaches_the_local_regime_law() -> None:
    text = _material(territorial_organisation).description

    assert "Ley 7/1985, Artículo 3." in text
    assert "Son Entidades Locales territoriales" in text


@pytest.mark.parametrize(
    ("number", "module"),
    [(5, government), (8, state_administration), (9, territorial_organisation)],
)
def test_units_of_the_auxiliar_programme_are_recognised(auxiliar_units, number, module) -> None:
    unit = next(u for u in auxiliar_units if u.number == number)

    assert find_topic_for_title(unit.title) is module.TOPIC


def test_other_syllabi_with_the_same_subjects_are_not_claimed() -> None:
    document = Source(title="archiveros", locator=str(SAMPLES / "Programa_Archiveros_0.pdf"))
    [programme] = discover_programmes(Call(title="a", source_id=document.id), document)
    administration = next(u for u in programme.units if u.title.startswith("La Administración"))

    assert "La Administración General del Estado" in administration.title
    assert find_topic_for_title(administration.title) is None
