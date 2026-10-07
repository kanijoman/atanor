from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.dependencies import CallRepositoryDep, StudyProgrammeRepositoryDep

router = APIRouter(prefix="/api/calls", tags=["calls"])


@router.get("")
def list_calls(repository: CallRepositoryDep) -> list[dict[str, object]]:
    return [
        {
            "id": str(call.id),
            "title": call.title,
        }
        for call in repository.list_all()
    ]


@router.get("/{call_id}")
def get_call(call_id: UUID, repository: CallRepositoryDep) -> dict[str, object]:
    call = repository.get_by_id(call_id)
    if call is None:
        raise HTTPException(status_code=404, detail="Call not found")

    return {
        "id": str(call.id),
        "title": call.title,
    }


@router.get("/{call_id}/programmes")
def list_call_programmes(
    call_id: UUID,
    call_repository: CallRepositoryDep,
    programme_repository: StudyProgrammeRepositoryDep,
) -> list[dict[str, object]]:
    if call_repository.get_by_id(call_id) is None:
        raise HTTPException(status_code=404, detail="Call not found")

    return [
        {
            "id": str(programme.id),
            "identifier": programme.identifier,
            "title": programme.title,
        }
        for programme in programme_repository.list_by_call(call_id)
    ]
