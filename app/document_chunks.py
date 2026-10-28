import os
from dataclasses import dataclass
from pathlib import Path

from app.chunker import chunk_text
from app.document_loader import load_text_document
from app.pdf_loader import load_pdf_pages


@dataclass(frozen=True)
class DocumentChunk:
    text: str
    source: str
    page_number: int | None


def load_document_chunks(
    file_path: str | Path,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[DocumentChunk]:
    """Load a supported document and return chunks with source details."""
    if not str(file_path).strip():
        raise ValueError("File path cannot be empty.")

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".txt":
        page_texts = [(None, load_text_document(path))]
    elif extension == ".pdf":
        page_texts = load_pdf_pages(path)
    else:
        raise ValueError(
            f"Unsupported file type: {extension or '[no extension]'}. "
            "Supported types are .txt and .pdf."
        )

    document_chunks = []

    for page_number, text in page_texts:
        for chunk in chunk_text(text, chunk_size, overlap):
            document_chunks.append(
                DocumentChunk(
                    text=chunk,
                    source=str(path),
                    page_number=page_number,
                )
            )

    return document_chunks


def find_supported_documents(path: str | Path) -> list[Path]:
    """Return one supported file or supported files under a directory."""
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(f"Path not found: {root}")
    if root.is_file():
        if root.suffix.lower() not in {".txt", ".pdf"}:
            raise ValueError(
                f"Unsupported file type: {root.suffix or '[no extension]'}. "
                "Supported types are .txt and .pdf."
            )
        return [root]
    if not root.is_dir():
        raise OSError(f"Path is neither a file nor a directory: {root}")

    ignored_directories = {".git", ".venv", "venv", "__pycache__", "node_modules"}
    supported = []

    def raise_walk_error(error: OSError) -> None:
        raise error

    for current, directories, filenames in os.walk(
        root, topdown=True, onerror=raise_walk_error, followlinks=False
    ):
        directories[:] = sorted(
            directory
            for directory in directories
            if not directory.startswith(".")
            and directory.casefold() not in ignored_directories
        )
        for filename in filenames:
            candidate = Path(current) / filename
            if not filename.startswith(".") and candidate.suffix.lower() in {
                ".txt",
                ".pdf",
            }:
                supported.append(candidate)

    return sorted(supported, key=lambda candidate: str(candidate).casefold())
