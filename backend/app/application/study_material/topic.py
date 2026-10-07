"""Description of one supported study topic."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from functools import cached_property
from pathlib import Path

from app.domain.models import Knowledge, Source

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


TitleMatcher = Callable[[str], bool]
CoverageStrategy = Callable[[Knowledge, tuple[str, ...]], tuple[str, ...]]


@dataclass(frozen=True)
class StudyTopic:
    """A knowledge topic Atanor can prepare study material for.

    `matches` decides whether a (casefolded) programme unit title refers to this
    topic, `content_file` names the curated study text under `content/`, and
    `covered_aspects` decides which required aspects the material covers.
    """

    name: str
    matches: TitleMatcher
    content_file: str
    sources: tuple[Source, ...]
    required_aspects: tuple[str, ...]
    covered_aspects: CoverageStrategy
    provenance: MaterialProvenance = MaterialProvenance(
        MaterialOrigin.CURATED, ReviewStatus.UNREVIEWED
    )

    @cached_property
    def content(self) -> str:
        return (_CONTENT_DIR / self.content_file).read_text(encoding="utf-8")
