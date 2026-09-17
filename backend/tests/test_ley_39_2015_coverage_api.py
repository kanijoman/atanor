from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.models import Call, Source, StudyProgramme, StudyProgrammeUnit
from app.main import app
from app.persistence.database import Base
from app.persistence.models.call import Call as PersistenceCall
from app.persistence.models.source import Source as PersistenceSource
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


class StudyCoverageApiDatabase:
    def __init__(self, database_path: Path) -> None:
        self.engine = create_engine(f"sqlite:///{database_path}")
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def close(self) -> None:
        self.engine.dispose()


def _seed_ley_39_2015_programme_unit(
    database: StudyCoverageApiDatabase,
) -> tuple[StudyProgramme, StudyProgrammeUnit]:
    source = Source(title="Synthetic call", locator="synthetic-call.pdf")
    call = Call(title="Synthetic call", source_id=source.id)
    unit = StudyProgrammeUnit(
        number=11,
        title="Las Leyes del Procedimiento Administrativo Común de las Administraciones",
        start_page=16,
        start_order=830,
        end_page=16,
        end_order=834,
    )
    programme = StudyProgramme(
        call_id=call.id,
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
        session.add(
            PersistenceCall(
                id=call.id,
                source_id=call.source_id,
                title=call.title,
            )
        )
        session.commit()

    SqlAlchemyStudyProgrammeRepository(database.session_factory).save(programme)
    return programme, unit


def test_get_ley_39_2015_study_material_exposes_coverage_summary(
    tmp_path, monkeypatch
) -> None:
    database = StudyCoverageApiDatabase(tmp_path / "api.db")
    programme, unit = _seed_ley_39_2015_programme_unit(database)
    monkeypatch.setattr("app.api.study.SessionLocal", database.session_factory)
    client = TestClient(app)

    response = client.get(f"/api/study/units/{unit.id}")

    assert response.status_code == 200
    assert response.json()["coverage"] == {
        "status": "partial",
        "covered_count": 2,
        "required_count": 8,
        "coverage_percentage": 25,
        "covered_aspects": [
            "Objeto y finalidad del procedimiento administrativo común",
            "Ámbito subjetivo de aplicación",
        ],
        "pending_aspects": [
            "Interesados, capacidad, representación y derechos",
            "Actividad administrativa, plazos y medios electrónicos",
            "Actos administrativos: requisitos, eficacia e invalidez",
            "Procedimiento administrativo común y sus fases",
            "Procedimientos sancionador y de responsabilidad patrimonial",
            "Revisión de actos, recursos, iniciativa legislativa y potestad reglamentaria",
        ],
    }
    database.close()
