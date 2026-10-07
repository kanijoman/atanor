"""Description of one supported study topic."""

from collections.abc import Callable
from dataclasses import dataclass

from app.application.study_material.providers import MaterialProvider
from app.domain.models import Knowledge

TitleMatcher = Callable[[str], bool]
CoverageStrategy = Callable[[Knowledge, tuple[str, ...]], tuple[str, ...]]


@dataclass(frozen=True)
class StudyTopic:
    """A knowledge topic Atanor can prepare study material for.

    `matches` decides whether a (casefolded) programme unit title refers to this
    topic, `provider` produces the material (curated or acquired) and
    `covered_aspects` decides which required aspects that material covers.
    """

    name: str
    matches: TitleMatcher
    provider: MaterialProvider
    required_aspects: tuple[str, ...]
    covered_aspects: CoverageStrategy
