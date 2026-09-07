from __future__ import annotations

import re
from pathlib import Path
from typing import Protocol

from pypdf import PdfReader

from app.domain.models import Source, StudyProgramme, StudyProgrammeUnit
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


class ProgrammeDiscoveryStrategy(Protocol):
    def discover(self, source: Source) -> list[StudyProgramme]: ...


class _TextUnit:
    def __init__(self, page: int, order: int, text: str) -> None:
        self.page = page
        self.order = order
        self.text = text


def _extract_units(source: Source) -> list[_TextUnit]:
    if not source.locator:
        return []
    reader = PdfReader(Path(source.locator))
    units: list[_TextUnit] = []
    order = 0
    for page, pdf_page in enumerate(reader.pages, start=1):
        for line in (pdf_page.extract_text() or "").splitlines():
            text = " ".join(line.split())
            if text:
                order += 1
                units.append(_TextUnit(page, order, text))
    return units


def _unit_span(units: list[_TextUnit], start: int, end: int, number: int, title: str) -> StudyProgrammeUnit:
    first = units[start]
    last = units[end - 1]
    return StudyProgrammeUnit(
        number=number,
        title=title,
        start_page=first.page,
        start_order=first.order,
        end_page=last.page,
        end_order=last.order,
    )


class BojaProgrammeDiscoveryStrategy:
    _HEADER = re.compile(r"^(?P<identifier>II\.(?:1|[A-Z]))\.\s+(?P<title>PROGRAMA DE MATERIAS.*)$", re.IGNORECASE)
    _TEMA = re.compile(r"^Tema\s+(\d+)[.\-–—]\s*(.*)$", re.IGNORECASE)

    def discover(self, source: Source) -> list[StudyProgramme]:
        units = _extract_units(source)
        headers = [
            (index, match)
            for index, unit in enumerate(units)
            if (match := self._HEADER.fullmatch(unit.text))
        ]
        programmes: list[StudyProgramme] = []
        for header_index, match in headers:
            next_header = next(
                (index for index, _ in headers if index > header_index), len(units)
            )
            continuation = (
                units[header_index + 1].text
                if header_index + 1 < next_header
                and not self._TEMA.fullmatch(units[header_index + 1].text)
                else ""
            )
            title = " ".join(part for part in (match.group("title"), continuation) if part)
            tema_indices = [
                index
                for index in range(header_index + 1, next_header)
                if self._TEMA.fullmatch(units[index].text)
            ]
            if not tema_indices:
                continue
            programme_units: list[StudyProgrammeUnit] = []
            for position, start in enumerate(tema_indices):
                end = tema_indices[position + 1] if position + 1 < len(tema_indices) else next_header
                tema = self._TEMA.fullmatch(units[start].text)
                assert tema is not None
                number = int(tema.group(1))
                title = tema.group(2).strip()
                programme_units.append(_unit_span(units, start, end, number, title))
            programmes.append(
                StudyProgramme(
                    source_id=source.id,
                    identifier=match.group("identifier"),
                    title=title,
                    units=tuple(programme_units),
                )
            )
        return programmes


class ArchiverosProgrammeDiscoveryStrategy:
    _TEMA = re.compile(r"^Tema\s+(\d+)[.\-–—]\s*(.*)$", re.IGNORECASE)

    def discover(self, source: Source) -> list[StudyProgramme]:
        units = _extract_units(source)
        temas = [
            index for index, unit in enumerate(units) if self._TEMA.fullmatch(unit.text)
        ]
        if not temas:
            return []
        first = temas[0]
        title = next(
            (
                unit.text
                for unit in reversed(units[:first])
                if "programa" in unit.text.casefold()
            ),
            "Study programme",
        )
        programme_units = []
        for position, start in enumerate(temas):
            end = temas[position + 1] if position + 1 < len(temas) else len(units)
            tema = self._TEMA.fullmatch(units[start].text)
            assert tema is not None
            programme_units.append(
                _unit_span(
                    units,
                    start,
                    end,
                    int(tema.group(1)),
                    tema.group(2).strip(),
                )
            )
        return [
            StudyProgramme(
                source_id=source.id,
                identifier="I",
                title=title,
                units=tuple(programme_units),
            )
        ]


class BoeProgrammeDiscoveryStrategy:
    _ANNEX = re.compile(r"^ANEXO\s+([IVXLCDM]+)$", re.IGNORECASE)
    _PROGRAMME = re.compile(r"^(\d+)\.\s+Programa\.$", re.IGNORECASE)
    _TOP_LEVEL = re.compile(r"^(\d+)\.\s+(.+)$")

    def discover(self, source: Source) -> list[StudyProgramme]:
        units = _extract_units(source)
        annexes = [
            (index, match.group(1).upper())
            for index, unit in enumerate(units)
            if (match := self._ANNEX.fullmatch(unit.text))
        ]
        programmes: list[StudyProgramme] = []
        for annex_index, identifier in annexes:
            next_annex = next(
                (index for index, _ in annexes if index > annex_index), len(units)
            )
            programme_index = next(
                (
                    index
                    for index in range(annex_index + 1, next_annex)
                    if self._PROGRAMME.fullmatch(units[index].text)
                ),
                None,
            )
            if programme_index is None:
                continue
            title = _boe_process_title(units, annex_index)
            item_indices = [
                index
                for index in range(programme_index + 1, next_annex)
                if self._TOP_LEVEL.fullmatch(units[index].text)
            ]
            if not item_indices:
                continue
            programme_units = []
            for position, start in enumerate(item_indices):
                end = item_indices[position + 1] if position + 1 < len(item_indices) else next_annex
                item = self._TOP_LEVEL.fullmatch(units[start].text)
                assert item is not None
                programme_units.append(
                    _unit_span(
                        units,
                        start,
                        end,
                        int(item.group(1)),
                        item.group(2).strip(),
                    )
                )
            programmes.append(
                StudyProgramme(
                    source_id=source.id,
                    identifier=identifier,
                    title=title,
                    units=tuple(programme_units),
                )
            )
        return programmes


def _boe_process_title(units: list[_TextUnit], annex_index: int) -> str:
    for unit in units[annex_index + 1 : annex_index + 9]:
        text = unit.text
        if "Cuerpo " in text or text.startswith("Cuerpo "):
            return text.rstrip(".")
    return f"ANEXO {units[annex_index].text.split(maxsplit=1)[-1]}"


def discover_programmes(source: Source) -> list[StudyProgramme]:
    units = _extract_units(source)
    if any(BojaProgrammeDiscoveryStrategy._HEADER.fullmatch(unit.text) for unit in units):
        return BojaProgrammeDiscoveryStrategy().discover(source)
    if any(BoeProgrammeDiscoveryStrategy._ANNEX.fullmatch(unit.text) for unit in units) and any(
        BoeProgrammeDiscoveryStrategy._PROGRAMME.fullmatch(unit.text) for unit in units
    ):
        return BoeProgrammeDiscoveryStrategy().discover(source)
    if any(ArchiverosProgrammeDiscoveryStrategy._TEMA.fullmatch(unit.text) for unit in units):
        return ArchiverosProgrammeDiscoveryStrategy().discover(source)
    return []


def discover_and_persist_programmes(
    source: Source,
    repository: SqlAlchemyStudyProgrammeRepository,
) -> list[StudyProgramme]:
    programmes = discover_programmes(source)
    return [repository.save(programme) for programme in programmes]
