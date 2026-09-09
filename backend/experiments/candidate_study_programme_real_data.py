from pathlib import Path
import re

from app.application.candidate_study_programme import get_candidate_study_map
from app.application.requirement_discovery import (
    PdfRequirementDiscoveryStrategy,
    discover_requirements,
)
from app.application.source import import_pdf_source
from app.application.study_programmes import discover_programmes
from app.domain.models import KnowledgeNeed, Requirement, RequirementScope
from app.persistence.database import Base
from app.persistence.source_repository import SqlAlchemySourceRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SAMPLES_DIR = Path(__file__).parent.parent / "tests" / "samples"
SAMPLES = (
    "BOE-A-2024-14098.pdf",
    "BOJA24-138-00046-48048-01_00304998.pdf",
    "OPOS_AYTO_LEON_INFORMATICA_B.pdf",
    "Programa_Archiveros_0.pdf",
)

_TOPIC_MARKER = re.compile(r"^Tema\s+\d+\s*[.\-–—:]?\s*", re.IGNORECASE)


def _normalise_title(title: str) -> str:
    """Normalise a discovered title for deterministic structural comparison."""
    title = _TOPIC_MARKER.sub("", title)
    return " ".join(title.split()).casefold()


def _build_structural_probe_requirements(source, programme, mentions):
    """Build an in-memory probe from structurally matching real mentions.

    The current requirement pipeline discovers requirement mentions but does not
    construct RequirementScope or KnowledgeNeed objects. This experiment therefore
    creates the smallest possible in-memory representation needed to validate the
    candidate-study projection.

    Matching is deterministic and intentionally limited to normalised titles. The
    probe does not use semantic matching, AI, persistence, or fabricated knowledge
    coverage.
    """
    mentions_by_title = {}
    for mention in mentions:
        mentions_by_title.setdefault(_normalise_title(mention.expression), []).append(
            mention
        )

    requirements = []
    for unit in programme.units:
        matching_mentions = mentions_by_title.get(_normalise_title(unit.title), ())
        for mention in matching_mentions:
            requirements.append(
                Requirement(
                    title=mention.expression,
                    source_id=source.id,
                    scopes=(
                        RequirementScope(
                            context=unit.title,
                            knowledge_needs=(
                                KnowledgeNeed(topic=unit.title, depth=1),
                            ),
                        ),
                    ),
                )
            )

    return tuple(requirements)


def _print_report(document, programme, mentions, requirements, study_map) -> None:
    mapped_units = [unit for unit in study_map if unit.knowledge_needs]
    covered_needs = sum(
        len(unit.covered_knowledge_needs) for unit in study_map
    )
    missing_needs = sum(
        len(unit.missing_knowledge_needs) for unit in study_map
    )

    print(f"\nPROGRAMME {programme.identifier} — {programme.title}")
    print(f"  units: {len(programme.units)}")
    print(f"  discovered requirement mentions: {len(mentions)}")
    print(f"  structural unit-title matches: {len(requirements)}")
    print(f"  mapped units: {len(mapped_units)}/{len(study_map)}")
    print(f"  knowledge needs: {covered_needs + missing_needs}")
    print(f"  coverage: {covered_needs} covered / {missing_needs} missing")
    print("  coverage source: unavailable in current pipeline")

    if mapped_units:
        print("  mapped examples:")
        for unit in mapped_units[:5]:
            print(f"    {unit.number}. {unit.title}")
            for need in unit.knowledge_needs:
                print(f"      - MISSING: {need.topic} [depth={need.depth}]")

    unmapped_count = len(study_map) - len(mapped_units)
    if unmapped_count:
        print(f"  unmapped units: {unmapped_count}")


def run() -> None:
    """Run the candidate study programme validation experiment."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    source_repository = SqlAlchemySourceRepository(session_factory)

    try:
        for document in SAMPLES:
            source = import_pdf_source(SAMPLES_DIR / document, source_repository)
            programmes = discover_programmes(source)
            mentions = discover_requirements(
                source,
                PdfRequirementDiscoveryStrategy(),
            )

            print(f"\n=== {document} ===")
            print(f"DISCOVERED PROGRAMMES: {len(programmes)}")
            print(f"DISCOVERED REQUIREMENT MENTIONS: {len(mentions)}")

            if not programmes:
                print("NO PROGRAMME AVAILABLE FOR CANDIDATE STUDY VALIDATION")
                continue

            for programme in programmes:
                requirements = _build_structural_probe_requirements(
                    source,
                    programme,
                    mentions,
                )
                study_map = get_candidate_study_map(programme, requirements)
                _print_report(
                    document,
                    programme,
                    mentions,
                    requirements,
                    study_map,
                )
    finally:
        engine.dispose()


if __name__ == "__main__":
    run()
