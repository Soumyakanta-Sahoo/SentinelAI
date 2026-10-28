from pathlib import Path

import pymupdf

from app.document_chunks import load_document_chunks


def test_text_chunks_include_source_filename(tmp_path: Path) -> None:
    text_path = tmp_path / "example.txt"
    text_path.write_text("SentinelAI reads text.", encoding="utf-8")

    chunks = load_document_chunks(text_path)

    assert len(chunks) == 1
    assert chunks[0].text == "SentinelAI reads text."
    assert chunks[0].source == str(text_path)
    assert chunks[0].page_number is None


def test_pdf_chunks_include_source_and_page_number(tmp_path: Path) -> None:
    pdf_path = tmp_path / "example.pdf"

    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((72, 72), "SentinelAI reads PDF pages.")
        pdf.save(pdf_path)

    chunks = load_document_chunks(pdf_path)

    assert len(chunks) == 1
    assert "SentinelAI reads PDF pages." in chunks[0].text
    assert chunks[0].source == str(pdf_path)
    assert chunks[0].page_number == 1
