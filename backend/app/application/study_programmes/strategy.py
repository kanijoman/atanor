"""Contract and shared helpers for provider-specific programme discovery."""

import re
from collections.abc import Sequence
from typing import Protocol

from app.application.study_programmes.text_units import TextUnit, unit_span
from app.domain.models import Call, StudyProgramme, StudyProgrammeUnit

TEMA_PATTERN = re.compile(r"^Tema\s+(\d+)\s*[.\-–—]\s*(.*)$", re.IGNORECASE)


class ProgrammeDiscoveryStrategy(Protocol):
    """Discovers study programmes in one family of official document layouts."""

    def matches(self, units: list[TextUnit]) -> bool:
        """Return whether the document follows this strategy's layout."""
        ...

    def discover(self, call: Call, units: list[TextUnit]) -> list[StudyProgramme]:
        """Extract the study programmes of a document that `matches`."""
        ...


def build_programme_units(
    units: list[TextUnit],
    starts: Sequence[int],
    pattern: re.Pattern[str],
    final_end: int,
    section_starts: Sequence[int] = (),
) -> tuple[StudyProgrammeUnit, ...]:
    """Build numbered programme units spanning from each start to the next boundary.

    A unit ends at the next start, at the first section start after it, or at
    `final_end`, whichever comes first. `pattern` captures (number, title).
    """
    programme_units = []
    for position, start in enumerate(starts):
        boundaries = [starts[position + 1] if position + 1 < len(starts) else final_end]
        boundaries.extend(index for index in section_starts if index > start)
        match = pattern.fullmatch(units[start].text)
        if match is None:
            raise ValueError(f"Programme unit marker does not match: {units[start].text!r}")
        programme_units.append(
            unit_span(units, start, min(boundaries), int(match.group(1)), match.group(2).strip())
        )
    return tuple(programme_units)
