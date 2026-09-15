"""Check persisted database hygiene without modifying the database.

Usage:
    python backend/scripts/check_database_hygiene.py

The diagnostic intentionally reports structural anomalies and obvious synthetic
records. It does not attempt to prove semantic correctness of imported data.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.persistence.database import SessionLocal
from app.persistence.models.call import Call
from app.persistence.models.source import Source
from app.persistence.models.study_programme import StudyProgramme, StudyProgrammeUnit


_SYNTHETIC_MARKERS = (
    "test",
    "fixture",
    "dummy",
    "example",
    "synthetic",
    "mock",
    "fake",
)


@dataclass(frozen=True)
class HygieneReport:
    calls: int
    programmes: int
    units: int
    duplicate_units: int
    synthetic_records: int
    source_anomalies: int
    relation_anomalies: int

    @property
    def status(self) -> str:
        return "clean" if self.anomaly_count == 0 else "contaminated"

    @property
    def anomaly_count(self) -> int:
        return (
            self.duplicate_units
            + self.synthetic_records
            + self.source_anomalies
            + self.relation_anomalies
        )


def _contains_synthetic_marker(value: str) -> bool:
    normalized = value.casefold()
    return any(marker in normalized for marker in _SYNTHETIC_MARKERS)


def build_report() -> HygieneReport:
    with SessionLocal() as session:
        sources = session.scalars(select(Source)).all()
        calls = session.scalars(select(Call)).all()
        programmes = session.scalars(select(StudyProgramme)).all()
        units = session.scalars(select(StudyProgrammeUnit)).all()

        duplicate_rows = session.execute(
            select(
                StudyProgrammeUnit.programme_id,
                StudyProgrammeUnit.number,
                StudyProgrammeUnit.title,
                func.count(StudyProgrammeUnit.id),
            )
            .group_by(
                StudyProgrammeUnit.programme_id,
                StudyProgrammeUnit.number,
                StudyProgrammeUnit.title,
            )
            .having(func.count(StudyProgrammeUnit.id) > 1)
        ).all()

        source_ids = {source.id for source in sources}
        call_ids = {call.id for call in calls}
        programme_ids = {programme.id for programme in programmes}

        source_anomalies = sum(
            1 for source in sources if not source.title.strip() or not source.locator.strip()
        )
        synthetic_records = sum(
            _contains_synthetic_marker(source.title)
            or _contains_synthetic_marker(source.locator)
            for source in sources
        )
        synthetic_records += sum(
            _contains_synthetic_marker(call.title) for call in calls
        )
        synthetic_records += sum(
            _contains_synthetic_marker(programme.title)
            or _contains_synthetic_marker(programme.identifier)
            for programme in programmes
        )
        synthetic_records += sum(
            _contains_synthetic_marker(unit.title) for unit in units
        )

        relation_anomalies = sum(
            call.source_id not in source_ids for call in calls
        )
        relation_anomalies += sum(
            programme.call_id not in call_ids for programme in programmes
        )
        relation_anomalies += sum(
            unit.programme_id not in programme_ids for unit in units
        )

    return HygieneReport(
        calls=len(calls),
        programmes=len(programmes),
        units=len(units),
        duplicate_units=len(duplicate_rows),
        synthetic_records=synthetic_records,
        source_anomalies=source_anomalies,
        relation_anomalies=relation_anomalies,
    )


def main() -> int:
    try:
        report = build_report()
    except SQLAlchemyError as exc:
        print("DATABASE HYGIENE")
        print("status: inconclusive")
        print(f"error: {exc}")
        return 2

    print("DATABASE HYGIENE")
    print(f"status: {report.status}")
    print(f"calls: {report.calls}")
    print(f"programmes: {report.programmes}")
    print(f"units: {report.units}")
    print(f"duplicate_units: {report.duplicate_units}")
    print(f"synthetic_records: {report.synthetic_records}")
    print(f"source_anomalies: {report.source_anomalies}")
    print(f"relation_anomalies: {report.relation_anomalies}")

    return 0 if report.status == "clean" else 1


if __name__ == "__main__":
    raise SystemExit(main())
