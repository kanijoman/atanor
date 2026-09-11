from uuid import uuid4

import pytest

from app.api import calls
from app.domain.models import Call, StudyProgramme, StudyProgrammeUnit


class InMemoryCallRepository:
    def __init__(self, _session_factory) -> None:
        self.calls = []

    def list_all(self):
        return self.calls

    def get_by_id(self, call_id):
        return next((call for call in self.calls if call.id == call_id), None)


class InMemoryStudyProgrammeRepository:
    programmes_by_call = {}

    def __init__(self, _session_factory) -> None:
        pass

    def list_by_call(self, call_id):
        return self.programmes_by_call.get(call_id, [])


def test_list_calls_returns_available_calls(monkeypatch) -> None:
    call = Call(title="Administrative Management Corps", source_id=uuid4())
    repository = InMemoryCallRepository(None)
    repository.calls = [call]

    monkeypatch.setattr(calls, "SqlAlchemyCallRepository", lambda _: repository)

    assert calls.list_calls() == [
        {
            "id": str(call.id),
            "title": "Administrative Management Corps",
        }
    ]


def test_get_call_returns_call(monkeypatch) -> None:
    call = Call(title="Administrative Management Corps", source_id=uuid4())
    repository = InMemoryCallRepository(None)
    repository.calls = [call]

    monkeypatch.setattr(calls, "SqlAlchemyCallRepository", lambda _: repository)

    assert calls.get_call(call.id) == {
        "id": str(call.id),
        "title": "Administrative Management Corps",
    }


def test_get_call_returns_404_when_call_does_not_exist(monkeypatch) -> None:
    repository = InMemoryCallRepository(None)
    monkeypatch.setattr(calls, "SqlAlchemyCallRepository", lambda _: repository)

    with pytest.raises(Exception) as error:
        calls.get_call(uuid4())

    assert error.value.status_code == 404
    assert error.value.detail == "Call not found"


def test_list_call_programmes_returns_programmes_for_call(monkeypatch) -> None:
    call = Call(title="Administrative Management Corps", source_id=uuid4())
    programme = StudyProgramme(
        call_id=call.id,
        identifier="I",
        title="General subjects",
        units=(
            StudyProgrammeUnit(
                number=1,
                title="Constitution",
                start_page=1,
                start_order=1,
                end_page=2,
                end_order=2,
            ),
        ),
    )

    call_repository = InMemoryCallRepository(None)
    call_repository.calls = [call]
    programme_repository = InMemoryStudyProgrammeRepository(None)
    programme_repository.programmes_by_call = {call.id: [programme]}

    def repository_factory(_):
        return call_repository

    monkeypatch.setattr(calls, "SqlAlchemyCallRepository", repository_factory)
    monkeypatch.setattr(
        calls,
        "SqlAlchemyStudyProgrammeRepository",
        lambda _: programme_repository,
    )

    assert calls.list_call_programmes(call.id) == [
        {
            "id": str(programme.id),
            "identifier": "I",
            "title": "General subjects",
        }
    ]


def test_list_call_programmes_returns_404_when_call_does_not_exist(
    monkeypatch,
) -> None:
    repository = InMemoryCallRepository(None)
    monkeypatch.setattr(calls, "SqlAlchemyCallRepository", lambda _: repository)

    with pytest.raises(Exception) as error:
        calls.list_call_programmes(uuid4())

    assert error.value.status_code == 404
    assert error.value.detail == "Call not found"
