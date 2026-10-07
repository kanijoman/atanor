import pytest

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


@pytest.mark.parametrize("depth", [0, -1])
def test_knowledge_need_depth_must_be_positive(depth: int) -> None:
    with pytest.raises(ValueError):
        KnowledgeNeed(topic="Processes", depth=depth)
