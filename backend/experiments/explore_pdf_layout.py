from collections import Counter
from pathlib import Path

from pypdf import PdfReader


PDF_PATH = Path("tests/samples/BOE-A-2024-14098.pdf")
MAX_EXAMPLES = 12
Y_TOLERANCE = 2.0


def extract_fragments(page) -> list[dict]:
    """Collect text fragments together with physical PDF layout metadata."""
    fragments = []

    def visitor_text(text, cm, tm, font_dict, font_size):
        text = text.replace("\n", "\\n")
        if not text.strip():
            return

        fragments.append(
            {
                "text": text,
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

    font_sizes = Counter(fragment["font_size"] for fragment in fragments)
    fonts = Counter(fragment["font"] for fragment in fragments)

    return {
        "page": page_number,
        "width": round(float(page.mediabox.width), 2),
        "height": round(float(page.mediabox.height), 2),
        "fragments": fragments,
        "lines": lines,
        "font_sizes": font_sizes,
        "fonts": fonts,
    }


def print_fragment_examples(fragments: list[dict]) -> None:
    print("TEXT FRAGMENT EXAMPLES")
    for fragment in fragments[:MAX_EXAMPLES]:
        print(
            f"  ({fragment['x']:7.2f}, {fragment['y']:7.2f}) "
            f"size={fragment['font_size']:5.2f} "
            f"font={fragment['font']} "
            f"flags={fragment['font_flags']} "
            f"text={fragment['text']!r}"
        )
    print()


def print_line_examples(lines: list[list[dict]]) -> None:
    print("RECONSTRUCTED LINE EXAMPLES")
    for line in lines[:MAX_EXAMPLES]:
        text = line_text(line)
        sizes = sorted({fragment["font_size"] for fragment in line})
        x = min(fragment["x"] for fragment in line)
        y = line[0]["y"]
        print(f"  ({x:7.2f}, {y:7.2f}) sizes={sizes} text={text!r}")
    print()


def print_target_context(page_summaries: list[dict], terms: tuple[str, ...]) -> None:
    print("TARGET CONTEXT")

    for summary in page_summaries:
        lines = summary["lines"]
        for index, line in enumerate(lines):
            text = line_text(line)
            if any(term.casefold() in text.casefold() for term in terms):
                print(f"  Page {summary['page']}, line {index + 1}:")
                start = max(0, index - 1)
                end = min(len(lines), index + 2)
                for current in range(start, end):
                    marker = ">>" if current == index else "  "
                    current_line = lines[current]
                    current_text = line_text(current_line)
                    sizes = sorted({f["font_size"] for f in current_line})
                    x = min(f["x"] for f in current_line)
                    y = current_line[0]["y"]
                    print(
                        f"    {marker} ({x:7.2f}, {y:7.2f}) "
                        f"sizes={sizes} {current_text!r}"
                    )
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

    print("PAGE DIMENSIONS")
    for summary in page_summaries[:MAX_EXAMPLES]:
        print(
            f"  Page {summary['page']:4d}: "
            f"{summary['width']:7.2f} x {summary['height']:7.2f} pt, "
            f"fragments={len(summary['fragments']):4d}, "
            f"lines={len(summary['lines']):4d}"
        )
    if len(page_summaries) > MAX_EXAMPLES:
        print(f"  ... {len(page_summaries) - MAX_EXAMPLES} more pages")
    print()

    print("FONT SIZES")
    for size, count in font_sizes.most_common(MAX_EXAMPLES):
        print(f"  {size:6.2f} pt: {count:6d} fragments")
    print()

    print("FONTS")
    for font, count in fonts.most_common(MAX_EXAMPLES):
        print(f"  {font:40s}: {count:6d} fragments")
    print()

    if page_summaries:
        first_page = page_summaries[0]
        print(f"FIRST PAGE ({first_page['page']})")
        print_fragment_examples(first_page["fragments"])
        print_line_examples(first_page["lines"])

    print_target_context(page_summaries, ("Programa", "ANEXO"))

    print("End of exploration.")


if __name__ == "__main__":
    main()
