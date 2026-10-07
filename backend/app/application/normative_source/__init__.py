"""Acquisition of authoritative normative sources (catalog, retrieval, articles)."""

from app.application.normative_source.articles import (
    NormativeArticle,
    extract_article,
    extract_articles,
)
from app.application.normative_source.catalog import (
    CONSTITUCION_ESPANOLA,
    LEY_7_1985,
    LEY_19_2013,
    LEY_39_2015,
    LEY_40_2015,
    LEY_50_1997,
    NormativeSourceCandidate,
    NormativeSourceResolver,
    OfficialNormativeSourceCatalog,
)
from app.application.normative_source.knowledge import (
    KnowledgeComparison,
    compare_knowledge_content,
    reconstruct_knowledge_from_article,
    reconstruct_knowledge_from_articles,
)
from app.application.normative_source.retrieval import (
    HttpSourceRetriever,
    RetrievedSource,
    SourceRetriever,
    acquire_normative_source,
)

__all__ = [
    "CONSTITUCION_ESPANOLA",
    "LEY_7_1985",
    "LEY_19_2013",
    "LEY_39_2015",
    "LEY_40_2015",
    "LEY_50_1997",
    "HttpSourceRetriever",
    "KnowledgeComparison",
    "NormativeArticle",
    "NormativeSourceCandidate",
    "NormativeSourceResolver",
    "OfficialNormativeSourceCatalog",
    "RetrievedSource",
    "SourceRetriever",
    "acquire_normative_source",
    "compare_knowledge_content",
    "extract_article",
    "extract_articles",
    "reconstruct_knowledge_from_article",
    "reconstruct_knowledge_from_articles",
]
