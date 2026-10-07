"""Programme discovery for calls listing `Tema N` items without section headers."""

from app.application.study_programmes.strategy import TEMA_PATTERN, build_programme_units
from app.application.study_programmes.text_units import TextUnit
from app.domain.models import Call, StudyProgramme


def _tema_indices(units: list[TextUnit]) -> list[int]:
    return [index for index, unit in enumerate(units) if TEMA_PATTERN.fullmatch(unit.text)]


class ArchiverosProgrammeDiscoveryStrategy:
    def matches(self, units: list[TextUnit]) -> bool:
        return bool(_tema_indices(units))

    def discover(self, call: Call, units: list[TextUnit]) -> list[StudyProgramme]:
        temas = _tema_indices(units)
        if not temas:
            return []
        title = next(
            (
                unit.text
                for unit in reversed(units[: temas[0]])
                if "programa" in unit.text.casefold()
            ),
            "Study programme",
        )
        return [
            StudyProgramme(
                call_id=call.id,
                identifier="I",
                title=title,
                units=build_programme_units(units, temas, TEMA_PATTERN, len(units)),
            )
        ]
