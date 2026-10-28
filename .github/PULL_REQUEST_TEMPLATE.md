## Summary

<!-- What changed and why? -->

## Verification

- [ ] `ruff check .`
- [ ] `ruff format --check .`
- [ ] `python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=80`
- [ ] `python -m build` and `python -m twine check dist/*`

## Checklist

- [ ] I added or updated tests for behavior changes.
- [ ] I updated documentation when user-visible behavior changed.
- [ ] I did not include private documents, extracted text, credentials, or user
      data.
