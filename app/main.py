from pathlib import Path

from app.document_loader import load_text_document


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    document_path = project_root / "sample_documents" / "example.txt"

    try:
        document_text = load_text_document(document_path)

        print("Document loaded successfully.")
        print(f"Characters extracted: {len(document_text)}")
        print("\nDocument contents:")
        print(document_text)

    except (OSError, UnicodeDecodeError, ValueError) as error:
        print(f"Document loading failed: {error}")


if __name__ == "__main__":
    main()
