# SentinelAI

[![Tests](https://github.com/Soumyakanta-Sahoo/SentinelAI/actions/workflows/tests.yml/badge.svg)](https://github.com/Soumyakanta-Sahoo/SentinelAI/actions/workflows/tests.yml)
[![Python versions](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

SentinelAI is a local command-line tool for finding relevant passages in text
documents and text-based PDFs. It extracts and chunks documents, ranks matching
chunks by keyword frequency, and reports the source file and PDF page when
available. Documents are processed locally.

The MIT license in this repository applies to SentinelAI's own code. PDF
extraction uses PyMuPDF, which is offered under AGPL and commercial licensing
terms by Artifex. Review the [PyMuPDF licensing information](https://pymupdf.readthedocs.io/en/latest/about.html)
for your intended use and distribution; see [third-party notices](THIRD_PARTY_NOTICES.md).

## Requirements

* Python 3.11 or newer
* Windows, macOS, or Linux

## Install

From the project directory, create and activate a virtual environment, then
install the project:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

On macOS or Linux, activate with `source .venv/bin/activate` instead. For a
runtime-only install, use `python -m pip install .` without the `[dev]` extra.

## Use

Run an interactive session with the bundled example:

```text
sentinelai
```

Or use the Python module directly:

```text
python -m app.main
```

Pass a single file or a directory. Directories are searched recursively for
`.txt` and `.pdf` files. Hidden files and common environment or dependency
directories are skipped:

```text
sentinelai ./research/
sentinelai ./research/report.pdf
```

Run one query and exit (useful in scripts):

```text
sentinelai ./research/ --query "machine learning"
```

Interactive mode accepts multiple queries. Enter `q`, `quit`, or `exit` to
finish. Set result count and chunking parameters with `--limit`, `--chunk-size`,
and `--overlap`. Use `sentinelai --help` to see all options.

## Search behavior and limits

Queries are case-insensitive and split into whole-word terms. A chunk's score is
the total frequency of the distinct query terms it contains; equal scores keep
document order. The default result count is five. Chunks default to 500
characters with 50 characters of overlap.

Text files must be UTF-8. PDFs must contain extractable text; scanned image-only
PDFs require OCR, which is not included. Search is lexical: semantic matching,
answer generation, and a persistent index are not included. On folder searches,
unreadable documents are reported and skipped so the other documents remain
searchable.

## Development

Install development and release tools with
`python -m pip install -e ".[dev,release]"`, then
run the same checks used in CI:

```bash
ruff check .
ruff format --check .
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=80
python -m build
python -m twine check dist/*
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and
[SECURITY.md](SECURITY.md) for vulnerability reporting. Release maintainers
should follow [RELEASING.md](RELEASING.md).
