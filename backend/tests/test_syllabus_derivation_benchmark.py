import pytest

from app.application.normative_source import HttpSourceRetriever
from app.application.study_material.registry import TOPICS
from app.application.syllabus_derivation.derive import MAX_ARTICLES
from app.application.syllabus_derivation.evaluation import evaluate, gold_sections, load_laws


@pytest.mark.network
def test_derivation_recovers_the_hand_made_mappings_of_most_sections() -> None:
    gold = gold_sections(TOPICS)
    laws = load_laws(gold, HttpSourceRetriever(timeout=120))

    report = evaluate(laws, gold)

    assert report.well_covered / len(gold) >= 0.6
    assert max(len(result.selected) for result in report.results) <= MAX_ARTICLES
