from pathlib import Path

from app.application.call_import import import_call_from_pdf
from app.domain.models import Call, Source, StudyProgramme


SAMPLES = Path(__file__).parent / "samples"


class InMemorySourceRepository:
    def __init__(self) -> None:
        self.sources: list[Source] = []

    def save(self, source: Source) -> None:
        self.sources.append(source)

    def list_all(self) -> list[Source]:
        return list(self.sources)


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


def test_import_call_from_pdf_persists_source_call_and_programmes() -> None:
    source_repository = InMemorySourceRepository()
    call_repository = InMemoryCallRepository()
    programme_repository = InMemoryStudyProgrammeRepository()

    call = import_call_from_pdf(
        SAMPLES / "BOE-A-2024-14098.pdf",
        source_repository,
        call_repository,
        programme_repository,
    )

    assert len(source_repository.sources) == 1
    assert source_repository.sources[0].title == "BOE-A-2024-14098.pdf"
    assert call_repository.calls == [call]
    assert len(programme_repository.programmes) == 10
    assert all(programme.call_id == call.id for programme in programme_repository.programmes)


def test_import_call_from_pdf_is_idempotent() -> None:
    source_repository = InMemorySourceRepository()
    call_repository = InMemoryCallRepository()
    programme_repository = InMemoryStudyProgrammeRepository()

    first_call = import_call_from_pdf(
        SAMPLES / "BOE-A-2024-14098.pdf",
        source_repository,
        call_repository,
        programme_repository,
    )
    second_call = import_call_from_pdf(
        SAMPLES / "BOE-A-2024-14098.pdf",
        source_repository,
        call_repository,
        programme_repository,
    )

    assert second_call == first_call
    assert len(source_repository.sources) == 1
    assert len(call_repository.calls) == 1
    assert len(programme_repository.programmes) == 10
