"""Programme discovery for BOJA calls (`II.x. PROGRAMA DE MATERIAS` with `Tema N` items)."""

import re

from app.application.study_programmes.strategy import TEMA_PATTERN, build_programme_units
from app.application.study_programmes.text_units import TextUnit
from app.domain.models import Call, StudyProgramme

_HEADER = re.compile(
    r"^(?P<identifier>II\.(?:1|[A-Z]))\.\s+(?P<title>PROGRAMA DE MATERIAS.*)$",
    re.IGNORECASE,
)


def _headers(units: list[TextUnit]) -> list[tuple[int, re.Match[str]]]:
    return [
        (index, match)
        for index, unit in enumerate(units)
        if (match := _HEADER.fullmatch(unit.text))
    ]


def _programme_title(units: list[TextUnit], header_index: int, next_header: int, title: str) -> str:
    """Join the header title with its continuation line, when there is one."""
    following = header_index + 1
    has_continuation = following < next_header and not TEMA_PATTERN.fullmatch(units[following].text)
    continuation = units[following].text if has_continuation else ""
    return " ".join(part for part in (title, continuation) if part)


class BojaProgrammeDiscoveryStrategy:
    def matches(self, units: list[TextUnit]) -> bool:
        return bool(_headers(units))

    def discover(self, call: Call, units: list[TextUnit]) -> list[StudyProgramme]:
        headers = _headers(units)
        programmes = []
        for header_index, match in headers:
            next_header = next((index for index, _ in headers if index > header_index), len(units))
            tema_indices = [
                index
                for index in range(header_index + 1, next_header)
                if TEMA_PATTERN.fullmatch(units[index].text)
            ]
            if not tema_indices:
                continue
            programmes.append(
                StudyProgramme(
                    call_id=call.id,
                    identifier=match.group("identifier"),
                    title=_programme_title(units, header_index, next_header, match.group("title")),
                    units=build_programme_units(units, tema_indices, TEMA_PATTERN, next_header),
                )
            )
        return programmes
