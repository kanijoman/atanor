"""Programme discovery for BOE calls (`ANEXO` sections with a numbered `Programa.` block)."""

import re
from collections.abc import Callable

from app.application.study_programmes.strategy import Sections, build_programme_units
from app.application.study_programmes.text_units import TextUnit
from app.domain.models import Call, StudyProgramme

_ANNEX = re.compile(r"^ANEXO\s+([IVXLCDM]+)$", re.IGNORECASE)
_PROGRAMME = re.compile(r"^(\d+)\.\s+Programa\.$", re.IGNORECASE)
_TOP_LEVEL = re.compile(r"^(\d+)\.\s+(.+)$")
_SECTION = re.compile(r"^[IVXLCDM]+\.\s+.+$")
_NON_PROGRAMME_SECTION = re.compile(r"^(?:REQUISITOS|MÉRITOS)\b", re.IGNORECASE)


def _annexes(units: list[TextUnit]) -> list[tuple[int, str]]:
    return [
        (index, match.group(1).upper())
        for index, unit in enumerate(units)
        if (match := _ANNEX.fullmatch(unit.text))
    ]


def _is_programme_item(text: str) -> bool:
    match = _TOP_LEVEL.fullmatch(text)
    return match is not None and not _NON_PROGRAMME_SECTION.match(match.group(2))


def _indices_between(
    units: list[TextUnit], start: int, end: int, pattern: re.Pattern[str]
) -> list[int]:
    return [index for index in range(start, end) if pattern.fullmatch(units[index].text)]


def _section_namer(
    units: list[TextUnit], section_indices: list[int]
) -> Callable[[int], str | None]:
    """Name the block (`I. ...`, `II. ...`) a programme item belongs to."""

    def section_of(start: int) -> str | None:
        previous = [index for index in section_indices if index < start]
        return units[previous[-1]].text if previous else None

    return section_of


def _discover_annex(
    call: Call, units: list[TextUnit], annex_index: int, next_annex: int, identifier: str
) -> StudyProgramme | None:
    programme_index = next(
        iter(_indices_between(units, annex_index + 1, next_annex, _PROGRAMME)), None
    )
    if programme_index is None:
        return None
    first = programme_index + 1
    item_indices = [
        index for index in range(first, next_annex) if _is_programme_item(units[index].text)
    ]
    if not item_indices:
        return None
    section_indices = _indices_between(units, first, next_annex, _SECTION)
    return StudyProgramme(
        call_id=call.id,
        identifier=identifier,
        title=f"ANEXO {identifier}",
        units=build_programme_units(
            units,
            item_indices,
            _TOP_LEVEL,
            next_annex,
            Sections(section_indices, _section_namer(units, section_indices)),
        ),
    )


class BoeProgrammeDiscoveryStrategy:
    def matches(self, units: list[TextUnit]) -> bool:
        return any(_ANNEX.fullmatch(unit.text) for unit in units) and any(
            _PROGRAMME.fullmatch(unit.text) for unit in units
        )

    def discover(self, call: Call, units: list[TextUnit]) -> list[StudyProgramme]:
        annexes = _annexes(units)
        programmes = []
        for annex_index, identifier in annexes:
            next_annex = next((index for index, _ in annexes if index > annex_index), len(units))
            programme = _discover_annex(call, units, annex_index, next_annex, identifier)
            if programme is not None:
                programmes.append(programme)
        return programmes
