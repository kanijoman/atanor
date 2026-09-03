from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re

from pypdf import PdfReader


SAMPLES_DIR = Path("tests/samples")
TARGET_SAMPLE = "BOE-A-2024-14098.pdf"
MAX_REGIONS = 40
MAX_TEXT_LENGTH = 120


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


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


def is_short_structural_candidate(text: str) -> bool:
    """Identify observable boundaries without assigning semantic meaning."""
    if len(text) > 120:
        return False
    if text.endswith((".", ",", ";", ":")):
        return False
    words = text.split()
    if len(words) > 14:
        return False
    return bool(re.search(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", text))


def build_regions(units: list[TextUnit]) -> list[tuple[int, int, list[TextUnit]]]:
    repeated = repeated_texts(units)
    candidates = {
        index
        for index, unit in enumerate(units)
        if is_short_structural_candidate(unit.text)
        and normalize_repeated_text(unit.text) not in repeated
    }

    regions: list[tuple[int, int, list[TextUnit]]] = []
    start = 0

    for index in sorted(candidates):
        if index <= start:
            continue
        chunk = units[start:index]
        if chunk:
            regions.append((start, index - 1, chunk))
        start = index

    if start < len(units):
        regions.append((start, len(units) - 1, units[start:]))

    return regions


def summarize_region(number: int, region: tuple[int, int, list[TextUnit]]) -> None:
    start, end, units = region
    first = units[0]
    last = units[-1]
    preview = " | ".join(unit.text for unit in units[:3])
    print(
        f"  region {number}: units {start + 1}-{end + 1} | "
        f"pages {first.page}-{last.page} | lines {len(units):,}"
    )
    print(f"    start: {first.text[:MAX_TEXT_LENGTH]}")
    print(f"    preview: {preview[:MAX_TEXT_LENGTH]}")


def summarize(pdf_path: Path) -> None:
    units = extract_units(pdf_path)
    print(pdf_path.name)
    print(f"  units: {len(units):,}")

    if not units:
        print("  status: no_extractable_text")
        return

    repeated = repeated_texts(units)
    print(f"  repeated boilerplate candidates: {len(repeated):,}")

    regions = build_regions(units)
    print(f"  candidate regions: {len(regions):,}")
    print("  first regions:")
    for number, region in enumerate(regions[:MAX_REGIONS], start=1):
        summarize_region(number, region)
    if len(regions) > MAX_REGIONS:
        print(f"  ... {len(regions) - MAX_REGIONS} more regions")


def main() -> None:
    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in: {SAMPLES_DIR}")

    print("DOCUMENT REGION DISCOVERY EXPLORATION")
    print("Goal: observe whether generic text-level signals can expose coherent regions.")
    print()

    target = [sample for sample in samples if sample.name == TARGET_SAMPLE]
    selected = target or samples[:1]
    for sample in selected:
        summarize(sample)


if __name__ == "__main__":
    main()
