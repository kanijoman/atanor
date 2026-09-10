from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.models import Source, StudyProgramme, StudyProgrammeUnit
from app.main import app
from app.persistence.database import Base
from app.persistence.models.source import Source as PersistenceSource
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


class TestDatabase:
    def __init__(self, database_path: Path) -> None:
        self.engine = create_engine(f"sqlite:///{database_path}")
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def close(self) -> None:
        self.engine.dispose()


def _seed_programme(database: TestDatabase) -> tuple[StudyProgramme, StudyProgrammeUnit]:
    source = Source(title="Synthetic call", locator="synthetic-call.pdf")
    unit = StudyProgrammeUnit(
        number=1,
        title="Derecho de acceso a la información pública",
        start_page=1,
        start_order=1,
        end_page=2,
        end_order=2,
    )
    programme = StudyProgramme(
        source_id=source.id,
        identifier="I",
        title="Programa oficial",
        units=(unit,),
    )

    with database.session_factory() as session:
        session.add(
            PersistenceSource(
                id=source.id,
                title=source.title,
                locator=source.locator,
            )
        )
        session.commit()

    SqlAlchemyStudyProgrammeRepository(database.session_factory).save(programme)
    return programme, unit


def test_list_programmes_returns_candidate_selectable_programmes(tmp_path, monkeypatch) -> None:
    database = TestDatabase(tmp_path / "api.db")
    programme, _ = _seed_programme(database)
    monkeypatch.setattr("app.api.study.SessionLocal", database.session_factory)
    client = TestClient(app)

    response = client.get("/api/study/programmes")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(programme.id),
            "identifier": "I",
            "title": "Programa oficial",
        }
    ]
    database.close()


def test_get_programme_returns_units_for_candidate_selection(tmp_path, monkeypatch) -> None:
    database = TestDatabase(tmp_path / "api.db")
    programme, unit = _seed_programme(database)
    monkeypatch.setattr("app.api.study.SessionLocal", database.session_factory)
    client = TestClient(app)

    response = client.get(f"/api/study/programmes/{programme.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": str(programme.id),
        "identifier": "I",
        "title": "Programa oficial",
        "units": [
            {
                "id": str(unit.id),
                "number": 1,
                "title": "Derecho de acceso a la información pública",
            }
        ],
    }
    database.close()


def test_get_programme_returns_not_found_for_unknown_programme(tmp_path, monkeypatch) -> None:
    database = TestDatabase(tmp_path / "api.db")
    monkeypatch.setattr("app.api.study.SessionLocal", database.session_factory)
    client = TestClient(app)

    response = client.get(f"/api/study/programmes/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Study programme not found"}
    database.close()
