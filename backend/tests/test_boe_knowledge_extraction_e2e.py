from pathlib import Path

from app.application.knowledge_acquisition import BoeKnowledgeAcquisitionStrategy
from app.application.knowledge_extraction import DeterministicKnowledgeExtractionStrategy
from app.application.pdf_extraction import extract_pdf_text
from app.application.source import import_pdf_source
from app.domain.models import KnowledgeNeed
from app.persistence.database import Base
from app.persistence.source_repository import SqlAlchemySourceRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def test_boe_can_provide_relevant_knowledge_for_a_need(tmp_path: Path) -> None:
    database_path = tmp_path / "e2e.db"
    engine = create_engine(f"sqlite:///{database_path}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    source_repository = SqlAlchemySourceRepository(session_factory)
    source = import_pdf_source(
        Path("tests/samples/BOE-A-2024-14098.pdf"),
        source_repository,
    )
    need = KnowledgeNeed(topic="Constitución Española", depth=1)

    acquired = BoeKnowledgeAcquisitionStrategy(source).acquire(need)
    assert acquired is not None

    extracted = DeterministicKnowledgeExtractionStrategy(context_lines=2).extract(
        need,
        extract_pdf_text(source),
    )

    assert extracted is not None
    assert extracted.title == need.topic
    assert extracted.description
    assert "Constitución Española" in extracted.description
    assert len(extracted.description) < len(acquired.description)
