import re
from collections import Counter
from dataclasses import dataclass

from app.document_chunks import DocumentChunk


@dataclass(frozen=True)
class SearchResult:
    """A matching chunk, its one-based document position, and match score."""

    chunk: DocumentChunk
    chunk_number: int
    score: int


def search_chunks(
    chunks: list[DocumentChunk], query: str, limit: int = 5
) -> list[SearchResult]:
    """Rank chunks by how many distinct query terms they contain.

    Matching is case-insensitive and based on whole word tokens. Equal scores
    keep the original document order so results are predictable.
    """
    if limit < 0:
        raise ValueError("Result limit cannot be negative.")

    terms = set(re.findall(r"\w+", query.casefold()))
    if not terms or limit == 0:
        return []

    results = []
    for chunk_number, chunk in enumerate(chunks, start=1):
        frequencies = Counter(re.findall(r"\w+", chunk.text.casefold()))
        score = sum(frequencies[term] for term in terms)
        if score:
            results.append(SearchResult(chunk, chunk_number, score))

    results.sort(key=lambda result: (-result.score, result.chunk_number))
    return results[:limit]
