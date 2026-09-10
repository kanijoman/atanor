from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.persistence.database import SessionLocal
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


router = APIRouter(prefix="/api/study", tags=["study"])


@router.get("/programmes")
def list_programmes() -> list[dict[str, object]]:
    repository = SqlAlchemyStudyProgrammeRepository(SessionLocal)
    programmes = []
    for source in _list_sources():
        for programme in repository.list_by_source(source):
            programmes.append(
                {
                    "id": str(programme.id),
                    "identifier": programme.identifier,
                    "title": programme.title,
                }
            )
    return programmes


@router.get("/programmes/{programme_id}")
def get_programme(programme_id: UUID) -> dict[str, object]:
    repository = SqlAlchemyStudyProgrammeRepository(SessionLocal)
    programme = repository.get_by_id(programme_id)
    if programme is None:
        raise HTTPException(status_code=404, detail="Study programme not found")

    return {
        "id": str(programme.id),
        "identifier": programme.identifier,
        "title": programme.title,
        "units": [
            {
                "id": str(unit.id),
                "number": unit.number,
                "title": unit.title,
            }
            for unit in programme.units
        ],
    }


def _list_sources() -> list[UUID]:
    from app.persistence.source_repository import SqlAlchemySourceRepository

    repository = SqlAlchemySourceRepository(SessionLocal)
    return [source.id for source in repository.list_all()]
