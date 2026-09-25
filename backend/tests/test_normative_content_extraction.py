from app.application.normative_source import (
    OfficialNormativeSourceCatalog,
    RetrievedSource,
    acquire_normative_source,
    extract_article,
)


def test_extract_article_1_from_boe_html() -> None:
    retrieved = RetrievedSource(
        candidate=OfficialNormativeSourceCatalog().resolve("Ley 39/2015"),
        content="""
        <html>
          <body>
            <h2>Artículo 1. Objeto de la Ley.</h2>
            <p>1. La presente Ley tiene por objeto regular los requisitos...</p>
            <h2>Artículo 2. Ámbito de aplicación.</h2>
            <p>1. La presente Ley se aplica...</p>
          </body>
        </html>
        """,
    )

    article = extract_article(retrieved, 1)

    assert article is not None
    assert article.identifier == "Artículo 1"
    assert article.title == "Objeto de la Ley."
    assert "La presente Ley tiene por objeto regular los requisitos" in article.content


def test_extract_article_returns_none_when_article_is_missing() -> None:
    retrieved = RetrievedSource(
        candidate=OfficialNormativeSourceCatalog().resolve("Ley 39/2015"),
        content="<h2>Artículo 2. Ámbito de aplicación.</h2>",
    )

    assert extract_article(retrieved, 1) is None
