from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import calls
from app.domain.models import Call, StudyProgramme
from app.main import app


class InMemoryCallRepository:
    calls: list[Call] = []

    def __init__(self, _session_factory) -> None:
        pass

    def list_all(self):
        return self.calls

    def get_by_id(self, call_id):
        return next((call for call in self.calls if call.id == call_id), None)


class InMemoryStudyProgrammeRepository:
    programmes_by_call: dict = {}

    def __init__(self, _session_factory) -> None:
        pass

    def list_by_call(self, call_id):
        return self.programmes_by_call.get(call_id, [])


client = TestClient(app)


def test_list_calls_returns_available_calls(monkeypatch) -> None:
    call = Call(title="Administrative Management Corps", source_id=uuid4())
    InMemoryCallRepository.calls = [call]
    monkeypatch.setattr(calls, "SqlAlchemyCallRepository", InMemoryCallRepository)

    response = client.get("/api/calls")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(call.id),
            "title": "Administrative Management Corps",
        }
    ]


def test_get_call_returns_call(monkeypatch) -> None:
    call = Call(title="Administrative Management Corps", source_id=uuid4())
    InMemoryCallRepository.calls = [call]
    monkeypatch.setattr(calls, "SqlAlchemyCallRepository", InMemoryCallRepository)

    response = client.get(f"/api/calls/{call.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": str(call.id),
        "title": "Administrative Management Corps",
    }


def test_get_call_returns_404_when_call_does_not_exist(monkeypatch) -> None:
    InMemoryCallRepository.calls = []
    monkeypatch.setattr(calls, "SqlAlchemyCallRepository", InMemoryCallRepository)

    response = client.get(f"/api/calls/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Call not found"}


def test_list_call_programmes_returns_programmes_for_call(monkeypatch) -> None:
    call = Call(title="Administrative Management Corps", source_id=uuid4())
    programme = StudyProgramme(
        call_id=call.id,
        identifier="I",
        title="General subjects",
    )
    InMemoryCallRepository.calls = [call]
    InMemoryStudyProgrammeRepository.programmes_by_call = {
        call.id: [programme],
    }

    monkeypatch.setattr(calls, "SqlAlchemyCallRepository", InMemoryCallRepository)
    monkeypatch.setattr(
        calls,
        "SqlAlchemyStudyProgrammeRepository",
        InMemoryStudyProgrammeRepository,
    )

    response = client.get(f"/api/calls/{call.id}/programmes")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(programme.id),
            "identifier": "I",
            "title": "General subjects",
        }
    ]


def test_list_call_programmes_returns_404_when_call_does_not_exist(
    monkeypatch,
) -> None:
    InMemoryCallRepository.calls = []
    monkeypatch.setattr(calls, "SqlAlchemyCallRepository", InMemoryCallRepository)

    response = client.get(f"/api/calls/{uuid4()}/programmes")

    assert response.status_code == 404
    assert response.json() == {"detail": "Call not found"}
