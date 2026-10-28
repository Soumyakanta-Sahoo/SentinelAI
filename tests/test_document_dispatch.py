from pathlib import Path

import pymupdf
import pytest

from app.main import load_document


def test_load_document_dispatches_by_extension(tmp_path: Path) -> None:
    text = "SentinelAI reads text documents."
    text_path = tmp_path / "example.txt"
    text_path.write_text(text, encoding="utf-8")

    pdf_path = tmp_path / "example.pdf"
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((72, 72), "SentinelAI reads PDF documents.")
        pdf.save(pdf_path)

    assert load_document(text_path) == text
    assert "SentinelAI reads PDF documents." in load_document(pdf_path)


def test_load_document_rejects_unsupported_extension(tmp_path: Path) -> None:
    document_path = tmp_path / "example.docx"
    document_path.write_text("unsupported", encoding="utf-8")

    with pytest.raises(ValueError, match="Supported types are .txt and .pdf"):
        load_document(document_path)
