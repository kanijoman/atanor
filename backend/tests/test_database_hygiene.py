from app.domain.models import Source
from scripts.check_database_hygiene import _find_synthetic_records


def test_known_boe_validation_source_is_not_reported_as_synthetic() -> None:
    source = Source(
        title="BOE-A-2024-14098.pdf",
        locator="tests\\samples\\BOE-A-2024-14098.pdf",
    )

    records = _find_synthetic_records([source], [], [], [])

    assert records == ()


def test_archiveros_sample_is_reported_as_synthetic() -> None:
    source = Source(
        title="Programa_Archiveros_0.pdf",
        locator="tests\\samples\\Programa_Archiveros_0.pdf",
    )

    records = _find_synthetic_records([source], [], [], [])

    assert len(records) == 1
    assert records[0].marker == "test"


def test_obvious_synthetic_source_is_reported_as_synthetic() -> None:
    source = Source(
        title="dummy.pdf",
        locator="tests\\samples\\dummy.pdf",
    )

    records = _find_synthetic_records([source], [], [], [])

    assert len(records) == 2
    assert {record.marker for record in records} == {"dummy", "test"}
