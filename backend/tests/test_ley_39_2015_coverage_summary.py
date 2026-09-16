from app.application.study_material import (
    build_study_coverage_summary,
    derive_covered_aspects,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import Knowledge, KnowledgeNeed, Source, StudyProgrammeUnit


def test_builds_candidate_facing_coverage_summary_for_ley_39_2015() -> None:
    programme_unit = StudyProgrammeUnit(
        number=11,
        title="Las Leyes del Procedimiento Administrativo Común de las Administraciones",
        start_page=16,
        start_order=830,
        end_page=16,
        end_order=834,
    )
    knowledge_need = KnowledgeNeed(
        topic="Procedimiento administrativo común",
        depth=1,
    )
    knowledge = Knowledge(
        title="Procedimiento administrativo común",
        description=(
            "1. Objeto de la ley\n"
            "La Ley 39/2015 establece las bases del procedimiento administrativo común.\n\n"
            "2. Ámbito subjetivo de aplicación\n"
            "La ley se aplica al sector público."
        ),
        sources=(
            Source(
                title="Ley 39/2015",
                locator="https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
            ),
        ),
    )

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)

    summary = build_study_coverage_summary(
        knowledge_need=knowledge_need,
        required_aspects=required_aspects,
        covered_aspects=covered_aspects,
    )

    assert summary.status == "partial"
    assert summary.covered_count == 2
    assert summary.required_count == 8
    assert summary.coverage_percentage == 25
    assert summary.covered_aspects == (
        "Objeto y finalidad del procedimiento administrativo común",
        "Ámbito subjetivo de aplicación",
    )
    assert summary.pending_aspects == (
        "Interesados, capacidad, representación y derechos",
        "Actividad administrativa, plazos y medios electrónicos",
        "Actos administrativos: requisitos, eficacia e invalidez",
        "Procedimiento administrativo común y sus fases",
        "Procedimientos sancionador y de responsabilidad patrimonial",
        "Revisión de actos, recursos, iniciativa legislativa y potestad reglamentaria",
    )
