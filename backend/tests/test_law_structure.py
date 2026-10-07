from app.application.normative_source import LEY_19_2013, RetrievedSource
from app.application.normative_source.structure import parse_law

BOE_LIKE = """
<html><body>
<ul id="lista-marcadores">
<li><a href="#a1">Artículo 1</a></li>
<li><a href="#a2">Artículo 2</a></li>
</ul>
<h4 class="titulo_num">TÍTULO PRELIMINAR</h4>
<h5 class="articulo">Artículo 1</h5>
<p class="parrafo">España se constituye en un Estado social y democrático de Derecho.</p>
<p class="linkSubir"><a href="#top">Subir</a></p>
<h4 class="titulo_num">TÍTULO II</h4>
<h4 class="titulo_tit">De la Corona</h4>
<h5 class="articulo">Artículo 56</h5>
<p class="parrafo">El Rey es el Jefe del Estado.</p>
<h4 class="capitulo_num">CAPÍTULO SEGUNDO</h4>
<h4 class="capitulo_tit">Derechos y libertades</h4>
<h5 class="articulo">Artículo 57. Sucesión</h5>
<p class="parrafo">La Corona de España es hereditaria.</p>
</body></html>
"""

GENERIC = """
<html><body>
<h2>TÍTULO I</h2>
<h2>Disposiciones generales</h2>
<h3>Artículo 1. Objeto.</h3>
<p>Esta ley regula la materia.</p>
<h2>CAPÍTULO II</h2>
<h2>Procedimiento</h2>
<h3>Artículo 2. Inicio.</h3>
<p>El procedimiento se inicia de oficio.</p>
<h3>Artículo 3. Fases.</h3>
<p>Instrucción y resolución.</p>
</body></html>
"""


def _parse(html: str):
    return parse_law("TEST", RetrievedSource(candidate=LEY_19_2013, content=html))


def test_titles_and_chapters_group_their_articles_using_the_boe_headings() -> None:
    law = _parse(BOE_LIKE)

    assert [d.heading for d in law.divisions] == [
        "TÍTULO PRELIMINAR",
        "TÍTULO II De la Corona",
        "TÍTULO II De la Corona · CAPÍTULO SEGUNDO Derechos y libertades",
    ]
    assert [d.article_numbers for d in law.divisions] == [(1,), (56,), (57,)]


def test_the_navigation_index_is_not_mistaken_for_articles() -> None:
    law = _parse(BOE_LIKE)

    assert sorted(law.articles) == [1, 56, 57]
    assert (
        law.articles[1].content
        == "España se constituye en un Estado social y democrático de Derecho."
    )
    assert "Subir" not in law.articles[1].content


def test_untitled_and_titled_articles_keep_their_title() -> None:
    law = _parse(BOE_LIKE)

    assert law.articles[1].title == ""
    assert law.articles[57].title == "Sucesión"


def test_plain_headings_name_the_title_and_chapter_that_precede_them() -> None:
    law = _parse(GENERIC)

    assert [d.heading for d in law.divisions] == [
        "TÍTULO I Disposiciones generales",
        "TÍTULO I Disposiciones generales · CAPÍTULO II Procedimiento",
    ]
    assert law.division_of(3).article_numbers == (2, 3)


def test_an_article_outside_any_division_is_kept() -> None:
    law = _parse("<h3>Artículo 1. Objeto.</h3><p>Texto.</p>")

    assert law.articles[1].content == "Texto."
    assert law.divisions[0].heading == ""
    assert law.division_of(99) is None
