"""Extraction of numbered articles from the HTML of a normative source."""

import re
from dataclasses import dataclass
from html.parser import HTMLParser

from app.application.normative_source.retrieval import RetrievedSource


@dataclass(frozen=True)
class NormativeArticle:
    identifier: str
    title: str
    content: str


_BLOCK_TAGS = frozenset(
    {"h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "li", "blockquote", "td", "th", "tr"}
)
_BODY_TAGS = frozenset({"p", "div", "li", "blockquote"})
_HEADING_TAGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
_NOISE = re.compile(r"^(?:Subir|\[Bloque \d+: [^\]]*\])$")


class _ElementParser(HTMLParser):
    """Collect (block tag, normalized text) pairs.

    Text of inline elements (links, emphasis, spans) belongs to the enclosing
    block, so a paragraph containing a link is a single element.
    """

    def __init__(self) -> None:
        super().__init__()
        self.elements: list[tuple[str, str]] = []
        self._block: str | None = None
        self._text: list[str] = []

    def _flush(self) -> None:
        text = " ".join("".join(self._text).split())
        if self._block is not None and text and not _NOISE.match(text):
            self.elements.append((self._block, text))
        self._text = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _BLOCK_TAGS:
            self._flush()
            self._block = tag
        elif tag == "br":
            self._text.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in _BLOCK_TAGS:
            self._flush()
            self._block = None

    def handle_data(self, data: str) -> None:
        if self._block is not None:
            self._text.append(data)


def _parse_elements(retrieved: RetrievedSource) -> list[tuple[str, str]]:
    parser = _ElementParser()
    parser.feed(retrieved.content)
    parser.close()
    return parser.elements


def _find_article_start(elements: list[tuple[str, str]], article_number: int) -> int | None:
    """Index of the heading of an article.

    Only headings count: gazette pages also list every article in a navigation
    index, and articles may be titled `Artículo 1` or `Artículo 1. Objeto.`
    """
    marker = re.compile(rf"^Artículo\s+{article_number}(?:\.|\s|$)", re.IGNORECASE)
    return next(
        (
            index
            for index, (tag, text) in enumerate(elements)
            if tag in _HEADING_TAGS and marker.match(text)
        ),
        None,
    )


def _collect_article_body(elements: list[tuple[str, str]]) -> str:
    body: list[str] = []
    for tag, text in elements:
        if tag in _HEADING_TAGS:
            break
        if tag in _BODY_TAGS:
            body.append(text)
    return " ".join(body)


def _build_article(elements: list[tuple[str, str]], article_number: int) -> NormativeArticle | None:
    start = _find_article_start(elements, article_number)
    if start is None:
        return None

    heading = elements[start][1]
    title = heading.split(".", 1)[1].strip() if "." in heading else ""
    return NormativeArticle(
        identifier=f"Artículo {article_number}",
        title=title,
        content=_collect_article_body(elements[start + 1 :]),
    )


def extract_article(retrieved: RetrievedSource, article_number: int) -> NormativeArticle | None:
    """Extract one article from the HTML representation of a normative source."""
    return _build_article(_parse_elements(retrieved), article_number)


def extract_articles(
    retrieved: RetrievedSource,
    article_numbers: tuple[int, ...],
) -> tuple[NormativeArticle, ...]:
    """Extract several articles, parsing the document only once."""
    elements = _parse_elements(retrieved)
    return tuple(
        article
        for number in article_numbers
        if (article := _build_article(elements, number)) is not None
    )
