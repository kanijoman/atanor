"""Import a convocatoria uploaded by a candidate as PDF bytes."""

from dataclasses import dataclass
from pathlib import Path

from app.application.call_import import (
    CallNotDiscoveredError,
    CallRepositories,
    import_call_from_pdf,
)
from app.application.source import content_hash_of
from app.domain.models import Call

MAX_UPLOAD_BYTES = 25 * 1024 * 1024
_PDF_SIGNATURE = b"%PDF-"
_MAX_TITLE_LENGTH = 255


class InvalidUploadError(ValueError):
    """The uploaded content cannot be used as a convocatoria."""


class UploadTooLargeError(InvalidUploadError):
    """The uploaded file exceeds the supported size."""


@dataclass(frozen=True)
class UploadResult:
    call: Call
    created: bool


def _display_title(filename: str) -> str:
    name = Path(filename.replace("\\", "/")).name.strip()
    return (name or "convocatoria.pdf")[:_MAX_TITLE_LENGTH]


def _validate(content: bytes) -> None:
    if not content:
        raise InvalidUploadError("The uploaded file is empty.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise UploadTooLargeError(
            f"The uploaded file is larger than {MAX_UPLOAD_BYTES // (1024 * 1024)} MB."
        )
    if not content.startswith(_PDF_SIGNATURE):
        raise InvalidUploadError("The uploaded file is not a PDF document.")


def import_call_from_upload(
    filename: str,
    content: bytes,
    uploads_dir: Path,
    repositories: CallRepositories,
) -> UploadResult:
    """Store an uploaded PDF by content hash and import the call it contains.

    Uploading the same document again returns the existing call (`created=False`).
    """
    _validate(content)
    content_hash = content_hash_of(content)
    already_known = repositories.sources.get_by_content_hash(content_hash) is not None

    uploads_dir.mkdir(parents=True, exist_ok=True)
    stored_path = uploads_dir / f"{content_hash}.pdf"
    if not stored_path.exists():
        stored_path.write_bytes(content)

    try:
        call = import_call_from_pdf(
            stored_path,
            repositories.sources,
            repositories.calls,
            repositories.programmes,
            title=_display_title(filename),
        )
    except CallNotDiscoveredError:
        if not already_known:
            stored_path.unlink(missing_ok=True)
        raise
    return UploadResult(call=call, created=not already_known)
