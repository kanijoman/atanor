from pathlib import Path

from app.application.call_discovery import (
    analyse_call_context,
    discover_and_persist_call,
    discover_calls,
)
from app.domain.models import Call, Source, StudyProgramme


SAMPLES = Path(__file__).parent / "samples"


def source(name: str) -> Source:
    return Source(title=name, locator=str(SAMPLES / name))


class InMemoryCallRepository:
    def __init__(self) -> None:
        self.calls: list[Call] = []

    def save(self, call: Call) -> Call:
        self.calls.append(call)
        return call

    def list_all(self) -> list[Call]:
        return list(self.calls)


class InMemoryStudyProgrammeRepository:
    def __init__(self) -> None:
        self.programmes: list[StudyProgramme] = []

    def save(self, programme: StudyProgramme) -> StudyProgramme:
        self.programmes.append(programme)
        return programme


def test_call_context_requires_combined_call_signals() -> None:
    context = analyse_call_context(
        "convocatoria plazas cuerpo sistema selectivo turno"
    )

    assert context.signals_present == 5
    assert context.strong_signals_present == 4
    assert context.nearby_call_signal_pairs == 4
    assert context.is_strong


def test_call_context_rejects_programme_only_text() -> None:
    context = analyse_call_context("Programa de materias. Cuerpo de Archiveros")

    assert context.signals_present == 1
    assert context.strong_signals_present == 1
    assert context.nearby_call_signal_pairs == 0
    assert not context.is_strong


def test_discovers_call_from_boe() -> None:
    source_document = source("BOE-A-2024-14098.pdf")

    calls = discover_calls(source_document)

    assert len(calls) == 1
    assert calls[0].title == "BOE-A-2024-14098.pdf"
    assert calls[0].source_id == source_document.id


def test_discovers_call_from_boja() -> None:
    calls = discover_calls(source("BOJA24-138-00046-48048-01_00304998.pdf"))

    assert len(calls) == 1


def test_does_not_discover_call_from_programme_only_document() -> None:
    calls = discover_calls(source("Programa_Archiveros_0.pdf"))

    assert calls == []


def test_does_not_discover_call_from_unreadable_document() -> None:
    calls = discover_calls(source("OPOS_AYTO_LEON_INFORMATICA_B.pdf"))

    assert calls == []


def test_discovers_and_persists_call_and_programmes_from_boe() -> None:
    source_document = source("BOE-A-2024-14098.pdf")
    call_repository = InMemoryCallRepository()
    programme_repository = InMemoryStudyProgrammeRepository()

    call = discover_and_persist_call(
        source_document,
        call_repository,
        programme_repository,
    )

    assert call is not None
    assert call_repository.calls == [call]
    assert len(programme_repository.programmes) == 10
    assert all(programme.call_id == call.id for programme in programme_repository.programmes)


def test_does_not_duplicate_existing_call() -> None:
    source_document = source("BOE-A-2024-14098.pdf")
    call_repository = InMemoryCallRepository()
    programme_repository = InMemoryStudyProgrammeRepository()

    first_call = discover_and_persist_call(
        source_document,
        call_repository,
        programme_repository,
    )
    second_call = discover_and_persist_call(
        source_document,
        call_repository,
        programme_repository,
    )

    assert second_call == first_call
    assert len(call_repository.calls) == 1
    assert len(programme_repository.programmes) == 10
