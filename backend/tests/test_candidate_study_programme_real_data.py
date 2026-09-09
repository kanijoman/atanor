from pathlib import Path

from app.application.candidate_study_programme import get_candidate_study_map
from app.application.requirement_discovery import PdfRequirementDiscoveryStrategy, discover_requirements
from app.application.requirement_workflow import get_study_requirements
from app.application.source import import_pdf_source
from app.application.study_programmes import discover_programmes
from app.domain.models import Knowledge, KnowledgeNeed, Requirement, RequirementScope, Source
from app.persistence.database import Base
from app.persistence.models.source import Source as PersistenceSource
from app.persistence.requirement_repository import SqlAlchemyRequirementRepository
from app.persistence.source_repository import SqlAlchemySourceRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SAMPLES_DIR = Path(__file__).parent / "samples"
SAMPLES = (
    "BOE-A-2024-14098.pdf",
    "BOJA24-138-00046-48048-01_00304998.pdf",
    "OPOS_AYTO_LEON_INFORMATICA_B.pdf",
    "Programa_Archiveros_0.pdf",
)


def _source(name: str) -> Source:
    return Source(title=name, locator=str(SAMPLES_DIR / name))


def _print_report(document: str, programme, requirements, study_map) -> None:
    print(f"\nDOCUMENT: {document}")
    print(f"PROGRAMME: {programme.identifier} — {programme.title}")
    print(f"UNITS: {len(programme.units)}")
    print(f"REQUIREMENTS: {len(requirements)}")

    mapped = sum(bool(unit.knowledge_needs) for unit in study_map)
    print(f"MAPPED UNITS: {mapped}/{len(study_map)}")
    print("UNITS WITHOUT KNOWLEDGE NEEDS:")
    for unit in study_map:
        if not unit.knowledge_needs:
            print(f"  {unit.number}. {unit.title}")

    print("MAPPED UNITS:")
    for unit in study_map:
        if not unit.knowledge_needs:
            continue
        print(f"  {unit.number}. {unit.title}")
        for need in unit.knowledge_needs:
            status = "COVERED" if need.knowledge is not None else "MISSING"
            print(f"    - {status}: {need.topic} [depth={need.depth}]")


def test_real_documents_candidate_study_map_diagnostic() -> None:
    """Print a bounded diagnostic report for all supported real document samples."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    source_repository = SqlAlchemySourceRepository(session_factory)
    requirement_repository = SqlAlchemyRequirementRepository(session_factory)

    try:
        for document in SAMPLES:
            source = import_pdf_source(SAMPLES_DIR / document, source_repository)
            programmes = discover_programmes(source)
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

            study_requirements = get_study_requirements(
                source,
                requirement_repository,
            )

            print(f"\n=== {document} ===")
            print(f"DISCOVERED PROGRAMMES: {len(programmes)}")
            print(f"DISCOVERED REQUIREMENT MENTIONS: {len(mentions)}")
            print(f"RESOLVED REQUIREMENTS: {len(study_requirements.requirements)}")
            assert known_requirements
            assert programmes

            for programme in programmes:
                study_map = get_candidate_study_map(
                    programme,
                    study_requirements.requirements,
                )
                _print_report(
                    document,
                    programme,
                    study_requirements.requirements,
                    study_map,
                )
    finally:
        engine.dispose()
