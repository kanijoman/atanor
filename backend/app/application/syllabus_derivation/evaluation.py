"""Benchmark: how much of the hand-made topic mappings can be recovered automatically.

The reference ("gold") sections are the aspect-to-article mappings written by hand in the
study-material topics. They are not an expert's judgement and they list key articles rather
than every relevant one, so recall is the meaningful measure and precision is not reported.
"""

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

from app.application.normative_source import (
    NormativeSourceCandidate,
    SourceRetriever,
)
from app.application.normative_source.structure import Law, parse_law
from app.application.study_material.providers import AcquiredNormativeMaterial
from app.application.study_material.topic import StudyTopic
from app.application.syllabus_derivation.retrieval import rank_divisions

WELL_COVERED_RECALL = 0.8
DEFAULT_TOP_DIVISIONS = 2


@dataclass(frozen=True)
class GoldSection:
    """An aspect of a topic and the articles of one law a person chose for it."""

    topic: str
    aspect: str
    law: NormativeSourceCandidate
    articles: tuple[int, ...]


@dataclass(frozen=True)
class SectionResult:
    gold: GoldSection
    selected: tuple[int, ...]

    @property
    def recall(self) -> float:
        wanted = set(self.gold.articles)
        return len(wanted & set(self.selected)) / len(wanted) if wanted else 1.0


@dataclass(frozen=True)
class EvaluationReport:
    top_divisions: int
    results: tuple[SectionResult, ...]

    @property
    def mean_recall(self) -> float:
        return sum(r.recall for r in self.results) / max(len(self.results), 1)

    @property
    def well_covered(self) -> int:
        return sum(r.recall >= WELL_COVERED_RECALL for r in self.results)

    @property
    def mean_selected(self) -> float:
        return sum(len(r.selected) for r in self.results) / max(len(self.results), 1)

    @property
    def missed(self) -> tuple[SectionResult, ...]:
        return tuple(r for r in self.results if r.recall == 0)


def gold_sections(topics: Iterable[StudyTopic]) -> list[GoldSection]:
    """Every (aspect, law, articles) mapping of the topics acquired from normative sources."""
    sections: list[GoldSection] = []
    for topic in topics:
        provider = topic.provider
        if not isinstance(provider, AcquiredNormativeMaterial):
            continue
        for section in provider.sections:
            sections.extend(
                GoldSection(topic.name, section.aspect, reference.source, reference.articles)
                for reference in provider.references(section)
            )
    return sections


def load_laws(gold: Sequence[GoldSection], retriever: SourceRetriever) -> dict[str, Law]:
    """Retrieve and parse each law the gold sections refer to, once."""
    laws: dict[str, Law] = {}
    for section in gold:
        identifier = section.law.identifier
        if identifier not in laws:
            laws[identifier] = parse_law(identifier, retriever.retrieve(section.law))
    return laws


def select_articles(law: Law, query: str, top_divisions: int) -> tuple[int, ...]:
    """The articles of the `top_divisions` titles/chapters that best match `query`."""
    ranked = rank_divisions(law, query)[:top_divisions]
    return tuple(number for item in ranked for number in item.division.article_numbers)


def evaluate(
    laws: Mapping[str, Law],
    gold: Sequence[GoldSection],
    top_divisions: int = DEFAULT_TOP_DIVISIONS,
) -> EvaluationReport:
    results = tuple(
        SectionResult(
            section, select_articles(laws[section.law.identifier], section.aspect, top_divisions)
        )
        for section in gold
    )
    return EvaluationReport(top_divisions=top_divisions, results=results)


def format_report(report: EvaluationReport) -> str:
    total = len(report.results)
    lines = [
        f"Sections evaluated: {total} (top {report.top_divisions} titles/chapters per aspect)",
        f"Mean recall of the hand-made articles: {report.mean_recall:.2f}",
        f"Sections with recall >= {WELL_COVERED_RECALL}: {report.well_covered}/{total}",
        f"Mean articles selected per section: {report.mean_selected:.1f}",
        f"Sections where no hand-made article was found: {len(report.missed)}",
    ]
    lines.extend(f"  - {r.gold.topic} | {r.gold.aspect}" for r in report.missed)
    return "\n".join(lines)
