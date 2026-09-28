from app.application.study_material import derive_knowledge_needs_for_programme_unit
from app.domain.models import StudyProgrammeUnit


def real_data_modeling_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=12,
        title=(
            "Modelos de datos. Entidades, atributos y relaciones. "
            "Modelo relacional. Normalización."
        ),
        start_page=86779,
        start_order=1,
        end_page=86779,
        end_order=2,
    )


def test_derives_knowledge_need_for_real_data_modeling_programme_unit() -> None:
    programme_unit = real_data_modeling_programme_unit()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)

    assert len(needs) == 1
    assert needs[0].topic == "Modelado de datos"
    assert needs[0].depth == 1
    assert needs[0].identity_key == ("Modelado de datos", 1)
