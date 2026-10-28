import pytest

from app.chunker import chunk_text


def test_chunk_text_splits_long_text() -> None:
    text = "one two three four five six seven eight nine ten"

    chunks = chunk_text(text, chunk_size=15, overlap=3)

    assert len(chunks) > 1
    assert all(len(chunk) <= 15 for chunk in chunks)


def test_chunk_text_returns_short_text_as_one_chunk() -> None:
    text = "SentinelAI reads documents."

    assert chunk_text(text) == [text]


def test_chunk_text_returns_no_chunks_for_whitespace() -> None:
    assert chunk_text("   \n  ") == []


def test_chunk_text_rejects_invalid_chunk_size() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        chunk_text("some text", chunk_size=0)


def test_chunk_text_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError, match="smaller than chunk size"):
        chunk_text("some text", chunk_size=10, overlap=10)
