from pathlib import Path
import re

from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Source


PDF_PATH = Path("tests/samples/BOE-A-2024-14098.pdf")
MAX_EXAMPLES = 8


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


def collect_examples(lines: list[str], signal: str) -> list[tuple[int, str]]:
    examples = []

    for index, line in enumerate(lines):
        if signal in get_signals(line):
            examples.append((index + 1, line))

    return examples[:MAX_EXAMPLES]


def print_examples(title: str, examples: list[tuple[int, str]]) -> None:
    print(title)

    if not examples:
        print("  None")
        return

    for line_number, line in examples:
        print(f"  {line_number:5d}: {line}")

    print()


def main() -> None:
    source = Source(
        title=PDF_PATH.stem,
        locator=str(PDF_PATH),
    )

    text = extract_pdf_text(source)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    print("=" * 80)
    print("DOCUMENT STRUCTURE EXPLORATION")
    print("=" * 80)
    print(f"PDF: {PDF_PATH}")
    print(f"Non-empty lines: {len(lines)}")
    print(f"Characters: {len(text):,}")
    print()

    # ------------------------------------------------------------------
    # Structural signal counts and representative examples
    # ------------------------------------------------------------------

    counts = {name: 0 for name in PATTERNS}

    for line in lines:
        detected = get_signals(line)
        for name in counts:
            if name in detected:
                counts[name] += 1

    print("STRUCTURAL SIGNALS")
    for name, count in counts.items():
        print(f"  {name:25s}: {count:4d}")
    print()

    for signal in PATTERNS:
        examples = collect_examples(lines, signal)
        print_examples(f"{signal.upper()} examples:", examples)

    # ------------------------------------------------------------------
    # Heading-like candidates
    # ------------------------------------------------------------------

    candidates = []

    for index, line in enumerate(lines):
        detected = get_signals(line)

        if (
            "short" in detected
            and (
                "decimal_numbering" in detected
                or "roman_numbering" in detected
                or "uppercase" in detected
            )
        ):
            candidates.append((index + 1, line, detected))

    print("HEADING-LIKE CANDIDATES")
    print(f"  Total candidates: {len(candidates)}")

    for line_number, line, detected in candidates[:MAX_EXAMPLES]:
        print(f"  {line_number:5d}: [{', '.join(detected)}] {line}")

    if len(candidates) > MAX_EXAMPLES:
        print(f"  ... {len(candidates) - MAX_EXAMPLES} more")
    print()

    # ------------------------------------------------------------------
    # Consecutive decimal numbering
    # ------------------------------------------------------------------

    numbered = []

    for index, line in enumerate(lines):
        match = re.match(r"^(\d+)[.)]\s+", line)
        if match:
            numbered.append((index, int(match.group(1)), line))

    sequences = []
    current = []

    for item in numbered:
        if not current or item[1] == current[-1][1] + 1:
            current.append(item)
        else:
            if len(current) >= 2:
                sequences.append(current)
            current = [item]

    if len(current) >= 2:
        sequences.append(current)

    print("CONSECUTIVE DECIMAL SEQUENCES")
    print(f"  Total sequences: {len(sequences)}")

    for sequence in sequences[:MAX_EXAMPLES]:
        first = sequence[0]
        last = sequence[-1]
        print(
            f"  Lines {first[0] + 1}-{last[0] + 1}: "
            f"{first[1]} -> {last[1]} "
            f"({len(sequence)} items)"
        )

    if len(sequences) > MAX_EXAMPLES:
        print(f"  ... {len(sequences) - MAX_EXAMPLES} more")
    print()

    # ------------------------------------------------------------------
    # Representative local context
    # ------------------------------------------------------------------

    print("REPRESENTATIVE CONTEXT")

    context_candidates = []
    for index, line in enumerate(lines):
        detected = get_signals(line)
        if "roman_numbering" in detected or "annex" in detected:
            context_candidates.append(index)

    for index in context_candidates[:MAX_EXAMPLES]:
        print(f"  Around line {index + 1}:")
        start = max(0, index - 1)
        end = min(len(lines), index + 2)

        for current in range(start, end):
            marker = ">>" if current == index else "  "
            print(f"    {marker} {current + 1:5d}: {lines[current]}")
        print()

    if len(context_candidates) > MAX_EXAMPLES:
        print(f"  ... {len(context_candidates) - MAX_EXAMPLES} more contexts")

    print("End of exploration.")


if __name__ == "__main__":
    main()
