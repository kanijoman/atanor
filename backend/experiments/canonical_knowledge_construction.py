"""Explore construction of canonical knowledge from a real KnowledgeNeed.

This is an evidence-gathering experiment, not a product contract. It deliberately
keeps the current domain model unchanged and separates:

    KnowledgeNeed -> canonical source candidates -> relevant source content

from the later construction of validated Knowledge.

The experiment uses the existing BOE sample and a manually selected legal topic
so that we can inspect what a canonical-source workflow actually requires before
introducing production abstractions.
"""

from pathlib import Path
import re

from app.application.requirement_discovery import (
    PdfRequirementDiscoveryStrategy,
    discover_requirements,
)
from app.application.source import import_pdf_source
from app.application.study_programmes import discover_programmes
from app.domain.models import KnowledgeNeed
from app.persistence.database import Base
from app.persistence.source_repository import SqlAlchemySourceRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SAMPLES_DIR = Path(__file__).parent.parent / "tests" / "samples"
SOURCE_DOCUMENT = "BOE-A-2024-14098.pdf"

_TOPIC_MARKER = re.compile(r"^Tema\s+\d+\s*[.\-–—:]?\s*", re.IGNORECASE)
_CANONICAL_HINTS = (
    "constitución",
    "ley ",
    "real decreto",
    "reglamento",
    "estatuto",
    "tratado",
    "derechos",
    "procedimiento administrativo",
    "organización administrativa",
)


def _normalise(text: str) -> str:
    return " ".join(text.split()).casefold()


def _is_canonical_candidate(title: str) -> bool:
    normalised = _normalise(_TOPIC_MARKER.sub("", title))
    return any(hint in normalised for hint in _CANONICAL_HINTS)


def _print_unit(unit, programme) -> None:
    print(f"\nPROGRAMME {programme.identifier} — {programme.title}")
    print(f"UNIT: {unit.number}. {unit.title}")
    print(f"SOURCE SPAN: pages {unit.start_page}-{unit.end_page}")
    print("KNOWLEDGE NEED")
    print(f"  topic: {unit.title}")
    print("  depth: 1")
    print("CANONICAL CLASSIFICATION")
    print("  candidate: YES")
    print("  basis: deterministic legal/canonical vocabulary hint")
    print("\nCANONICAL SOURCE CANDIDATES")
    print("  [to be identified]")
    print("\nREQUIRED EVIDENCE QUESTIONS")
    print("  1. Which authoritative source(s) define the required knowledge?")
    print("  2. Which source provisions/content are relevant to this need?")
    print("  3. Is the source current for the selected call?")
    print("  4. Is the extracted content sufficient to claim coverage?")
    print("\nCURRENT KNOWLEDGE MODEL")
    print("  Knowledge: not constructed")
    print("  Coverage: MISSING")
    print("  reason: canonical source identification and validation are not yet")
    print("          an implemented product capability")


def run() -> None:
    """Inspect candidate canonical topics in the real BOE study programme."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    source_repository = SqlAlchemySourceRepository(session_factory)

    try:
        source = import_pdf_source(SAMPLES_DIR / SOURCE_DOCUMENT, source_repository)
        programmes = discover_programmes(source)
        mentions = discover_requirements(
            source,
            PdfRequirementDiscoveryStrategy(),
        )

        print(f"=== {SOURCE_DOCUMENT} ===")
        print(f"PROGRAMMES: {len(programmes)}")
        print(f"REQUIREMENT MENTIONS: {len(mentions)}")
        print("\nCANONICAL KNOWLEDGE CONSTRUCTION PROBE")
        print("This experiment does not use AI, semantic matching, or fabricated")
        print("knowledge. It only identifies promising legal/canonical topics and")
        print("records the evidence still needed to construct Knowledge.")

        candidate_count = 0
        for programme in programmes:
            for unit in programme.units:
                if not _is_canonical_candidate(unit.title):
                    continue
                candidate_count += 1
                KnowledgeNeed(topic=unit.title, depth=1)
                _print_unit(unit, programme)
                if candidate_count >= 3:
                    break
            if candidate_count >= 3:
                break

        print(f"\nCANONICAL CANDIDATES INSPECTED: {candidate_count}")
        print("EXPERIMENT STATUS: READY FOR MANUAL SOURCE-MAPPING")
    finally:
        engine.dispose()


if __name__ == "__main__":
    run()
