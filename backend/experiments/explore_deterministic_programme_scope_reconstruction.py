"""Explore deterministic reconstruction of programme scopes in a BOJA document.

This experiment tests whether structural programme headers can reconstruct the
scope of each Tema sequence without relying on semantic services.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


SAMPLE = "BOJA24-138-00046-48048-01_00304998.pdf"


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


@dataclass(frozen=True)
class ProgrammeHeader:
    label: str
    order: int
    page: int
    text: str


@dataclass(frozen=True)
class TopicMarker:
    number: int
    order: int
    page: int


@dataclass(frozen=True)
class ProgrammeScope:
    header: ProgrammeHeader
    start: int
    end: int
    topics: tuple[TopicMarker, ...]


PROGRAMME_HEADER_PATTERN = re.compile(
    r"^(II(?:\.[A-Z]|\.\d+))\.\s+PROGRAMA DE MATERIAS\b",
    re.IGNORECASE,
)
TOPIC_PATTERN = re.compile(
    r"^Tema\s+(\d+)(?:\s*[.\-–—])\s*.*$",
    re.IGNORECASE,
)


def extract_units(path: Path) -> list[TextUnit]:
    reader = PdfReader(path)
    units: list[TextUnit] = []
    order = 0
    for page_number, page in enumerate(reader.pages, start=1):
        for line in (page.extract_text() or "").splitlines():
            text = " ".join(line.split())
            if text:
                order += 1
                units.append(TextUnit(page_number, order, text))
    return units


def find_headers(units: list[TextUnit]) -> list[ProgrammeHeader]:
    headers: list[ProgrammeHeader] = []
    for unit in units:
        match = PROGRAMME_HEADER_PATTERN.fullmatch(unit.text)
        if match:
            headers.append(
                ProgrammeHeader(
                    label=match.group(1).upper(),
                    order=unit.order,
                    page=unit.page,
                    text=unit.text,
                )
            )
    return headers


def find_topics(units: list[TextUnit]) -> list[TopicMarker]:
    topics: list[TopicMarker] = []
    for unit in units:
        match = TOPIC_PATTERN.fullmatch(unit.text)
        if match:
            topics.append(
                TopicMarker(
                    number=int(match.group(1)),
                    order=unit.order,
                    page=unit.page,
                )
            )
    return topics


def reconstruct_scopes(
    units: list[TextUnit],
    headers: list[ProgrammeHeader],
    topics: list[TopicMarker],
) -> list[ProgrammeScope]:
    scopes: list[ProgrammeScope] = []
    for index, header in enumerate(headers):
        next_header_order = (
            headers[index + 1].order if index + 1 < len(headers) else len(units) + 1
        )
        scoped_topics = tuple(
            topic
            for topic in topics
            if header.order < topic.order < next_header_order
        )
        start = scoped_topics[0].order if scoped_topics else header.order
        end = (
            scoped_topics[-1].order
            if scoped_topics
            else next_header_order - 1
        )
        scopes.append(
            ProgrammeScope(
                header=header,
                start=start,
                end=end,
                topics=scoped_topics,
            )
        )
    return scopes


def validate_scopes(
    scopes: list[ProgrammeScope],
    topics: list[TopicMarker],
) -> tuple[bool, bool, bool, bool]:
    assigned = [topic.order for scope in scopes for topic in scope.topics]
    unique_assignment = len(assigned) == len(set(assigned)) == len(topics)
    monotonic = all(
        scopes[index].start < scopes[index + 1].start
        for index in range(len(scopes) - 1)
    )
    non_overlapping = all(
        scopes[index].end < scopes[index + 1].start
        for index in range(len(scopes) - 1)
    )
    traceable = all(
        scope.header.order < scope.start <= scope.end
        for scope in scopes
        if scope.topics
    )
    return unique_assignment, monotonic, non_overlapping, traceable


def print_scope(scope: ProgrammeScope) -> None:
    numbers = [topic.number for topic in scope.topics]
    if numbers:
        topic_range = f"Tema {numbers[0]}-{numbers[-1]}"
    else:
        topic_range = "no topics"
    print(
        f"  {scope.header.label}: u{scope.start}-u{scope.end} "
        f"{topic_range} header=u{scope.header.order} p{scope.header.page}"
    )


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"
    units = extract_units(samples_dir / SAMPLE)
    headers = find_headers(units)
    topics = find_topics(units)
    scopes = reconstruct_scopes(units, headers, topics)
    validation = validate_scopes(scopes, topics)

    print("DETERMINISTIC PROGRAMME SCOPE RECONSTRUCTION")
    print("  purpose: reconstruct programme scopes from structural headers")
    print("  rule: each Tema belongs to the nearest preceding programme header")
    print()
    print(f"DOCUMENT: {SAMPLE}")
    print(f"  text units: {len(units):,}")
    print(f"  programme headers: {len(headers)}")
    print(f"  Tema markers: {len(topics)}")
    print()
    print("PROGRAMME SCOPES")
    for scope in scopes:
        print_scope(scope)
    print()
    print("VALIDATION")
    print(f"  unique topic assignment: {'OK' if validation[0] else 'FAIL'}")
    print(f"  monotonic scopes: {'OK' if validation[1] else 'FAIL'}")
    print(f"  non-overlapping scopes: {'OK' if validation[2] else 'FAIL'}")
    print(f"  traceable scopes: {'OK' if validation[3] else 'FAIL'}")
    print(f"  status: {'COHERENT' if all(validation) else 'NEEDS_REVIEW'}")


if __name__ == "__main__":
    main()
