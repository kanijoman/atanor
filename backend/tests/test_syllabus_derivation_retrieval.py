import pytest

from app.application.normative_source import LEY_19_2013, RetrievedSource
from app.application.normative_source.structure import Law, parse_law
from app.application.syllabus_derivation.retrieval import Bm25Index, rank_divisions
from app.application.syllabus_derivation.text import strip_accents, tokens

LAW_HTML = """
<html><body>
<h4 class="titulo_num">TÍTULO I</h4>
<h4 class="titulo_tit">De la Corona</h4>
<h5 class="articulo">Artículo 1</h5>
<p>El Rey es el Jefe del Estado y simboliza su unidad y permanencia.</p>
<h5 class="articulo">Artículo 2</h5>
<p>La sucesión en el trono seguirá el orden regular de primogenitura.</p>
<h4 class="titulo_num">TÍTULO II</h4>
<h4 class="titulo_tit">Del régimen disciplinario</h4>
<h5 class="articulo">Artículo 3. Faltas</h5>
<p>Las faltas disciplinarias se clasifican en muy graves, graves y leves.</p>
<h5 class="articulo">Artículo 4. Sanciones</h5>
<p>Las sanciones por faltas muy graves incluyen la separación del servicio.</p>
<h4 class="titulo_num">TÍTULO III</h4>
<h4 class="titulo_tit">De las retribuciones</h4>
<h5 class="articulo">Artículo 5. Sueldo</h5>
<p>Las retribuciones básicas comprenden el sueldo y los trienios.</p>
</body></html>
"""


@pytest.fixture(scope="module")
def law() -> Law:
    return parse_law("TEST", RetrievedSource(candidate=LEY_19_2013, content=LAW_HTML))


def test_accents_and_case_are_ignored() -> None:
    assert strip_accents("Régimen DISCIPLINARIO") == "regimen disciplinario"


def test_function_words_are_dropped_and_words_are_stemmed_by_prefix() -> None:
    assert tokens("El régimen de las retribuciones") == ["regime", "retrib"]
    assert tokens("retribución") == tokens("retribuciones")


def test_function_words_and_fragments_of_one_or_two_characters_are_dropped() -> None:
    assert tokens("de la y el") == []
    assert tokens("Ley 39/2015") == ["ley", "2015"]


def test_a_query_ranks_first_the_division_whose_heading_names_it(law) -> None:
    ranked = rank_divisions(law, "Régimen disciplinario")

    assert ranked[0].division.heading == "TÍTULO II Del régimen disciplinario"
    assert ranked[0].score > ranked[1].score


def test_the_heading_outweighs_a_passing_mention_in_the_text(law) -> None:
    ranked = rank_divisions(law, "La Corona")

    assert ranked[0].division.heading == "TÍTULO I De la Corona"


def test_words_in_the_articles_find_a_division_even_when_the_heading_does_not(law) -> None:
    ranked = rank_divisions(law, "trienios")

    assert ranked[0].division.heading == "TÍTULO III De las retribuciones"


def test_every_division_is_ranked_and_ties_keep_document_order(law) -> None:
    ranked = rank_divisions(law, "palabrainexistente")

    assert [r.division.article_numbers for r in ranked] == [(1, 2), (3, 4), (5,)]
    assert {r.score for r in ranked} == {0.0}


def test_bm25_scores_a_rarer_term_higher_than_a_common_one() -> None:
    index = Bm25Index([["comun", "raro"], ["comun"], ["comun"]])

    assert index.score(["raro"], 0) > index.score(["comun"], 0)
    assert index.rank(["raro"])[0][0] == 0
