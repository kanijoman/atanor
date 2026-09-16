from app.application.study_material import derive_knowledge_needs_for_programme_unit
from app.domain.models import StudyProgrammeUnit


def test_reuses_the_same_knowledge_need_identity_across_real_programme_units() -> None:
    programme_units = (
        StudyProgrammeUnit(
            number=11,
            title="Las Leyes del Procedimiento Administrativo Común de las Administraciones",
            start_page=16,
            start_order=830,
            end_page=16,
            end_order=834,
        ),
        StudyProgrammeUnit(
            number=3,
            title="Las Leyes del Procedimiento Administrativo Común de las Administraciones",
            start_page=27,
            start_order=1412,
            end_page=27,
            end_order=1417,
        ),
        StudyProgrammeUnit(
            number=2,
            title="Las Leyes del Procedimiento Administrativo Común de las Administraciones",
            start_page=35,
            start_order=1821,
            end_page=35,
            end_order=1824,
        ),
    )

    needs = tuple(
        derive_knowledge_needs_for_programme_unit(unit)
        for unit in programme_units
    )

    assert len({unit.id for unit in programme_units}) == 3
    assert all(len(unit_needs) == 1 for unit_needs in needs)
    assert {unit_needs[0].identity_key for unit_needs in needs} == {
        ("Procedimiento administrativo común", 1)
    }
