"""Okapi BM25 ranking of the divisions (titles and chapters) of a law against a query."""

import math
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from app.application.normative_source.structure import Law, LawDivision
from app.application.syllabus_derivation.text import tokens

# The headings of a title or chapter describe its subject better than any single article,
# so their words count several times.
HEADING_WEIGHT = 4
_K1 = 1.4
_B = 0.75


class Bm25Index:
    """BM25 over pre-tokenised documents."""

    def __init__(self, documents: Sequence[Sequence[str]]) -> None:
        self._documents = documents
        self._frequencies = [Counter(document) for document in documents]
        count = len(documents)
        self._average_length = sum(len(d) for d in documents) / max(count, 1)
        document_frequency = Counter(term for document in documents for term in set(document))
        self._idf = {
            term: math.log(1 + (count - n + 0.5) / (n + 0.5))
            for term, n in document_frequency.items()
        }

    def score(self, query: Sequence[str], index: int) -> float:
        frequencies = self._frequencies[index]
        length_norm = 1 - _B + _B * len(self._documents[index]) / max(self._average_length, 1)
        return sum(
            self._idf[term]
            * frequencies[term]
            * (_K1 + 1)
            / (frequencies[term] + _K1 * length_norm)
            for term in query
            if term in frequencies
        )

    def rank(self, query: Sequence[str]) -> list[tuple[int, float]]:
        """Document indexes with their score, best first; ties keep document order."""
        scored = [(index, self.score(query, index)) for index in range(len(self._documents))]
        return sorted(scored, key=lambda item: (-item[1], item[0]))


@dataclass(frozen=True)
class RankedDivision:
    division: LawDivision
    score: float


def _division_document(law: Law, division: LawDivision) -> list[str]:
    body = " ".join(
        f"{law.articles[number].title} {law.articles[number].content}"
        for number in division.article_numbers
    )
    return tokens(division.heading) * HEADING_WEIGHT + tokens(body)


def rank_divisions(law: Law, query: str) -> list[RankedDivision]:
    """The titles and chapters of `law`, ordered by how well they match `query`."""
    index = Bm25Index([_division_document(law, division) for division in law.divisions])
    return [
        RankedDivision(law.divisions[position], score)
        for position, score in index.rank(tokens(query))
    ]
