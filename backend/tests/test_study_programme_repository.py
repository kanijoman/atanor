from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.models import StudyProgramme
from app.persistence.database import Base
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


def test_list_by_call_orders_programmes_by_identifier_sequence() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    repository = SqlAlchemyStudyProgrammeRepository(session_factory)
    call_id = uuid4()

    try:
        for identifier in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"):
            repository.save(
                StudyProgramme(
                    call_id=call_id,
                    identifier=identifier,
                    title=f"ANEXO {identifier}",
                )
            )

        programmes = repository.list_by_call(call_id)

        assert [programme.identifier for programme in programmes] == [
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
    finally:
        engine.dispose()
