from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_session_factory
from app.application.call_import import import_call_from_pdf
from app.main import app
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import Base
from app.persistence.source_repository import SqlAlchemySourceRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository

SAMPLES = Path(__file__).parent / "samples"


def test_imported_call_and_programmes_are_available_through_calls_api() -> None:
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

    imported_call = import_call_from_pdf(
        SAMPLES / "BOE-A-2024-14098.pdf",
        source_repository,
        call_repository,
        programme_repository,
    )

    app.dependency_overrides[get_session_factory] = lambda: session_factory
    try:
        client = TestClient(app)
        call_response = client.get("/api/calls")
        programmes_response = client.get(f"/api/calls/{imported_call.id}/programmes")
    finally:
        app.dependency_overrides.clear()
        engine.dispose()

    assert call_response.status_code == 200
    assert call_response.json() == [
        {
            "id": str(imported_call.id),
            "title": "BOE-A-2024-14098.pdf",
        }
    ]

    assert programmes_response.status_code == 200
    programmes = programmes_response.json()
    assert len(programmes) == 10
    assert [programme["identifier"] for programme in programmes] == [
        "I",
        "II",
        "III",
        "IV",
        "V",
        "VI",
        "VII",
        "VIII",
        "IX",
        "X",
    ]
