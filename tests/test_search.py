from app.document_chunks import DocumentChunk
from app.search import search_chunks


def make_chunk(text: str, source: str = "example.txt") -> DocumentChunk:
    return DocumentChunk(text=text, source=source, page_number=None)


def test_search_matches_case_insensitively() -> None:
    chunks = [make_chunk("The Machine reads documents.")]

    results = search_chunks(chunks, "mAcHiNe")

    assert len(results) == 1
    assert results[0].chunk.text == "The Machine reads documents."
    assert results[0].score == 1


def test_search_ranks_by_query_term_occurrences() -> None:
    chunks = [
        make_chunk("machine tools"),
        make_chunk("machine machine tools"),
    ]

    results = search_chunks(chunks, "machine tools")

    assert [result.chunk_number for result in results] == [2, 1]
    assert [result.score for result in results] == [3, 2]


def test_search_preserves_document_order_for_equal_scores() -> None:
    chunks = [make_chunk("machine A"), make_chunk("machine B")]

    results = search_chunks(chunks, "machine")

    assert [result.chunk_number for result in results] == [1, 2]


def test_search_respects_result_limit() -> None:
    chunks = [make_chunk(f"machine {index}") for index in range(4)]

    results = search_chunks(chunks, "machine", limit=2)

    assert [result.chunk_number for result in results] == [1, 2]
