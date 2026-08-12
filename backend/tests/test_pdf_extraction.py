from pathlib import Path

import pytest

from app.application.pdf import extract_pdf_text
from app.domain.models import Source


def _pdf_with_pages(*texts: str) -> bytes:
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R 6 0 R] /Count 2 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        None,
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 8 0 R >> >> /Contents 7 0 R >>",
        None,
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    for index, text in enumerate(texts):
        stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
        objects[index * 4 + 3] = (
            b"<< /Length "
            + str(len(stream)).encode()
            + b" >>\nstream\n"
            + stream
            + b"\nendstream"
        )

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for object_number, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output += f"{object_number} 0 obj\n".encode() + obj + b"\nendobj\n"

    xref_offset = len(output)
    output += f"xref\n0 {len(objects) + 1}\n".encode()
    output += b"0000000000 65535 f \n"
    for offset in offsets[1:]:
        output += f"{offset:010d} 00000 n \n".encode()
    output += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    ).encode()
    return bytes(output)


def test_extract_pdf_text_returns_page_content_in_order(tmp_path: Path) -> None:
    pdf_path = tmp_path / "call.pdf"
    pdf_path.write_bytes(_pdf_with_pages("First page", "Second page"))
    source = Source(title=pdf_path.name, locator=str(pdf_path))

    result = extract_pdf_text(source)

    assert result == "First page\nSecond page"


def test_extract_pdf_text_requires_a_source_locator() -> None:
    source = Source(title="call.pdf")

    with pytest.raises(ValueError, match="must have a locator"):
        extract_pdf_text(source)


def test_extract_pdf_text_requires_an_existing_file(tmp_path: Path) -> None:
    source = Source(title="call.pdf", locator=str(tmp_path / "missing.pdf"))

    with pytest.raises(FileNotFoundError, match="Source file not found"):
        extract_pdf_text(source)


def test_extract_pdf_text_rejects_non_pdf_sources(tmp_path: Path) -> None:
    file_path = tmp_path / "call.txt"
    file_path.write_text("not a pdf", encoding="utf-8")
    source = Source(title=file_path.name, locator=str(file_path))

    with pytest.raises(ValueError, match="must be a PDF"):
        extract_pdf_text(source)
