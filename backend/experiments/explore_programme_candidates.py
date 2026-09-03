from pathlib import Path
import re

from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Source


SAMPLES_DIR = Path("tests/samples")
MAX_CANDIDATES = 6
CONTEXT_BEFORE = 2
CONTEXT_AFTER = 2

PROGRAMME_TERMS = (
    "programa",
    "temario",
    "materias",
    "contenido del programa",
)
PROCESS_TERMS = (
    "proceso selectivo",
    "cuerpo",
    "escala",
    "ingreso libre",
    "promoción interna",
)


def extract_lines(pdf_path: Path) -> list[str]:
    source = Source(title=pdf_path.stem, locator=str(pdf_path))
    text = extract_pdf_text(source)
    return [line.strip() for line in text.splitlines() if line.strip()]


def contains_any(line: str, terms: tuple[str, ...]) -> bool:
    normalized = line.casefold()
    return any(term in normalized for term in terms)


def is_programme_candidate(line: str) -> bool:
    normalized = line.casefold().strip(" .:")
    if normalized in PROGRAMME_TERMS:
        return True
    return contains_any(line, PROGRAMME_TERMS) and len(line) <= 180


def nearest_process_context(lines: list[str], index: int) -> str | None:
    start = max(0, index - 30)
    for candidate in reversed(lines[start:index]):
        if contains_any(candidate, PROCESS_TERMS):
            return candidate
    return None


def find_candidates(lines: list[str]) -> list[tuple[int, str, str | None]]:
    candidates = []
    for index, line in enumerate(lines):
        if is_programme_candidate(line):
            candidates.append((index, line, nearest_process_context(lines, index)))
    return candidates


def print_candidate(lines: list[str], index: int, line: str, process: str | None) -> None:
    print(f"  line {index + 1}: {line}")
    if process:
        print(f"    process context: {process}")

    start = max(0, index - CONTEXT_BEFORE)
    end = min(len(lines), index + CONTEXT_AFTER + 1)
    for context_index in range(start, end):
        if context_index == index:
            continue
        print(f"    {context_index + 1}: {lines[context_index][:160]}")


def inspect_sample(pdf_path: Path) -> None:
    lines = extract_lines(pdf_path)
    print(f"{pdf_path.name}")
    print(f"  lines: {len(lines):,}")

    if not lines:
        print("  status: no_extractable_text")
        print()
        return

    candidates = find_candidates(lines)
    print(f"  programme candidates: {len(candidates)}")

    for index, line, process in candidates[:MAX_CANDIDATES]:
        print_candidate(lines, index, line, process)
    if len(candidates) > MAX_CANDIDATES:
        print(f"  ... {len(candidates) - MAX_CANDIDATES} more candidates")
    print()


def main() -> None:
    if not SAMPLES_DIR.is_dir():
        raise FileNotFoundError(f"Samples directory not found: {SAMPLES_DIR}")

    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in: {SAMPLES_DIR}")

    print("PROGRAMME CANDIDATE EXPLORATION")
    print(f"Samples: {len(samples)}")
    print()

    for pdf_path in samples:
        inspect_sample(pdf_path)


if __name__ == "__main__":
    main()
