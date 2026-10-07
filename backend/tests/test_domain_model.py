import pytest

from app.domain.coverage import CoverageStatus, evaluate_coverage
from app.domain.models import Call, Knowledge, KnowledgeNeed, Source, StudyProgrammeUnit


def _unit(*needs: KnowledgeNeed) -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=1,
        title="La Ley 39/2015",
        start_page=1,
        start_order=1,
        end_page=1,
        end_order=2,
        knowledge_needs=needs,
    )


def test_call_identifies_the_examination_opportunity_from_its_source() -> None:
    source = Source(title="Official examination notice", locator="call.pdf")

    call = Call(title="Administrative Management Corps", source_id=source.id)

    assert call.source_id == source.id
    assert call.title == "Administrative Management Corps"


def test_programme_unit_starts_without_knowledge_needs() -> None:
    assert _unit().knowledge_needs == ()


def test_knowledge_need_can_require_different_depths() -> None:
    processes = Knowledge(title="Processes")

    basic_need = KnowledgeNeed(topic="Processes", depth=2, knowledge=processes)
    technical_need = KnowledgeNeed(topic="Processes", depth=4, knowledge=processes)

    assert basic_need.depth == 2
    assert technical_need.depth == 4
    assert basic_need.knowledge is technical_need.knowledge
    assert basic_need.identity_key != technical_need.identity_key


def test_knowledge_need_can_exist_without_available_knowledge() -> None:
    need = KnowledgeNeed(topic="Process synchronization", depth=4)

    assert need.knowledge is None


def test_knowledge_need_does_not_require_a_persisted_knowledge_identifier() -> None:
    need = KnowledgeNeed(topic="Process synchronization", depth=4)

    assert need.knowledge_id is None
    assert need.id is not None


def test_needs_of_a_unit_are_independent_of_available_knowledge() -> None:
    unit = _unit(KnowledgeNeed(topic="Process synchronization", depth=4))

    assert unit.knowledge_needs[0].knowledge is None


def test_knowledge_need_without_knowledge_is_missing() -> None:
    need = KnowledgeNeed(topic="Article 1", depth=1)

    assert evaluate_coverage(need) == CoverageStatus.MISSING


def test_knowledge_need_with_knowledge_is_covered() -> None:
    knowledge = Knowledge(title="Spanish Constitution - Article 1")
    need = KnowledgeNeed(topic="Article 1", depth=1, knowledge=knowledge)

    assert evaluate_coverage(need) == CoverageStatus.COVERED


def test_same_knowledge_can_cover_multiple_needs() -> None:
    knowledge = Knowledge(title="Processes")

    first = KnowledgeNeed(topic="Processes", depth=2, knowledge=knowledge)
    second = KnowledgeNeed(topic="Processes", depth=4, knowledge=knowledge)

    assert evaluate_coverage(first) == CoverageStatus.COVERED
    assert evaluate_coverage(second) == CoverageStatus.COVERED


def test_unit_can_contain_covered_and_missing_needs() -> None:
    knowledge = Knowledge(title="Spanish Constitution - Article 1")
    covered_need = KnowledgeNeed(topic="Article 1", depth=1, knowledge=knowledge)
    missing_need = KnowledgeNeed(topic="Article 2", depth=1)
    unit = _unit(covered_need, missing_need)

    assert evaluate_coverage(unit.knowledge_needs[0]) == CoverageStatus.COVERED
    assert evaluate_coverage(unit.knowledge_needs[1]) == CoverageStatus.MISSING


@pytest.mark.parametrize("depth", [0, -1])
def test_knowledge_need_depth_must_be_positive(depth: int) -> None:
    with pytest.raises(ValueError):
        KnowledgeNeed(topic="Processes", depth=depth)
