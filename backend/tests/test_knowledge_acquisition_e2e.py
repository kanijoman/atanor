from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.knowledge_acquisition import (
    BoeKnowledgeAcquisitionStrategy,
    acquire_knowledge,
)
from app.application.source import import_pdf_source
from app.domain.models import KnowledgeNeed
from app.persistence.database import Base
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository
from app.persistence.source_repository import SqlAlchemySourceRepository


SAMPLES_DIR = Path(__file__).parent / "samples"


def test_atanor_can_acquire_knowledge_from_boe_without_candidate_input(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "e2e.db"
    engine = create_engine(f"sqlite:///{database_path}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    source_repository = SqlAlchemySourceRepository(session_factory)
    knowledge_repository = SqlAlchemyKnowledgeRepository(session_factory)

    source = import_pdf_source(
        SAMPLES_DIR / "BOE-A-2024-14098.pdf",
        source_repository,
    )
    need = KnowledgeNeed(topic="Constitución Española", depth=1)

    assert need.knowledge is None

    acquired = acquire_knowledge(
        need,
        BoeKnowledgeAcquisitionStrategy(source),
    )

    assert acquired is not None
    assert acquired.title == need.topic
    assert acquired.description
    assert acquired.sources == (source,)

    persisted = knowledge_repository.save(acquired)
    restored = knowledge_repository.get_by_id(persisted.id)

    assert restored is not None
    assert restored.title == need.topic
    assert restored.description == acquired.description
