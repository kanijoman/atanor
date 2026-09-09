"""Explore canonical knowledge construction from one real legal KnowledgeNeed.

This is a deterministic discovery experiment, not a production contract. It
follows one real study-programme unit outside the call PDF's own content:

    KnowledgeNeed -> canonical legal source -> source material
    -> relevant provisions -> candidate Knowledge -> coverage evidence

The experiment intentionally keeps the production domain model unchanged.
"""

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.request import Request, urlopen

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

CANONICAL_SOURCE = {
    "title": "Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno",
    "identifier": "BOE-A-2013-12887",
    "locator": "https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
    "authority": "Boletín Oficial del Estado",
}

RELEVANCE_TERMS = (
    "transparencia",
    "acceso a la información",
    "buen gobierno",
)


@dataclass(frozen=True)
class SourceFragment:
    """Experiment representation of a source provision relevant to a need."""

    source_identifier: str
    locator: str
    title: str
    text: str


class _LawHtmlParser(HTMLParser):
    """Extract article headings and their following text from BOE HTML."""

    _ARTICLE_PATTERN = re.compile(r"Artículo\s+([0-9]+(?:\s+bis)?)\.\s*(.*)", re.I)

    def __init__(self) -> None:
        super().__init__()
        self.articles: list[tuple[str, str, str]] = []
        self._current_number: str | None = None
        self._current_title: str | None = None
        self._current_text: list[str] = []
        self._capture_heading = False
        self._capture_body = False

    def handle_starttag(self, tag: str, attrs) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id", "")
        if element_id.startswith("a") and element_id[1:].isdigit():
            self._finish_article()
        if tag in {"h4", "h5"}:
            self._capture_heading = True
        elif self._current_number is not None and tag in {"p", "li"}:
            self._capture_body = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"h4", "h5"}:
            self._capture_heading = False
        elif tag in {"p", "li"}:
            self._capture_body = False

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if not text:
            return
        if self._capture_heading:
            match = self._ARTICLE_PATTERN.match(text)
            if match:
                self._finish_article()
                self._current_number = match.group(1)
                self._current_title = match.group(2)
                return
        if self._current_number is not None and self._capture_body:
            self._current_text.append(text)

    def _finish_article(self) -> None:
        if self._current_number is None or self._current_title is None:
            return
        self.articles.append(
            (self._current_number, self._current_title, " ".join(self._current_text))
        )
        self._current_number = None
        self._current_title = None
        self._current_text = []

    def close(self) -> None:
        super().close()
        self._finish_article()


def _normalise(text: str) -> str:
    return " ".join(text.split()).casefold()


def _matches_target(title: str) -> bool:
    return _normalise(title).startswith(_normalise(TARGET_TITLE))


def _find_target(programmes):
    for programme in programmes:
        for unit in programme.units:
            if _matches_target(unit.title):
                return programme, unit
    raise RuntimeError(f"Target study unit not found: {TARGET_TITLE}")


