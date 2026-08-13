from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.domain.models import Requirement as DomainRequirement
from app.persistence.database import Base
from app.persistence.models.requirement import Requirement
from app.persistence.models.knowledge_need import KnowledgeNeed as PersistenceKnowledgeNeed
from app.persistence.models.requirement_scope import RequirementScope as PersistenceRequirementScope
from app.persistence.models.source import Source
from app.persistence.requirement_repository import SqlAlchemyRequirementRepository


def test_requirement_can_be_persisted_and_retrieved_without_scope(tmp_path) -> None:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        source_id = uuid4()
        with session_factory() as session:
            session.add(Source(id=source_id, title="Call PDF", locator="call.pdf"))
            requirement = Requirement(
                title="Spanish Constitution Article 1",
                description="The first article of the Spanish Constitution.",
                source_id=source_id,
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
        assert persisted_requirement.description == "The first article of the Spanish Constitution."
        assert persisted_requirement.source_id == source_id
        assert persisted_requirement.scopes == []
        assert persisted_requirement.created_at is not None
        assert persisted_requirement.updated_at is not None
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_requirement_can_have_multiple_contextual_scopes(tmp_path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        source_id = uuid4()
        with session_factory() as session:
            session.add(Source(id=source_id, title="Call PDF", locator="call.pdf"))
            requirement = Requirement(
                title="Operating Systems",
                source_id=source_id,
                scopes=[
                    PersistenceRequirementScope(context="General Administration"),
                    PersistenceRequirementScope(context="Information Technology"),
                ],
            )
            session.add(requirement)
            session.commit()
            requirement_id = requirement.id

        with session_factory() as session:
            persisted_requirement = session.get(Requirement, requirement_id)

        assert persisted_requirement is not None
        assert [scope.context for scope in persisted_requirement.scopes] == [
            "General Administration",
            "Information Technology",
        ]
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_knowledge_need_can_be_persisted_without_available_knowledge(tmp_path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        source_id = uuid4()
        with session_factory() as session:
            session.add(Source(id=source_id, title="Call PDF", locator="call.pdf"))
            requirement = Requirement(
                title="Operating Systems",
                source_id=source_id,
                scopes=[
                    PersistenceRequirementScope(
                        context="Information Technology",
                        knowledge_needs=[
                            PersistenceKnowledgeNeed(
                                topic="Process synchronization",
                                depth=4,
                                knowledge_id=None,
                            )
                        ],
                    )
                ],
            )
            session.add(requirement)
            session.commit()
            requirement_id = requirement.id

        with session_factory() as session:
            persisted_requirement = session.get(Requirement, requirement_id)

        assert persisted_requirement is not None
        assert len(persisted_requirement.scopes) == 1
        assert len(persisted_requirement.scopes[0].knowledge_needs) == 1
        need = persisted_requirement.scopes[0].knowledge_needs[0]
        assert need.topic == "Process synchronization"
        assert need.depth == 4
        assert need.knowledge_id is None
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_requirement_repository_list_all_returns_empty_list_for_empty_database(tmp_path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        repository = SqlAlchemyRequirementRepository(session_factory)
        assert repository.list_all() == []
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_requirement_repository_list_all_returns_requirements_in_id_order(tmp_path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        source_id = uuid4()
        repository = SqlAlchemyRequirementRepository(session_factory)
        repository.save(DomainRequirement(title="First requirement", source_id=source_id))
        repository.save(DomainRequirement(title="Second requirement", source_id=source_id))

        requirements = repository.list_all()

        assert [requirement.title for requirement in requirements] == [
            "First requirement",
            "Second requirement",
        ]
        assert [requirement.source_id for requirement in requirements] == [
            source_id,
            source_id,
        ]
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_requirement_update_preserves_creation_time_and_updates_modification_time(tmp_path) -> None:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        source_id = uuid4()
        with session_factory() as session:
            session.add(Source(id=source_id, title="Call PDF", locator="call.pdf"))
            requirement = Requirement(
                title="Spanish Constitution Article 1",
                description="The first article of the Spanish Constitution.",
                source_id=source_id,
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
            persisted_requirement = session.get(Requirement, requirement_id)

        assert persisted_requirement is not None
        assert persisted_requirement.description == "Updated description."
        assert persisted_requirement.created_at == created_at
        assert persisted_requirement.updated_at > updated_at
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_requirement_timestamps_are_persisted_as_utc(tmp_path) -> None:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        source_id = uuid4()
        before_creation = datetime.now(UTC)
        with session_factory() as session:
            session.add(Source(id=source_id, title="Call PDF", locator="call.pdf"))
            requirement = Requirement(title="UTC timestamp requirement", source_id=source_id)
            session.add(requirement)
            session.commit()
            requirement_id = requirement.id

        after_creation = datetime.now(UTC)
        with session_factory() as session:
            persisted_requirement = session.get(Requirement, requirement_id)

        assert persisted_requirement is not None
        assert persisted_requirement.created_at.tzinfo == UTC
        assert persisted_requirement.updated_at.tzinfo == UTC
        assert before_creation <= persisted_requirement.created_at <= after_creation
        assert before_creation <= persisted_requirement.updated_at <= after_creation
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
