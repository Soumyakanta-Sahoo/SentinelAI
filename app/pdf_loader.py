from pathlib import Path

import pymupdf


def load_pdf_pages(file_path: str | Path) -> list[tuple[int, str]]:
    """Extract text from a PDF, returning each page with its page number."""
    if not str(file_path).strip():
        raise ValueError("File path cannot be empty.")

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.is_dir():
        raise IsADirectoryError(
            f"Expected a PDF file, but received a directory: {path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError("The supplied file must have a .pdf extension.")

    pages = []

    with pymupdf.open(path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            pages.append((page_number, page.get_text()))

    return pages


def load_pdf_document(file_path: str | Path) -> str:
    """Extract PDF text and return it as one string."""
    pages = load_pdf_pages(file_path)
    return "\n".join(page_text for _, page_text in pages)
