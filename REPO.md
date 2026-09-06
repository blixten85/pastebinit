# REPO.md

`Pastebinit` är ett Python-projekt med tester under `tests/` och Debian-paketering under `debian/`.

## Invarians

- `pyproject.toml` är källa till sanning för paketversionen.
- Versionen `MAJOR.MINOR.PATCH` ska matcha stabil release-tagg `vMAJOR.MINOR.PATCH`.

## Validering

- Läs `pyproject.toml`, berörda tester och relevanta Debian-filer innan relaterat beteende ändras.
- Kör relevanta pytest-, compile- och build-kontroller för den ändrade delen.
- När `debian/` eller Debian-paketgenerering ändras, kör förrådets Debian-validering.
