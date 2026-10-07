from dataclasses import replace
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.study_material.registry import find_topic_for_title
from app.application.study_material.wording import leading_statement
from app.application.study_programmes import discover_programmes
from app.application.study_programmes.strategy import is_page_noise
from app.domain.models import Call, Source, StudyProgramme
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import Base
from app.persistence.source_repository import SqlAlchemySourceRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository

SAMPLES = Path(__file__).parent / "samples"


def _programmes(name: str) -> list[StudyProgramme]:
    document = Source(title=name, locator=str(SAMPLES / name))
    call = Call(title=name, source_id=document.id)
    return discover_programmes(call, document)


@pytest.fixture(scope="module")
def auxiliar_agb() -> StudyProgramme:
    """Annex I of the BOE call: Cuerpo General Auxiliar de la Administración del Estado."""
    return next(p for p in _programmes("BOE-A-2024-14098.pdf") if p.identifier == "I")


def test_programme_keeps_the_two_blocks_that_restart_numbering(auxiliar_agb) -> None:
    sections = [unit.section for unit in auxiliar_agb.units]

    assert len(auxiliar_agb.units) == 28
    assert sections.count("I. Organización pública") == 16
    assert sections.count("II. Actividad administrativa y ofimática") == 12
    first_of_second_block = next(u for u in auxiliar_agb.units if u.section.startswith("II."))
    assert first_of_second_block.number == 1


def test_unit_keeps_its_complete_official_wording(auxiliar_agb) -> None:
    constitution = auxiliar_agb.units[0]

    assert constitution.title == (
        "La Constitución Española de 1978. Características. Los principios constitucionales "
        "y los valores superiores. Derechos y deberes fundamentales. Su garantía y suspensión."
    )


def test_page_headers_and_footers_do_not_leak_into_the_wording(auxiliar_agb) -> None:
    for unit in auxiliar_agb.units:
        for noise in ("BOLETÍN OFICIAL", "cve:", "Verificable", "Núm. 166"):
            assert noise not in unit.title


def test_the_last_unit_of_an_annex_stops_before_the_next_annex(auxiliar_agb) -> None:
    last = auxiliar_agb.units[-1]

    assert last.title.endswith("Funcionalidades básicas de los navegadores web.")
    assert "ANEXO II" not in last.title


def test_boja_wording_is_complete_and_free_of_gazette_noise() -> None:
    programme = next(p for p in _programmes("BOJA24-138-00046-48048-01_00304998.pdf"))
    first = programme.units[0]

    assert first.title.endswith("El procedimiento de reforma constitucional.")
    assert "Boletín Oficial de la Junta de Andalucía" not in first.title
    assert "BOJABOJA" not in first.title
    assert first.section is None


def test_archiveros_wording_is_complete() -> None:
    [programme] = _programmes("Programa_Archiveros_0.pdf")

    assert programme.units[0].title == (
        "La Constitución Española (I): estructura. Contenidos de los títulos: "
        "preliminar, I, IV y VIII."
    )


@pytest.mark.parametrize(
    "line",
    [
        "BOLETÍN OFICIAL DEL ESTADO",
        "Núm. 166 Miércoles 10 de julio de 2024 Sec. II.B. Pág. 86754",
        "cve: BOE-A-2024-14098",
        "Verificable en https://www.boe.es",
        "Número 138 - Miércoles, 17 de julio de 2024",
        "página 48048/21",
        "00304998",
    ],
)
def test_gazette_page_furniture_is_recognised_as_noise(line: str) -> None:
    assert is_page_noise(line)


def test_programme_wording_is_not_mistaken_for_noise() -> None:
    assert not is_page_noise("garantía y suspensión.")


def test_leading_statement_is_the_first_sentence_of_the_wording() -> None:
    wording = "La Ley 19/2013, de 9 de diciembre, de transparencia. La Agenda 2030 y los ODS."

    assert leading_statement(wording) == "La Ley 19/2013, de 9 de diciembre, de transparencia."
    assert leading_statement(wording.casefold()).startswith("la ley 19/2013")
    assert leading_statement("Un solo enunciado") == "Un solo enunciado"


def test_a_later_mention_of_a_law_does_not_make_the_unit_that_law() -> None:
    employment_statute = (
        "El texto refundido del Estatuto Básico del Empleo Público y demás normativa de "
        "aplicación: derechos y deberes. La Ley 19/2013, de 9 de diciembre, de transparencia, "
        "acceso a la información pública y buen gobierno."
    )

    assert find_topic_for_title(employment_statute) is None


def test_a_law_listed_second_does_not_make_a_unit_data_protection() -> None:
    patient_law = (
        "Ley básica reguladora de la autonomía del paciente. El derecho de información. "
        "Ley Orgánica de Protección de Datos Personales y garantía de los derechos digitales."
    )

    assert find_topic_for_title(patient_law) is None


def test_the_procedure_unit_is_recognised_from_its_complete_wording(auxiliar_agb) -> None:
    unit = next(u for u in auxiliar_agb.units if u.title.startswith("Las Leyes del Procedimiento"))

    topic = find_topic_for_title(unit.title)

    assert topic is not None
    assert topic.name.startswith("Las Leyes del Procedimiento Administrativo Común y del Régimen")


def test_persisted_units_keep_document_order_when_numbering_restarts(tmp_path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'order.db'}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    try:
        document = Source(title="boe", locator="boe.pdf")
        SqlAlchemySourceRepository(session_factory).save(document)
        call = SqlAlchemyCallRepository(session_factory).save(
            Call(title="boe", source_id=document.id)
        )
        programme = next(p for p in _programmes("BOE-A-2024-14098.pdf") if p.identifier == "I")
        repository = SqlAlchemyStudyProgrammeRepository(session_factory)
        repository.save(replace(programme, call_id=call.id))

        [stored] = [p for p in repository.list_by_call(call.id) if p.identifier == "I"]

        sections = [unit.section for unit in stored.units]
        assert sections == [unit.section for unit in programme.units]
        assert [unit.number for unit in stored.units[:17]] == [*range(1, 17), 1]
    finally:
        engine.dispose()
