from pathlib import Path


def load_text_document(file_path: str | Path) -> str:
    """
    Load and return the contents of a UTF-8 text document.
    """
    if not str(file_path).strip():
        raise ValueError("File path cannot be empty.")

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    if path.is_dir():
        raise IsADirectoryError(f"Expected a file, but received a directory: {path}")

    with path.open("r", encoding="utf-8") as file:
        content = file.read()

    return content
