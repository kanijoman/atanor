from collections import Counter
from pathlib import Path
import re

from pypdf import PdfReader

from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Source


SAMPLES_DIR = Path("tests/samples")
MAX_EXAMPLES = 5

PATTERNS = {
    "decimal_numbering": re.compile(r"^\d+[.)]\s+"),
    "hierarchical_numbering": re.compile(r"^\d+(?:\.\d+)+[.)]?\s+"),
    "roman_numbering": re.compile(r"^[IVXLCDM]+[.)]\s+", re.IGNORECASE),
    "letter_numbering": re.compile(r"^[a-z][.)]\s+", re.IGNORECASE),
    "annex": re.compile(r"^ANEXO\b", re.IGNORECASE),
}


def get_signals(line: str) -> list[str]:
    signals = []

    for name, pattern in PATTERNS.items():
        if pattern.search(line):
            signals.append(name)

    if line.isupper() and len(line) <= 120:
        signals.append("uppercase")

    if len(line) <= 80:
        signals.append("short")

    if line.endswith("."):
        signals.append("ends_with_period")

    return signals


def extract_text_characteristics(pdf_path: Path) -> dict:
    source = Source(title=pdf_path.stem, locator=str(pdf_path))
    text = extract_pdf_text(source)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    counts = {name: 0 for name in PATTERNS}
    for line in lines:
        for signal in get_signals(line):
            if signal in counts:
                counts[signal] += 1

    repeated_lines = Counter(lines)
    repeated = [
        (line, count)
        for line, count in repeated_lines.most_common()
        if count > 1
    ]

    return {
        "text": text,
        "lines": lines,
        "characters": len(text),
        "non_empty_lines": len(lines),
        "replacement_characters": text.count("\ufffd"),
        "alphabetic_characters": sum(c.isalpha() for c in text),
        "whitespace_characters": sum(c.isspace() for c in text),
        "average_line_length": len(text) / len(lines) if lines else 0,
        "signals": counts,
        "repeated_lines": repeated,
    }


def extract_layout_characteristics(pdf_path: Path) -> dict:
    reader = PdfReader(pdf_path)
    font_sizes = Counter()
    fonts = Counter()
    fragments = 0

    for page in reader.pages:
        def visitor_text(text, cm, tm, font_dict, font_size):
            nonlocal fragments
            if not text.strip():
                return

            fragments += 1
            font_sizes[round(float(font_size), 2)] += 1
            font = font_dict.get("/BaseFont", "<unknown>") if font_dict else "<unknown>"
            fonts[str(font)] += 1

        page.extract_text(visitor_text=visitor_text)

    return {
        "pages": len(reader.pages),
        "fragments": fragments,
        "font_sizes": font_sizes,
        "fonts": fonts,
    }


def format_counter(counter: Counter, limit: int = MAX_EXAMPLES) -> str:
    if not counter:
        return "None"

    values = [f"{value} ({count})" for value, count in counter.most_common(limit)]
    if len(counter) > limit:
        values.append(f"... {len(counter) - limit} more")
    return ", ".join(values)


def print_text_characteristics(characteristics: dict) -> None:
    print("TEXT")
    print(f"  Characters:              {characteristics['characters']:,}")
    print(f"  Non-empty lines:         {characteristics['non_empty_lines']:,}")
    print(f"  Average line length:     {characteristics['average_line_length']:.1f}")
    print(f"  Replacement characters:  {characteristics['replacement_characters']:,}")
    print(f"  Alphabetic characters:   {characteristics['alphabetic_characters']:,}")
    print(f"  Whitespace characters:   {characteristics['whitespace_characters']:,}")
    print()


def print_structural_signals(characteristics: dict) -> None:
    print("STRUCTURAL SIGNALS")
    for name, count in characteristics["signals"].items():
        print(f"  {name:25s}: {count:5d}")
    print()


def print_layout_characteristics(characteristics: dict) -> None:
    print("PHYSICAL LAYOUT")
    print(f"  Pages:                   {characteristics['pages']:,}")
    print(f"  Text fragments:          {characteristics['fragments']:,}")
    print(f"  Font sizes:              {format_counter(characteristics['font_sizes'])}")
    print(f"  Fonts:                   {format_counter(characteristics['fonts'])}")
    print()


def print_repeated_lines(characteristics: dict) -> None:
    print("REPEATED LINES")
    repeated = characteristics["repeated_lines"]
    if not repeated:
        print("  None")
        print()
        return

    for line, count in repeated[:MAX_EXAMPLES]:
        print(f"  ({count:3d}x) {line}")
    if len(repeated) > MAX_EXAMPLES:
        print(f"  ... {len(repeated) - MAX_EXAMPLES} more")
    print()


def print_representative_lines(characteristics: dict) -> None:
    print("REPRESENTATIVE TEXT")
    lines = characteristics["lines"]
    if not lines:
        print("  No extractable text")
        print()
        return

    for line in lines[:MAX_EXAMPLES]:
        print(f"  {line}")
    print()


def characterize_text(characteristics: dict) -> str:
    characters = characteristics["characters"]
    replacement_characters = characteristics["replacement_characters"]

    if characters == 0:
        return "no_extractable_text"
    if replacement_characters > 0:
        return "text_with_replacement_characters"
    if characters < 1_000:
        return "very_low_text_volume"
    if characters < 10_000:
        return "low_text_volume"
    return "substantial_text"


def print_characterization(characteristics: dict) -> None:
    print("PRELIMINARY CHARACTERIZATION")
    print(f"  Text extraction:        {characterize_text(characteristics)}")
    print(f"  Numbering signals:      {sum(characteristics['signals'].values()):,}")
    print(f"  Repeated lines:         {len(characteristics['repeated_lines']):,}")
    print("  NOTE: These are observations, not document-type classifications.")
    print()


def analyze_sample(pdf_path: Path) -> None:
    print("=" * 80)
    print(f"SAMPLE: {pdf_path.name}")
    print("=" * 80)

    text_characteristics = extract_text_characteristics(pdf_path)
    layout_characteristics = extract_layout_characteristics(pdf_path)

    print_text_characteristics(text_characteristics)
    print_layout_characteristics(layout_characteristics)
    print_structural_signals(text_characteristics)
    print_repeated_lines(text_characteristics)
    print_representative_lines(text_characteristics)
    print_characterization(text_characteristics)


def main() -> None:
    if not SAMPLES_DIR.is_dir():
        raise FileNotFoundError(f"Samples directory not found: {SAMPLES_DIR}")

    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in: {SAMPLES_DIR}")

    print("=" * 80)
    print("PDF SAMPLE CHARACTERIZATION")
    print("=" * 80)
    print(f"Samples directory: {SAMPLES_DIR}")
    print(f"Samples found:     {len(samples)}")
    print()

    for pdf_path in samples:
        analyze_sample(pdf_path)

    print("=" * 80)
    print("End of characterization.")
    print("=" * 80)


if __name__ == "__main__":
    main()
