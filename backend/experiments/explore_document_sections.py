from pathlib import Path
import re

from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Source


SAMPLES_DIR = Path("tests/samples")
MAX_SECTIONS = 12
MAX_TITLE_LENGTH = 100

NUMBERED_HEADING = re.compile(
    r"^(?:\d+(?:\.\d+)*[.)]?|[IVXLCDM]+[.)]|[A-Z][.)])\s+\S+",
    re.IGNORECASE,
)


def is_heading_candidate(line: str) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) > MAX_TITLE_LENGTH:
        return False

    words = stripped.split()
    if len(words) <= 12 and NUMBERED_HEADING.match(stripped):
        return True

    letters = [char for char in stripped if char.isalpha()]
    if letters and len(letters) >= 4:
        uppercase_ratio = sum(char.isupper() for char in letters) / len(letters)
        if uppercase_ratio >= 0.8 and len(words) <= 10:
            return True

    return False


def detect_sections(lines: list[str]) -> list[tuple[int, str]]:
    return [
        (index + 1, line.strip())
        for index, line in enumerate(lines)
        if is_heading_candidate(line)
    ]


def summarize(pdf_path: Path) -> None:
    source = Source(title=pdf_path.stem, locator=str(pdf_path))
    text = extract_pdf_text(source)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    print(pdf_path.name)
    print(f"  lines: {len(lines):,}")

    if not lines:
        print("  status: no_extractable_text")
        print()
        return

    candidates = detect_sections(lines)
    print(f"  heading candidates: {len(candidates):,}")
    print("  first candidates:")
    for line_number, title in candidates[:MAX_SECTIONS]:
        print(f"    {line_number:>5}: {title}")
    if len(candidates) > MAX_SECTIONS:
        print(f"    ... {len(candidates) - MAX_SECTIONS} more")
    print()


def main() -> None:
    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in: {SAMPLES_DIR}")

    print("DOCUMENT SECTION EXPLORATION")
    print(f"Samples: {len(samples)}")
    print()

    for sample in samples:
        summarize(sample)


if __name__ == "__main__":
    main()
