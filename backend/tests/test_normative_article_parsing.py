from app.application.normative_source import (
    LEY_19_2013,
    RetrievedSource,
    extract_article,
    extract_articles,
)

BOE_LIKE_HTML = """
<html><body>
<h5 class="articulo">Artículo 12. Derecho de acceso a la información pública.</h5>
<p class="parrafo">Todos tienen derecho a acceder a la información pública, en los términos
previstos en el <a href="#c">artículo 105.b) de la Constitución</a>, y en esta Ley.</p>
<p class="parrafo_2">Asimismo, será de aplicación la <em>normativa autonómica</em>
correspondiente.</p>
<a href="#top">Subir</a>
<p>[Bloque 21: #a13]</p>
<h5 class="articulo">Artículo 13. Información pública.</h5>
<p>Se entiende por información pública los contenidos o documentos.</p>
</body></html>
"""


def _retrieved(html: str = BOE_LIKE_HTML) -> RetrievedSource:
    return RetrievedSource(candidate=LEY_19_2013, content=html)


def test_inline_links_do_not_split_or_drop_paragraph_text() -> None:
    article = extract_article(_retrieved(), 12)

    assert article is not None
    assert article.title == "Derecho de acceso a la información pública."
    assert article.content == (
        "Todos tienen derecho a acceder a la información pública, en los términos "
        "previstos en el artículo 105.b) de la Constitución, y en esta Ley. "
        "Asimismo, será de aplicación la normativa autonómica correspondiente."
    )


def test_navigation_and_block_markers_are_not_part_of_the_article() -> None:
    article = extract_article(_retrieved(), 12)

    assert article is not None
    assert "Subir" not in article.content
    assert "[Bloque" not in article.content


def test_an_article_ends_where_the_next_one_starts() -> None:
    article = extract_article(_retrieved(), 13)

    assert article is not None
    assert article.content == "Se entiende por información pública los contenidos o documentos."


def test_missing_articles_are_skipped_when_extracting_several() -> None:
    articles = extract_articles(_retrieved(), (12, 99, 13))

    assert [article.identifier for article in articles] == ["Artículo 12", "Artículo 13"]
