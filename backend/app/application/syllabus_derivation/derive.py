"""Derive, for one syllabus aspect, the articles of a law that develop it.

The result is reproducible (same law and wording, same articles) and explainable: it is the
text of the titles and chapters whose headings and articles best match the aspect. An aspect
that matches nothing is reported as unresolved, never filled with a guess.
"""

from dataclasses import dataclass

from app.application.normative_source.structure import Law
from app.application.syllabus_derivation.retrieval import RankedDivision, rank_divisions

# Divisions are added in rank order while they score at least this share of the best one.
RELATIVE_SCORE = 0.5
MAX_DIVISIONS = 6
# A section longer than this is no longer a focused reading for one aspect.
MAX_ARTICLES = 25


@dataclass(frozen=True)
class DerivedSection:
    aspect: str
    articles: tuple[int, ...]

    @property
    def resolved(self) -> bool:
        return bool(self.articles)


def _matching_divisions(law: Law, aspect: str) -> list[RankedDivision]:
    ranked = rank_divisions(law, aspect)[:MAX_DIVISIONS]
    if not ranked or ranked[0].score <= 0:
        return []
    return [item for item in ranked if item.score >= RELATIVE_SCORE * ranked[0].score]


def derive_section(law: Law, aspect: str) -> DerivedSection:
    articles: list[int] = []
    for item in _matching_divisions(law, aspect):
        numbers = item.division.article_numbers
        if articles and len(articles) + len(numbers) > MAX_ARTICLES:
            continue
        articles.extend(numbers)
    return DerivedSection(aspect, tuple(articles))
