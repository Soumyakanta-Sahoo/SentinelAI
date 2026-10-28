# Releasing SentinelAI

Releases are currently built and published manually. CI validates and stores
the source distribution and wheel as workflow artifacts; it does not publish
to PyPI or create GitHub releases automatically.

## Checklist

1. Confirm the intended use and distribution comply with the PyMuPDF terms in
   [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
2. Update `version` in `pyproject.toml` and move the completed changes from
   `[Unreleased]` in `CHANGELOG.md` into a dated version section.
3. Run the checks in [CONTRIBUTING.md](CONTRIBUTING.md) and review the built
   archives with `twine check`.
4. Review the Git diff, generated archive contents, and license notices.
5. Create a version tag and GitHub release only after the checks pass.
6. Publish to a package index only after configuring its trusted publishing
   permissions and reviewing the package metadata and dependency licensing.
