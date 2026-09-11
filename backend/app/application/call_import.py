"""Import a competitive-exam call from a PDF source."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from app.application.call_discovery import discover_and_persist_call
from app.application.source import import_pdf_source
from app.domain.models import Call, Source, StudyProgramme


class SourceRepository(Protocol):
    def save(self, source: Source) -> None: ...

    def list_all(self) -> list[Source]: ...


class CallRepository(Protocol):
    def save(self, call: Call) -> Call: ...

    def list_all(self) -> list[Call]: ...


class StudyProgrammeRepository(Protocol):
    def save(self, programme: StudyProgramme) -> StudyProgramme: ...


def import_call_from_pdf(
    path: str | Path,
    source_repository: SourceRepository,
    call_repository: CallRepository,
    programme_repository: StudyProgrammeRepository,
) -> Call:
    """Import a PDF and persist its discovered call and study programmes."""
    pdf_path = Path(path)
    existing_source = next(
        (
            source
            for source in source_repository.list_all()
            if source.locator == str(pdf_path)
        ),
        None,
    )
    source = existing_source or import_pdf_source(pdf_path, source_repository)

    call = discover_and_persist_call(
        source,
        call_repository,
        programme_repository,
    )
    if call is None:
        raise ValueError(f"No competitive-exam call discovered in {pdf_path}")

    return call