def _fetch_canonical_text() -> str:
    request = Request(
        CANONICAL_SOURCE["locator"],
        headers={"User-Agent": "Atanor canonical-knowledge experiment"},
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def _extract_articles(html: str) -> list[SourceFragment]:
    parser = _LawHtmlParser()
    parser.feed(html)
    parser.close()
    return [
        SourceFragment(
            source_identifier=CANONICAL_SOURCE["identifier"],
            locator=CANONICAL_SOURCE["locator"] + f"#a{number.replace(' ', '')}",
            title=f"Artículo {number}. {title}",
            text=text,
        )
        for number, title, text in parser.articles
    ]


def _score_fragment(fragment: SourceFragment) -> int:
    haystack = _normalise(f"{fragment.title} {fragment.text}")
    return sum(haystack.count(_normalise(term)) for term in RELEVANCE_TERMS)


def _select_relevant_fragments(
    fragments: list[SourceFragment],
) -> list[tuple[SourceFragment, int]]:
    scored = [(fragment, _score_fragment(fragment)) for fragment in fragments]
    return sorted(
        ((fragment, score) for fragment, score in scored if score > 0),
        key=lambda item: (-item[1], item[0].title),
    )


def _build_candidate_knowledge(
    need: KnowledgeNeed,
    fragments: list[SourceFragment],
) -> Knowledge:
    source = Source(
        title=CANONICAL_SOURCE["title"],
        locator=CANONICAL_SOURCE["locator"],
    )
    return Knowledge(
        title=need.topic,
        description=(
            "Candidate knowledge grounded in the official consolidated text of the law. "
            f"The experiment identified {len(fragments)} potentially relevant articles; "
            "relevance and completeness still require validation."
        ),
        sources=(source,),
    )


def _print_probe(
    programme,
    unit,
    need,
    fragments: list[tuple[SourceFragment, int]],
    candidate: Knowledge,
) -> None:
    print(f"\nPROGRAMME {programme.identifier} — {programme.title}")
    print(f"STUDY UNIT: {unit.number}. {unit.title}")
    print(f"CALL SOURCE SPAN: pages {unit.start_page}-{unit.end_page}")

    print("\n1. KNOWLEDGE NEED")
    print(f"  topic: {need.topic}")
    print(f"  depth: {need.depth}")

    print("\n2. CANONICAL LEGAL SOURCE")
    for key in ("title", "identifier", "authority", "locator"):
        print(f"  {key}: {CANONICAL_SOURCE[key]}")

    print("\n3. SOURCE MATERIAL")
    print("  status: ACQUIRED")
    print(f"  candidate relevant articles: {len(fragments)}")
    print("  source role: canonical legal reference")

    print("\n4. RELEVANT SOURCE CONTENT")
    if not fragments:
        print("  no candidate provisions identified")
    else:
        for fragment, score in fragments:
            print(f"  - {fragment.title} (relevance score: {score})")
            print(f"    locator: {fragment.locator}")
            print(f"    excerpt: {fragment.text[:240]}")

    print("\n5. CANDIDATE KNOWLEDGE")
    print(f"  title: {candidate.title}")
    print(f"  sources: {len(candidate.sources)}")
    print("  status: CANDIDATE — NOT VALIDATED")

    print("\n6. COVERAGE EVIDENCE")
    print("  source authority: SATISFIED")
    print("  source acquisition: SATISFIED")
    print(
        "  relevant-content identification: "
        + ("PARTIAL" if fragments else "MISSING")
    )
    print("  completeness against KnowledgeNeed: NOT ESTABLISHED")
    print("  current-version validation: NOT ESTABLISHED")
    print("  coverage result: NOT COVERED")

    print("\n7. MODEL OBSERVATIONS")
    print("  Knowledge can reference the canonical Source.")
    print("  The experiment can identify concrete source fragments outside the call.")
    print("  Knowledge.sources still cannot represent which fragments support it.")
    print("  The experiment therefore tests whether source-fragment provenance")
    print("  is the missing evidence boundary rather than assuming a new domain model.")


def run() -> None:
    """Run the single-case canonical knowledge construction probe."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    source_repository = SqlAlchemySourceRepository(session_factory)

    try:
        source = import_pdf_source(SAMPLES_DIR / CALL_DOCUMENT, source_repository)
        programmes = discover_programmes(source)
        mentions = discover_requirements(source, PdfRequirementDiscoveryStrategy())
        programme, unit = _find_target(programmes)
        need = KnowledgeNeed(topic=unit.title, depth=1)

        print(f"=== {CALL_DOCUMENT} ===")
        print(f"PROGRAMMES: {len(programmes)}")
        print(f"REQUIREMENT MENTIONS: {len(mentions)}")
        print("\nCANONICAL KNOWLEDGE CONSTRUCTION — SINGLE CASE")
        print("The call defines the study scope; the official law provides the")
        print("canonical legal content. No coverage is claimed without evidence.")

        html = _fetch_canonical_text()
        articles = _extract_articles(html)
        relevant = _select_relevant_fragments(articles)
        candidate = _build_candidate_knowledge(
            need, [fragment for fragment, _ in relevant]
        )
        _print_probe(programme, unit, need, relevant, candidate)

        print("\nEXPERIMENT CONCLUSION")
        print("  1. Canonical source acquisition: WORKS")
        print("     The experiment can obtain the current consolidated legal source.")
        print("  2. Source-fragment extraction: WORKS")
        print("     Concrete provisions can be identified outside the call document.")
        print("  3. Relevant-content selection: PARTIAL")
        print("     Deterministic matching produces candidates, but does not prove")
        print("     that the selected provisions fully satisfy the study scope.")
        print("  4. Knowledge model: PARTIALLY SUFFICIENT")
        print("     It can identify the knowledge and canonical source, but cannot")
        print("     record the exact source fragments supporting the knowledge.")
        print("  5. Coverage: NOT ESTABLISHED")
        print("     Source authority and acquisition are not sufficient to establish")
        print("     completeness against the KnowledgeNeed.")
        print("\nEXPERIMENT STATUS: EVIDENCE COLLECTED — MODEL EXTENSION NOT YET IMPLEMENTED")
    finally:
        engine.dispose()


if __name__ == "__main__":
    run()
