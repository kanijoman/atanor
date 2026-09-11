from pathlib import Path

from app.application.call_discovery import analyse_call_context, discover_calls
from app.domain.models import Source


SAMPLES = Path(__file__).parent / "samples"


def source(name: str) -> Source:
    return Source(title=name, locator=str(SAMPLES / name))


def test_call_context_requires_combined_call_signals() -> None:
    context = analyse_call_context(
        "convocatoria plazas cuerpo sistema selectivo turno"
    )

    assert context.signals_present == 5
    assert context.strong_signals_present == 4
    assert context.nearby_call_signal_pairs == 4
    assert context.is_strong


def test_call_context_rejects_programme_only_text() -> None:
    context = analyse_call_context("Programa de materias. Cuerpo de Archiveros")

    assert context.signals_present == 1
    assert context.strong_signals_present == 1
    assert context.nearby_call_signal_pairs == 0
    assert not context.is_strong


def test_discovers_call_from_boe() -> None:
    source_document = source("BOE-A-2024-14098.pdf")

    calls = discover_calls(source_document)

    assert len(calls) == 1
    assert calls[0].title == "BOE-A-2024-14098.pdf"
    assert calls[0].source_id == source_document.id


def test_discovers_call_from_boja() -> None:
    calls = discover_calls(source("BOJA24-138-00046-48048-01_00304998.pdf"))

    assert len(calls) == 1


def test_does_not_discover_call_from_programme_only_document() -> None:
    calls = discover_calls(source("Programa_Archiveros_0.pdf"))

    assert calls == []


def test_does_not_discover_call_from_unreadable_document() -> None:
    calls = discover_calls(source("OPOS_AYTO_LEON_INFORMATICA_B.pdf"))

    assert calls == []
