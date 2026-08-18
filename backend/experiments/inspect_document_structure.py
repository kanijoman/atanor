from pathlib import Path
import re

from pypdf import PdfReader

from app.application.pdf_extraction import extract_pdf_text
from app.application.source import import_pdf_source


SAMPLES = [
    ("BOE", Path("tests/samples/BOE-A-2024-14098.pdf")),
    ("BOJA", Path("tests/samples/BOJA24-138-00046-48048-01_00304998.pdf")),
    ("Programa Archiveros", Path("tests/samples/Programa_Archiveros_0.pdf")),
    ("Ayuntamiento de León", Path("tests/samples/OPOS_AYTO_LEON_INFORMATICA_B.pdf")),
]

MAX_EXAMPLES = 20

NUMBERED_PATTERN = re.compile(
    r"^(?:\d+(?:\.\d+)*[.)]?|[IVXLCDM]+[.)]|Tema\s+\d+[.:)])\s+",
    re.IGNORECASE,
)
PROGRAMME_PATTERN = re.compile(r"\bprograma(?:\s+de\s+materias)?\b", re.IGNORECASE)
TOPIC_PATTERN = re.compile(r"\btema\s+\d+\b", re.IGNORECASE)
SECTION_PATTERN = re.compile(
    r"^(?:[IVXLCDM]+(?:\.\d+)*[.)]?|[A-Z](?:\.\d+)*[.)]?)\s+",
    re.IGNORECASE,
)


def _is_uppercase_candidate(line: str) -> bool:
    letters = [character for character in line if character.isalpha()]
    return bool(letters) and all(character.isupper() for character in letters)


def _is_short_candidate(line: str) -> bool:
    return 0 < len(line) <= 80


def _examples(lines: list[str], predicate) -> list[tuple[int, str]]:
    return [
        (index + 1, line)
        for index, line in enumerate(lines)
        if predicate(line)
    ][:MAX_EXAMPLES]


def _print_examples(title: str, matches: list[tuple[int, str]], total: int) -> None:
    print(f"\n{title}: {total}")
    for line_number, line in matches:
        print(f"  {line_number:6}: {line}")
    if total > len(matches):
        print(f"  ... {total - len(matches)} more")


def inspect_document(name: str, path: Path) -> None:
    source = import_pdf_source(path, _InMemorySourceRepository())
    text = extract_pdf_text(source)
    lines = text.splitlines()
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    pages = len(PdfReader(path).pages)

    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)
    print(f"File: {path}")
    print(f"Pages: {pages}")
    print(f"Characters: {len(text)}")
    print(f"Lines: {len(lines)}")
    print(f"Non-empty lines: {len(non_empty_lines)}")

    if len(non_empty_lines) < 2:
        print("Extraction status: IMAGE_ONLY_OR_EMPTY")
        print("Structural analysis: SKIPPED")
        print("Reason: no meaningful text was extracted from the PDF.")
        return

    print("Extraction status: TEXT")

    numbered = _examples(non_empty_lines, NUMBERED_PATTERN.match)
    programmes = _examples(non_empty_lines, PROGRAMME_PATTERN.search)
    topics = _examples(non_empty_lines, TOPIC_PATTERN.search)
    sections = _examples(non_empty_lines, SECTION_PATTERN.match)
    uppercase = _examples(non_empty_lines, _is_uppercase_candidate)
    short_lines = _examples(non_empty_lines, _is_short_candidate)

    _print_examples(
        "Numbered / hierarchical candidates",
        numbered,
        sum(bool(NUMBERED_PATTERN.match(line)) for line in non_empty_lines),
    )
    _print_examples(
        "Programme markers",
        programmes,
        sum(bool(PROGRAMME_PATTERN.search(line)) for line in non_empty_lines),
    )
    _print_examples(
        "Topic markers",
        topics,
        sum(bool(TOPIC_PATTERN.search(line)) for line in non_empty_lines),
    )
    _print_examples(
        "Section-like candidates",
        sections,
        sum(bool(SECTION_PATTERN.match(line)) for line in non_empty_lines),
    )
    _print_examples(
        "Uppercase candidates",
        uppercase,
        sum(_is_uppercase_candidate(line) for line in non_empty_lines),
    )
    _print_examples(
        "Short-line candidates (<= 80 chars)",
        short_lines,
        sum(_is_short_candidate(line) for line in non_empty_lines),
    )


def main() -> None:
    for name, path in SAMPLES:
        inspect_document(name, path)


class _InMemorySourceRepository:
    def save(self, source):
        return source


if __name__ == "__main__":
    main()
