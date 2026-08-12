from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.domain.models import Source as DomainSource
from app.persistence.database import Base
from app.persistence.models.source import Source
from app.persistence.source_repository import SqlAlchemySourceRepository


def test_source_can_be_persisted_and_retrieved_by_uuid(tmp_path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        source = DomainSource(title="Official call", locator="call.pdf")
        repository = SqlAlchemySourceRepository(session_factory)
        repository.save(source)

        persisted = repository.get_by_id(source.id)

        assert persisted == source
        assert isinstance(persisted.id, UUID)
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_source_timestamps_are_persisted_as_utc(tmp_path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        before_creation = datetime.now(UTC)
        repository = SqlAlchemySourceRepository(session_factory)
        source = DomainSource(title="Official call", locator="call.pdf")
        repository.save(source)
        after_creation = datetime.now(UTC)
        with session_factory() as session:
            persisted_source = session.scalar(
                select(Source).where(Source.id == source.id)
            )
        assert persisted_source is not None
        assert persisted_source.id == source.id
        assert persisted_source.created_at.tzinfo == UTC
        assert persisted_source.updated_at.tzinfo == UTC
        assert before_creation <= persisted_source.created_at <= after_creation
        assert before_creation <= persisted_source.updated_at <= after_creation
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_source_list_returns_all_persisted_sources(tmp_path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        repository = SqlAlchemySourceRepository(session_factory)
        first = DomainSource(title="First call", locator="first.pdf")
        second = DomainSource(title="Second call", locator="second.pdf")
        repository.save(first)
        repository.save(second)

        sources = repository.list_all()

        assert {source.id for source in sources} == {first.id, second.id}
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
