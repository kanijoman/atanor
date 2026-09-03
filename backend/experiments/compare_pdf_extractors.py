from pathlib import Path

from pypdf import PdfReader

from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Source


SAMPLES_DIR = Path("tests/samples")
MAX_LINES = 3


def extract_with_pypdf(pdf_path: Path) -> tuple[int, list[str]]:
    reader = PdfReader(pdf_path)
    pages = len(reader.pages)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return pages, lines


def extract_with_application(pdf_path: Path) -> list[str]:
    source = Source(title=pdf_path.stem, locator=str(pdf_path))
    text = extract_pdf_text(source)
    return [line.strip() for line in text.splitlines() if line.strip()]


def summarize(pdf_path: Path) -> None:
    pages, pypdf_lines = extract_with_pypdf(pdf_path)
    application_lines = extract_with_application(pdf_path)

    print(f"{pdf_path.name}")
    print(f"  pages: {pages}")
    print(f"  pypdf: {len(pypdf_lines):,} lines / {sum(map(len, pypdf_lines)):,} chars")
    print(
        f"  app:   {len(application_lines):,} lines / "
        f"{sum(map(len, application_lines)):,} chars"
    )
    print("  sample:")
    for line in pypdf_lines[:MAX_LINES]:
        print(f"    {line[:160]}")
    if not pypdf_lines:
        print("    <no extractable text>")
    print()


def main() -> None:
    if not SAMPLES_DIR.is_dir():
        raise FileNotFoundError(f"Samples directory not found: {SAMPLES_DIR}")

    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in: {SAMPLES_DIR}")

    print("PDF EXTRACTOR COMPARISON")
    print(f"Samples: {len(samples)}")
    print()

    for pdf_path in samples:
        summarize(pdf_path)


if __name__ == "__main__":
    main()
