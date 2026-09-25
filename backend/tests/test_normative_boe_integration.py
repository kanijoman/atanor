from app.application.normative_source import (
    HttpSourceRetriever,
    OfficialNormativeSourceCatalog,
    extract_article,
    reconstruct_knowledge_from_article,
)


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
