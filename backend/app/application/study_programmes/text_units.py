"""Ordered text lines extracted from a PDF source, with page/order provenance."""

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from app.domain.models import Source, StudyProgrammeUnit


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


def extract_units(source: Source) -> list[TextUnit]:
    if not source.locator:
        return []
    reader = PdfReader(Path(source.locator))
    units: list[TextUnit] = []
    order = 0
    for page, pdf_page in enumerate(reader.pages, start=1):
        for line in (pdf_page.extract_text() or "").splitlines():
            text = " ".join(line.split())
            if text:
                order += 1
                units.append(TextUnit(page, order, text))
    return units


def unit_span(
    units: list[TextUnit], start: int, end: int, number: int, title: str
) -> StudyProgrammeUnit:
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
