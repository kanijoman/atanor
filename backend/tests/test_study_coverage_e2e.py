from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.requirement_discovery import (
    PdfRequirementDiscoveryStrategy,
    discover_requirements,
)
from app.application.source import import_pdf_source
from app.application.study_coverage import get_study_coverage
from app.domain.models import Knowledge, KnowledgeNeed, Requirement, RequirementScope
from app.persistence.database import Base
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository
from app.persistence.requirement_repository import SqlAlchemyRequirementRepository
from app.persistence.source_repository import SqlAlchemySourceRepository


SAMPLES_DIR = Path(__file__).parent / "samples"


def test_candidate_can_see_knowledge_coverage_for_a_convocatoria(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "e2e.db"
    engine = create_engine(f"sqlite:///{database_path}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    source_repository = SqlAlchemySourceRepository(session_factory)
    requirement_repository = SqlAlchemyRequirementRepository(session_factory)
    knowledge_repository = SqlAlchemyKnowledgeRepository(session_factory)

    source = import_pdf_source(
        SAMPLES_DIR / "Programa_Archiveros_0.pdf",
        source_repository,
    )
    mentions = discover_requirements(
        source,
        PdfRequirementDiscoveryStrategy(),
    )
    assert len(mentions) >= 2

    constitution = knowledge_repository.save(
        Knowledge(title="Constitución Española")
    )

    covered_requirement = requirement_repository.save(
        Requirement(
            title=mentions[0].expression,
            source_id=source.id,
            scopes=(
                RequirementScope(
                    context="study",
                    knowledge_needs=(
                        KnowledgeNeed(
                            topic="Constitución Española",
                            depth=1,
                            knowledge=constitution,
                        ),
                    ),
                ),
            ),
        )
    )
    missing_requirement = requirement_repository.save(
        Requirement(
            title=mentions[1].expression,
            source_id=source.id,
            scopes=(
                RequirementScope(
                    context="study",
                    knowledge_needs=(
                        KnowledgeNeed(
                            topic="Unknown topic",
                            depth=1,
                        ),
                    ),
                ),
            ),
        )
    )

    result = get_study_coverage(source, requirement_repository)

    assert result.total == 2
    assert result.covered == 1
    assert result.missing == 1
    assert result.coverage_percentage == 50.0
    assert {item.requirement.id for item in result.items} == {
        covered_requirement.id,
        missing_requirement.id,
    }
