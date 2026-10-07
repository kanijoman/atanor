import pytest

from app.application.normative_source import LEY_19_2013, RetrievedSource
from app.application.normative_source.structure import Law, parse_law
from app.application.syllabus_derivation import derive
from app.application.syllabus_derivation.derive import derive_section


def _articles(count: int, first: int) -> str:
    return "".join(
        f'<h5 class="articulo">Artículo {n}</h5><p>Sanciones disciplinarias {n}.</p>'
        for n in range(first, first + count)
    )


LAW_HTML = (
    '<h4 class="titulo_num">TÍTULO I</h4><h4 class="titulo_tit">Régimen disciplinario</h4>'
    + _articles(2, 1)
    + '<h4 class="titulo_num">TÍTULO II</h4><h4 class="titulo_tit">Retribuciones</h4>'
    '<h5 class="articulo">Artículo 3</h5><p>El sueldo y los trienios.</p>'
    '<h4 class="titulo_num">TÍTULO III</h4><h4 class="titulo_tit">Faltas disciplinarias</h4>'
    + _articles(30, 4)
)


@pytest.fixture(scope="module")
def law() -> Law:
    return parse_law("TEST", RetrievedSource(candidate=LEY_19_2013, content=LAW_HTML))


def test_the_best_matching_division_is_selected(law) -> None:
    section = derive_section(law, "Las retribuciones")

    assert section.articles == (3,)
    assert section.resolved


def test_an_aspect_that_matches_nothing_is_unresolved_and_selects_no_article(law) -> None:
    section = derive_section(law, "Palabra inexistente")

    assert section.articles == ()
    assert not section.resolved


def test_a_division_that_would_exceed_the_size_limit_is_skipped(law) -> None:
    section = derive_section(law, "Régimen disciplinario")

    assert len(section.articles) <= derive.MAX_ARTICLES
    assert section.articles[:2] == (1, 2)


def test_divisions_far_below_the_best_score_are_left_out(law) -> None:
    assert 3 not in derive_section(law, "Régimen disciplinario").articles
