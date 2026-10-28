import argparse
from collections.abc import Sequence
from pathlib import Path

from app.document_chunks import (
    DocumentChunk,
    find_supported_documents,
    load_document_chunks,
)
from app.document_loader import load_text_document
from app.pdf_loader import load_pdf_document
from app.search import SearchResult, search_chunks


def load_document(file_path: str | Path) -> str:
    """Load a supported document as text (kept for simple library use)."""
    path = Path(file_path)
    if path.suffix.lower() == ".txt":
        return load_text_document(path)
    if path.suffix.lower() == ".pdf":
        return load_pdf_document(path)
    raise ValueError(
        f"Unsupported file type: {path.suffix or '[no extension]'}. "
        "Supported types are .txt and .pdf."
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentinelai",
        description="Search text and text-based PDF documents by keyword.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="a .txt/.pdf file or a directory to search (default: bundled sample)",
    )
    parser.add_argument(
        "-q", "--query", help="run one search and exit; omit for interactive search"
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=5,
        help="maximum results per query (default: 5)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="chunk length in characters (default: 500)",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=50,
        help="overlap between chunks in characters (default: 50)",
    )
    return parser


def _show_results(results: list[SearchResult]) -> None:
    if not results:
        print("No matching chunks found.")
        return

    print(f"\nShowing {len(results)} result(s):")
    for result in results:
        chunk = result.chunk
        location = chunk.source
        if chunk.page_number is not None:
            location += f" — page {chunk.page_number}"
        print(f"\nChunk {result.chunk_number} | {location}")
        print(f"Keyword matches: {result.score}")
        print(chunk.text)


def _interactive_search(chunks: list[DocumentChunk], limit: int) -> None:
    print("Enter keywords to search. Enter 'q' or press Ctrl+C to quit.")
    while True:
        try:
            query = input("\nSearch> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return

        if query.casefold() in {"q", "quit", "exit"}:
            print("Goodbye.")
            return
        if not query:
            print("Enter one or more keywords, or 'q' to quit.")
            continue
        _show_results(search_chunks(chunks, query, limit=limit))


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.limit < 1:
        parser.error("--limit must be at least 1")
    if args.chunk_size <= 0:
        parser.error("--chunk-size must be greater than zero")
    if args.overlap < 0 or args.overlap >= args.chunk_size:
        parser.error("--overlap must be non-negative and smaller than --chunk-size")

    path = (
        Path(args.path)
        if args.path
        else Path(__file__).resolve().parent / "sample_documents" / "example.txt"
    )
    if not path.is_absolute():
        path = Path.cwd() / path

    try:
        documents = find_supported_documents(path)
    except (OSError, ValueError) as error:
        print(f"Could not use '{path}': {error}")
        return 2

    if not documents:
        print(f"No .txt or .pdf documents found in '{path}'.")
        return 1

    chunks: list[DocumentChunk] = []
    failed = 0
    for document in documents:
        try:
            chunks.extend(
                load_document_chunks(
                    document, chunk_size=args.chunk_size, overlap=args.overlap
                )
            )
        except Exception as error:
            failed += 1
            print(f"Could not load '{document}': {error}")

    if not chunks:
        if failed == 0:
            print("The document(s) loaded, but contained no searchable text.")
        return 1

    print(
        f"Loaded {len(chunks)} searchable chunk(s) "
        f"from {len(documents) - failed} document(s)."
    )
    if failed:
        print(f"Skipped {failed} document(s) that could not be read.")

    if args.query is not None:
        if not args.query.strip():
            parser.error("--query cannot be empty")
        _show_results(search_chunks(chunks, args.query, limit=args.limit))
    else:
        _interactive_search(chunks, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
