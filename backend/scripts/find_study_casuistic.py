"""Find imported programme units matching a study casuistic.

Usage:
    python backend/scripts/find_study_casuistic.py
"""

from __future__ import annotations

from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import select

from app.persistence.database import SessionLocal
from app.persistence.models.study_programme import StudyProgrammeUnit


_KEYWORDS = (
    "protección de datos",
    "datos personales",
    "reglamento general de protección de datos",
    "rgpd",
    "privacidad",
)


def main() -> None:
    with SessionLocal() as session:
        units = session.scalars(
            select(StudyProgrammeUnit).order_by(
                StudyProgrammeUnit.programme_id,
                StudyProgrammeUnit.number,
            )
        ).all()

        matches = [
            unit
            for unit in units
            if any(keyword in unit.title.casefold() for keyword in _KEYWORDS)
        ]

        print(f"matches: {len(matches)}")
        for unit in matches:
            print(
                f"{unit.number} | {unit.title} | "
                f"programme={unit.programme.title}"
            )


if __name__ == "__main__":
    main()
