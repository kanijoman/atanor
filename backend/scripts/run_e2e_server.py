from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
E2E_DATABASE = BACKEND_ROOT / "e2e.db"
E2E_UPLOADS = BACKEND_ROOT / "e2e-uploads"

os.environ["DATABASE_URL"] = f"sqlite:///{E2E_DATABASE.as_posix()}"
os.environ["UPLOADS_DIR"] = str(E2E_UPLOADS)

if E2E_DATABASE.exists():
    E2E_DATABASE.unlink()
shutil.rmtree(E2E_UPLOADS, ignore_errors=True)

import uvicorn

from app.api.dependencies import get_source_retriever
from app.application.call_import import import_call_from_pdf
from app.main import app
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import Base, SessionLocal, engine
from app.persistence.source_repository import SqlAlchemySourceRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository

sys.path.insert(0, str(BACKEND_ROOT / "tests"))
from support import FixtureSourceRetriever


def prepare_database() -> None:
    Base.metadata.create_all(engine)

    source_repository = SqlAlchemySourceRepository(SessionLocal)
    call_repository = SqlAlchemyCallRepository(SessionLocal)
    programme_repository = SqlAlchemyStudyProgrammeRepository(SessionLocal)

    import_call_from_pdf(
        BACKEND_ROOT / "tests" / "samples" / "BOE-A-2024-14098.pdf",
        source_repository,
        call_repository,
        programme_repository,
    )


if __name__ == "__main__":
    prepare_database()
    # Acquired study material is served from saved BOE pages: e2e needs no network.
    app.dependency_overrides[get_source_retriever] = FixtureSourceRetriever
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("E2E_BACKEND_PORT", "8000")))
