"""Explore canonical knowledge construction from one real legal KnowledgeNeed.

This is a deterministic discovery experiment, not a production contract. It
follows one real study-programme unit outside the call PDF's own content:

    KnowledgeNeed -> canonical legal source -> relevant source content
    -> candidate Knowledge -> coverage evidence

The experiment intentionally keeps the production domain model unchanged.
"""

from dataclasses import dataclass
from pathlib import Path
import re

from app.application.requirement_discovery import (
    PdfRequirementDiscoveryStrategy,
    discover_requirements,
)
from app.application.source import import_pdf_source
from app.application.study_programmes import discover_programmes
from app.domain.models import Knowledge, KnowledgeNeed, Source
from app.persistence.database import Base
from app.persistence.source_repository import SqlAlchemySourceRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SAMPLES_DIR = Path(__file__).parent.parent / "tests" / "samples"
CALL_DOCUMENT = "BOE-A-2024-14098.pdf"
TARGET_TITLE = (
    "La Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información"
)

# Canonical source configured for the experiment. This is deliberately experiment
# data rather than a new production source-discovery abstraction.
CANONICAL_SOURCE = {
    "title": "Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno",
    "identifier": "BOE-A-2013-12887",
    "locator": "https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
    "authority": "Boletín Oficial del Estado",
}


def _normalise(text: str) -> str:
    return " ".join(text.split()).casefold()


def _matches_target(title: str) -> bool:
    return _normalise(title).startswith(_normalise(TARGET_TITLE))


@dataclass(frozen=True)
class RelevantContent:
    """Experiment representation of a source fragment relevant to a need."""

    source_identifier: str
    locator: str
    description: str


def _find_target(programmes):
    for programme in programmes:
        for unit in programme.units:
            if _matches_target(unit.title):
                return programme, unit
    raise RuntimeError(f"Target study unit not found: {TARGET_TITLE}")


def _build_candidate_knowledge(need: KnowledgeNeed) -> Knowledge:
    source = Source(
        title=CANONICAL_SOURCE["title"],
        locator=CANONICAL_SOURCE["locator"],
    )
    return Knowledge(
        title=need.topic,
        description=(
            "Candidate knowledge grounded in the official consolidated text of "
            "the identified law. Relevance and completeness still require validation."
        ),
        sources=(source,),
    )


def _print_probe(programme, unit, need, relevant_content, candidate):
    print(f"\nPROGRAMME {programme.identifier} — {programme.title}")
    print(f"STUDY UNIT: {unit.number}. {unit.title}")
    print(f"CALL SOURCE SPAN: pages {unit.start_page}-{unit.end_page}")

    print("\n1. KNOWLEDGE NEED")
    print(f"  topic: {need.topic}")
    print(f"  depth: {need.depth}")

    print("\n2. CANONICAL LEGAL SOURCE")
    for key in ("title", "identifier", "authority", "locator"):
        print(f"  {key}: {CANONICAL_SOURCE[key]}")

    print("\n3. RELEVANT SOURCE CONTENT")
    print(f"  source: {relevant_content.source_identifier}")
    print(f"  locator: {relevant_content.locator}")
    print(f"  description: {relevant_content.description}")
    print("  status: NOT ACQUIRED IN THIS EXPERIMENT")

    print("\n4. CANDIDATE KNOWLEDGE")
    print(f"  title: {candidate.title}")
    print(f"  sources: {len(candidate.sources)}")
    print("  status: CANDIDATE — NOT VALIDATED")

    print("\n5. COVERAGE EVIDENCE")
    print("  source authority: SATISFIED")
    print("  source acquisition: MISSING")
    print("  relevant-content identification: MISSING")
    print("  completeness against KnowledgeNeed: MISSING")
    print("  current-version validation: MISSING")
    print("  coverage result: NOT COVERED")

    print("\n6. MODEL OBSERVATIONS")
    print("  Knowledge can reference the canonical Source.")
    print("  Knowledge can describe the candidate content at a coarse level.")
    print("  The current model cannot represent the relevant source fragment")
    print("  or the evidence connecting that fragment to the KnowledgeNeed.")
    print("  Therefore Knowledge.sources alone is insufficient for auditable coverage.")


def run() -> None:
    """Run the single-case canonical knowledge construction probe."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    source_repository = SqlAlchemySourceRepository(session_factory)

    try:
        source = import_pdf_source(SAMPLES_DIR / CALL_DOCUMENT, source_repository)
        programmes = discover_programmes(source)
        mentions = discover_requirements(
            source,
            PdfRequirementDiscoveryStrategy(),
        )
        programme, unit = _find_target(programmes)
        need = KnowledgeNeed(topic=unit.title, depth=1)

        relevant_content = RelevantContent(
            source_identifier=CANONICAL_SOURCE["identifier"],
            locator=CANONICAL_SOURCE["locator"],
            description=(
                "The provisions of Ley 19/2013 relevant to the study-programme "
                "scope. Exact articles must be identified from the consolidated text."
            ),
        )
        candidate = _build_candidate_knowledge(need)

        print(f"=== {CALL_DOCUMENT} ===")
        print(f"PROGRAMMES: {len(programmes)}")
        print(f"REQUIREMENT MENTIONS: {len(mentions)}")
        print("\nCANONICAL KNOWLEDGE CONSTRUCTION — SINGLE CASE")
        print("The call defines the study scope; the official law provides the")
        print("canonical legal content. No coverage is claimed without evidence.")

        _print_probe(programme, unit, need, relevant_content, candidate)

        print("\nEXPERIMENT CONCLUSION")
        print("  1. Current Knowledge model: PARTIALLY SUFFICIENT")
        print("     It can identify the knowledge and its canonical source, but not")
        print("     the source fragment/evidence needed for auditable coverage.")
        print("  2. Direct KnowledgeNeed -> Knowledge: INSUFFICIENT FOR COVERAGE")
        print("     A relationship alone does not explain why the need is covered.")
        print("  3. Required evidence: authoritative source + relevant content +")
        print("     completeness/currentness validation.")
        print("  4. Source granularity: the need may map to a subset of the law.")
        print("  5. Boundary: acquisition obtains source material; construction")
        print("     produces candidate Knowledge; coverage evaluates evidence.")
        print("\nEXPERIMENT STATUS: EVIDENCE COLLECTED — MODEL EXTENSION NOT YET IMPLEMENTED")
    finally:
        engine.dispose()


if __name__ == "__main__":
    run()
