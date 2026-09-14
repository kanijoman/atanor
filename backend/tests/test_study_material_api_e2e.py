from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api import study
from app.application.call_import import import_call_from_pdf
from app.main import app
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import Base
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository
from app.persistence.source_repository import SqlAlchemySourceRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


SAMPLES = Path(__file__).parent / "samples"


def test_selected_programme_unit_exposes_candidate_study_material() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    source_repository = SqlAlchemySourceRepository(session_factory)
    call_repository = SqlAlchemyCallRepository(session_factory)
    programme_repository = SqlAlchemyStudyProgrammeRepository(session_factory)
    knowledge_repository = SqlAlchemyKnowledgeRepository(session_factory)

    imported_call = import_call_from_pdf(
        SAMPLES / "BOE-A-2024-14098.pdf",
        source_repository,
        call_repository,
        programme_repository,
    )
    programmes = programme_repository.list_by_call(imported_call.id)
    unit = next(
        unit
        for programme in programmes
        for unit in programme.units
        if "ley 19/2013" in unit.title.casefold()
        and "transparencia" in unit.title.casefold()
    )

    original_session_local = study.SessionLocal
    original_knowledge_repository = study.SqlAlchemyKnowledgeRepository
    study.SessionLocal = session_factory
    study.SqlAlchemyKnowledgeRepository = lambda _: knowledge_repository
    try:
        client = TestClient(app)
        response = client.get(f"/api/study/units/{unit.id}")
    finally:
        study.SessionLocal = original_session_local
        study.SqlAlchemyKnowledgeRepository = original_knowledge_repository
        engine.dispose()

    assert response.status_code == 200
    assert response.json()["programme_unit"] == {
        "id": str(unit.id),
        "number": unit.number,
        "title": unit.title,
    }
    assert response.json()["knowledge_need"] == {
        "title": "Derecho de acceso a la información pública",
    }
    assert "Artículo 12" in response.json()["study_material"]
