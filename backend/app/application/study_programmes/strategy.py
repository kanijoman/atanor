"""Contract and shared helpers for provider-specific programme discovery."""

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from typing import Protocol

from app.application.study_programmes.text_units import TextUnit, unit_span
from app.domain.models import Call, StudyProgramme, StudyProgrammeUnit

TEMA_PATTERN = re.compile(r"^Tema\s+(\d+)\s*[.\-–—]+\s*(.*)$", re.IGNORECASE)

# Page headers and footers that official gazettes print in the middle of a programme.
_PAGE_NOISE = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^BOLET[ÍI]N OFICIAL DEL ESTADO$",
        r"^Núm\. \d+\b.*\bPág\. ?\d+",
        r"^cve: [A-Z]+-[A-Z]-\d{4}-\d+$",
        r"^Verificable en https?://\S+$",
        r"^Boletín Oficial de la Junta de Andalucía$",
        r"^Boletín Oficial de Castilla y León$",
        r"^BOJA(?:BOJA)*$",
        r"^Depósito Legal: .*ISSN: .*$",
        r"^https?://www\.juntadeandalucia\.es/\S*$",
        r"^Número \d+ - .+\d{4}$",
        r"^página \d+/\d+$",
        r"^\d{8}$",
    )
)


def is_page_noise(text: str) -> bool:
    return any(pattern.match(text) for pattern in _PAGE_NOISE)


class ProgrammeDiscoveryStrategy(Protocol):
    """Discovers study programmes in one family of official document layouts."""

    def matches(self, units: list[TextUnit]) -> bool:
        """Return whether the document follows this strategy's layout."""
        ...

    def discover(self, call: Call, units: list[TextUnit]) -> list[StudyProgramme]:
        """Extract the study programmes of a document that `matches`."""
        ...


def _unnamed(_start: int) -> None:
    return None


@dataclass(frozen=True)
class Sections:
    """Blocks of a programme (programmes may restart numbering in each block)."""

    starts: Sequence[int] = ()
    name_of: Callable[[int], str | None] = _unnamed


NO_SECTIONS = Sections()


def _official_wording(units: list[TextUnit], start: int, end: int, first_line: str) -> str:
    """The unit's full wording: its first line plus continuation lines, without page noise."""
    parts = [first_line.strip()]
    parts.extend(unit.text for unit in units[start + 1 : end] if not is_page_noise(unit.text))
    return " ".join(" ".join(parts).split())


def build_programme_units(
    units: list[TextUnit],
    starts: Sequence[int],
    pattern: re.Pattern[str],
    final_end: int,
    sections: Sections = NO_SECTIONS,
) -> tuple[StudyProgrammeUnit, ...]:
    """Build numbered programme units spanning from each start to the next boundary.

    A unit ends at the next start, at the first section start after it, or at
    `final_end`, whichever comes first. `pattern` captures (number, title); the
    unit keeps its complete official wording, and `section_of` names the block it
    belongs to (programmes can restart numbering in each block).
    """
    programme_units = []
    for position, start in enumerate(starts):
        boundaries = [starts[position + 1] if position + 1 < len(starts) else final_end]
        boundaries.extend(index for index in sections.starts if index > start)
        end = min(boundaries)
        match = pattern.fullmatch(units[start].text)
        if match is None:
            raise ValueError(f"Programme unit marker does not match: {units[start].text!r}")
        unit = unit_span(
            units,
            start,
            end,
            int(match.group(1)),
            _official_wording(units, start, end, match.group(2)),
        )
        programme_units.append(replace(unit, section=sections.name_of(start)))
    return tuple(programme_units)
