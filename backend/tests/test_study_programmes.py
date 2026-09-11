import re
from pathlib import Path

import pytest

from app.application.study_programmes import (
    BoeProgrammeDiscoveryStrategy,
    _extract_units,
    discover_programmes,
)
from app.domain.models import Call, Source
from app.persistence.database import Base
from app.persistence.models.call import Call as PersistenceCall
from app.persistence.models.source import Source as PersistenceSource
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SAMPLES = Path(__file__).parent / "samples"


def source(name: str) -> Source:
    return Source(title=name, locator=str(SAMPLES / name))


def call_for(source_document: Source) -> Call:
    return Call(title=f"Call for {source_document.title}", source_id=source_document.id)


def test_discovers_boja_programmes() -> None:
    source_document = source("BOJA24-138-00046-48048-01_00304998.pdf")
    call = call_for(source_document)
    programmes = discover_programmes(call, source_document)

    assert len(programmes) == 7
    assert [programme.identifier for programme in programmes] == [
        "II.1", "II.A", "II.B", "II.C", "II.D", "II.E", "II.F",
    ]
    assert len(programmes[0].units) == 30
    assert len(programmes[1].units) == 39
    assert programmes[1].units[0].number == 1
    assert programmes[1].units[-1].number == 40
    assert all(programme.call_id == call.id for programme in programmes)


def test_discovers_boe_programmes() -> None:
    source_document = source("BOE-A-2024-14098.pdf")
    call = call_for(source_document)
    programmes = discover_programmes(call, source_document)

    assert len(programmes) == 10
    assert [programme.identifier for programme in programmes] == [
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    ]
    assert all(programme.units for programme in programmes)
    assert all(programme.call_id == call.id for programme in programmes)


def test_discovery_rejects_a_call_from_another_source() -> None:
    source_document = source("BOE-A-2024-14098.pdf")
    unrelated_source = source("Programa_Archiveros_0.pdf")

    with pytest.raises(ValueError, match="Call source does not match the supplied source"):
        discover_programmes(call_for(unrelated_source), source_document)


def test_boe_units_do_not_cross_section_boundaries() -> None:
    source_document = source("BOE-A-2024-14098.pdf")
    units = _extract_units(source_document)
    programmes = discover_programmes(call_for(source_document), source_document)
    section_header = re.compile(r"^[IVXLCDM]+\.\s+.+$")
    section_orders = {
        unit.order
        for unit in units
        if section_header.fullmatch(unit.text)
    }

    assert section_orders

    for programme in programmes:
        for unit in programme.units:
            crossed_sections = [
                order
                for order in section_orders
                if unit.start_order < order <= unit.end_order
            ]
            assert not crossed_sections, (
                f"Programme {programme.identifier} unit {unit.number} "
                f"crosses section boundary at order(s) {crossed_sections}"
            )


def test_discovers_archiveros_programme() -> None:
    source_document = source("Programa_Archiveros_0.pdf")
    call = call_for(source_document)
    programmes = discover_programmes(call, source_document)

    assert len(programmes) == 1
    assert programmes[0].identifier == "I"
    assert len(programmes[0].units) == 25
    assert programmes[0].units[0].number == 1
    assert programmes[0].units[-1].number == 25
    assert programmes[0].call_id == call.id


def test_repository_round_trip() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    repository = SqlAlchemyStudyProgrammeRepository(session_factory)
    source_document = source("Programa_Archiveros_0.pdf")
    call = call_for(source_document)
    programme = discover_programmes(call, source_document)[0]
    persisted_source = PersistenceSource(
        id=source_document.id,
        title=source_document.title,
        locator=source_document.locator,
    )
    persisted_call = PersistenceCall(
        id=call.id,
        source_id=call.source_id,
        title=call.title,
    )
    with session_factory() as session:
        session.add(persisted_source)
        session.add(persisted_call)
        session.commit()

    saved = repository.save(programme)
    loaded = repository.get_by_id(saved.id)

    assert loaded == saved
    assert loaded is not None
    assert loaded.call_id == call.id
    assert loaded.units[0].start_page == 1
    assert loaded.units[-1].end_page == 2

    engine.dispose()
