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
class ArticleRef:
    """Articles of one law."""

    source: NormativeSourceCandidate
    articles: tuple[int, ...]


@dataclass(frozen=True)
class ArticleSection:
    """One required aspect and the articles that develop it.

    `articles` belong to the material's own source unless `source` says otherwise;
    `also` adds articles of other laws when an aspect spans several of them.
    """

    aspect: str
    articles: tuple[int, ...]
    source: NormativeSourceCandidate | None = None
    also: tuple[ArticleRef, ...] = ()


@dataclass(frozen=True)
class AcquiredNormativeMaterial:
    """Study text assembled from the articles of authoritative normative sources.

    Each section is titled with the aspect it develops, so coverage can be
    derived from the text actually acquired. The aspect-to-article mapping is an
    explicit contract that still needs expert review. When the material draws on
    more than one law, every article is labelled with the law it comes from.
    """

    candidate: NormativeSourceCandidate
    sections: tuple[ArticleSection, ...]
    provenance: MaterialProvenance = MaterialProvenance(
        MaterialOrigin.ACQUIRED, ReviewStatus.UNREVIEWED
    )

    def references(self, section: ArticleSection) -> tuple[ArticleRef, ...]:
        own = ArticleRef(section.source or self.candidate, section.articles)
        return (own, *section.also)

    def _candidates(self) -> tuple[NormativeSourceCandidate, ...]:
        unique = {
            reference.source.identifier: reference.source
            for section in self.sections
            for reference in self.references(section)
        }
        return tuple(unique.values())

    @property
    def sources(self) -> tuple[Source, ...]:
        return tuple(candidate.source for candidate in self._candidates())

    def description(self, retriever: SourceRetriever | None) -> str:
        retriever = retriever or HttpSourceRetriever()
        candidates = self._candidates()
        articles = {
            candidate.identifier: self._acquire(candidate, retriever) for candidate in candidates
        }
        labelled = len(candidates) > 1
        rendered = [
            self._render(index, section, articles, labelled)
            for index, section in enumerate(self.sections, start=1)
        ]
        text = "\n\n".join(section for section in rendered if section)
        if not text:
            names = ", ".join(candidate.identifier for candidate in candidates)
            raise MaterialUnavailableError(f"No article of {names} could be extracted")
        return text

    def _acquire(
        self, candidate: NormativeSourceCandidate, retriever: SourceRetriever
    ) -> dict[str, NormativeArticle]:
        try:
            retrieved = retriever.retrieve(candidate)
        except OSError as exc:
            raise MaterialUnavailableError(
                f"Could not retrieve {candidate.identifier} from {candidate.authority}"
            ) from exc
        numbers = tuple(
            number
            for section in self.sections
            for reference in self.references(section)
            if reference.source.identifier == candidate.identifier
            for number in reference.articles
        )
        return {article.identifier: article for article in extract_articles(retrieved, numbers)}

    def _render(
        self,
        index: int,
        section: ArticleSection,
        articles: dict[str, dict[str, NormativeArticle]],
        labelled: bool,
    ) -> str:
        entries: list[str] = []
        for reference in self.references(section):
            law = reference.source if labelled else None
            by_identifier = articles[reference.source.identifier]
            for number in reference.articles:
                article = by_identifier.get(f"Artículo {number}")
                if article is not None:
                    # Indented so article paragraphs ("1. ...") never look like section headings.
                    entries.append(f"  {_heading(article, law)}\n  {article.content}".rstrip())
        if not entries:
            return ""
        return f"{index}. {section.aspect}\n" + "\n".join(entries)


def _heading(article: NormativeArticle, law: NormativeSourceCandidate | None) -> str:
    """`Artículo 12. Título.`, or just `Artículo 12.` for untitled articles (Constitution).

    The law's name is prefixed when the material draws on several laws.
    """
    heading = f"{article.identifier}. {article.title}".rstrip()
    return heading if law is None else f"{law.label or law.source.title}, {heading}"
