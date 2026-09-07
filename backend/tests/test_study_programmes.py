from pathlib import Path

from app.application.study_programmes import discover_programmes
from app.domain.models import Source
from app.persistence.database import Base
from app.persistence.models.source import Source as PersistenceSource
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SAMPLES = Path(__file__).parent / "samples"


def source(name: str) -> Source:
    return Source(title=name, locator=str(SAMPLES / name))


def test_discovers_boja_programmes() -> None:
    programmes = discover_programmes(source("BOJA24-138-00046-48048-01_00304998.pdf"))

    assert len(programmes) == 7
    assert [programme.identifier for programme in programmes] == [
        "II.1", "II.A", "II.B", "II.C", "II.D", "II.E", "II.F",
    ]
    assert len(programmes[0].units) == 30
    assert len(programmes[1].units) == 39
    assert programmes[1].units[0].number == 1
    assert programmes[1].units[-1].number == 40


def test_discovers_boe_programmes() -> None:
    programmes = discover_programmes(source("BOE-A-2024-14098.pdf"))

    assert len(programmes) == 10
    assert [programme.identifier for programme in programmes] == [
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    ]
    assert all(programme.units for programme in programmes)


def test_discovers_archiveros_programme() -> None:
    programmes = discover_programmes(source("Programa_Archiveros_0.pdf"))

    assert len(programmes) == 1
    assert programmes[0].identifier == "I"
    assert len(programmes[0].units) == 25
    assert programmes[0].units[0].number == 1
    assert programmes[0].units[-1].number == 25


def test_repository_round_trip() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    repository = SqlAlchemyStudyProgrammeRepository(session_factory)
    programme = discover_programmes(source("Programa_Archiveros_0.pdf"))[0]
    persisted_source = PersistenceSource(
        id=programme.source_id,
        title="Programa_Archiveros_0.pdf",
    )
    with session_factory() as session:
        session.add(persisted_source)
        session.commit()

    saved = repository.save(programme)
    loaded = repository.get_by_id(saved.id)

    assert loaded == saved
    assert loaded is not None
    assert loaded.source_id == programme.source_id
    assert loaded.units[0].start_page == 1
    assert loaded.units[-1].end_page == 2

    engine.dispose()
