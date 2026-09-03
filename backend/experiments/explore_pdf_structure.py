from pathlib import Path
import re

from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Source


PDF_PATH = Path("tests/samples/BOE-A-2024-14098.pdf")


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


def main() -> None:
    source = Source(
        title=PDF_PATH.stem,
        locator=str(PDF_PATH),
    )

    text = extract_pdf_text(source)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    print("=" * 100)
    print("DOCUMENT STRUCTURE EXPLORATION")
    print("=" * 100)
    print(f"PDF: {PDF_PATH}")
    print(f"Non-empty lines: {len(lines)}")
    print(f"Characters: {len(text):,}")
    print()

    # ------------------------------------------------------------------
    # 1. Numbering signals
    # ------------------------------------------------------------------

    print("=" * 100)
    print("1. NUMBERING SIGNALS")
    print("=" * 100)

    for index, line in enumerate(lines):
        detected = get_signals(line)

        if any(
            signal in detected
            for signal in (
                "decimal_numbering",
                "hierarchical_numbering",
                "roman_numbering",
                "letter_numbering",
                "annex",
            )
        ):
            print(
                f"{index + 1:5d}: "
                f"[{', '.join(detected)}] "
                f"{line}"
            )

    print()

    # ------------------------------------------------------------------
    # 2. Short / heading-like lines
    # ------------------------------------------------------------------

    print("=" * 100)
    print("2. SHORT / HEADING-LIKE LINES")
    print("=" * 100)

    for index, line in enumerate(lines):
        detected = get_signals(line)

        if "short" in detected and len(line) <= 60:
            print(
                f"{index + 1:5d}: "
                f"[{', '.join(detected)}] "
                f"{line}"
            )

    print()

    # ------------------------------------------------------------------
    # 3. Structural candidates with context
    # ------------------------------------------------------------------

    print("=" * 100)
    print("3. STRUCTURAL CANDIDATES WITH CONTEXT")
    print("=" * 100)

    candidate_indexes = []

    for index, line in enumerate(lines):
        detected = get_signals(line)

        if any(
            signal in detected
            for signal in (
                "decimal_numbering",
                "roman_numbering",
                "annex",
                "uppercase",
            )
        ):
            candidate_indexes.append(index)

    for index in candidate_indexes:
        print("-" * 100)

        start = max(0, index - 1)
        end = min(len(lines), index + 3)

        for current in range(start, end):
            marker = ">>" if current == index else "  "

            print(
                f"{marker} "
                f"{current + 1:5d}: "
                f"{lines[current]}"
            )

    print()

    # ------------------------------------------------------------------
    # 4. Structural statistics
    # ------------------------------------------------------------------

    print("=" * 100)
    print("4. STRUCTURAL STATISTICS")
    print("=" * 100)

    counts = {name: 0 for name in PATTERNS}

    for line in lines:
        detected = get_signals(line)

        for name in counts:
            if name in detected:
                counts[name] += 1

    for name, count in counts.items():
        print(f"{name:25s}: {count}")

    print()

    lengths = [len(line) for line in lines]

    print(f"Minimum line length: {min(lengths)}")
    print(f"Maximum line length: {max(lengths)}")
    print(f"Average line length: {sum(lengths) / len(lengths):.1f}")
    print(f"Lines <= 40 chars:   {sum(x <= 40 for x in lengths)}")
    print(f"Lines <= 60 chars:   {sum(x <= 60 for x in lengths)}")
    print(f"Lines <= 80 chars:   {sum(x <= 80 for x in lengths)}")
    print()

    # ------------------------------------------------------------------
    # 5. Consecutive decimal numbering
    # ------------------------------------------------------------------

    print("=" * 100)
    print("5. CONSECUTIVE NUMBERING")
    print("=" * 100)

    numbered = []

    for index, line in enumerate(lines):
        match = re.match(r"^(\d+)[.)]\s+", line)

        if match:
            numbered.append(
                (
                    index,
                    int(match.group(1)),
                    line,
                )
            )

    previous_number = None
    previous_index = None

    for index, number, line in numbered:
        if previous_number is not None:
            if number == previous_number + 1:
                print(
                    f"{previous_index + 1:5d} -> "
                    f"{index + 1:5d}: "
                    f"{previous_number} -> {number}"
                )

        previous_number = number
        previous_index = index

    print()
    print("End of exploration.")


if __name__ == "__main__":
    main()
