"""The structure of a law: its titles and chapters, and the articles each one contains."""

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from app.application.normative_source.articles import parse_blocks
from app.application.normative_source.retrieval import RetrievedSource

_HEADING_TAGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
_BODY_TAGS = frozenset({"p", "div", "li", "blockquote"})
_ARTICLE = re.compile(r"^Artículo\s+(\d+)\b\.?\s*(.*)$", re.IGNORECASE)
_TITLE_NUMBER = re.compile(r"^(?:T[ÍI]TULO|LIBRO)\b", re.IGNORECASE)
_CHAPTER_NUMBER = re.compile(r"^CAP[ÍI]TULO\b", re.IGNORECASE)
_SECTION = re.compile(r"^SECCI[ÓO]N\b", re.IGNORECASE)
_MAX_NAME_LENGTH = 160

# CSS classes the BOE gives to the headings of a consolidated law.
_BOE_TITLE_NUMBER = "titulo_num"
_BOE_TITLE_NAME = "titulo_tit"
_BOE_CHAPTER_NUMBER = "capitulo_num"
_BOE_CHAPTER_NAME = "capitulo_tit"


@dataclass(frozen=True)
class LawArticle:
    number: int
    title: str
    content: str


@dataclass(frozen=True)
class LawDivision:
    """A title and chapter of a law (the unit its headings describe) and its articles."""

    heading: str
    article_numbers: tuple[int, ...]


@dataclass(frozen=True)
class Law:
    identifier: str
    articles: Mapping[int, LawArticle] = field(default_factory=dict)
    divisions: tuple[LawDivision, ...] = ()

    def division_of(self, article_number: int) -> LawDivision | None:
        return next((d for d in self.divisions if article_number in d.article_numbers), None)


@dataclass
class _Builder:
    title: str = ""
    chapter: str = ""
    naming: str | None = None  # "title" or "chapter": the next plain heading names it
    order: list[tuple[str, str]] = field(default_factory=list)
    members: dict[tuple[str, str], list[int]] = field(default_factory=dict)
    articles: dict[int, tuple[str, list[str]]] = field(default_factory=dict)
    current: int | None = None

    def heading(self, text: str, css: str) -> None:
        self.current = None
        if css == _BOE_TITLE_NUMBER or (not css and _TITLE_NUMBER.match(text)):
            self.title, self.chapter, self.naming = text, "", "title"
        elif css == _BOE_TITLE_NAME:
            self.title = f"{self.title} {text}".strip()
        elif css == _BOE_CHAPTER_NUMBER or (not css and _CHAPTER_NUMBER.match(text)):
            self.chapter, self.naming = text, "chapter"
        elif css == _BOE_CHAPTER_NAME:
            self.chapter = f"{self.chapter} {text}".strip()
        elif not css and self.naming and len(text) <= _MAX_NAME_LENGTH:
            self._name(text)

    def _name(self, text: str) -> None:
        """Generic HTML: the short heading after `TÍTULO I` / `CAPÍTULO II` is its name."""
        if self.naming == "title":
            self.title = f"{self.title} {text}"
        else:
            self.chapter = f"{self.chapter} {text}"
        self.naming = None

    def article(self, number: int, title: str) -> None:
        key = (self.title, self.chapter)
        if key not in self.members:
            self.members[key] = []
            self.order.append(key)
        if number not in self.articles:
            self.articles[number] = (title, [])
            self.members[key].append(number)
        self.current = number

    def body(self, text: str) -> None:
        if self.current is not None:
            self.articles[self.current][1].append(text)


def parse_law(identifier: str, retrieved: RetrievedSource) -> Law:
    """Parse the HTML of a consolidated law into titles, chapters and articles.

    Works with the BOE's classed headings and, failing that, with plain headings
    such as `TÍTULO I`, `CAPÍTULO II` followed by their name. The first article
    heading of each number wins (navigation indexes are lists, not headings).
    """
    builder = _Builder()
    blocks, css_classes = parse_blocks(retrieved)
    for (tag, text), css in zip(blocks, css_classes, strict=True):
        if tag in _HEADING_TAGS:
            match = _ARTICLE.match(text)
            if match:
                builder.article(int(match.group(1)), match.group(2).strip())
            else:
                builder.heading(text, css)
        elif tag in _BODY_TAGS:
            builder.body(text)

    divisions = tuple(
        LawDivision(
            heading=" · ".join(part for part in key if part),
            article_numbers=tuple(builder.members[key]),
        )
        for key in builder.order
    )
    articles = MappingProxyType(
        {
            number: LawArticle(number, title, " ".join(body))
            for number, (title, body) in builder.articles.items()
        }
    )
    return Law(identifier=identifier, articles=articles, divisions=divisions)
