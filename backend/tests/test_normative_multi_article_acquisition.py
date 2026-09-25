from app.application.normative_source import (
    HttpSourceRetriever,
    OfficialNormativeSourceCatalog,
    extract_articles,
    reconstruct_knowledge_from_articles,
)


def test_acquire_multiple_articles_from_same_boe_source() -> None:
    candidate = OfficialNormativeSourceCatalog().resolve("Ley 39/2015")
    assert candidate is not None

    retrieved = HttpSourceRetriever().retrieve(candidate)
    articles = extract_articles(retrieved, (1, 2))
    knowledge = reconstruct_knowledge_from_articles(retrieved, articles)

    assert tuple(article.identifier for article in articles) == (
        "Artículo 1",
        "Artículo 2",
    )
    assert "Objeto de la Ley" in articles[0].title
    assert "Ámbito subjetivo de aplicación." in articles[1].title
    assert "tiene por objeto" in knowledge.description
    assert "se aplica al sector público" in knowledge.description
    assert knowledge.sources == (candidate.source,)
