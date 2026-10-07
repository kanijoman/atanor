import pytest
from support import FixtureSourceRetriever

from app.application.normative_source import LEY_19_2013, RetrievedSource
from app.application.normative_source.structure import Law, parse_law
from app.application.study_material.registry import TOPICS
from app.application.syllabus_derivation.evaluation import (
    GoldSection,
    SectionResult,
    evaluate,
    format_report,
    gold_sections,
    load_laws,
    select_articles,
)

LAW_HTML = """
<html><body>
<h4 class="titulo_num">TÍTULO I</h4>
<h4 class="titulo_tit">De la Corona</h4>
<h5 class="articulo">Artículo 1</h5>
<p>El Rey es el Jefe del Estado.</p>
<h5 class="articulo">Artículo 2</h5>
<p>La sucesión en el trono sigue la primogenitura.</p>
<h4 class="titulo_num">TÍTULO II</h4>
<h4 class="titulo_tit">Del régimen disciplinario</h4>
<h5 class="articulo">Artículo 3. Faltas</h5>
<p>Las faltas disciplinarias son muy graves, graves y leves.</p>
<h5 class="articulo">Artículo 4. Sanciones</h5>
<p>Las sanciones por faltas muy graves incluyen la separación.</p>
</body></html>
"""


@pytest.fixture(scope="module")
def law() -> Law:
    return parse_law(
        LEY_19_2013.identifier, RetrievedSource(candidate=LEY_19_2013, content=LAW_HTML)
    )


def _gold(aspect: str, articles: tuple[int, ...]) -> GoldSection:
    return GoldSection("Tema", aspect, LEY_19_2013, articles)


def test_the_articles_of_the_best_matching_chapters_are_selected(law) -> None:
    assert select_articles(law, "Régimen disciplinario", top_divisions=1) == (3, 4)
    assert select_articles(law, "Régimen disciplinario", top_divisions=2) == (3, 4, 1, 2)


def test_recall_is_the_share_of_hand_made_articles_that_were_selected() -> None:
    result = SectionResult(_gold("x", (1, 2, 3, 4)), selected=(3, 4, 9))

    assert result.recall == pytest.approx(0.5)
    assert SectionResult(_gold("x", ()), selected=()).recall == 1.0


def test_the_report_counts_well_covered_and_missed_sections(law) -> None:
    gold = [
        _gold("Régimen disciplinario", (3, 4)),
        _gold("La Corona", (1,)),
        _gold("Tema sin relación alguna", (4,)),
    ]

    report = evaluate({LEY_19_2013.identifier: law}, gold, top_divisions=1)

    assert [round(r.recall, 2) for r in report.results] == [1.0, 1.0, 0.0]
    assert report.well_covered == 2
    assert [r.gold.aspect for r in report.missed] == ["Tema sin relación alguna"]
    assert report.mean_selected == pytest.approx(2.0)
    assert report.mean_recall == pytest.approx(2 / 3)


def test_the_formatted_report_names_the_missed_sections(law) -> None:
    gold = [_gold("Régimen disciplinario", (3,)), _gold("Tema sin relación alguna", (4,))]

    text = format_report(evaluate({LEY_19_2013.identifier: law}, gold, top_divisions=1))

    assert "Sections evaluated: 2" in text
    assert "Sections with recall >= 0.8: 1/2" in text
    assert "  - Tema | Tema sin relación alguna" in text


def test_gold_sections_come_from_every_acquired_topic() -> None:
    gold = gold_sections(TOPICS)

    assert len(gold) >= 80
    assert {section.law.identifier for section in gold} >= {
        "BOE-A-1978-31229",
        "BOE-A-2015-10565",
        "BOE-A-1998-16718",
    }
    assert all(section.articles for section in gold)


def test_laws_are_loaded_once_each_and_parsed_into_divisions() -> None:
    gold = [g for g in gold_sections(TOPICS) if g.law.identifier == "BOE-A-1978-31229"]

    laws = load_laws(gold, FixtureSourceRetriever())

    assert list(laws) == ["BOE-A-1978-31229"]
    assert 1 in laws["BOE-A-1978-31229"].articles
