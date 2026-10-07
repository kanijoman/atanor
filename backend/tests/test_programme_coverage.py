from uuid import uuid4

from app.application.programme_coverage import ProgrammeCoverage, summarize_programme_coverage
from app.domain.models import StudyProgramme, StudyProgrammeUnit


def _unit(number: int, title: str) -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=number, title=title, start_page=1, start_order=1, end_page=1, end_order=2
    )


def test_programme_coverage_counts_units_that_have_study_material() -> None:
    programme = StudyProgramme(
        call_id=uuid4(),
        identifier="I",
        title="Programme",
        units=(
            _unit(
                1, "La Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información"
            ),
            _unit(2, "El modelo TCP/IP y el modelo de referencia de interconexión de sistemas"),
            _unit(3, "La protección de datos personales y su régimen jurídico"),
        ),
    )

    assert summarize_programme_coverage(programme) == ProgrammeCoverage(
        units_total=3, units_with_material=2
    )


def test_an_empty_programme_has_no_coverage() -> None:
    programme = StudyProgramme(call_id=uuid4(), identifier="I", title="Programme")

    assert summarize_programme_coverage(programme) == ProgrammeCoverage(0, 0)
