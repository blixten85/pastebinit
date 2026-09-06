# REPO.md

`pastebinit` is a Python project with tests under `tests/` and Debian packaging under `debian/`.

## Validation

- Read `pyproject.toml`, affected tests and relevant Debian packaging files before changing related behavior.
- Run relevant pytest/compile/build checks for the changed area. Validate Debian packaging when `debian/` or release packaging changes.
- `pyproject.toml` is the Python package version source and must match stable `vMAJOR.MINOR.PATCH` releases.

The live repository rules currently require the `python` check. Do not rename a required check without updating and verifying the live ruleset in the same migration.

Pin third-party GitHub Actions and shared reusable workflows to immutable full commit SHAs.
