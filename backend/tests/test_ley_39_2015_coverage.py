from app.application.study_material import derive_required_aspects_for_programme_unit
from app.domain.models import StudyProgrammeUnit


def test_defines_required_aspects_for_ley_39_2015_procedure_scope() -> None:
    programme_unit = StudyProgrammeUnit(
        number=11,
        title="Las Leyes del Procedimiento Administrativo Común de las Administraciones",
        start_page=16,
        start_order=830,
        end_page=16,
        end_order=834,
    )

    aspects = derive_required_aspects_for_programme_unit(programme_unit)

    assert aspects == (
        "Objeto y finalidad del procedimiento administrativo común",
        "Ámbito subjetivo de aplicación",
        "Interesados, capacidad, representación y derechos",
        "Actividad administrativa, plazos y medios electrónicos",
        "Actos administrativos: requisitos, eficacia e invalidez",
        "Procedimiento administrativo común y sus fases",
        "Procedimientos sancionador y de responsabilidad patrimonial",
        "Revisión de actos, recursos, iniciativa legislativa y potestad reglamentaria",
    )
