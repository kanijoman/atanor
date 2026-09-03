import re
from pathlib import Path
from statistics import median

from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Source


SAMPLES_DIR = Path("tests/samples")
MAX_EXAMPLES = 4
HEADING_PATTERN = re.compile(r"^(?:\d+(?:\.\d+)*[.)]?|[IVXLCDM]+[.)]|[A-Z][.)])\s+")
TERMINAL_PATTERN = re.compile(r"[.!?;:]$|[.!?;:]\s+[\)\]]$")


def raw_lines(pdf_path: Path) -> list[str]:
    source = Source(title=pdf_path.stem, locator=str(pdf_path))
    return [line.rstrip() for line in extract_pdf_text(source).splitlines()]


def split_on_blank_lines(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        if line.strip():
            current.append(line.strip())
        elif current:
            blocks.append(current)
            current = []

    if current:
        blocks.append(current)
    return blocks


def split_on_text_continuity(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        text = line.strip()
        if not text:
            if current:
                blocks.append(current)
                current = []
            continue

        starts_heading = bool(HEADING_PATTERN.match(text))
        if starts_heading and current:
            blocks.append(current)
            current = []

        current.append(text)

        if TERMINAL_PATTERN.search(text):
            blocks.append(current)
            current = []

    if current:
        blocks.append(current)
    return blocks


def summarize_blocks(blocks: list[list[str]]) -> tuple[int, float, int, int]:
    lengths = [len(block) for block in blocks]
    return len(blocks), median(lengths) if lengths else 0, min(lengths, default=0), max(lengths, default=0)


def print_examples(blocks: list[list[str]]) -> None:
    for index, block in enumerate(blocks[:MAX_EXAMPLES], start=1):
        text = " ".join(block)
        print(f"    {index}: {len(block)} lines | {text[:140]}")


def summarize(pdf_path: Path) -> None:
    lines = raw_lines(pdf_path)
    non_empty = sum(bool(line.strip()) for line in lines)
    blank = len(lines) - non_empty
    blank_blocks = split_on_blank_lines(lines)
    continuity_blocks = split_on_text_continuity(lines)

    print(pdf_path.name)
    print(f"  raw lines: {len(lines):,} | non-empty: {non_empty:,} | blank: {blank:,}")

    for name, blocks in (
        ("blank-line", blank_blocks),
        ("text-continuity", continuity_blocks),
    ):
        count, med, minimum, maximum = summarize_blocks(blocks)
        print(f"  {name}: {count:,} blocks | median: {med:g} lines | range: {minimum}-{maximum}")
        print_examples(blocks)
    print()


def main() -> None:
    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in: {SAMPLES_DIR}")

    print("TEXT BLOCK EXPLORATION")
    print(f"Samples: {len(samples)}")
    print()

    for sample in samples:
        summarize(sample)


if __name__ == "__main__":
    main()
