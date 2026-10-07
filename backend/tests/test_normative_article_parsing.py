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


CONSTITUTION_LIKE_HTML = """
<html><body>
<ul id="lista-marcadores">
  <li><a href="#a1">Artículo 1</a></li>
  <li><a href="#a2">Artículo 2</a></li>
</ul>
<h4 class="titulo_num">TÍTULO PRELIMINAR</h4>
<h5 class="articulo">Artículo 1</h5>
<p class="parrafo">1. España se constituye en un Estado social y democrático de Derecho.</p>
<p class="parrafo">2. La soberanía nacional reside en el pueblo español.</p>
<p class="linkSubir"><a href="#top">Subir</a></p>
<h5 class="articulo">Artículo 2</h5>
<p class="parrafo">La Constitución se fundamenta en la indisoluble unidad de la Nación española.</p>
<h4 class="titulo_num">TÍTULO I</h4>
<p class="centro_negrita">De los derechos y deberes fundamentales</p>
</body></html>
"""


def test_articles_without_title_are_found_by_their_heading_not_by_the_index() -> None:
    article = extract_article(_retrieved(CONSTITUTION_LIKE_HTML), 1)

    assert article is not None
    assert article.title == ""
    assert article.content == (
        "1. España se constituye en un Estado social y democrático de Derecho. "
        "2. La soberanía nacional reside en el pueblo español."
    )


def test_an_article_ends_at_the_next_title_or_chapter_heading() -> None:
    article = extract_article(_retrieved(CONSTITUTION_LIKE_HTML), 2)

    assert article is not None
    assert article.content == (
        "La Constitución se fundamenta en la indisoluble unidad de la Nación española."
    )
