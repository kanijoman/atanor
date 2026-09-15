from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.models import Knowledge as DomainKnowledge
from app.persistence.database import Base
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository


def test_knowledge_can_be_retrieved_by_identity_after_persistence(tmp_path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        knowledge = DomainKnowledge(
            title="Procedimiento administrativo común",
            description="Reusable study material",
            identity_key=("Procedimiento administrativo común", 1),
        )
        repository = SqlAlchemyKnowledgeRepository(session_factory)
        repository.save(knowledge)

        fresh_repository = SqlAlchemyKnowledgeRepository(session_factory)
        persisted = fresh_repository.get_by_identity(knowledge.identity_key)

        assert persisted == knowledge
        assert persisted is not knowledge
        assert persisted.id == knowledge.id
        assert persisted.identity_key == knowledge.identity_key
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
