"""Where study material comes from: curated text or acquired authoritative articles."""

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Protocol

from app.application.normative_source import (
    HttpSourceRetriever,
    NormativeArticle,
    NormativeSourceCandidate,
    SourceRetriever,
    extract_articles,
)
from app.domain.models import Source

_CONTENT_DIR = Path(__file__).parent / "content"


class MaterialOrigin(StrEnum):
    """How the study material was produced."""

    CURATED = "curated"  # written by Atanor or an expert from open-domain knowledge
    ACQUIRED = "acquired"  # extracted from an authoritative source


class ReviewStatus(StrEnum):
    """Whether a person qualified in the subject has validated the material."""

    UNREVIEWED = "unreviewed"
    REVIEWED = "reviewed"


@dataclass(frozen=True)
class MaterialProvenance:
    origin: MaterialOrigin
    review_status: ReviewStatus


class MaterialUnavailableError(Exception):
    """The material for a topic could not be produced right now."""


class MaterialProvider(Protocol):
    @property
    def provenance(self) -> MaterialProvenance: ...

    @property
    def sources(self) -> tuple[Source, ...]: ...

    def description(self, retriever: SourceRetriever | None) -> str:
        """Return the study text; `retriever` is used only by acquiring providers."""
        ...


@dataclass(frozen=True)
class CuratedMaterial:
    """Study text written by Atanor, stored under `content/`, citing reference sources."""

    content_file: str
    sources: tuple[Source, ...]
    provenance: MaterialProvenance = MaterialProvenance(
        MaterialOrigin.CURATED, ReviewStatus.UNREVIEWED
    )

    def description(self, retriever: SourceRetriever | None) -> str:
        return (_CONTENT_DIR / self.content_file).read_text(encoding="utf-8")


@dataclass(frozen=True)
class ArticleSection:
    """One required aspect and the articles of the source that develop it."""

    aspect: str
    articles: tuple[int, ...]


@dataclass(frozen=True)
class AcquiredNormativeMaterial:
    """Study text assembled from the articles of an authoritative normative source.

    Each section is titled with the aspect it develops, so coverage can be
    derived from the text actually acquired. The aspect-to-article mapping is an
    explicit contract that still needs expert review.
    """

    candidate: NormativeSourceCandidate
    sections: tuple[ArticleSection, ...]
    provenance: MaterialProvenance = MaterialProvenance(
        MaterialOrigin.ACQUIRED, ReviewStatus.UNREVIEWED
    )

    @property
    def sources(self) -> tuple[Source, ...]:
        return (self.candidate.source,)

    def description(self, retriever: SourceRetriever | None) -> str:
        retriever = retriever or HttpSourceRetriever()
        try:
            retrieved = retriever.retrieve(self.candidate)
        except OSError as exc:
            raise MaterialUnavailableError(
                f"Could not retrieve {self.candidate.identifier} from {self.candidate.authority}"
            ) from exc

        numbers = tuple(number for section in self.sections for number in section.articles)
        by_identifier = {
            article.identifier: article for article in extract_articles(retrieved, numbers)
        }
        rendered = [
            _render_section(index, section, by_identifier)
            for index, section in enumerate(self.sections, start=1)
        ]
        text = "\n\n".join(section for section in rendered if section)
        if not text:
            raise MaterialUnavailableError(
                f"No article of {self.candidate.identifier} could be extracted"
            )
        return text


def _render_section(
    index: int, section: ArticleSection, articles: dict[str, NormativeArticle]
) -> str:
    found = [
        articles[f"Artículo {number}"]
        for number in section.articles
        if f"Artículo {number}" in articles
    ]
    if not found:
        return ""
    # Indented so article paragraphs ("1. ...") are never mistaken for section headings.
    body = "\n".join(f"  {a.identifier}. {a.title}\n  {a.content}".rstrip() for a in found)
    return f"{index}. {section.aspect}\n{body}"
