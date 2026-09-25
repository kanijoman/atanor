from dataclasses import dataclass
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


def extract_article(retrieved: RetrievedSource, article_number: int) -> NormativeArticle | None:
    """Extract one article from the HTML representation of a normative source."""
    from html.parser import HTMLParser
    import re

    class _ArticleParser(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.headings: list[tuple[str, str]] = []
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

    parser = _ArticleParser()
    parser.feed(retrieved.content)

    marker = re.compile(
        rf"^Artículo\s+{article_number}(?:\.|\s)",
        re.IGNORECASE,
    )
    start = next(
        (
            index
            for index, (_, text) in enumerate(parser.elements)
            if marker.match(text)
        ),
        None,
    )
    if start is None:
        return None

    heading = parser.elements[start][1]
    title = heading.split(".", 1)[1].strip() if "." in heading else ""
    body: list[str] = []
    for tag, text in parser.elements[start + 1 :]:
        if re.match(r"^Artículo\s+\d+(?:\.|\s)", text, re.IGNORECASE):
            break
        if tag in {"p", "div", "li"}:
            body.append(text)

    return NormativeArticle(
        identifier=f"Artículo {article_number}",
        title=title,
        content=" ".join(body),
    )
def compare_knowledge_content(
    acquired: Knowledge,
    reference: str,
) -> KnowledgeComparison:
    """Compare acquired content with reference aspects using explicit phrases."""
    reference_phrases = (
        phrase.strip()
        for phrase in reference.split(".")
        if phrase.strip()
    )
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
