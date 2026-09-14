"""Probe the study-material API for persisted programme units."""

from app.main import app
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import SessionLocal
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository
from fastapi.testclient import TestClient


call_repository = SqlAlchemyCallRepository(SessionLocal)
programme_repository = SqlAlchemyStudyProgrammeRepository(SessionLocal)
client = TestClient(app)

calls = call_repository.list_all()
print(f"Calls: {len(calls)}")

for call in calls:
    programmes = programme_repository.list_by_call(call.id)
    print(f"\n=== Call: {call.title} ({call.id}) ===")
    print(f"Programmes: {len(programmes)}")

    for programme in programmes:
        print(f"\n--- Programme {programme.identifier}: {programme.title} ---")

        for unit in programme.units:
            response = client.get(f"/api/study/units/{unit.id}")
            print(f"{unit.number}. {unit.title} -> {response.status_code}")

            if response.status_code != 200:
                print(f"  detail: {response.json().get('detail')}")
            else:
                payload = response.json()
                print(f"  knowledge_need: {payload['knowledge_need']['title']}")
                print(f"  material: {payload['study_material'][:120]!r}")
