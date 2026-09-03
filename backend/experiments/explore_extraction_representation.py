from collections import Counter
from pathlib import Path

from pypdf import PdfReader


SAMPLES_DIR = Path("tests/samples")
MAX_BOUNDARIES = 3
MAX_TEXT_LENGTH = 100


def page_lines(pdf_path: Path) -> list[tuple[int, int, str]]:
    reader = PdfReader(pdf_path)
    units: list[tuple[int, int, str]] = []
    order = 0

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for line in text.splitlines():
            value = " ".join(line.split())
            if not value:
                continue
            order += 1
            units.append((page_number, order, value))

    return units


def summarize(pdf_path: Path) -> None:
    units = page_lines(pdf_path)
    pages = len(PdfReader(pdf_path).pages)
    page_counts = Counter(page for page, _, _ in units)
    used_pages = len(page_counts)
    repeated = sum(1 for count in Counter(text for _, _, text in units).values() if count > 1)

    print(pdf_path.name)
    print(f"  pages: {pages} | units: {len(units):,} | pages with text: {used_pages}")
    print(f"  repeated unit texts: {repeated:,}")

    if not units:
        print("  status: no_extractable_text")
        print()
        return

    boundaries = [
        (page, page_counts[page], units[index][2])
        for index, (page, _, _) in enumerate(units)
        if index == 0 or page != units[index - 1][0]
    ]

    print("  page boundaries:")
    for page, count, first_text in boundaries[:MAX_BOUNDARIES]:
        print(f"    p{page}: {count:,} units | {first_text[:MAX_TEXT_LENGTH]}")
    if len(boundaries) > MAX_BOUNDARIES:
        print(f"    ... {len(boundaries) - MAX_BOUNDARIES} more")
    print()


def main() -> None:
    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in: {SAMPLES_DIR}")

    print("EXTRACTION REPRESENTATION EXPLORATION")
    print(f"Samples: {len(samples)}")
    print()

    for sample in samples:
        summarize(sample)


if __name__ == "__main__":
    main()
