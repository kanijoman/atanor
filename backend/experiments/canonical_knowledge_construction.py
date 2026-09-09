"""Explore the minimum useful knowledge unit for one real legal study scope.

This is a deterministic discovery experiment, not a production contract. It takes
one real study-programme unit and manually decomposes its broad legal scope into
provisional, teachable knowledge needs. Each need is then mapped to authoritative
provisions from the canonical BOE text.

The experiment intentionally keeps the production domain model unchanged. Its
purpose is to discover whether a stable boundary emerges between:

    Study Scope -> Knowledge Need -> Relevant Knowledge Content -> Source Evidence
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


@dataclass(frozen=True)
class SourceFragment:
    """Experiment representation of one canonical source provision."""

    source_identifier: str
    locator: str
    title: str
    text: str


@dataclass(frozen=True)
class ProvisionalKnowledgeNeed:
    """Exploratory decomposition of a broad study scope."""

    topic: str
    description: str
    article_numbers: tuple[str, ...]


# This is deliberately manual: the experiment tests the semantic granularity
# of a useful knowledge need rather than pretending that keyword matching can
# infer the study structure.
PROVISIONAL_NEEDS = (
    ProvisionalKnowledgeNeed(
        topic="Objeto, ámbito y definiciones",
        description="What the law regulates, who it applies to, and its key definitions.",
        article_numbers=("1", "2", "3", "4"),
    ),
    ProvisionalKnowledgeNeed(
        topic="Principios generales y publicidad activa",
        description="General transparency principles and the obligations of active publicity.",
        article_numbers=tuple(str(number) for number in range(5, 12)),
    ),
    ProvisionalKnowledgeNeed(
        topic="Derecho de acceso a la información pública",
        description="The right of access, its procedure, limits, and review mechanisms.",
        article_numbers=tuple(str(number) for number in range(12, 25)),
    ),
    ProvisionalKnowledgeNeed(
        topic="Buen gobierno",
        description="Principles, duties, infringements, sanctions, and enforcement of good governance.",
        article_numbers=tuple(str(number) for number in range(25, 33)),
    ),
    ProvisionalKnowledgeNeed(
        topic="Consejo de Transparencia y Buen Gobierno",
        description="Purpose, composition, functions, legal regime, and accountability of the Council.",
        article_numbers=tuple(str(number) for number in range(33, 41)),
    ),
)


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


def _extract_articles(html: str) -> dict[str, SourceFragment]:
    parser = _LawHtmlParser()
    parser.feed(html)
    parser.close()
    return {
        number: SourceFragment(
            source_identifier=CANONICAL_SOURCE["identifier"],
            locator=CANONICAL_SOURCE["locator"] + f"#a{number.replace(' ', '')}",
            title=f"Artículo {number}. {title}",
            text=text,
        )
        for number, title, text in parser.articles
    }


def _resolve_evidence(
    need: ProvisionalKnowledgeNeed,
    articles: dict[str, SourceFragment],
) -> tuple[SourceFragment, ...]:
    missing = [number for number in need.article_numbers if number not in articles]
    if missing:
        raise RuntimeError(
            f"Canonical source is missing expected articles for '{need.topic}': {missing}"
        )
    return tuple(articles[number] for number in need.article_numbers)


def _build_candidate_knowledge(
    need: ProvisionalKnowledgeNeed,
    evidence: tuple[SourceFragment, ...],
) -> tuple[KnowledgeNeed, Knowledge]:
    knowledge_need = KnowledgeNeed(topic=need.topic, depth=1)
    source = Source(
        title=CANONICAL_SOURCE["title"],
        locator=CANONICAL_SOURCE["locator"],
    )
    knowledge = Knowledge(
        title=need.topic,
        description=need.description,
        sources=(source,),
    )
    return knowledge_need, knowledge


def _print_need(
    index: int,
    need: ProvisionalKnowledgeNeed,
    knowledge_need: KnowledgeNeed,
    knowledge: Knowledge,
    evidence: tuple[SourceFragment, ...],
) -> None:
    print(f"\n{index}. PROVISIONAL KNOWLEDGE NEED")
    print(f"  topic: {knowledge_need.topic}")
    print(f"  depth: {knowledge_need.depth}")
    print(f"  description: {need.description}")
    print(f"  canonical evidence: articles {', '.join(need.article_numbers)}")
    print(f"  evidence fragments resolved: {len(evidence)}")

    print("  evidence examples:")
    for fragment in evidence[:2]:
        print(f"    - {fragment.title}")
        print(f"      locator: {fragment.locator}")
        print(f"      excerpt: {fragment.text[:180]}")

    print("  candidate knowledge:")
    print(f"    title: {knowledge.title}")
    print(f"    sources: {len(knowledge.sources)}")
    print("    status: CANDIDATE — NOT VALIDATED")


def run() -> None:
    """Run the semantic granularity probe for the selected legal scope."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    source_repository = SqlAlchemySourceRepository(session_factory)

    try:
        source = import_pdf_source(SAMPLES_DIR / CALL_DOCUMENT, source_repository)
        programmes = discover_programmes(source)
        mentions = discover_requirements(source, PdfRequirementDiscoveryStrategy())
        programme, unit = _find_target(programmes)

        print(f"=== {CALL_DOCUMENT} ===")
        print(f"PROGRAMMES: {len(programmes)}")
        print(f"REQUIREMENT MENTIONS: {len(mentions)}")
        print("\nCANONICAL KNOWLEDGE CONSTRUCTION — SEMANTIC GRANULARITY")
        print("The call defines a broad study scope; this experiment manually")
        print("decomposes it into provisional teachable knowledge needs and")
        print("maps each need to authoritative canonical provisions.")
        print("No coverage is claimed: this is a granularity and evidence probe.")

        print(f"\nPROGRAMME {programme.identifier} — {programme.title}")
        print(f"STUDY UNIT: {unit.number}. {unit.title}")
        print(f"CALL SOURCE SPAN: pages {unit.start_page}-{unit.end_page}")

        print("\nCANONICAL LEGAL SOURCE")
        for key in ("title", "identifier", "authority", "locator"):
            print(f"  {key}: {CANONICAL_SOURCE[key]}")

        articles = _extract_articles(_fetch_canonical_text())
        print(f"  extracted article provisions: {len(articles)}")

        print("\nPROVISIONAL SCOPE DECOMPOSITION")
        print(f"  study unit -> {len(PROVISIONAL_NEEDS)} knowledge needs")

        resolved_needs = []
        for index, provisional_need in enumerate(PROVISIONAL_NEEDS, start=1):
            evidence = _resolve_evidence(provisional_need, articles)
            knowledge_need, knowledge = _build_candidate_knowledge(
                provisional_need, evidence
            )
            resolved_needs.append((provisional_need, knowledge_need, knowledge, evidence))
            _print_need(index, provisional_need, knowledge_need, knowledge, evidence)

        print("\nBOUNDARY OBSERVATIONS")
        print("  1. One programme unit is too broad to act as one useful learning unit.")
        print("  2. Each provisional need maps to a coherent group of canonical provisions.")
        print("  3. The mapping is semantic and scope-driven, not based on keyword frequency.")
        print("  4. Canonical articles provide evidence, but their raw text is not yet")
        print("     candidate-facing study content.")
        print("  5. The candidate Knowledge model can represent each provisional unit,")
        print("     but cannot yet retain the evidence mapping used by this experiment.")
        print("  6. KnowledgeNeed.depth remains undefined as a meaningful learning-depth")
        print("     contract; depth=1 is retained only to exercise the current model.")

        print("\nEXPERIMENT CONCLUSION")
        print("  Study Scope -> Knowledge Need: EVIDENCE OF USEFUL DECOMPOSITION")
        print("  Knowledge Need -> canonical evidence: WORKS FOR THIS CLOSED CORPUS")
        print("  Canonical evidence -> candidate Knowledge: PARTIAL")
        print("  Candidate Knowledge -> study-ready content: NOT YET TESTED")
        print("  Coverage: NOT ESTABLISHED")
        print("\nEXPERIMENT STATUS: GRANULARITY EVIDENCE COLLECTED — MODEL EXTENSION NOT YET IMPLEMENTED")
    finally:
        engine.dispose()


if __name__ == "__main__":
    run()
