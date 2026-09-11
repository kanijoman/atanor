"""Diagnostic experiment for call-context signals in real sample PDFs.

The experiment composes existing PDF extraction and document processing only. It
looks for deterministic textual signals that distinguish a competitive-exam call
from a programme-only document.

Run from the backend directory:
    python experiments/call_context_diagnostic.py
"""

from __future__ import annotations

import re
from pathlib import Path

from app.application.document_processing import process_document
from app.domain.models import Source


SAMPLES_DIR = Path(__file__).resolve().parents[1] / "tests" / "samples"
SAMPLE_NAMES = (
    "BOE-A-2024-14098.pdf",
    "BOJA24-138-00046-48048-01_00304998.pdf",
    "Programa_Archiveros_0.pdf",
    "OPOS_AYTO_LEON_INFORMATICA_B.pdf",
)

SIGNALS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("convocatoria", (r"\bconvocatoria\b", r"\bconvocatoria[s]?\b")),
    ("plazas", (r"\bplazas?\b",)),
    ("cuerpo_escala", (r"\bcuerpo[s]?\b", r"\bescala[s]?\b")),
    ("sistema_selectivo", (r"\bsistema\s+selectivo\b",)),
    ("turno", (r"\bturno[s]?\b",)),
    ("organo_convocante", (r"\b[oó]rgano\s+convocante\b",)),
    ("resolucion_orden", (r"\bresoluci[oó]n(?:es)?\b", r"\borden(?:es)?\b")),
    ("fecha", (r"\bfecha\b", r"\bde\s+\d{1,2}\s+de\s+\w+\s+de\s+\d{4}\b")),
)


def _count_matches(text: str, patterns: tuple[str, ...]) -> int:
    return sum(len(re.findall(pattern, text, flags=re.IGNORECASE)) for pattern in patterns)


def _positions(text: str, patterns: tuple[str, ...]) -> list[int]:
    positions: list[int] = []
    for pattern in patterns:
        positions.extend(match.start() for match in re.finditer(pattern, text, flags=re.IGNORECASE))
    return sorted(positions)


def _has_nearby_signals(
    text: str,
    signal_a: tuple[str, ...],
    signal_b: tuple[str, ...],
    window: int = 3000,
) -> bool:
    positions_a = _positions(text, signal_a)
    positions_b = _positions(text, signal_b)
    return any(abs(a - b) <= window for a in positions_a for b in positions_b)


def analyse_sample(path: Path) -> dict[str, object]:
    source = Source(title=path.name, locator=str(path))
    processing = process_document(source)
    text = processing.text

    counts = {
        name: _count_matches(text, patterns) for name, patterns in SIGNALS
    }
    present = {name: count > 0 for name, count in counts.items()}

    strong_names = {
        "convocatoria",
        "plazas",
        "cuerpo_escala",
        "sistema_selectivo",
        "organo_convocante",
    }
    strong_present = sum(present[name] for name in strong_names)
    total_present = sum(present.values())

    signal_patterns = dict(SIGNALS)
    call_context_pairs = (
        ("convocatoria", "plazas"),
        ("convocatoria", "cuerpo_escala"),
        ("plazas", "sistema_selectivo"),
        ("cuerpo_escala", "sistema_selectivo"),
    )
    nearby_pairs = sum(
        _has_nearby_signals(text, signal_patterns[left], signal_patterns[right])
        for left, right in call_context_pairs
    )

    if len(text.strip()) < 100:
        confidence = "UNKNOWN"
    elif strong_present >= 3 and nearby_pairs >= 2:
        confidence = "HIGH"
    elif strong_present >= 2 or total_present >= 4:
        confidence = "MEDIUM"
    elif strong_present == 1 or total_present >= 2:
        confidence = "LOW"
    else:
        confidence = "NONE"

    return {
        "sample": path.name,
        "extracted_characters": len(text),
        "signals": counts,
        "signals_present": total_present,
        "strong_signals_present": strong_present,
        "nearby_call_signal_pairs": nearby_pairs,
        "confidence": confidence,
    }


def main() -> None:
    print("CALL CONTEXT DIAGNOSTIC")
    print("=" * 80)
    print("Diagnostic only: no Call is created or persisted.")
    print()

    for sample_name in SAMPLE_NAMES:
        path = SAMPLES_DIR / sample_name
        if not path.is_file():
            print(f"{sample_name}: MISSING")
            continue

        result = analyse_sample(path)
        print(result["sample"])
        print(f"  extracted characters:       {result['extracted_characters']}")
        print(f"  signals present:            {result['signals_present']}")
        print(f"  strong signals present:     {result['strong_signals_present']}")
        print(f"  nearby call signal pairs:   {result['nearby_call_signal_pairs']}")
        print(f"  confidence:                 {result['confidence']}")
        print("  signal counts:")
        for name, count in result["signals"].items():
            print(f"    {name:24} {count}")
        print()


if __name__ == "__main__":
    main()
