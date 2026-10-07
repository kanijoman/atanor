import re
from pathlib import Path

import pytest
from support import FixtureSourceRetriever

from app.application.call_discovery import discover_call
from app.application.normative_source import NormativeSourceCandidate, RetrievedSource
from app.application.study_material.providers import MaterialOrigin, ReviewStatus
from app.application.study_material.registry import TOPICS, find_topic_for_title
from app.application.study_material.topics import (
    constitution,
    constitutional_court_and_crown,
    cortes_generales,
    judicial_power,
)
from app.application.study_programmes import discover_programmes
from app.domain.models import Call, Knowledge, Source, StudyProgrammeUnit

SAMPLES = Path(__file__).parent / "samples"
CONSTITUTION_TOPICS = [
    constitution,
    constitutional_court_and_crown,
    cortes_generales,
    judicial_power,
]


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


@pytest.mark.parametrize("module", CONSTITUTION_TOPICS, ids=lambda m: m.__name__.split(".")[-1])
def test_every_aspect_is_covered_by_the_acquired_articles(module) -> None:
    topic = module.TOPIC

    knowledge = _material(module)

    assert topic.covered_aspects(knowledge, topic.required_aspects) == topic.required_aspects
    assert knowledge.sources[0].locator == "https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229"


@pytest.mark.parametrize("module", CONSTITUTION_TOPICS, ids=lambda m: m.__name__.split(".")[-1])
def test_material_is_acquired_and_not_reviewed(module) -> None:
    provenance = module.TOPIC.provider.provenance

    assert provenance.origin is MaterialOrigin.ACQUIRED
    assert provenance.review_status is ReviewStatus.UNREVIEWED


def test_articles_of_the_constitution_have_no_title_and_no_stray_space() -> None:
    text = _material(constitution).description

    assert "  Artículo 1.\n  1. España se constituye en un Estado social y democrático" in text
    assert "Artículo 1. \n" not in text


class _WithoutArticle123(FixtureSourceRetriever):
    """The Constitution as retrieved, minus article 123 (the Tribunal Supremo)."""

    def retrieve(self, candidate: NormativeSourceCandidate) -> RetrievedSource:
        retrieved = super().retrieve(candidate)
        content = re.sub(
            r'<h5 class="articulo">Artículo 123</h5>\s*<p class="parrafo">.*?</p>',
            "",
            retrieved.content,
            flags=re.DOTALL,
        )
        return RetrievedSource(candidate=candidate, content=content)


def test_an_article_that_cannot_be_acquired_leaves_its_aspect_pending() -> None:
    topic = judicial_power.TOPIC
    description = topic.provider.description(_WithoutArticle123())
    knowledge = Knowledge(title=topic.name, description=description)

    covered = topic.covered_aspects(knowledge, topic.required_aspects)

    assert "Artículo 123" not in description
    assert "El Tribunal Supremo" in topic.required_aspects
    assert "El Tribunal Supremo" not in covered
    assert len(covered) == len(topic.required_aspects) - 1


@pytest.mark.parametrize(
    ("number", "module"),
    [
        (1, constitution),
        (2, constitutional_court_and_crown),
        (3, cortes_generales),
        (4, judicial_power),
    ],
)
def test_units_of_the_auxiliar_programme_are_recognised(auxiliar_units, number, module) -> None:
    unit = next(u for u in auxiliar_units if u.number == number)

    assert find_topic_for_title(unit.title) is module.TOPIC


def test_units_outside_the_constitution_are_not_claimed_by_these_topics(auxiliar_units) -> None:
    claimed = {
        unit.number
        for unit in auxiliar_units
        if (topic := find_topic_for_title(unit.title))
        and topic.name in {m.TOPIC.name for m in CONSTITUTION_TOPICS}
    }

    assert claimed == {1, 2, 3, 4}


def test_a_syllabus_with_other_subtopics_is_not_presented_as_covered() -> None:
    document = Source(title="boja", locator=str(SAMPLES / "BOJA24-138-00046-48048-01_00304998.pdf"))
    programmes = discover_programmes(Call(title="boja", source_id=document.id), document)
    constitution_units = [
        unit
        for programme in programmes
        for unit in programme.units
        if unit.title.startswith("La Constitución Española de 1978")
    ]

    assert constitution_units
    assert all(find_topic_for_title(unit.title) is None for unit in constitution_units)


def test_topic_names_are_unique() -> None:
    names = [topic.name for topic in TOPICS]

    assert len(names) == len(set(names))
