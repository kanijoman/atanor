from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import SessionLocal
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


router = APIRouter(prefix="/api/calls", tags=["calls"])


@router.get("")
def list_calls() -> list[dict[str, object]]:
    repository = SqlAlchemyCallRepository(SessionLocal)
    return [
        {
            "id": str(call.id),
            "title": call.title,
        }
        for call in repository.list_all()
    ]


@router.get("/{call_id}")
def get_call(call_id: UUID) -> dict[str, object]:
    repository = SqlAlchemyCallRepository(SessionLocal)
    call = repository.get_by_id(call_id)
    if call is None:
        raise HTTPException(status_code=404, detail="Call not found")

    return {
        "id": str(call.id),
        "title": call.title,
    }


@router.get("/{call_id}/programmes")
def list_call_programmes(call_id: UUID) -> list[dict[str, object]]:
    call_repository = SqlAlchemyCallRepository(SessionLocal)
    if call_repository.get_by_id(call_id) is None:
        raise HTTPException(status_code=404, detail="Call not found")

    programme_repository = SqlAlchemyStudyProgrammeRepository(SessionLocal)
    return [
        {
            "id": str(programme.id),
            "identifier": programme.identifier,
            "title": programme.title,
        }
        for programme in programme_repository.list_by_call(call_id)
    ]
