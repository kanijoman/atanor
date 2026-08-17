from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.models import (
    Knowledge,
    KnowledgeNeed,
    Requirement,
    RequirementScope,
    Source,
)
from app.persistence.database import Base
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository
from app.persistence.requirement_repository import SqlAlchemyRequirementRepository
from app.persistence.source_repository import SqlAlchemySourceRepository


def test_requirement_preserves_known_and_unknown_knowledge_after_persistence(tmp_path) -> None:
    database_path = tmp_path / "e2e.db"
    engine = create_engine(f"sqlite:///{database_path}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    source_repository = SqlAlchemySourceRepository(session_factory)
    knowledge_repository = SqlAlchemyKnowledgeRepository(session_factory)
    requirement_repository = SqlAlchemyRequirementRepository(session_factory)

    source = Source(title="Call", locator="call.pdf")
    source_repository.save(source)

    known_knowledge = knowledge_repository.save(
        Knowledge(title="Spanish Constitution")
    )
    requirement = Requirement(
        title="Study topics",
        source_id=source.id,
        scopes=(
            RequirementScope(
                context="Candidate study",
                knowledge_needs=(
                    KnowledgeNeed(
                        topic="Spanish Constitution",
                        depth=1,
                        knowledge=known_knowledge,
                    ),
                    KnowledgeNeed(
                        topic="Open management topic",
                        depth=1,
                    ),
                ),
            ),
        ),
    )

    saved = requirement_repository.save(requirement)
    loaded = requirement_repository.get_by_id(saved.id)

    assert loaded is not None
    knowledge_needs = loaded.scopes[0].knowledge_needs
    assert knowledge_needs[0].knowledge is not None
    assert knowledge_needs[0].knowledge.title == "Spanish Constitution"
    assert knowledge_needs[1].knowledge is None
    assert knowledge_needs[1].knowledge_id is None
