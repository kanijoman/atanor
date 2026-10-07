from pathlib import Path

import pytest

from app.application.study_support_report import build_support_report, format_support_report
from app.cli import main

SAMPLES = Path(__file__).parent / "samples"
BOE_SAMPLE = SAMPLES / "BOE-A-2024-14098.pdf"


def test_report_counts_supported_units_for_the_boe_sample() -> None:
    report = build_support_report(BOE_SAMPLE)

    assert report.call_detected
    assert report.unit_count > 0
    assert 0 < report.supported_count < report.unit_count
    supported_topics = {
        unit.topic for programme in report.programmes for unit in programme.units if unit.supported
    }
    assert (
        "Las Leyes del Procedimiento Administrativo Común y del Régimen Jurídico del Sector Público"
        in supported_topics
    )


def test_report_marks_supported_and_unsupported_units() -> None:
    text = format_support_report(build_support_report(BOE_SAMPLE))

    assert "units supported" in text
    assert "[x] 11. Las Leyes del Procedimiento Administrativo Común" in text
    assert "[ ] " in text


def test_report_rejects_missing_files(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        build_support_report(tmp_path / "missing.pdf")


def test_cli_prints_a_report_for_each_pdf(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["study-support-report", str(BOE_SAMPLE)])

    assert exit_code == 0
    assert "BOE-A-2024-14098.pdf: call detected" in capsys.readouterr().out
