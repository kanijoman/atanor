import json
from pathlib import Path

import pytest

from app.application.syllabus_derivation.boe_lookup import BoeLawLookup
from app.application.syllabus_derivation.identification_evaluation import (
    evaluate_identification,
    format_identification_report,
    unit_titles,
)
from app.application.syllabus_derivation.identify import identify_laws
from app.application.syllabus_derivation.references import LawReference, find_references

SAMPLE = Path(__file__).parent / "samples" / "BOE-A-2024-14098.pdf"


def _labels(text: str) -> set[str]:
    return {item.law.label for item in identify_laws(text).laws}


def test_references_keep_their_kind_and_ignore_duplicates() -> None:
    text = "La Ley Orgánica 3/2007 y la Ley 3/2007; de nuevo la ley organica 3/2007."

    assert find_references(text) == (
        LawReference("ley organica", "3/2007"),
        LawReference("ley", "3/2007"),
    )


def test_a_cited_law_in_the_catalog_is_identified_by_reference() -> None:
    result = identify_laws("La Ley 19/2013, de 9 de diciembre, de transparencia")

    assert [(i.law.label, i.basis) for i in result.laws] == [("Ley 19/2013", "reference")]
    assert result.unresolved_references == ()


def test_a_cited_law_outside_the_catalog_is_reported_not_guessed() -> None:
    result = identify_laws("La Ley 5/2010 de Autonomía Local")

    assert result.laws == ()
    assert [r.designation for r in result.unresolved_references] == ["ley 5/2010"]


def test_keywords_identify_laws_that_the_unit_does_not_cite() -> None:
    assert _labels("El Defensor del Pueblo. Las Cortes Generales") == {
        "Constitución Española",
        "LO 3/1981",
    }


def test_a_phrase_must_match_whole_words() -> None:
    assert _labels("Los funcionariados imaginarios") == set()


def test_open_government_is_not_the_government_of_the_state() -> None:
    assert _labels("El Gobierno Abierto: concepto y principios informadores") == set()


def test_assistance_to_disabled_people_is_not_the_legal_regime_of_disability() -> None:
    assert _labels("Atención de personas con discapacidad") == set()
    assert "RDL 1/2013" in _labels("Discapacidad y dependencia: régimen jurídico")


def _response(*entries: tuple[str, str, str]) -> str:
    return json.dumps(
        {
            "data": [
                {
                    "identificador": identifier,
                    "numero_oficial": number,
                    "rango": {"texto": kind},
                    "titulo": f"{kind} {number}, titulo",
                }
                for identifier, number, kind in entries
            ]
        }
    )


def test_the_boe_lookup_resolves_a_reference_matching_kind_and_number() -> None:
    lookup = BoeLawLookup(
        lambda _url: _response(
            ("BOE-A-1-1", "3/2007", "Ley"), ("BOE-A-2-2", "3/2007", "Ley Orgánica")
        )
    )

    candidate = lookup.find(LawReference("ley organica", "3/2007"))

    assert candidate is not None
    assert candidate.identifier == "BOE-A-2-2"
    assert candidate.source.locator == "https://www.boe.es/buscar/act.php?id=BOE-A-2-2"


def test_the_boe_lookup_leaves_ambiguous_or_missing_laws_unresolved() -> None:
    twice = BoeLawLookup(
        lambda _url: _response(("BOE-A-1-1", "5/2010", "Ley"), ("BOE-A-2-2", "5/2010", "Ley"))
    )
    nothing = BoeLawLookup(lambda _url: _response())

    assert twice.find(LawReference("ley", "5/2010")) is None
    assert nothing.find(LawReference("ley", "5/2010")) is None


def test_identification_finds_every_law_of_the_hand_made_annex_i_topics() -> None:
    results = evaluate_identification(unit_titles(SAMPLE))

    assert results
    assert all(not result.missing for result in results)
    assert "Laws of the hand-made topics found: 23/23" in format_identification_report(results)


@pytest.mark.network
def test_the_live_boe_lookup_resolves_a_law_by_kind_and_number() -> None:
    candidate = BoeLawLookup().find(LawReference("ley organica", "6/1985"))

    assert candidate is not None
    assert candidate.identifier == "BOE-A-1985-12666"
