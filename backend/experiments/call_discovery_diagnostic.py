"""Diagnostic experiment for call-discovery signals in real sample PDFs.

This experiment intentionally does not introduce a production Call discovery API,
new domain models, or persistence. It composes existing document processing,
programme discovery, and requirement discovery capabilities and reports the
signals they already provide for candidate call identification.

Run from the backend directory:
    python experiments/call_discovery_diagnostic.py
"""

from pathlib import Path

from app.application.document_processing import process_document
from app.application.requirement_discovery import PdfRequirementDiscoveryStrategy
from app.application.requirement_discovery import discover_requirements
from app.application.study_programmes import discover_programmes
from app.domain.models import Call, Source


SAMPLES_DIR = Path(__file__).resolve().parents[1] / "tests" / "samples"
SAMPLE_NAMES = (
    "BOE-A-2024-14098.pdf",
    "BOJA24-138-00046-48048-01_00304998.pdf",
    "Programa_Archiveros_0.pdf",
    "OPOS_AYTO_LEON_INFORMATICA_B.pdf",
)


def _signal_level(programme_count: int, requirement_count: int) -> str:
    """Provide a diagnostic-only signal level from existing capabilities."""
    if programme_count > 0 and requirement_count > 0:
        return "HIGH"
    if programme_count > 0:
        return "LOW"
    return "NONE"


def analyse_sample(path: Path) -> dict[str, object]:
    source = Source(title=path.name, locator=str(path))
    processing = process_document(source)

    # A synthetic Call is used only to exercise the existing programme discovery
    # API. No Call is persisted and no call identity is inferred here.
    call = Call(title=source.title, source_id=source.id)
    programmes = discover_programmes(call, source)
    requirements = discover_requirements(source, PdfRequirementDiscoveryStrategy())

    structural = sum(
        marker.classification == "STRUCTURAL" for marker in processing.structure
    )
    enumerations = sum(
        marker.classification == "ENUMERATION" for marker in processing.structure
    )
    programme_units = sum(len(programme.units) for programme in programmes)

    return {
        "sample": path.name,
        "extracted_characters": len(processing.text),
        "structure_markers": len(processing.structure),
        "structural_markers": structural,
        "enumeration_markers": enumerations,
        "programmes": len(programmes),
        "programme_units": programme_units,
        "requirement_mentions": len(requirements),
        "signal": _signal_level(len(programmes), len(requirements)),
    }


def main() -> None:
    print("CALL DISCOVERY DIAGNOSTIC")
    print("=" * 80)
    print("Diagnostic only: no Call or other domain entity is persisted.")
    print()

    for sample_name in SAMPLE_NAMES:
        path = SAMPLES_DIR / sample_name
        if not path.is_file():
            print(f"{sample_name}: MISSING")
            continue

        result = analyse_sample(path)
        print(result["sample"])
        print(f"  extracted characters: {result['extracted_characters']}")
        print(f"  structure markers:    {result['structure_markers']}")
        print(f"    structural:         {result['structural_markers']}")
        print(f"    enumerations:       {result['enumeration_markers']}")
        print(f"  programmes:           {result['programmes']}")
        print(f"  programme units:      {result['programme_units']}")
        print(f"  requirement mentions: {result['requirement_mentions']}")
        print(f"  diagnostic signal:    {result['signal']}")
        print()


if __name__ == "__main__":
    main()
