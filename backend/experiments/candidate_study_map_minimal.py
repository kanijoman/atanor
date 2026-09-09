from pathlib import Path

from app.application.study_programmes import discover_programmes
from app.domain.models import Source


SAMPLE = Path(__file__).parent.parent / "tests" / "samples" / "BOE-A-2024-14098.pdf"


def run(pdf_path: Path = SAMPLE) -> None:
    """Print the smallest candidate-readable study map from a real BOE call."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"Sample not found: {pdf_path}")

    source = Source(title=pdf_path.name, locator=str(pdf_path))
    programmes = discover_programmes(source)

    print("Study map")
    print("=========")
    print(f"Source: {source.title}")
    print()

    if not programmes:
        print("No study programmes discovered.")
        return

    for programme in programmes:
        print(f"Programme {programme.identifier}")
        for unit in programme.units:
            print(f"  {unit.number}. {unit.title}")
        print()


if __name__ == "__main__":
    run()
