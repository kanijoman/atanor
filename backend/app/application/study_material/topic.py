"""Description of one supported study topic."""

from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from app.domain.models import Knowledge, Source

_CONTENT_DIR = Path(__file__).parent / "content"

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

    @cached_property
    def content(self) -> str:
        return (_CONTENT_DIR / self.content_file).read_text(encoding="utf-8")
