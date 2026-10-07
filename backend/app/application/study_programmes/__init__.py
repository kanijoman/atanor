"""Study-programme discovery: provider-specific strategies behind one entry point."""

from typing import Protocol

from app.application.study_programmes.archiveros import ArchiverosProgrammeDiscoveryStrategy
from app.application.study_programmes.boe import BoeProgrammeDiscoveryStrategy
from app.application.study_programmes.boja import BojaProgrammeDiscoveryStrategy
from app.application.study_programmes.strategy import ProgrammeDiscoveryStrategy
from app.application.study_programmes.text_units import extract_units
from app.domain.models import Call, Source, StudyProgramme

# Order matters: the first strategy whose layout matches is used.
STRATEGIES: tuple[ProgrammeDiscoveryStrategy, ...] = (
    BojaProgrammeDiscoveryStrategy(),
    BoeProgrammeDiscoveryStrategy(),
    ArchiverosProgrammeDiscoveryStrategy(),
)


class StudyProgrammeRepository(Protocol):
    def save(self, programme: StudyProgramme) -> StudyProgramme: ...


def discover_programmes(call: Call, source: Source) -> list[StudyProgramme]:
    if call.source_id != source.id:
        raise ValueError("Call source does not match the supplied source")

    units = extract_units(source)
    strategy = next((candidate for candidate in STRATEGIES if candidate.matches(units)), None)
    return strategy.discover(call, units) if strategy is not None else []


def discover_and_persist_programmes(
    call: Call,
    source: Source,
    repository: StudyProgrammeRepository,
) -> list[StudyProgramme]:
    return [repository.save(programme) for programme in discover_programmes(call, source)]


__all__ = [
    "STRATEGIES",
    "ArchiverosProgrammeDiscoveryStrategy",
    "BoeProgrammeDiscoveryStrategy",
    "BojaProgrammeDiscoveryStrategy",
    "ProgrammeDiscoveryStrategy",
    "StudyProgrammeRepository",
    "discover_and_persist_programmes",
    "discover_programmes",
    "extract_units",
]
