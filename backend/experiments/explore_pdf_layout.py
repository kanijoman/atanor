from collections import Counter
from pathlib import Path

from pypdf import PdfReader


PDF_PATH = Path("tests/samples/BOE-A-2024-14098.pdf")
MAX_EXAMPLES = 5
Y_TOLERANCE = 2.0
TARGET_TERMS = ("Programa", "ANEXO")


def extract_fragments(page) -> list[dict]:
    """Collect text fragments together with physical PDF layout metadata."""
    fragments = []

    def visitor_text(text, cm, tm, font_dict, font_size):
        if not text.strip():
            return

        fragments.append(
            {
                "text": text.replace("\n", "\\n"),
                "x": round(float(tm[4]), 2),
                "y": round(float(tm[5]), 2),
                "font_size": round(float(font_size), 2),
                "font": _font_name(font_dict),
                "font_flags": _font_flags(font_dict),
            }
        )

    page.extract_text(visitor_text=visitor_text)
    return fragments


def _font_name(font_dict) -> str:
    if not font_dict:
        return "<unknown>"
    return str(font_dict.get("/BaseFont", "<unknown>"))


def _font_flags(font_dict) -> int | None:
    if not font_dict:
        return None
    value = font_dict.get("/Flags")
    return int(value) if value is not None else None


def group_fragments_into_lines(fragments: list[dict]) -> list[list[dict]]:
    """Group fragments by their approximate vertical position."""
    lines: list[list[dict]] = []

    for fragment in sorted(fragments, key=lambda item: (-item["y"], item["x"])):
        for line in lines:
            if abs(line[0]["y"] - fragment["y"]) <= Y_TOLERANCE:
                line.append(fragment)
                break
        else:
            lines.append([fragment])

    for line in lines:
        line.sort(key=lambda item: item["x"])

    return lines


def line_text(line: list[dict]) -> str:
    return "".join(fragment["text"] for fragment in line).strip()


def summarize_page(page_number: int, page) -> dict:
    fragments = extract_fragments(page)
    lines = group_fragments_into_lines(fragments)

    return {
        "page": page_number,
        "width": round(float(page.mediabox.width), 2),
        "height": round(float(page.mediabox.height), 2),
        "fragments": fragments,
        "lines": lines,
        "font_sizes": Counter(fragment["font_size"] for fragment in fragments),
        "fonts": Counter(fragment["font"] for fragment in fragments),
    }


def format_line(line: list[dict]) -> str:
    sizes = sorted({fragment["font_size"] for fragment in line})
    flags = sorted({fragment["font_flags"] for fragment in line})
    x = min(fragment["x"] for fragment in line)
    y = line[0]["y"]
    return f"({x:.1f}, {y:.1f}) size={sizes} flags={flags} {line_text(line)!r}"


def print_target_examples(page_summaries: list[dict]) -> None:
    print("TARGET EXAMPLES")
    examples = 0

    for summary in page_summaries:
        for index, line in enumerate(summary["lines"]):
            text = line_text(line)
            if not any(term.casefold() in text.casefold() for term in TARGET_TERMS):
                continue

            print(f"  Page {summary['page']}, line {index + 1}: {format_line(line)}")
            examples += 1
            if examples >= MAX_EXAMPLES:
                print()
                return

    if examples == 0:
        print("  None")
    print()


def main() -> None:
    if not PDF_PATH.is_file():
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    reader = PdfReader(PDF_PATH)
    page_summaries = [
        summarize_page(page_number, page)
        for page_number, page in enumerate(reader.pages, start=1)
    ]

    total_fragments = sum(len(summary["fragments"]) for summary in page_summaries)
    total_lines = sum(len(summary["lines"]) for summary in page_summaries)
    font_sizes = Counter()
    fonts = Counter()

    for summary in page_summaries:
        font_sizes.update(summary["font_sizes"])
        fonts.update(summary["fonts"])

    print("=" * 80)
    print("PDF PHYSICAL LAYOUT EXPLORATION")
    print("=" * 80)
    print(f"PDF: {PDF_PATH}")
    print(f"Pages: {len(reader.pages)}")
    print(f"Text fragments: {total_fragments:,}")
    print(f"Reconstructed lines: {total_lines:,}")
    print()

    print("FONT SIZES")
    for size, count in font_sizes.most_common(MAX_EXAMPLES):
        print(f"  {size:6.2f} pt: {count:6d} fragments")
    print(f"  ... {len(font_sizes)} distinct sizes")
    print()

    print("FONTS")
    for font, count in fonts.most_common(MAX_EXAMPLES):
        print(f"  {font:35s}: {count:6d} fragments")
    print(f"  ... {len(fonts)} distinct fonts")
    print()

    print("PAGE SAMPLE")
    for summary in page_summaries[:MAX_EXAMPLES]:
        print(
            f"  Page {summary['page']:4d}: "
            f"{summary['width']:.1f} x {summary['height']:.1f} pt, "
            f"fragments={len(summary['fragments'])}, lines={len(summary['lines'])}"
        )
    if len(page_summaries) > MAX_EXAMPLES:
        print(f"  ... {len(page_summaries) - MAX_EXAMPLES} more pages")
    print()

    print_target_examples(page_summaries)
    print("End of exploration.")


if __name__ == "__main__":
    main()
