from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request, Response
from starlette.concurrency import run_in_threadpool

from app.api.dependencies import (
    CallImportRepositoriesDep,
    CallRepositoryDep,
    StudyProgrammeRepositoryDep,
    UploadsDirDep,
)
from app.application.call_import import CallNotDiscoveredError
from app.application.call_upload import (
    MAX_UPLOAD_BYTES,
    InvalidUploadError,
    UploadTooLargeError,
    import_call_from_upload,
)

router = APIRouter(prefix="/api/calls", tags=["calls"])

NOT_A_CONVOCATORIA = (
    "We could not find a convocatoria with a study programme in this PDF. "
    "Scanned or image-only PDFs are not supported yet."
)


@router.get("")
def list_calls(repository: CallRepositoryDep) -> list[dict[str, object]]:
    return [
        {
            "id": str(call.id),
            "title": call.title,
        }
        for call in repository.list_all()
    ]


async def _read_limited_body(request: Request) -> bytes:
    declared = request.headers.get("content-length")
    if declared is not None and declared.isdigit() and int(declared) > MAX_UPLOAD_BYTES:
        raise UploadTooLargeError("The uploaded file is too large.")
    received = bytearray()
    async for chunk in request.stream():
        received.extend(chunk)
        if len(received) > MAX_UPLOAD_BYTES:
            raise UploadTooLargeError("The uploaded file is too large.")
    return bytes(received)


@router.post("", status_code=201)
async def import_call(
    request: Request,
    response: Response,
    repositories: CallImportRepositoriesDep,
    uploads_dir: UploadsDirDep,
    filename: str = Query(min_length=1, max_length=255),
) -> dict[str, object]:
    """Import the convocatoria PDF sent as the request body.

    Responds 201 for a new call and 200 when the same document was imported before.
    """
    try:
        content = await _read_limited_body(request)
        result = await run_in_threadpool(
            import_call_from_upload,
            filename,
            content,
            uploads_dir,
            repositories,
        )
    except UploadTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc
    except InvalidUploadError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except CallNotDiscoveredError as exc:
        raise HTTPException(status_code=422, detail=NOT_A_CONVOCATORIA) from exc

    if not result.created:
        response.status_code = 200
    return {"id": str(result.call.id), "title": result.call.title}


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
