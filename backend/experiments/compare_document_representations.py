from collections import Counter
from pathlib import Path

from pypdf import PdfReader

from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Source


SAMPLES_DIR = Path("tests/samples")
MAX_EXAMPLES = 6


def extracted_lines(pdf_path: Path) -> list[str]:
    source = Source(title=pdf_path.stem, locator=str(pdf_path))
    return [line.strip() for line in extract_pdf_text(source).splitlines() if line.strip()]


def physical_fragments(pdf_path: Path) -> list[tuple[int, str, float, float, float]]:
    fragments: list[tuple[int, str, float, float, float]] = []
    reader = PdfReader(pdf_path)

    for page_number, page in enumerate(reader.pages, start=1):
        def visitor(text: str, cm: list[float], tm: list[float], font_dict, font_size: float) -> None:
            value = " ".join(text.split())
            if not value:
                return
            fragments.append((page_number, value, tm[4], tm[5], font_size))

        page.extract_text(visitor_text=visitor)

    return fragments


def summarize(pdf_path: Path) -> None:
    lines = extracted_lines(pdf_path)
    fragments = physical_fragments(pdf_path)

    pages = len(PdfReader(pdf_path).pages)
    unique_lines = len(set(lines))
    repeated_lines = sum(1 for count in Counter(lines).values() if count > 1)

    print(pdf_path.name)
    print(f"  pages: {pages}")
    print(f"  text lines: {len(lines):,}")
    print(f"  physical fragments: {len(fragments):,}")
    print(f"  unique text lines: {unique_lines:,}")
    print(f"  repeated text lines: {repeated_lines:,}")

    if not fragments:
        print("  physical examples: none")
        print()
        return

    print("  physical examples:")
    for page, text, x, y, size in fragments[:MAX_EXAMPLES]:
        print(f"    p{page}: x={x:>7.1f} y={y:>7.1f} size={size:>4.1f} | {text[:80]}")
    print()


def main() -> None:
    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in: {SAMPLES_DIR}")

    print("DOCUMENT REPRESENTATION COMPARISON")
    print(f"Samples: {len(samples)}")
    print()

    for sample in samples:
        summarize(sample)


if __name__ == "__main__":
    main()
