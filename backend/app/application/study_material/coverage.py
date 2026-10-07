"""Candidate-facing study coverage: summary contract and reusable strategies."""

import re
from dataclasses import dataclass

from app.application.study_material.topic import CoverageStrategy
from app.domain.models import Knowledge, KnowledgeNeed


@dataclass(frozen=True)
class StudyCoverageSummary:
    """Candidate-facing summary of the current study coverage."""

    knowledge_need: str
    status: str
    required_aspects: tuple[str, ...]
    covered_aspects: tuple[str, ...]
    pending_aspects: tuple[str, ...]
    covered_count: int
    required_count: int
    coverage_percentage: float


def _status(covered_count: int, required_count: int) -> str:
    if covered_count == 0:
        return "missing"
    if covered_count == required_count:
        return "covered"
    return "partial"


def build_study_coverage_summary(
    knowledge_need: KnowledgeNeed,
    required_aspects: tuple[str, ...],
    covered_aspects: tuple[str, ...],
) -> StudyCoverageSummary:
    required_count = len(required_aspects)
    covered_count = len(covered_aspects)
    return StudyCoverageSummary(
        knowledge_need=knowledge_need.topic,
        status=_status(covered_count, required_count),
        required_aspects=required_aspects,
        covered_aspects=covered_aspects,
        pending_aspects=tuple(a for a in required_aspects if a not in covered_aspects),
        covered_count=covered_count,
        required_count=required_count,
        coverage_percentage=(covered_count / required_count) * 100 if required_count else 0.0,
    )


_SECTION_HEADING = re.compile(r"^\d+\.\s+(?P<heading>.+)$")
MIN_SECTION_WORDS = 15


def _sections(text: str) -> dict[str, str]:
    """Split numbered-section text into {casefolded heading: body}."""
    sections: dict[str, list[str]] = {}
    current: list[str] | None = None
    for line in text.splitlines():
        heading = _SECTION_HEADING.match(line)
        if heading:
            current = sections.setdefault(heading.group("heading").casefold(), [])
        elif current is not None:
            current.append(line)
    return {heading: " ".join(body).strip() for heading, body in sections.items()}


def _heading_names_aspect(heading: str, aspect: str) -> bool:
    normalized_aspect = aspect.casefold()
    return heading in normalized_aspect or normalized_aspect in heading


def aspects_covered_by_sections(
    knowledge: Knowledge, required_aspects: tuple[str, ...]
) -> tuple[str, ...]:
    """An aspect is covered when the material has a section for it with real content.

    A section names an aspect when its heading and the aspect contain one another
    (case-insensitively); an empty or token section is not evidence of coverage.
    """
    sections = _sections(knowledge.description or "")
    return tuple(
        aspect
        for aspect in required_aspects
        if any(
            _heading_names_aspect(heading, aspect) and len(body.split()) >= MIN_SECTION_WORDS
            for heading, body in sections.items()
        )
    )


def aspects_covered_by_signals(
    signals: tuple[tuple[str, tuple[str, ...]], ...],
) -> CoverageStrategy:
    """Build a strategy covering an aspect when all of its signal terms appear in the text."""

    def strategy(knowledge: Knowledge, _required_aspects: tuple[str, ...]) -> tuple[str, ...]:
        content = (knowledge.description or "").casefold()
        return tuple(aspect for aspect, terms in signals if all(term in content for term in terms))

    return strategy
