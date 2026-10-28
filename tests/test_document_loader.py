from pathlib import Path

import pytest

from app.document_loader import load_text_document


def test_load_text_document_success(tmp_path: Path) -> None:
    document = tmp_path / "example.txt"
    expected_text = "SentinelAI reads documents."

    document.write_text(expected_text, encoding="utf-8")

    result = load_text_document(document)

    assert result == expected_text


def test_load_empty_document(tmp_path: Path) -> None:
    document = tmp_path / "empty.txt"
    document.write_text("", encoding="utf-8")

    result = load_text_document(document)

    assert result == ""


def test_missing_document_raises_error(tmp_path: Path) -> None:
    document = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        load_text_document(document)


def test_directory_instead_of_file_raises_error(tmp_path: Path) -> None:
    directory = tmp_path / "documents"
    directory.mkdir()

    with pytest.raises(IsADirectoryError):
        load_text_document(directory)


def test_empty_path_raises_error() -> None:
    with pytest.raises(ValueError, match="File path cannot be empty"):
        load_text_document("")


def test_invalid_utf8_document_raises_error(tmp_path: Path) -> None:
    document = tmp_path / "invalid.txt"
    document.write_bytes(b"\x80\x81\x82")

    with pytest.raises(UnicodeDecodeError):
        load_text_document(document)
