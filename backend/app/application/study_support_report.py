"""Measure how much of a call's syllabus Atanor can currently prepare study material for."""

from dataclasses import dataclass
from pathlib import Path

from app.application.call_discovery import discover_calls
from app.application.study_material import derive_knowledge_needs_for_programme_unit
from app.application.study_programmes import discover_programmes
from app.domain.models import Source, StudyProgramme, StudyProgrammeUnit


@dataclass(frozen=True)
class UnitSupport:
    number: int
    title: str
    topic: str | None

    @property
    def supported(self) -> bool:
        return self.topic is not None


@dataclass(frozen=True)
class ProgrammeSupport:
    identifier: str
    title: str
    units: tuple[UnitSupport, ...]

    @property
    def supported_count(self) -> int:
        return sum(unit.supported for unit in self.units)


@dataclass(frozen=True)
class SourceSupportReport:
    source_title: str
    call_detected: bool
    programmes: tuple[ProgrammeSupport, ...]

    @property
    def unit_count(self) -> int:
        return sum(len(programme.units) for programme in self.programmes)

    @property
    def supported_count(self) -> int:
        return sum(programme.supported_count for programme in self.programmes)


def _unit_support(unit: StudyProgrammeUnit) -> UnitSupport:
    try:
        topic = derive_knowledge_needs_for_programme_unit(unit)[0].topic
    except ValueError:
        topic = None
    return UnitSupport(number=unit.number, title=unit.title, topic=topic)


def _programme_support(programme: StudyProgramme) -> ProgrammeSupport:
    return ProgrammeSupport(
        identifier=programme.identifier,
        title=programme.title,
        units=tuple(_unit_support(unit) for unit in programme.units),
    )


def build_support_report(pdf_path: Path) -> SourceSupportReport:
    """Analyse one PDF without persisting anything."""
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Source file not found: {pdf_path}")
    source = Source(title=pdf_path.name, locator=str(pdf_path))
    calls = discover_calls(source)
    programmes = [programme for call in calls for programme in discover_programmes(call, source)]
    return SourceSupportReport(
        source_title=source.title,
        call_detected=bool(calls),
        programmes=tuple(_programme_support(programme) for programme in programmes),
    )


def _percentage(part: int, total: int) -> str:
    return f"{part / total:.0%}" if total else "n/a"


def format_support_report(report: SourceSupportReport) -> str:
    lines = [
        f"{report.source_title}: call {'detected' if report.call_detected else 'NOT detected'}, "
        f"{len(report.programmes)} programme(s), "
        f"{report.supported_count}/{report.unit_count} units supported "
        f"({_percentage(report.supported_count, report.unit_count)})"
    ]
    for programme in report.programmes:
        lines.append(
            f"  {programme.identifier} - {programme.title}: "
            f"{programme.supported_count}/{len(programme.units)} supported"
        )
        lines.extend(
            f"    [{'x' if unit.supported else ' '}] {unit.number}. {unit.title}"
            + (f"  -> {unit.topic}" if unit.topic else "")
            for unit in programme.units
        )
    return "\n".join(lines)
