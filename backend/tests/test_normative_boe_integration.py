import importlib

import pytest

from app.application.normative_source import (
    HttpSourceRetriever,
    OfficialNormativeSourceCatalog,
    extract_article,
    reconstruct_knowledge_from_article,
)
from app.domain.models import Knowledge


@pytest.mark.network
def test_live_boe_retrieval_extracts_ley_39_2015_article_1() -> None:
    candidate = OfficialNormativeSourceCatalog().resolve("Ley 39/2015")
    assert candidate is not None

    retrieved = HttpSourceRetriever().retrieve(candidate)

    article = extract_article(retrieved, 1)

    assert article is not None
    assert article.identifier == "Artículo 1"
    assert "Objeto de la Ley" in article.title
    assert "La presente Ley tiene por objeto" in article.content

    knowledge = reconstruct_knowledge_from_article(retrieved, article)

    assert knowledge.title == "Objeto de la Ley."
    assert knowledge.description == article.content
    assert knowledge.sources == (candidate.source,)
    assert "procedimiento administrativo común" in knowledge.description.lower()


@pytest.mark.network
@pytest.mark.parametrize(
    ("topic_module", "expected_aspects"),
    [
        ("procedure", 8),
        ("access", 10),
        ("constitution", 4),
        ("constitutional_court_and_crown", 4),
        ("cortes_generales", 4),
        ("judicial_power", 4),
        ("government", 4),
        ("state_administration", 6),
        ("territorial_organisation", 5),
        ("civil_servants", 7),
        ("civil_servants_rights", 6),
        ("state_budget", 5),
    ],
)
def test_live_boe_pages_cover_every_aspect_of_the_acquired_topics(
    topic_module: str, expected_aspects: int
) -> None:
    """Guards the aspect-to-article mapping against the real, current BOE text."""
    topic = importlib.import_module(f"app.application.study_material.topics.{topic_module}").TOPIC
    knowledge = Knowledge(
        title=topic.name,
        description=topic.provider.description(HttpSourceRetriever(timeout=60)),
    )

    covered = topic.covered_aspects(knowledge, topic.required_aspects)

    assert len(topic.required_aspects) == expected_aspects
    assert covered == topic.required_aspects
