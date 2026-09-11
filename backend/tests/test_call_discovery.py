from pathlib import Path

from app.application.call_discovery import analyse_call_context, discover_calls
from app.domain.models import Source


SAMPLES = Path(__file__).parent / "samples"


def source(name: str) -> Source:
    return Source(title=name, locator=str(SAMPLES / name))


def test_call_context_identifies_real_call_documents() -> None:
    boe = analyse_call_context(source("BOE-A-2024-14098.pdf").locator and " ")

    assert boe.signals_present == 0


def test_discovers_call_from_boe() -> None:
    calls = discover_calls(source("BOE-A-2024-14098.pdf"))

    assert len(calls) == 1
    assert calls[0].title == "BOE-A-2024-14098.pdf"


def test_discovers_call_from_boja() -> None:
    calls = discover_calls(source("BOJA24-138-00046-48048-01_00304998.pdf"))

    assert len(calls) == 1


def test_does_not_discover_call_from_programme_only_document() -> None:
    calls = discover_calls(source("Programa_Archiveros_0.pdf"))

    assert calls == []


def test_does_not_discover_call_from_unreadable_document() -> None:
    calls = discover_calls(source("OPOS_AYTO_LEON_INFORMATICA_B.pdf"))

    assert calls == []
