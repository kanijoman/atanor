"""Find persisted study programme units related to Ley 39/2015.

Usage:
    uv run python experiments/find_ley_39_2015_units.py

The script is read-only and does not modify the database.
"""

from __future__ import annotations

from pathlib import Path
import sys

from sqlalchemy import select

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.persistence.database import SessionLocal
from app.persistence.models.study_programme import StudyProgramme, StudyProgrammeUnit


SEARCH_TERM = "ley 39/2015"


def main() -> int:
    with SessionLocal() as session:
        rows = session.execute(
            select(StudyProgramme, StudyProgrammeUnit)
            .join(
                StudyProgrammeUnit,
                StudyProgrammeUnit.programme_id == StudyProgramme.id,
            )
            .where(StudyProgrammeUnit.title.ilike(f"%{SEARCH_TERM}%"))
            .order_by(
                StudyProgramme.identifier,
                StudyProgrammeUnit.number,
            )
        ).all()

    print("LEY 39/2015 STUDY UNITS")
    print(f"matches: {len(rows)}")

    for programme, unit in rows:
        print()
        print(f"PROGRAMME: {programme.identifier} - {programme.title}")
        print(f"UNIT: {unit.number}")
        print(f"ID: {unit.id}")
        print(f"TITLE: {unit.title}")
        print(
            f"SPAN: pages {unit.start_page}-{unit.end_page}, "
            f"orders {unit.start_order}-{unit.end_order}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
