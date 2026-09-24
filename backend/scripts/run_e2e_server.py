from __future__ import annotations

import os
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
E2E_DATABASE = BACKEND_ROOT / "e2e.db"

os.environ["DATABASE_URL"] = f"sqlite:///{E2E_DATABASE.as_posix()}"

if E2E_DATABASE.exists():
    E2E_DATABASE.unlink()

from app.application.call_import import import_call_from_pdf
from app.main import app
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import Base, engine, SessionLocal
from app.persistence.source_repository import SqlAlchemySourceRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository
import uvicorn


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
    uvicorn.run(app, host="127.0.0.1", port=8000)
