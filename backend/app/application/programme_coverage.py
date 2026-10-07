"""How much of a study programme Atanor can already prepare study material for."""

from dataclasses import dataclass

from app.application.study_material import is_study_material_available_for_programme_unit
from app.domain.models import StudyProgramme


@dataclass(frozen=True)
class ProgrammeCoverage:
    units_total: int
    units_with_material: int


def summarize_programme_coverage(programme: StudyProgramme) -> ProgrammeCoverage:
    return ProgrammeCoverage(
        units_total=len(programme.units),
        units_with_material=sum(
            is_study_material_available_for_programme_unit(unit) for unit in programme.units
        ),
    )
