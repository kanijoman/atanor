from pathlib import Path

import pytest
from support import FixtureSourceRetriever

from app.application.call_discovery import discover_call
from app.application.study_material.registry import find_topic_for_title
from app.application.study_material.topics import (
    civil_servants,
    civil_servants_rights,
    state_budget,
)
from app.application.study_programmes import discover_programmes
from app.domain.models import Call, Knowledge, Source, StudyProgrammeUnit

SAMPLES = Path(__file__).parent / "samples"
BATCH_C = [civil_servants, civil_servants_rights, state_budget]


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


@pytest.mark.parametrize("module", BATCH_C, ids=lambda m: m.__name__.split(".")[-1])
def test_every_aspect_is_covered_by_the_acquired_articles(module) -> None:
    topic = module.TOPIC

    knowledge = _material(module)

    assert topic.covered_aspects(knowledge, topic.required_aspects) == topic.required_aspects


@pytest.mark.parametrize(
    ("module", "identifiers"),
    [
        (civil_servants, {"BOE-A-2015-11719"}),
        (civil_servants_rights, {"BOE-A-2015-11719", "BOE-A-2000-12140"}),
        (state_budget, {"BOE-A-2003-21614", "BOE-A-1978-31229"}),
    ],
    ids=["civil_servants", "civil_servants_rights", "state_budget"],
)
def test_material_cites_every_law_it_draws_from(module, identifiers) -> None:
    cited = {source.locator.rsplit("=", 1)[1] for source in module.TOPIC.provider.sources}

    assert cited == identifiers


def test_the_social_security_aspect_comes_from_its_own_law() -> None:
    text = _material(civil_servants_rights).description

    assert "RDL 4/2000, Artículo 1." in text
    assert "TREBEP, Artículo 93." in text


def test_the_budget_cycle_draws_on_execution_and_control_articles() -> None:
    text = _material(state_budget).description

    assert "Ley 47/2003, Artículo 73." in text
    assert "Ley 47/2003, Artículo 131." in text
    assert "Constitución Española, Artículo 134." in text


@pytest.mark.parametrize(
    ("number", "module"),
    [(13, civil_servants), (14, civil_servants_rights), (15, state_budget)],
)
def test_units_of_the_auxiliar_programme_are_recognised(auxiliar_units, number, module) -> None:
    unit = next(u for u in auxiliar_units if u.number == number)

    assert find_topic_for_title(unit.title) is module.TOPIC


def test_a_unit_that_asks_for_less_than_the_material_covers_is_not_claimed() -> None:
    narrower_than_the_topic = (
        "Derechos y deberes de los funcionarios. La carrera administrativa. Régimen disciplinario."
    )

    assert find_topic_for_title(narrower_than_the_topic) is None


def test_a_unit_that_asks_for_more_than_the_material_covers_is_not_claimed() -> None:
    broader_than_the_topic = (
        "El presupuesto del Estado en España. Contenido, elaboración y estructura. Fases del "
        "ciclo presupuestario. El control del gasto público y la deuda."
    )
    exactly_the_topic = (
        "El presupuesto del Estado en España. Contenido, elaboración y estructura. Fases del "
        "ciclo presupuestario."
    )

    assert find_topic_for_title(broader_than_the_topic) is None
    assert find_topic_for_title(exactly_the_topic) is state_budget.TOPIC


def test_other_syllabi_naming_the_same_subjects_differently_are_not_claimed() -> None:
    document = Source(title="boja", locator=str(SAMPLES / "BOJA24-138-00046-48048-01_00304998.pdf"))
    programmes = discover_programmes(Call(title="b", source_id=document.id), document)
    claimed = [
        unit
        for programme in programmes
        for unit in programme.units
        if (topic := find_topic_for_title(unit.title)) and topic in {m.TOPIC for m in BATCH_C}
    ]

    assert claimed == []
