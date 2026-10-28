from pathlib import Path

import pymupdf
import pytest

from app.pdf_loader import load_pdf_document


def create_test_pdf(path: Path, text: str) -> None:
    """Create a small PDF for testing."""
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((72, 72), text)
        pdf.save(path)


def test_load_pdf_success(tmp_path: Path) -> None:
    pdf_path = tmp_path / "example.pdf"
    create_test_pdf(pdf_path, "SentinelAI reads PDF documents.")

    result = load_pdf_document(pdf_path)

    assert "SentinelAI reads PDF documents." in result


def test_load_empty_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "empty.pdf"

    with pymupdf.open() as pdf:
        pdf.new_page()
        pdf.save(pdf_path)

    result = load_pdf_document(pdf_path)

    assert result == ""


def test_missing_pdf_raises_error(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_pdf_document(tmp_path / "missing.pdf")


def test_directory_raises_error(tmp_path: Path) -> None:
    directory = tmp_path / "documents"
    directory.mkdir()

    with pytest.raises(IsADirectoryError):
        load_pdf_document(directory)


def test_non_pdf_file_raises_error(tmp_path: Path) -> None:
    text_file = tmp_path / "example.txt"
    text_file.write_text("This is not a PDF.", encoding="utf-8")

    with pytest.raises(ValueError, match="must have a .pdf extension"):
        load_pdf_document(text_file)


def test_empty_path_raises_error() -> None:
    with pytest.raises(ValueError, match="File path cannot be empty"):
        load_pdf_document("")
