from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_call_repository, get_study_programme_repository
from app.domain.models import Call, StudyProgramme
from app.main import app


class InMemoryCallRepository:
    def __init__(self, calls: list[Call]) -> None:
        self._calls = calls

    def list_all(self) -> list[Call]:
        return self._calls

    def get_by_id(self, call_id: UUID) -> Call | None:
        return next((call for call in self._calls if call.id == call_id), None)


class InMemoryStudyProgrammeRepository:
    def __init__(self, programmes_by_call: dict[UUID, list[StudyProgramme]]) -> None:
        self._programmes_by_call = programmes_by_call

    def list_by_call(self, call_id: UUID) -> list[StudyProgramme]:
        return self._programmes_by_call.get(call_id, [])


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()


def _use_calls(calls: list[Call]) -> None:
    app.dependency_overrides[get_call_repository] = lambda: InMemoryCallRepository(calls)


def test_list_calls_returns_available_calls(client: TestClient) -> None:
    call = Call(title="Administrative Management Corps", source_id=uuid4())
    _use_calls([call])

    response = client.get("/api/calls")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(call.id),
            "title": "Administrative Management Corps",
        }
    ]


def test_get_call_returns_call(client: TestClient) -> None:
    call = Call(title="Administrative Management Corps", source_id=uuid4())
    _use_calls([call])

    response = client.get(f"/api/calls/{call.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": str(call.id),
        "title": "Administrative Management Corps",
    }


def test_get_call_returns_404_when_call_does_not_exist(client: TestClient) -> None:
    _use_calls([])

    response = client.get(f"/api/calls/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Call not found"}


def test_list_call_programmes_returns_programmes_for_call(client: TestClient) -> None:
    call = Call(title="Administrative Management Corps", source_id=uuid4())
    programme = StudyProgramme(
        call_id=call.id,
        identifier="I",
        title="General subjects",
    )
    _use_calls([call])
    app.dependency_overrides[get_study_programme_repository] = lambda: (
        InMemoryStudyProgrammeRepository({call.id: [programme]})
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


def test_list_call_programmes_returns_404_when_call_does_not_exist(client: TestClient) -> None:
    _use_calls([])

    response = client.get(f"/api/calls/{uuid4()}/programmes")

    assert response.status_code == 404
    assert response.json() == {"detail": "Call not found"}
