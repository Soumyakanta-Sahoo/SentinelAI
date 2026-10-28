# Contributing

Thanks for helping improve SentinelAI. Bug reports, focused fixes, and
documentation improvements are welcome.

## Before you start

* Search existing issues before opening a new one.
* For a substantial change, open an issue first so its scope can be discussed.
* Never commit private documents, extracted text, credentials, or other personal
  data. Tests should create temporary documents in the test fixture directory.

## Local setup

Use Python 3.11 or newer and create a virtual environment:

```bash
python -m venv .venv
```

Activate it, then install the project and development tools:

```bash
python -m pip install -e ".[dev,release]"
```

## Make and verify a change

Keep pull requests focused and add or update tests for behavior changes. Before
opening a pull request, run:

```bash
ruff check .
ruff format --check .
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=80
python -m build
python -m twine check dist/*
```

Describe the user-visible behavior, the reason for the change, and the checks
you ran. Update the README when commands, supported files, or search behavior
change.
