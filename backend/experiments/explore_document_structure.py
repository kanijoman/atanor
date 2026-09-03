from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re

from pypdf import PdfReader


SAMPLES_DIR = Path("tests/samples")
TARGET_SAMPLE = "BOE-A-2024-14098.pdf"
CONTEXT = 2
MAX_CANDIDATES = 80
MAX_TEXT_LENGTH = 110


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


@dataclass(frozen=True)
class Signals:
    short: bool
    long: bool
    repeated: bool
    starts_with_number: bool
    starts_with_letter: bool
    starts_with_roman: bool
    uppercase_like: bool
    ends_with_punctuation: bool


def extract_units(pdf_path: Path) -> list[TextUnit]:
    reader = PdfReader(pdf_path)
    units: list[TextUnit] = []
    order = 0

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for line in text.splitlines():
            value = " ".join(line.split())
            if not value:
                continue
            order += 1
            units.append(TextUnit(page_number, order, value))

    return units


def normalize_repeated_text(text: str) -> str:
    return re.sub(r"\\d+", "#", text.casefold()).strip()


def repeated_texts(units: list[TextUnit]) -> set[str]:
    counts = Counter(normalize_repeated_text(unit.text) for unit in units)
    return {text for text, count in counts.items() if count >= 3 and len(text) >= 8}


def classify(text: str, repeated: set[str]) -> Signals:
    stripped = text.strip()
    words = stripped.split()
    alpha = [char for char in stripped if char.isalpha()]
    uppercase_like = bool(alpha) and sum(char.isupper() for char in alpha) / len(alpha) >= 0.8

    return Signals(
        short=len(stripped) <= 120,
        long=len(stripped) > 120,
        repeated=normalize_repeated_text(stripped) in repeated,
        starts_with_number=bool(re.match(r"^\\d+(?:[.)] |$)", stripped)),
        starts_with_letter=bool(re.match(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][.)] ", stripped)),
        starts_with_roman=bool(re.match(r"^(?:[IVXLCDM]+)[.)] ", stripped, re.IGNORECASE)),
        uppercase_like=uppercase_like,
        ends_with_punctuation=stripped.endswith((".", ",", ";", ":", ")")),
    )


def score_transition(previous: TextUnit | None, current: TextUnit, signals: Signals) -> int:
    """Score an observable transition; this is intentionally not a semantic classifier."""
    if previous is None:
        return 0

    score = 0
    if current.page != previous.page:
        score += 1
    if signals.starts_with_number or signals.starts_with_letter or signals.starts_with_roman:
        score += 1
    if signals.uppercase_like and len(current.text) <= 100:
        score += 1
    if previous.text.endswith((".", ":", ";")):
        score += 1
    if len(previous.text) > 140 and len(current.text) < 100:
        score += 1
    return score


def find_transitions(units: list[TextUnit]) -> list[tuple[int, int, Signals]]:
    repeated = repeated_texts(units)
    candidates: list[tuple[int, int, Signals]] = []

    for index, current in enumerate(units):
        previous = units[index - 1] if index else None
        signals = classify(current.text, repeated)
        score = score_transition(previous, current, signals)
        if score >= 2:
            candidates.append((score, index, signals))

    return sorted(candidates, key=lambda item: (-item[0], item[1]))


def print_candidate(units: list[TextUnit], index: int, score: int, signals: Signals) -> None:
    start = max(0, index - CONTEXT)
    end = min(len(units), index + CONTEXT + 1)
    current = units[index]

    print(
        f"  score {score} | unit {current.order} | page {current.page} | "
        f"signals={signals}"
    )
    for unit in units[start:end]:
        marker = ">" if unit is current else " "
        print(f"    {marker} p{unit.page} u{unit.order}: {unit.text[:MAX_TEXT_LENGTH]}")


def summarize(pdf_path: Path) -> None:
    units = extract_units(pdf_path)
    print(pdf_path.name)
    print(f"  units: {len(units):,}")

    if not units:
        print("  status: no_extractable_text")
        return

    candidates = find_transitions(units)
    print(f"  transition candidates: {len(candidates):,}")
    print("  strongest transitions:")
    for score, index, signals in candidates[:MAX_CANDIDATES]:
        print_candidate(units, index, score, signals)


def main() -> None:
    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in: {SAMPLES_DIR}")

    print("DOCUMENT STRUCTURE SIGNAL EXPLORATION")
    print("Goal: observe whether local observable signals reveal structural transitions.")
    print()

    target = [sample for sample in samples if sample.name == TARGET_SAMPLE]
    selected = target or samples[:1]
    for sample in selected:
        summarize(sample)


if __name__ == "__main__":
    main()
