from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.requirement_discovery import (
    PdfRequirementDiscoveryStrategy,
    discover_requirements,
)
from app.application.requirement_workflow import get_study_requirements
from app.application.source import import_pdf_source
from app.domain.models import Requirement
from app.persistence.database import Base
from app.persistence.requirement_repository import SqlAlchemyRequirementRepository
from app.persistence.source_repository import SqlAlchemySourceRepository


def test_program_archiveros_produces_study_requirements_from_known_knowledge(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "e2e.db"
    engine = create_engine(f"sqlite:///{database_path}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    source_repository = SqlAlchemySourceRepository(session_factory)
    requirement_repository = SqlAlchemyRequirementRepository(session_factory)

    sample_path = Path("tests/samples/Programa_Archiveros_0.pdf")

    source = import_pdf_source(sample_path, source_repository)

    mentions = discover_requirements(
        source,
        PdfRequirementDiscoveryStrategy(),
    )

    known_requirements = [
        requirement_repository.save(
            Requirement(
                title=mention.expression,
                source_id=source.id,
            )
        )
        for mention in mentions
    ]

    result = get_study_requirements(
        source,
        requirement_repository,
    )

    assert len(mentions) == 25
    assert len(known_requirements) == 25
    assert len(result.requirements) == 25

    assert [requirement.title for requirement in result.requirements] == [
        requirement.title for requirement in known_requirements
    ]

    assert all(
        requirement.source_id == source.id
        for requirement in result.requirements
    )
