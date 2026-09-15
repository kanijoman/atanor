"""Report provenance for persisted sources without modifying the database.

Usage:
    python backend/scripts/diagnose_database_provenance.py

The diagnostic is intended to explain which calls, programmes, and study units
are downstream of each persisted source, especially sources flagged as
synthetic by the database hygiene check.
"""

from __future__ import annotations

from pathlib import Path
import sys

from sqlalchemy import select

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.persistence.database import SessionLocal
from app.persistence.models.call import Call
from app.persistence.models.source import Source
from app.persistence.models.study_programme import StudyProgramme, StudyProgrammeUnit


def main() -> int:
    with SessionLocal() as session:
        sources = session.scalars(select(Source)).all()
        calls = session.scalars(select(Call)).all()
        programmes = session.scalars(select(StudyProgramme)).all()
        units = session.scalars(select(StudyProgrammeUnit)).all()

    print("DATABASE PROVENANCE")
    print(f"sources: {len(sources)}")
    print(f"calls: {len(calls)}")
    print(f"programmes: {len(programmes)}")
    print(f"units: {len(units)}")

    programmes_by_call = {}
    units_by_programme = {}
    for programme in programmes:
        programmes_by_call.setdefault(programme.call_id, []).append(programme)
    for unit in units:
        units_by_programme.setdefault(unit.programme_id, []).append(unit)

    for source in sources:
        source_calls = [call for call in calls if call.source_id == source.id]
        source_programmes = [
            programme
            for call in source_calls
            for programme in programmes_by_call.get(call.id, [])
        ]
        source_units = [
            unit
            for programme in source_programmes
            for unit in units_by_programme.get(programme.id, [])
        ]

        print(f"\nSOURCE {source.id}")
        print(f"  title: {source.title}")
        print(f"  locator: {source.locator}")
        print(f"  calls: {len(source_calls)}")
        print(f"  programmes: {len(source_programmes)}")
        print(f"  units: {len(source_units)}")

        for call in source_calls:
            call_programmes = programmes_by_call.get(call.id, [])
            print(f"  CALL {call.id}: {call.title}")
            print(f"    programmes: {len(call_programmes)}")
            for programme in call_programmes:
                programme_units = units_by_programme.get(programme.id, [])
                print(
                    f"    PROGRAMME {programme.id}: "
                    f"{programme.identifier} - {programme.title} "
                    f"(units: {len(programme_units)})"
                )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
