from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.requirement import (
    PdfRequirementDiscoveryStrategy,
    discover_and_persist_requirements,
    list_requirements,
)
from app.application.source import import_pdf_source
from app.persistence.database import Base
from app.persistence.requirement_repository import SqlAlchemyRequirementRepository
from app.persistence.source_repository import SqlAlchemySourceRepository


SAMPLES_DIR = Path(__file__).parent / "samples"


@pytest.mark.parametrize(
    "sample_name",
    [
        "BOE-A-2024-14098.pdf",
        "Programa_Archiveros_0.pdf",
    ],
)
def test_real_textual_sample_flows_from_source_to_persisted_requirements(
    sample_name: str, tmp_path: Path
) -> None:
    database_url = f"sqlite:///{tmp_path / 'e2e.db'}"
    engine = create_engine(database_url)
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    source_repository = SqlAlchemySourceRepository(session_factory)
    requirement_repository = SqlAlchemyRequirementRepository(session_factory)
    source_path = SAMPLES_DIR / sample_name

    source = import_pdf_source(source_path, source_repository)
    requirements = discover_and_persist_requirements(
        source,
        PdfRequirementDiscoveryStrategy(),
        requirement_repository,
    )

    assert requirements
    assert all(requirement.source_id == source.id for requirement in requirements)
    assert list_requirements(requirement_repository) == requirements

    for requirement in requirements:
        restored = requirement_repository.get_by_id(requirement.id)
        assert restored is not None
        assert restored.id == requirement.id
        assert restored.title == requirement.title
        assert restored.source_id == source.id



def test_scanned_sample_is_imported_but_produces_no_requirements(tmp_path: Path) -> None:
    database_url = f"sqlite:///{tmp_path / 'e2e.db'}"
    engine = create_engine(database_url)
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    source_repository = SqlAlchemySourceRepository(session_factory)
    requirement_repository = SqlAlchemyRequirementRepository(session_factory)
    source_path = SAMPLES_DIR / "OPOS_AYTO_LEON_INFORMATICA_B.pdf"

    source = import_pdf_source(source_path, source_repository)
    requirements = discover_and_persist_requirements(
        source,
        PdfRequirementDiscoveryStrategy(),
        requirement_repository,
    )

    assert requirements == []
    assert list_requirements(requirement_repository) == []
    assert source_repository.get_by_id(source.id) is not None
