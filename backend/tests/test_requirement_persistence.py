from datetime import UTC, datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.persistence.database import Base
from app.persistence.models.requirement import Requirement


def test_requirement_can_be_persisted_and_retrieved(tmp_path) -> None:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    session_factory = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    try:
        with session_factory() as session:
            requirement = Requirement(
                title="Spanish Constitution Article 1",
                description="The first article of the Spanish Constitution.",
                context="Public administration examination",
            )
            session.add(requirement)
            session.commit()
            requirement_id = requirement.id

        with session_factory() as session:
            persisted_requirement = session.scalar(
                select(Requirement).where(Requirement.id == requirement_id)
            )

        assert persisted_requirement is not None
        assert persisted_requirement.id == requirement_id
        assert persisted_requirement.title == "Spanish Constitution Article 1"
        assert (
            persisted_requirement.description
            == "The first article of the Spanish Constitution."
        )
        assert persisted_requirement.context == "Public administration examination"
        assert persisted_requirement.created_at is not None
        assert persisted_requirement.updated_at is not None
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_requirement_update_preserves_creation_time_and_updates_modification_time(
    tmp_path,
) -> None:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    session_factory = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    try:
        with session_factory() as session:
            requirement = Requirement(
                title="Spanish Constitution Article 1",
                description="The first article of the Spanish Constitution.",
                context="Public administration examination",
            )
            session.add(requirement)
            session.commit()
            requirement_id = requirement.id
            created_at = requirement.created_at
            updated_at = requirement.updated_at

        assert created_at is not None
        assert updated_at is not None

        with session_factory() as session:
            requirement = session.get(Requirement, requirement_id)
            assert requirement is not None
            requirement.description = "Updated description."
            session.commit()

        with session_factory() as session:
            persisted_requirement = session.scalar(
                select(Requirement).where(Requirement.id == requirement_id)
            )

        assert persisted_requirement is not None
        assert persisted_requirement.description == "Updated description."
        assert persisted_requirement.created_at == created_at
        assert persisted_requirement.updated_at is not None
        assert persisted_requirement.updated_at > updated_at
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_requirement_timestamps_are_persisted_as_utc(tmp_path) -> None:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    session_factory = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    try:
        before_creation = datetime.now(UTC)

        with session_factory() as session:
            requirement = Requirement(title="UTC timestamp requirement")
            session.add(requirement)
            session.commit()
            requirement_id = requirement.id

        after_creation = datetime.now(UTC)

        with session_factory() as session:
            persisted_requirement = session.get(Requirement, requirement_id)

        assert persisted_requirement is not None
        assert persisted_requirement.created_at is not None
        assert persisted_requirement.updated_at is not None
        assert persisted_requirement.created_at.tzinfo == UTC
        assert persisted_requirement.updated_at.tzinfo == UTC
        assert before_creation <= persisted_requirement.created_at <= after_creation
        assert before_creation <= persisted_requirement.updated_at <= after_creation
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
