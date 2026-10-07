"""Knowledge candidates built from acquired normative articles."""

from dataclasses import dataclass

from app.application.normative_source.articles import NormativeArticle
from app.application.normative_source.catalog import normalize
from app.application.normative_source.retrieval import RetrievedSource
from app.domain.models import Knowledge


@dataclass(frozen=True)
class KnowledgeComparison:
    matched_aspects: tuple[str, ...]
    missing_aspects: tuple[str, ...]


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


def compare_knowledge_content(
    acquired: Knowledge,
    reference_aspects: tuple[str, ...],
) -> KnowledgeComparison:
    """Compare acquired content with explicit reference aspects."""
    normalized_acquired = normalize(acquired.description or "")
    matched = tuple(a for a in reference_aspects if normalize(a) in normalized_acquired)
    missing = tuple(a for a in reference_aspects if a not in matched)
    return KnowledgeComparison(matched_aspects=matched, missing_aspects=missing)
