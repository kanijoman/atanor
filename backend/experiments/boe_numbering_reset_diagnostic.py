from pathlib import Path

from app.application.study_programmes import (
    BoeProgrammeDiscoveryStrategy,
    _extract_units,
)
from app.domain.models import Source


SAMPLE = Path(__file__).parent.parent / "tests" / "samples" / "BOE-A-2024-14098.pdf"
CONTEXT = 3


def run(pdf_path: Path = SAMPLE) -> None:
    """Print context around top-level numbering resets inside BOE annexes."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"Sample not found: {pdf_path}")

    source = Source(title=pdf_path.name, locator=str(pdf_path))
    units = _extract_units(source)
    strategy = BoeProgrammeDiscoveryStrategy()

    annexes = [
        (index, match.group(1).upper())
        for index, unit in enumerate(units)
        if (match := strategy._ANNEX.fullmatch(unit.text))
    ]

    print("BOE numbering reset diagnostic")
    print("==============================")
    print(f"Source: {source.title}")
    print()

    for annex_position, (annex_index, identifier) in enumerate(annexes):
        next_annex = (
            annexes[annex_position + 1][0]
            if annex_position + 1 < len(annexes)
            else len(units)
        )
        programme_index = next(
            (
                index
                for index in range(annex_index + 1, next_annex)
                if strategy._PROGRAMME.fullmatch(units[index].text)
            ),
            None,
        )
        if programme_index is None:
            continue

        candidates = []
        for index in range(programme_index + 1, next_annex):
            match = strategy._TOP_LEVEL.fullmatch(units[index].text)
            if match and not strategy._NON_PROGRAMME_SECTION.match(match.group(2)):
                candidates.append((index, int(match.group(1)), match.group(2)))

        resets = [
            candidate
            for previous, candidate in zip(candidates, candidates[1:])
            if candidate[1] <= previous[1]
        ]

        print(f"ANEXO {identifier}")
        print(f"  candidates: {len(candidates)}")
        print(f"  numbering resets: {len(resets)}")

        if not resets:
            print("  No numbering reset detected.")
            print()
            continue

        for index, number, title in resets:
            print()
            print(f"  RESET -> {number}. {title}")
            print("  Context:")
            start = max(programme_index + 1, index - CONTEXT)
            end = min(next_annex, index + CONTEXT + 1)
            for context_index in range(start, end):
                marker = "  >>" if context_index == index else "    "
                unit = units[context_index]
                print(
                    f"{marker} page={unit.page} order={unit.order}: {unit.text}"
                )

        print()


if __name__ == "__main__":
    run()
