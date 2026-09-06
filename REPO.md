# REPO.md

`pastebinit` is a Python project with tests under `tests/` and Debian packaging under `debian/`.

## Validation

- Read `pyproject.toml`, affected tests and relevant Debian packaging files before changing related behavior.
- Run relevant pytest/compile/build checks for the changed area.
- When `debian/` or Debian package generation changes, run the repository's Debian packaging validation.
- `pyproject.toml` is the package version source; version `MAJOR.MINOR.PATCH` must match stable release tag `vMAJOR.MINOR.PATCH`.
- The default-branch ruleset currently requires the `python` check. Do not rename it without updating and verifying that ruleset in the same migration.
- Pin third-party GitHub Actions and shared reusable workflows to full commit SHAs.
