"""Summarize study-material availability for persisted programme units."""

from collections import Counter
import logging

from app.main import app
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import SessionLocal
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository
from fastapi.testclient import TestClient


logging.getLogger("httpx").setLevel(logging.WARNING)

call_repository = SqlAlchemyCallRepository(SessionLocal)
programme_repository = SqlAlchemyStudyProgrammeRepository(SessionLocal)
client = TestClient(app)

calls = call_repository.list_all()
print(f"Calls: {len(calls)}")

for call in calls:
    programmes = programme_repository.list_by_call(call.id)
    print(f"\nCALL: {call.title}")

    statuses: Counter[int] = Counter()
    available = 0
    unavailable = 0

    for programme in programmes:
        print(f"\nProgramme {programme.identifier}: {programme.title}")

        for unit in programme.units:
            response = client.get(f"/api/study/units/{unit.id}")
            statuses[response.status_code] += 1

            if response.status_code == 200:
                available += 1
                marker = "✓"
            else:
                unavailable += 1
                marker = "-"

            print(f"  {unit.number}. {unit.title} -> {response.status_code} {marker}")

    total = available + unavailable
    print("\nSummary:")
    print(f"  programmes: {len(programmes)}")
    print(f"  study units: {total}")
    print(f"  study material available: {available}")
    print(f"  study material unavailable: {unavailable}")
    print(f"  status codes: {dict(sorted(statuses.items()))}")
