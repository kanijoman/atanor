from app.application.study_material import derive_knowledge_needs_for_programme_unit
from app.domain.models import StudyProgrammeUnit


def real_personal_data_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=7,
        title=(
            "La protección de datos personales y su régimen jurídico: "
            "principios, derechos y obligaciones. Derechos digitales."
        ),
        start_page=86778,
        start_order=3,
        end_page=86778,
        end_order=4,
    )


def test_derives_knowledge_need_for_real_personal_data_programme_unit() -> None:
    programme_unit = real_personal_data_programme_unit()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)

    assert len(needs) == 1
    assert needs[0].topic == "Protección de datos personales"
    assert needs[0].depth == 1
    assert needs[0].identity_key == ("Protección de datos personales", 1)
