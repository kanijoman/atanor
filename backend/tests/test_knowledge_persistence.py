from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.models import Knowledge as DomainKnowledge
from app.domain.models import Source as DomainSource
from app.persistence.database import Base
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository
from app.persistence.models.source import Source as PersistenceSource


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


def test_concurrent_saves_of_the_same_identity_converge_on_the_stored_knowledge(
    tmp_path, monkeypatch
) -> None:
    """Two requests may both miss the cache and save the same material and source."""
    engine = create_engine(f"sqlite:///{tmp_path / 'race.db'}")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        source = DomainSource(title="Ley", locator="https://example.org/ley")
        identity = ("Tema", 1)
        repository = SqlAlchemyKnowledgeRepository(session_factory)
        first = repository.save(
            DomainKnowledge(title="Tema", sources=(source,), identity_key=identity)
        )

        # Simulate the lost race: this save does not see the source created by the first one.
        def blind_source_lookup(session, source):
            persisted = PersistenceSource(id=source.id, title=source.title, locator=source.locator)
            session.add(persisted)
            session.flush()
            return persisted

        monkeypatch.setattr(repository, "_get_or_create_source", blind_source_lookup)
        second = repository.save(
            DomainKnowledge(title="Tema", sources=(source,), identity_key=identity)
        )

        assert second.id == first.id
    finally:
        Base.metadata.drop_all(bind=engine)
