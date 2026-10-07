"""Import a competitive-exam call from a PDF source."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from app.application.call_discovery import (
    discover_and_persist_call,
    discover_call,
    persist_call,
)
from app.application.source import SourceRepository, new_pdf_source
from app.domain.models import Call, Source, StudyProgramme


class CallNotDiscoveredError(ValueError):
    """The document does not contain a recognisable call with a study programme."""


class CallRepository(Protocol):
    def save(self, call: Call) -> Call: ...

    def list_all(self) -> list[Call]: ...


class StudyProgrammeRepository(Protocol):
    def save(self, programme: StudyProgramme) -> StudyProgramme: ...


@dataclass(frozen=True)
class CallRepositories:
    """The persistence ports needed to import a call."""

    sources: SourceRepository
    calls: CallRepository
    programmes: StudyProgrammeRepository


def _find_existing_source(source: Source, repository: SourceRepository) -> Source | None:
    """Match by content, then by locator for sources imported before hashes existed."""
    if source.content_hash is not None:
        by_hash = repository.get_by_content_hash(source.content_hash)
        if by_hash is not None:
            return by_hash
    return next((item for item in repository.list_all() if item.locator == source.locator), None)


def import_call_from_pdf(
    path: str | Path,
    source_repository: SourceRepository,
    call_repository: CallRepository,
    programme_repository: StudyProgrammeRepository,
    title: str | None = None,
) -> Call:
    """Import a PDF and persist its discovered call and study programmes.

    Nothing is persisted for a document that does not contain a recognisable call.
    Importing the same content again returns the call that was already imported.
    """
    candidate = new_pdf_source(path, title)
    existing_source = _find_existing_source(candidate, source_repository)
    if existing_source is not None:
        call = discover_and_persist_call(existing_source, call_repository, programme_repository)
    else:
        discovered = discover_call(candidate)
        if discovered is None:
            raise CallNotDiscoveredError(f"No competitive-exam call discovered in {path}")
        source_repository.save(candidate)
        call = persist_call(discovered, call_repository, programme_repository)

    if call is None:
        raise CallNotDiscoveredError(f"No competitive-exam call discovered in {path}")
    return call
