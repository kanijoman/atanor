from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.models import (
    Call,
    Knowledge,
    KnowledgeNeed,
    Source,
    StudyProgramme,
    StudyProgrammeUnit,
)
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import Base
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository
from app.persistence.source_repository import SqlAlchemySourceRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


def _repositories(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'e2e.db'}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    return (
        engine,
        SqlAlchemySourceRepository(session_factory),
        SqlAlchemyCallRepository(session_factory),
        SqlAlchemyKnowledgeRepository(session_factory),
        SqlAlchemyStudyProgrammeRepository(session_factory),
    )


def _save_unit_with_needs(sources, calls, programmes, *needs: KnowledgeNeed) -> StudyProgrammeUnit:
    source = Source(title="Call", locator=f"call-{uuid4()}.pdf")
    sources.save(source)
    call = calls.save(Call(title="Call", source_id=source.id))
    unit = StudyProgrammeUnit(
        number=1,
        title="Study topics",
        start_page=1,
        start_order=1,
        end_page=1,
        end_order=2,
        knowledge_needs=needs,
    )
    programmes.save(
        StudyProgramme(call_id=call.id, identifier="I", title="Programme", units=(unit,))
    )
    return unit


def test_unit_preserves_known_and_unknown_knowledge_after_persistence(tmp_path) -> None:
    engine, sources, calls, knowledge_repository, programmes = _repositories(tmp_path)
    try:
        known = knowledge_repository.save(Knowledge(title="Spanish Constitution"))
        unit = _save_unit_with_needs(
            sources,
            calls,
            programmes,
            KnowledgeNeed(topic="Spanish Constitution", depth=1, knowledge=known),
            KnowledgeNeed(topic="Open management topic", depth=1),
        )

        loaded = programmes.get_unit_by_id(unit.id)

        assert loaded is not None
        first, second = loaded.knowledge_needs
        assert first.knowledge is not None
        assert first.knowledge.title == "Spanish Constitution"
        assert second.knowledge is None
        assert second.knowledge_id is None
    finally:
        engine.dispose()


def test_linking_knowledge_makes_a_missing_need_available(tmp_path) -> None:
    engine, sources, calls, knowledge_repository, programmes = _repositories(tmp_path)
    try:
        need = KnowledgeNeed(topic="Open management topic", depth=1)
        unit = _save_unit_with_needs(sources, calls, programmes, need)
        knowledge = knowledge_repository.save(Knowledge(title="Open management topic"))

        programmes.link_knowledge(need.id, knowledge.id)

        loaded = programmes.get_unit_by_id(unit.id)
        assert loaded is not None
        assert loaded.knowledge_needs[0].knowledge_id == knowledge.id
    finally:
        engine.dispose()


def test_needs_are_stored_for_a_unit_that_has_none_and_never_replaced(tmp_path) -> None:
    engine, sources, calls, _, programmes = _repositories(tmp_path)
    try:
        unit = _save_unit_with_needs(sources, calls, programmes)

        first = programmes.save_knowledge_needs(unit.id, (KnowledgeNeed(topic="A", depth=1),))
        second = programmes.save_knowledge_needs(unit.id, (KnowledgeNeed(topic="B", depth=1),))

        assert first is not None and second is not None
        assert [need.topic for need in second.knowledge_needs] == ["A"]
    finally:
        engine.dispose()
