from pathlib import Path

from app.application.study_programmes import discover_programmes
from app.domain.models import Call, Source

SAMPLES = Path(__file__).parent / "samples"


def source(name: str) -> Source:
    return Source(title=name, locator=str(SAMPLES / name))


def call_for(source_document: Source) -> Call:
    return Call(title=f"Call for {source_document.title}", source_id=source_document.id)


def assert_valid_programmes(programmes, call: Call) -> None:
    assert programmes

    for programme in programmes:
        assert programme.call_id == call.id
        assert programme.identifier
        assert programme.title
        assert programme.units

        previous_end = None
        for unit in programme.units:
            assert unit.number > 0
            assert unit.title
            assert unit.start_page > 0
            assert unit.end_page >= unit.start_page
            assert unit.start_order > 0
            assert unit.end_order >= unit.start_order

            if previous_end is not None:
                assert unit.start_order > previous_end
            previous_end = unit.end_order


def test_boe_programmes_are_complete_and_traceable() -> None:
    source_document = source("BOE-A-2024-14098.pdf")
    call = call_for(source_document)
    programmes = discover_programmes(call, source_document)

    assert len(programmes) == 10
    assert all(programme.units for programme in programmes)
    assert_valid_programmes(programmes, call)


def test_boja_programmes_are_complete_and_traceable() -> None:
    source_document = source("BOJA24-138-00046-48048-01_00304998.pdf")
    call = call_for(source_document)
    programmes = discover_programmes(call, source_document)

    assert len(programmes) == 7
    assert [len(programme.units) for programme in programmes] == [30, 39, 40, 40, 40, 40, 40]
    assert_valid_programmes(programmes, call)


def test_archiveros_programme_is_complete_and_traceable() -> None:
    source_document = source("Programa_Archiveros_0.pdf")
    call = call_for(source_document)
    programmes = discover_programmes(call, source_document)

    assert len(programmes) == 1
    assert len(programmes[0].units) == 25
    assert [unit.number for unit in programmes[0].units] == list(range(1, 26))
    assert_valid_programmes(programmes, call)


def test_scanned_pdf_does_not_produce_false_programmes() -> None:
    source_document = source("OPOS_AYTO_LEON_INFORMATICA_B.pdf")

    assert discover_programmes(call_for(source_document), source_document) == []
