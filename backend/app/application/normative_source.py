import re
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Protocol
from urllib.request import Request, urlopen

from app.domain.models import Knowledge, Source


@dataclass(frozen=True)
class KnowledgeComparison:
    matched_aspects: tuple[str, ...]
    missing_aspects: tuple[str, ...]


@dataclass(frozen=True)
class NormativeSourceCandidate:
    source: Source
    authority: str
    identifier: str


@dataclass(frozen=True)
class RetrievedSource:
    candidate: NormativeSourceCandidate
    content: str


class NormativeSourceResolver(Protocol):
    def resolve(self, text: str) -> NormativeSourceCandidate | None: ...


class SourceRetriever(Protocol):
    def retrieve(self, candidate: NormativeSourceCandidate) -> RetrievedSource: ...


class OfficialNormativeSourceCatalog:
    """Resolve supported normative references to authoritative source locators."""

    _ENTRIES = (
        (
            (
                "ley 39/2015",
                "procedimiento administrativo comun",
                "procedimiento administrativo común",
            ),
            NormativeSourceCandidate(
                source=Source(
                    title=(
                        "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo "
                        "Común de las Administraciones Públicas"
                    ),
                    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
                ),
                authority="BOE",
                identifier="BOE-A-2015-10565",
            ),
        ),
        (
            (
                "ley 19/2013",
                "transparencia",
                "acceso a la informacion publica",
                "acceso a la información pública",
            ),
            NormativeSourceCandidate(
                source=Source(
                    title=(
                        "Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la "
                        "información pública y buen gobierno"
                    ),
                    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
                ),
                authority="BOE",
                identifier="BOE-A-2013-12887",
            ),
        ),
    )

    def resolve(self, text: str) -> NormativeSourceCandidate | None:
        normalized_text = _normalize(text)
        for aliases, candidate in self._ENTRIES:
            if any(_normalize(alias) in normalized_text for alias in aliases):
                return candidate
        return None


class HttpSourceRetriever:
    """Retrieve authoritative source content without knowing its content in advance."""

    def __init__(self, timeout: float = 20.0) -> None:
        self._timeout = timeout

    def retrieve(self, candidate: NormativeSourceCandidate) -> RetrievedSource:
        if candidate.source.locator is None:
            raise ValueError("Normative source must have a locator")

        request = Request(
            candidate.source.locator,
            headers={"User-Agent": "Atanor/0.1"},
        )
        with urlopen(request, timeout=self._timeout) as response:
            content = response.read().decode(response.headers.get_content_charset() or "utf-8")

        return RetrievedSource(candidate=candidate, content=content)


@dataclass(frozen=True)
class NormativeArticle:
    identifier: str
    title: str
    content: str


class _ElementParser(HTMLParser):
    """Collect (tag, normalized text) pairs for every element of an HTML document."""

    def __init__(self) -> None:
        super().__init__()
        self.current_tag: str | None = None
        self.current_text: list[str] = []
        self.elements: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.current_tag = tag
        self.current_text = []

    def handle_endtag(self, tag: str) -> None:
        if self.current_tag == tag:
            text = " ".join("".join(self.current_text).split())
            if text:
                self.elements.append((tag, text))
            self.current_tag = None
            self.current_text = []

    def handle_data(self, data: str) -> None:
        if self.current_tag is not None:
            self.current_text.append(data)


_ANY_ARTICLE_HEADING = re.compile(r"^Artículo\s+\d+(?:\.|\s)", re.IGNORECASE)
_BODY_TAGS = {"p", "div", "li"}


def _find_article_start(elements: list[tuple[str, str]], article_number: int) -> int | None:
    marker = re.compile(rf"^Artículo\s+{article_number}(?:\.|\s)", re.IGNORECASE)
    return next((index for index, (_, text) in enumerate(elements) if marker.match(text)), None)


def _collect_article_body(elements: list[tuple[str, str]]) -> str:
    body: list[str] = []
    for tag, text in elements:
        if _ANY_ARTICLE_HEADING.match(text):
            break
        if tag in _BODY_TAGS:
            body.append(text)
    return " ".join(body)


def extract_article(retrieved: RetrievedSource, article_number: int) -> NormativeArticle | None:
    """Extract one article from the HTML representation of a normative source."""
    parser = _ElementParser()
    parser.feed(retrieved.content)

    start = _find_article_start(parser.elements, article_number)
    if start is None:
        return None

    heading = parser.elements[start][1]
    title = heading.split(".", 1)[1].strip() if "." in heading else ""
    return NormativeArticle(
        identifier=f"Artículo {article_number}",
        title=title,
        content=_collect_article_body(parser.elements[start + 1 :]),
    )


def extract_articles(
    retrieved: RetrievedSource,
    article_numbers: tuple[int, ...],
) -> tuple[NormativeArticle, ...]:
    """Extract multiple articles from the same normative source."""
    return tuple(
        article
        for article_number in article_numbers
        if (article := extract_article(retrieved, article_number)) is not None
    )


def reconstruct_knowledge_from_articles(
    retrieved: RetrievedSource,
    articles: tuple[NormativeArticle, ...],
) -> Knowledge:
    """Build Knowledge from multiple extracted articles of one normative source."""
    if not articles:
        raise ValueError("At least one normative article is required")

    description = "\n\n".join(
        f"{article.identifier}. {article.title}\n{article.content}".strip() for article in articles
    )
    return Knowledge(
        title=retrieved.candidate.source.title,
        description=description,
        sources=(retrieved.candidate.source,),
    )


def compare_knowledge_content(
    acquired: Knowledge,
    reference_aspects: tuple[str, ...],
) -> KnowledgeComparison:
    """Compare acquired content with explicit reference aspects."""
    reference_phrases = reference_aspects
    matched: list[str] = []
    missing: list[str] = []
    normalized_acquired = _normalize(acquired.description or "")

    for phrase in reference_phrases:
        normalized_phrase = _normalize(phrase)
        if normalized_phrase in normalized_acquired:
            matched.append(phrase)
        else:
            missing.append(phrase)

    return KnowledgeComparison(
        matched_aspects=tuple(matched),
        missing_aspects=tuple(missing),
    )


def reconstruct_knowledge_from_article(
    retrieved: RetrievedSource,
    article: NormativeArticle,
) -> Knowledge:
    """Build a Knowledge candidate directly from an extracted normative article."""
    return Knowledge(
        title=article.title or article.identifier,
        description=article.content,
        sources=(retrieved.candidate.source,),
    )


def acquire_normative_source(
    text: str,
    resolver: NormativeSourceResolver,
    retriever: SourceRetriever,
) -> RetrievedSource:
    """Resolve and retrieve an authoritative normative source."""
    candidate = resolver.resolve(text)
    if candidate is None:
        raise ValueError("No supported normative source could be identified")

    return retriever.retrieve(candidate)


def _normalize(value: str) -> str:
    return " ".join(value.casefold().split())
