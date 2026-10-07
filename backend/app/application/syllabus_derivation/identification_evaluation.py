"""Benchmark: does law identification find the laws the hand-made topics were built on?"""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from app.application.call_discovery import discover_calls
from app.application.study_material.registry import TOPICS, find_topic_for_title
from app.application.study_material.topic import StudyTopic
from app.application.study_programmes import discover_programmes
from app.application.syllabus_derivation.evaluation import gold_sections
from app.application.syllabus_derivation.identify import identify_laws
from app.domain.models import Source


@dataclass(frozen=True)
class UnitIdentification:
    title: str
    expected: frozenset[str]  # law identifiers used by the hand-made topic
    found: frozenset[str]

    @property
    def missing(self) -> frozenset[str]:
        return self.expected - self.found

    @property
    def extra(self) -> frozenset[str]:
        return self.found - self.expected


def unit_titles(pdf_path: Path) -> list[str]:
    source = Source(title=pdf_path.name, locator=str(pdf_path))
    calls = discover_calls(source)
    return [
        unit.title
        for call in calls
        for programme in discover_programmes(call, source)
        for unit in programme.units
    ]


def _expected_laws(topics: Iterable[StudyTopic]) -> dict[str, frozenset[str]]:
    laws: dict[str, set[str]] = {}
    for section in gold_sections(topics):
        laws.setdefault(section.topic, set()).add(section.law.identifier)
    return {topic: frozenset(identifiers) for topic, identifiers in laws.items()}


def evaluate_identification(titles: Sequence[str]) -> list[UnitIdentification]:
    """Units that a hand-made acquired topic supports, with the laws found for their title."""
    expected = _expected_laws(TOPICS)
    results = []
    for title in titles:
        topic = find_topic_for_title(title)
        if topic is not None and topic.name in expected:
            found = identify_laws(title).identifiers
            results.append(UnitIdentification(title, expected[topic.name], found))
    return results


def format_identification_report(results: Sequence[UnitIdentification]) -> str:
    expected = sum(len(item.expected) for item in results)
    found = sum(len(item.expected & item.found) for item in results)
    lines = [
        f"Units with a hand-made acquired topic: {len(results)}",
        f"Laws of the hand-made topics found: {found}/{expected}",
        f"Units where every expected law was found: {sum(not r.missing for r in results)}",
        f"Extra laws identified (not used by the hand-made topic): "
        f"{sum(len(r.extra) for r in results)}",
    ]
    lines.extend(f"  - missing {sorted(r.missing)} | {r.title[:70]}" for r in results if r.missing)
    return "\n".join(lines)
