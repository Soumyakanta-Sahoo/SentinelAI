from pathlib import Path

from app.main import main


def test_one_shot_search_prints_matching_source(tmp_path: Path, capsys) -> None:
    document = tmp_path / "notes.txt"
    document.write_text("A machine can search these notes.", encoding="utf-8")

    exit_code = main([str(document), "--query", "machine"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Loaded 1 searchable chunk(s)" in output
    assert "Chunk 1 |" in output
    assert "A machine can search these notes." in output


def test_directory_search_loads_supported_files(tmp_path: Path, capsys) -> None:
    (tmp_path / "first.txt").write_text("machine one", encoding="utf-8")
    (tmp_path / "second.txt").write_text("machine two", encoding="utf-8")
    (tmp_path / "ignore.md").write_text("machine ignored", encoding="utf-8")
    hidden_dir = tmp_path / ".venv"
    hidden_dir.mkdir()
    (hidden_dir / "hidden.txt").write_text("machine hidden", encoding="utf-8")

    exit_code = main([str(tmp_path), "--query", "machine"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "machine one" in output
    assert "machine two" in output
    assert "machine ignored" not in output
    assert "machine hidden" not in output


def test_interactive_search_reuses_loaded_document(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    document = tmp_path / "notes.txt"
    document.write_text("machine", encoding="utf-8")
    queries = iter(["machine", "q"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(queries))

    exit_code = main([str(document)])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert output.count("Showing 1 result(s)") == 1
    assert "Goodbye." in output


def test_unsupported_file_returns_user_error(tmp_path: Path, capsys) -> None:
    document = tmp_path / "notes.docx"
    document.write_text("unsupported", encoding="utf-8")

    exit_code = main([str(document), "--query", "notes"])

    assert exit_code == 2
    assert "Supported types are .txt and .pdf" in capsys.readouterr().out
