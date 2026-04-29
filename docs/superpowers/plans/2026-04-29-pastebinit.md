# pastebinit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite pastebinit from scratch as a modern Python package with full per-backend API integration, encrypted credentials, and a proper Debian package.

**Architecture:** Python package (`pastebinit/`) with one file per backend under `backends/`, a shared `BasePastebin` ABC, TOML config, Fernet-encrypted keystore, and argparse CLI. Tested with pytest + `unittest.mock`. Distributed as a `.deb` built in CI.

**Tech Stack:** Python 3.10+, `cryptography` (Fernet/PBKDF2), `keyring`, `tomllib` (stdlib 3.11+) / `tomli`, `tomli-w`, `xmlrpc.client` (stdlib), `urllib` (stdlib), `pytest`, `dpkg-buildpackage`

---

## File Map

```
pastebinit/
├── pastebinit/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── credentials.py
│   ├── syntax.py
│   └── backends/
│       ├── __init__.py
│       ├── base.py
│       ├── pastebin_com.py
│       ├── dpaste.py
│       ├── paste_debian_net.py
│       ├── paste_ubuntu_com.py
│       ├── sprunge.py
│       ├── paste_opendev.py
│       ├── bpa_st.py
│       └── paste_opensuse.py
├── tests/
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_credentials.py
│   ├── test_syntax.py
│   ├── test_cli.py
│   └── backends/
│       ├── test_pastebin_com.py
│       ├── test_dpaste.py
│       ├── test_paste_debian_net.py
│       ├── test_paste_ubuntu_com.py
│       ├── test_sprunge.py
│       ├── test_paste_opendev.py
│       ├── test_bpa_st.py
│       └── test_paste_opensuse.py
├── debian/
│   ├── control
│   ├── changelog
│   ├── rules
│   ├── compat
│   ├── copyright
│   ├── pastebinit.1
│   └── pastebinit.bash-completion
├── pyproject.toml
├── release-please-config.json
├── .release-please-manifest.json
├── LICENSE
├── README.md
└── .github/
    ├── workflows/
    │   ├── build.yml
    │   ├── codeql.yml
    │   ├── auto-merge.yml
    │   ├── auto-label.yml
    │   ├── auto-rebase.yml
    │   └── auto-release.yml
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    ├── dependabot.yml
    ├── labeler.yml
    └── FUNDING.yml
```

---

## Task 1: Create GitHub repository

**Files:** `.github/` tree, `LICENSE`, `pyproject.toml` skeleton

- [ ] **Step 1: Create repo on GitHub**

```bash
cd /home/claude/pastebinit
gh repo create blixten85/pastebinit \
  --public \
  --description "Send text and files to pastebin services from the command line" \
  --homepage "https://github.com/blixten85/pastebinit"
git remote add origin git@github.com:blixten85/pastebinit.git
```

- [ ] **Step 2: Write LICENSE**

```
Create file: LICENSE
```

```
                    GNU GENERAL PUBLIC LICENSE
                       Version 2, June 1991

 Copyright (C) 1989, 1991 Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

[... full GPL v2 text — copy from https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt ...]
```

- [ ] **Step 3: Write pyproject.toml**

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "pastebinit"
version = "2.0.0"
description = "Send text and files to pastebin services from the command line"
readme = "README.md"
license = { text = "GPL-2.0-or-later" }
authors = [
  { name = "Anders Eriksson", email = "36226327+blixten85@users.noreply.github.com" },
]
requires-python = ">=3.10"
dependencies = [
  "cryptography>=41",
  "keyring>=24",
  "tomli-w>=1.0",
  "tomli>=2.0; python_version < '3.11'",
]

[project.scripts]
pastebinit = "pastebinit.cli:main"

[project.urls]
Homepage = "https://github.com/blixten85/pastebinit"
"Bug Tracker" = "https://github.com/blixten85/pastebinit/issues"
"Original Project" = "https://launchpad.net/pastebinit"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.setuptools.packages.find]
where = ["."]
include = ["pastebinit*"]
```

- [ ] **Step 4: Create package skeleton**

```bash
mkdir -p pastebinit/backends tests/backends
touch pastebinit/__init__.py pastebinit/__main__.py
touch pastebinit/cli.py pastebinit/config.py
touch pastebinit/credentials.py pastebinit/syntax.py
touch pastebinit/backends/__init__.py pastebinit/backends/base.py
touch pastebinit/backends/pastebin_com.py pastebinit/backends/dpaste.py
touch pastebinit/backends/paste_debian_net.py pastebinit/backends/paste_ubuntu_com.py
touch pastebinit/backends/sprunge.py pastebinit/backends/paste_opendev.py
touch pastebinit/backends/bpa_st.py pastebinit/backends/paste_opensuse.py
touch tests/__init__.py tests/backends/__init__.py
touch tests/conftest.py tests/test_config.py tests/test_credentials.py
touch tests/test_syntax.py tests/test_cli.py
touch tests/backends/test_pastebin_com.py tests/backends/test_dpaste.py
touch tests/backends/test_paste_debian_net.py tests/backends/test_paste_ubuntu_com.py
touch tests/backends/test_sprunge.py tests/backends/test_paste_opendev.py
touch tests/backends/test_bpa_st.py tests/backends/test_paste_opensuse.py
```

- [ ] **Step 5: Write pastebinit/__init__.py**

```python
# pastebinit/__init__.py
__version__ = "2.0.0"
```

- [ ] **Step 6: Write pastebinit/__main__.py**

```python
# pastebinit/__main__.py
from pastebinit.cli import main
main()
```

- [ ] **Step 7: Install dev dependencies and verify import**

```bash
pip install -e ".[dev]" 2>/dev/null || pip install -e .
pip install pytest cryptography keyring tomli-w
python3 -c "import pastebinit; print(pastebinit.__version__)"
```

Expected: `2.0.0`

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "chore: initial package scaffold

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 2: GitHub Actions CI/CD

**Files:** `.github/workflows/*.yml`, `.github/ISSUE_TEMPLATE/*.md`, `.github/dependabot.yml`, `.github/labeler.yml`, `.github/FUNDING.yml`

- [ ] **Step 1: Write build.yml**

```yaml
# .github/workflows/build.yml
name: Build

on:
  push:
    branches: [main]
    paths-ignore:
      - '**.md'
      - '.github/**'
      - '!.github/workflows/build.yml'
  pull_request:
    branches: [main]
  release:
    types: [published]
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest

      - name: Run tests
        run: pytest -v

  build-deb:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'release'
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4

      - name: Install build tools
        run: |
          sudo apt-get update
          sudo apt-get install -y devscripts debhelper dh-python python3-all

      - name: Build .deb
        run: dpkg-buildpackage -us -uc -b

      - name: Upload .deb to release
        run: |
          DEB=$(ls ../pastebinit_*.deb | head -1)
          gh release upload ${{ github.event.release.tag_name }} "$DEB"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- [ ] **Step 2: Write codeql.yml**

```yaml
# .github/workflows/codeql.yml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'
  workflow_dispatch:

permissions:
  actions: read
  contents: read
  security-events: write

jobs:
  analyze:
    name: Analyze (python)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v4
        with:
          languages: python
          queries: security-and-quality

      - name: Autobuild
        uses: github/codeql-action/autobuild@v4

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v4
        with:
          category: "/language:python"
```

- [ ] **Step 3: Write auto-merge.yml**

```yaml
# .github/workflows/auto-merge.yml
name: Bot Auto-Merge

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: write
  pull-requests: write

jobs:
  dependabot:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Fetch Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v2
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Auto-merge github_actions updates
        if: |
          steps.metadata.outputs.package-ecosystem == 'github_actions' && (
          steps.metadata.outputs.update-type == 'version-update:semver-patch' ||
          steps.metadata.outputs.update-type == 'version-update:semver-minor' ||
          steps.metadata.outputs.update-type == 'version-update:semver-major')
        run: gh pr merge --admin --delete-branch --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GHCR_TOKEN }}

      - name: Auto-merge patch and minor pip updates
        if: |
          steps.metadata.outputs.package-ecosystem != 'github_actions' && (
          steps.metadata.outputs.update-type == 'version-update:semver-patch' ||
          steps.metadata.outputs.update-type == 'version-update:semver-minor')
        run: gh pr merge --auto --delete-branch --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  release-please:
    runs-on: ubuntu-latest
    if: startsWith(github.head_ref, 'release-please--')
    steps:
      - name: Merge release PR
        run: gh pr merge --admin --squash --delete-branch "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GHCR_TOKEN }}

  security-autofix:
    runs-on: ubuntu-latest
    if: |
      contains(github.head_ref, 'alert-autofix') ||
      contains(github.head_ref, 'copilot')
    steps:
      - name: Enable auto-merge for security fixes
        run: gh pr merge --auto --squash --delete-branch "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GHCR_TOKEN }}

  claude:
    runs-on: ubuntu-latest
    if: startsWith(github.head_ref, 'claude/')
    steps:
      - name: Auto-merge Claude AI PRs once checks pass
        run: gh pr merge --auto --squash --delete-branch "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GHCR_TOKEN }}
```

- [ ] **Step 4: Write auto-label.yml**

```yaml
# .github/workflows/auto-label.yml
name: Auto-Label PRs

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/labeler.yml
          sync-labels: true
```

- [ ] **Step 5: Write auto-rebase.yml**

```yaml
# .github/workflows/auto-rebase.yml
name: Auto-Update PRs

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  update:
    runs-on: ubuntu-latest
    if: "!contains(github.event.head_commit.message, '[skip ci]')"
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Find open PRs with auto-rebase label
        id: find-prs
        uses: actions/github-script@v7
        with:
          script: |
            const { data: prs } = await github.rest.pulls.list({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open'
            });
            const updatable = prs.filter(pr =>
              pr.user.login !== 'dependabot[bot]' &&
              pr.labels.some(l => l.name === 'auto-rebase' || l.name === 'auto-merge')
            ).map(pr => pr.number);
            return updatable;

      - name: Update PR branches
        uses: actions/github-script@v7
        with:
          script: |
            const prNumbers = ${{ steps.find-prs.outputs.result }};
            for (const prNumber of prNumbers) {
              try {
                await github.rest.pulls.updateBranch({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  pull_number: prNumber
                });
                console.log(`Updated PR #${prNumber}`);
              } catch (e) {
                console.log(`Could not update PR #${prNumber}: ${e.message}`);
              }
            }
```

- [ ] **Step 6: Write auto-release.yml**

```yaml
# .github/workflows/auto-release.yml
name: Auto-Release

on:
  push:
    branches: [main]
    paths-ignore:
      - '**.md'
      - '.github/**'
      - '!.github/workflows/auto-release.yml'
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write
  issues: write
  actions: read

jobs:
  release:
    runs-on: ubuntu-latest
    if: "!contains(github.event.head_commit.message, '[skip ci]')"
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          token: ${{ secrets.GHCR_TOKEN }}
          config-file: release-please-config.json
          manifest-file: .release-please-manifest.json
```

- [ ] **Step 7: Write support files**

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "Europe/Stockholm"
    labels: ["dependencies", "auto-merge"]
    open-pull-requests-limit: 5

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "Europe/Stockholm"
    labels: ["ci", "auto-merge"]
    open-pull-requests-limit: 10
```

```yaml
# .github/labeler.yml
ci:
  - changed-files:
    - any-glob-to-any-file: '.github/**'

documentation:
  - changed-files:
    - any-glob-to-any-file: ['**.md', 'debian/pastebinit.1']

dependencies:
  - changed-files:
    - any-glob-to-any-file: 'pyproject.toml'

debian:
  - changed-files:
    - any-glob-to-any-file: 'debian/**'
```

```yaml
# .github/FUNDING.yml
github: [blixten85]
```

- [ ] **Step 8: Write issue templates**

```markdown
<!-- .github/ISSUE_TEMPLATE/bug_report.md -->
---
name: "🐛 Bug Report"
about: Report a bug
title: "[BUG] "
labels: bug
assignees: ''
---

**Description**
A clear description of the bug.

**Steps to Reproduce**
1. Run `pastebinit ...`
2. See error

**Expected Behavior**
What should happen.

**Environment**
- OS: [e.g. Ubuntu 24.04]
- pastebinit version: [e.g. v2.0.0]
- Python version: [e.g. 3.12]
- Backend: [e.g. pastebin.com]

**Logs**
```bash
# paste output here
```
```

```markdown
<!-- .github/ISSUE_TEMPLATE/feature_request.md -->
---
name: "💡 Feature Request"
about: Suggest a new feature
title: "[FEATURE] "
labels: enhancement
assignees: ''
---

**Description**
What feature would you like?

**Problem This Solves**
What problem does this address?

**Use Case**
How would you use this?

**Alternatives Considered**
Any alternatives you've thought of?
```

- [ ] **Step 9: Write release-please config**

```json
// release-please-config.json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "release-type": "simple",
  "packages": {
    ".": {
      "release-type": "simple",
      "changelog-path": "CHANGELOG.md"
    }
  }
}
```

```json
// .release-please-manifest.json
{
  ".": "2.0.0"
}
```

- [ ] **Step 10: Commit and push**

```bash
git add -A
git commit -m "ci: add GitHub Actions workflows and repo config

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push -u origin main
```

---

## Task 3: Test infrastructure

**Files:** `tests/conftest.py`

- [ ] **Step 1: Write conftest.py**

```python
# tests/conftest.py
import json
from contextlib import contextmanager
from unittest.mock import MagicMock, patch


def make_http_response(body: str, url: str = "https://example.com/abc123") -> MagicMock:
    """Return a mock that behaves like urllib.request.urlopen()'s context manager."""
    mock = MagicMock()
    mock.read.return_value = body.encode()
    mock.url = url
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


def patch_urlopen(body: str, url: str = "https://example.com/abc123"):
    """Patch urllib.request.urlopen to return a fake response."""
    return patch(
        "urllib.request.urlopen",
        return_value=make_http_response(body, url),
    )
```

- [ ] **Step 2: Install pytest and verify**

```bash
pip install pytest
pytest --collect-only
```

Expected: collected 0 items (no errors)

---

## Task 4: BasePastebin ABC

**Files:** `pastebinit/backends/base.py`, `tests/backends/test_base.py`

- [ ] **Step 1: Write failing test**

```python
# tests/backends/test_base.py
import pytest
from pastebinit.backends.base import (
    BasePastebin, PasteOptions, BackendError, NotSupportedError, AuthError
)


class MinimalBackend(BasePastebin):
    name = "test"
    url = "https://test.example.com"

    def paste(self, content: str, opts: PasteOptions) -> str:
        return "https://test.example.com/abc"


def test_paste_options_defaults():
    opts = PasteOptions()
    assert opts.title == ""
    assert opts.format == "text"
    assert opts.private == 1
    assert opts.expiry == "N"
    assert opts.folder is None


def test_concrete_backend_paste():
    b = MinimalBackend()
    url = b.paste("hello", PasteOptions())
    assert url == "https://test.example.com/abc"


def test_unsupported_raises():
    b = MinimalBackend()
    with pytest.raises(NotSupportedError):
        b.login("user", "pass")
    with pytest.raises(NotSupportedError):
        b.list_pastes("key")
    with pytest.raises(NotSupportedError):
        b.delete_paste("key", "ukey")
    with pytest.raises(NotSupportedError):
        b.list_folders("ukey")
    with pytest.raises(NotSupportedError):
        b.create_folder("name", "ukey")
    with pytest.raises(NotSupportedError):
        b.get_user_info("ukey")
```

- [ ] **Step 2: Run test — expect failure**

```bash
pytest tests/backends/test_base.py -v
```

Expected: `ImportError` or `ModuleNotFoundError`

- [ ] **Step 3: Write base.py**

```python
# pastebinit/backends/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


class BackendError(Exception):
    pass


class NotSupportedError(BackendError):
    pass


class AuthError(BackendError):
    pass


@dataclass
class PasteOptions:
    title: str = ""
    format: str = "text"
    private: int = 1
    expiry: str = "N"
    folder: Optional[str] = None
    create_folder: bool = False
    user_key: Optional[str] = None


class BasePastebin(ABC):
    name: str
    url: str
    supports_auth: bool = False
    supports_folders: bool = False
    supports_expiry: bool = False
    supports_privacy: bool = False
    supports_syntax: bool = False

    @abstractmethod
    def paste(self, content: str, opts: PasteOptions) -> str: ...

    def login(self, username: str, password: str) -> str:
        raise NotSupportedError(f"{self.name} does not support authentication")

    def list_pastes(self, user_key: str) -> list[dict]:
        raise NotSupportedError(f"{self.name} does not support listing pastes")

    def delete_paste(self, paste_key: str, user_key: str) -> bool:
        raise NotSupportedError(f"{self.name} does not support deleting pastes")

    def list_folders(self, user_key: str) -> list[dict]:
        raise NotSupportedError(f"{self.name} does not support folders")

    def create_folder(self, name: str, user_key: str) -> str:
        raise NotSupportedError(f"{self.name} does not support creating folders")

    def get_user_info(self, user_key: str) -> dict:
        raise NotSupportedError(f"{self.name} does not support user info")
```

- [ ] **Step 4: Run tests — expect pass**

```bash
pytest tests/backends/test_base.py -v
```

Expected: 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add pastebinit/backends/base.py tests/backends/test_base.py
git commit -m "feat: add BasePastebin ABC with PasteOptions and error hierarchy

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 5: Config system

**Files:** `pastebinit/config.py`, `tests/test_config.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_config.py
import sys
import pytest
from pathlib import Path
from unittest.mock import patch


def test_load_returns_defaults_when_no_file(tmp_path):
    with patch("pastebinit.config.CONFIG_FILE", tmp_path / "config.toml"):
        from pastebinit import config
        result = config.load()
        assert result["defaults"]["backend"] == "bpa.st"
        assert result["defaults"]["private"] == 1


def test_save_and_load_roundtrip(tmp_path):
    cfg_file = tmp_path / "config.toml"
    with patch("pastebinit.config.CONFIG_FILE", cfg_file), \
         patch("pastebinit.config.CONFIG_DIR", tmp_path):
        from pastebinit import config
        data = {"defaults": {"backend": "dpaste.com", "private": 0}}
        config.save(data)
        assert cfg_file.exists()
        loaded = config.load()
        assert loaded["defaults"]["backend"] == "dpaste.com"


def test_get_default_backend(tmp_path):
    with patch("pastebinit.config.CONFIG_FILE", tmp_path / "none.toml"):
        from pastebinit import config
        assert config.get_default("backend") == "bpa.st"
```

- [ ] **Step 2: Run — expect failure**

```bash
pytest tests/test_config.py -v
```

- [ ] **Step 3: Write config.py**

```python
# pastebinit/config.py
import sys
from pathlib import Path
from typing import Any, Optional
import os

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import tomli_w

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "pastebinit"
CONFIG_FILE = CONFIG_DIR / "config.toml"

_DEFAULTS: dict[str, Any] = {
    "defaults": {
        "backend": "bpa.st",
        "private": 1,
        "expiry": "N",
        "format": "auto",
    }
}


def load() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        return {k: dict(v) for k, v in _DEFAULTS.items()}
    with CONFIG_FILE.open("rb") as f:
        return tomllib.load(f)


def save(config: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("wb") as f:
        tomli_w.dump(config, f)


def get_default(key: str, config: Optional[dict] = None) -> Any:
    if config is None:
        config = load()
    return config.get("defaults", {}).get(key, _DEFAULTS["defaults"].get(key))
```

- [ ] **Step 4: Run tests — expect pass**

```bash
pytest tests/test_config.py -v
```

- [ ] **Step 5: Commit**

```bash
git add pastebinit/config.py tests/test_config.py
git commit -m "feat: add TOML config system with XDG support

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 6: Credential storage

**Files:** `pastebinit/credentials.py`, `tests/test_credentials.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_credentials.py
import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


def test_get_from_env_var(tmp_path):
    with patch.dict(os.environ, {"PASTEBIN_API_KEY": "testkey123"}):
        from pastebinit import credentials
        result = credentials.get("pastebin.com", "api_dev_key")
        assert result == "testkey123"


def test_get_returns_none_when_nothing_configured(tmp_path):
    clean_env = {k: v for k, v in os.environ.items()
                 if k not in ("PASTEBIN_API_KEY", "PASTEBIN_PASSWORD", "PASTEBIN_USERNAME")}
    with patch.dict(os.environ, clean_env, clear=True), \
         patch("pastebinit.credentials.KEYSTORE_FILE", tmp_path / "keystore"), \
         patch("pastebinit.credentials._keyring_get", return_value=None):
        from pastebinit import credentials
        result = credentials.get("pastebin.com", "api_dev_key")
        assert result is None


def test_store_and_retrieve_from_keystore(tmp_path):
    ks = tmp_path / "keystore"
    with patch("pastebinit.credentials.KEYSTORE_FILE", ks), \
         patch("pastebinit.credentials.CONFIG_DIR", tmp_path), \
         patch("pastebinit.credentials._keyring_get", return_value=None), \
         patch("pastebinit.credentials._keyring_set", return_value=False):
        from pastebinit import credentials
        credentials._keystore_set("pastebin.com", "api_dev_key", "secretkey", "mypassword")
        assert ks.exists()
        assert oct(ks.stat().st_mode)[-3:] == "600"
        result = credentials._keystore_get("pastebin.com", "api_dev_key", "mypassword")
        assert result == "secretkey"


def test_wrong_password_returns_none(tmp_path):
    ks = tmp_path / "keystore"
    with patch("pastebinit.credentials.KEYSTORE_FILE", ks), \
         patch("pastebinit.credentials.CONFIG_DIR", tmp_path):
        from pastebinit import credentials
        credentials._keystore_set("pastebin.com", "pw", "value", "correct")
        result = credentials._keystore_get("pastebin.com", "pw", "wrong")
        assert result is None
```

- [ ] **Step 2: Run — expect failure**

```bash
pytest tests/test_credentials.py -v
```

- [ ] **Step 3: Write credentials.py**

```python
# pastebinit/credentials.py
import base64
import json
import os
import stat
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "pastebinit"
KEYSTORE_FILE = CONFIG_DIR / "keystore"

_ENV_MAP: dict[str, dict[str, str]] = {
    "pastebin.com": {
        "api_dev_key": "PASTEBIN_API_KEY",
        "password": "PASTEBIN_PASSWORD",
        "username": "PASTEBIN_USERNAME",
    },
}


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def _keyring_get(backend: str, field: str) -> Optional[str]:
    try:
        import keyring
        return keyring.get_password(f"pastebinit:{backend}", field)
    except Exception:
        return None


def _keyring_set(backend: str, field: str, value: str) -> bool:
    try:
        import keyring
        keyring.set_password(f"pastebinit:{backend}", field, value)
        return True
    except Exception:
        return False


def _keystore_get(backend: str, field: str, password: str) -> Optional[str]:
    if not KEYSTORE_FILE.exists():
        return None
    try:
        raw = KEYSTORE_FILE.read_bytes()
        salt, token = raw[:16], raw[16:]
        key = _derive_key(password, salt)
        decrypted = json.loads(Fernet(key).decrypt(token))
        return decrypted.get(backend, {}).get(field)
    except (InvalidToken, Exception):
        return None


def _keystore_set(backend: str, field: str, value: str, password: str) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    existing: dict = {}
    if KEYSTORE_FILE.exists():
        try:
            raw = KEYSTORE_FILE.read_bytes()
            salt_old, token = raw[:16], raw[16:]
            existing = json.loads(Fernet(_derive_key(password, salt_old)).decrypt(token))
        except Exception:
            pass
    salt = os.urandom(16)
    existing.setdefault(backend, {})[field] = value
    encrypted = Fernet(_derive_key(password, salt)).encrypt(json.dumps(existing).encode())
    KEYSTORE_FILE.write_bytes(salt + encrypted)
    KEYSTORE_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)


def get(backend: str, field: str) -> Optional[str]:
    """Return credential: env var → OS keyring → encrypted keystore."""
    env_key = _ENV_MAP.get(backend, {}).get(field)
    if env_key:
        val = os.environ.get(env_key)
        if val:
            return val

    val = _keyring_get(backend, field)
    if val:
        return val

    return None  # keystore requires explicit password prompt — call _keystore_get directly


def store(backend: str, field: str, value: str, password: str) -> None:
    """Store credential in keyring if available, else encrypted keystore."""
    if not _keyring_set(backend, field, value):
        _keystore_set(backend, field, value, password)
```

- [ ] **Step 4: Run tests — expect pass**

```bash
pytest tests/test_credentials.py -v
```

- [ ] **Step 5: Commit**

```bash
git add pastebinit/credentials.py tests/test_credentials.py
git commit -m "feat: add encrypted credential storage (Fernet/PBKDF2 + keyring)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 7: Syntax auto-detection

**Files:** `pastebinit/syntax.py`, `tests/test_syntax.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_syntax.py
from pastebinit.syntax import detect


def test_detect_by_extension_python():
    assert detect("print('hi')", filename="script.py") == "python"


def test_detect_by_extension_rust():
    assert detect("fn main() {}", filename="main.rs") == "rust"


def test_detect_by_extension_typescript():
    assert detect("const x: number = 1", filename="app.ts") == "typescript"


def test_detect_dockerfile():
    assert detect("FROM ubuntu", filename="Dockerfile") == "bash"


def test_detect_makefile():
    assert detect("all:", filename="Makefile") == "make"


def test_detect_shebang_python():
    assert detect("#!/usr/bin/env python3\nprint('hi')") == "python"


def test_detect_shebang_bash():
    assert detect("#!/bin/bash\necho hi") == "bash"


def test_detect_shebang_node():
    assert detect("#!/usr/bin/env node\nconsole.log('hi')") == "javascript"


def test_detect_unknown_falls_back_to_text():
    assert detect("hello world") == "text"


def test_detect_explicit_format_overrides():
    # When caller passes format explicitly it bypasses detect()
    # (CLI handles this — detect() itself always returns a value)
    assert detect("", filename="file.py") == "python"
```

- [ ] **Step 2: Run — expect failure**

```bash
pytest tests/test_syntax.py -v
```

- [ ] **Step 3: Write syntax.py**

```python
# pastebinit/syntax.py
from pathlib import Path
from typing import Optional

EXTENSION_MAP: dict[str, str] = {
    ".py": "python", ".pyw": "python",
    ".js": "javascript", ".mjs": "javascript", ".cjs": "javascript",
    ".ts": "typescript", ".tsx": "typescript",
    ".jsx": "javascript",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".c": "c", ".h": "c",
    ".cpp": "cpp", ".cxx": "cpp", ".cc": "cpp", ".hpp": "cpp",
    ".cs": "csharp",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin", ".kts": "kotlin",
    ".scala": "scala",
    ".sh": "bash", ".bash": "bash", ".zsh": "bash", ".fish": "bash",
    ".ps1": "powershell",
    ".html": "html5", ".htm": "html5",
    ".css": "css", ".scss": "css", ".sass": "css",
    ".json": "json",
    ".yaml": "yaml", ".yml": "yaml",
    ".toml": "ini", ".ini": "ini", ".cfg": "ini", ".conf": "ini",
    ".xml": "xml",
    ".sql": "sql",
    ".md": "markdown", ".markdown": "markdown",
    ".lua": "lua",
    ".r": "rsplus", ".R": "rsplus",
    ".dart": "dart",
    ".ex": "erlang", ".exs": "erlang", ".erl": "erlang",
    ".hs": "haskell",
    ".ml": "ocaml", ".mli": "ocaml",
    ".vim": "vim",
    ".pl": "perl", ".pm": "perl",
    ".tf": "ini",
    ".env": "ini",
    ".mk": "make",
    ".groovy": "groovy",
    ".gradle": "groovy",
    ".clj": "clojure",
    ".nim": "nim",
    ".zig": "text",
}

SHEBANG_MAP: dict[str, str] = {
    "python": "python", "python3": "python", "python2": "python",
    "node": "javascript", "nodejs": "javascript",
    "bash": "bash", "sh": "bash", "zsh": "bash", "dash": "bash",
    "ruby": "ruby",
    "perl": "perl",
    "php": "php",
    "lua": "lua",
    "rscript": "rsplus",
}

_SPECIAL_NAMES: dict[str, str] = {
    "dockerfile": "bash",
    "makefile": "make",
    "gnumakefile": "make",
    "gemfile": "ruby",
    "rakefile": "ruby",
    "vagrantfile": "ruby",
    "cmakelists.txt": "cmake",
}


def detect(content: str, filename: Optional[str] = None) -> str:
    """Return pastebin syntax format for content, using filename hint if given."""
    if filename:
        p = Path(filename)
        name_lower = p.name.lower()
        if name_lower in _SPECIAL_NAMES:
            return _SPECIAL_NAMES[name_lower]
        ext = p.suffix.lower()
        if ext in EXTENSION_MAP:
            return EXTENSION_MAP[ext]

    lines = content.splitlines()
    if lines and lines[0].startswith("#!"):
        parts = lines[0].lstrip("#!").strip().split()
        if parts:
            interpreter = Path(parts[-1]).name.lower()
            if interpreter in SHEBANG_MAP:
                return SHEBANG_MAP[interpreter]
            # handle /usr/bin/env python3 style
            if len(parts) > 1:
                interpreter = Path(parts[-1]).name.lower()
                if interpreter in SHEBANG_MAP:
                    return SHEBANG_MAP[interpreter]

    return "text"
```

- [ ] **Step 4: Run tests — expect pass**

```bash
pytest tests/test_syntax.py -v
```

- [ ] **Step 5: Commit**

```bash
git add pastebinit/syntax.py tests/test_syntax.py
git commit -m "feat: add syntax auto-detection from extension and shebang

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 8: Backend registry

**Files:** `pastebinit/backends/__init__.py`

- [ ] **Step 1: Write backends/__init__.py**

```python
# pastebinit/backends/__init__.py
from .pastebin_com import PastebinCom
from .dpaste import DPaste
from .paste_debian_net import PasteDebianNet
from .paste_ubuntu_com import PasteUbuntuCom
from .sprunge import Sprunge
from .paste_opendev import PasteOpenDev
from .bpa_st import BpaSt
from .paste_opensuse import PasteOpenSUSE

BACKENDS: dict[str, type] = {
    "pastebin.com": PastebinCom,
    "dpaste.com": DPaste,
    "paste.debian.net": PasteDebianNet,
    "paste.ubuntu.com": PasteUbuntuCom,
    "sprunge.us": Sprunge,
    "paste.opendev.org": PasteOpenDev,
    "bpa.st": BpaSt,
    "paste.opensuse.org": PasteOpenSUSE,
}

DEFAULT_BACKEND = "bpa.st"


def get_backend(name: str):
    """Return instantiated backend by name, raise ValueError if unknown."""
    cls = BACKENDS.get(name)
    if cls is None:
        known = ", ".join(sorted(BACKENDS))
        raise ValueError(f"Unknown backend '{name}'. Known backends: {known}")
    return cls()
```

Note: all backend files must exist (even as stubs) before this import works. Fill each stub with a `pass`-level class first, then implement fully in Tasks 9–16.

- [ ] **Step 2: Write stubs for all backends**

Each file gets this minimal stub so the registry import succeeds:

```python
# pastebinit/backends/dpaste.py  (repeat pattern for all 7 non-pastebin.com backends)
from .base import BasePastebin, PasteOptions, BackendError


class DPaste(BasePastebin):
    name = "dpaste.com"
    url = "https://dpaste.com"
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        raise NotImplementedError
```

Create matching stubs (same pattern, different `name`/`url`/`supports_*`) for:
- `paste_debian_net.py` → `PasteDebianNet`, `"paste.debian.net"`, supports_auth=True, supports_expiry=True, supports_privacy=True, supports_syntax=True
- `paste_ubuntu_com.py` → `PasteUbuntuCom`, `"paste.ubuntu.com"`, supports_privacy=True, supports_syntax=True
- `sprunge.py` → `Sprunge`, `"sprunge.us"`, supports_syntax=True
- `paste_opendev.py` → `PasteOpenDev`, `"paste.opendev.org"`, supports_auth=True, supports_expiry=True, supports_privacy=True, supports_syntax=True
- `bpa_st.py` → `BpaSt`, `"bpa.st"`, supports_expiry=True, supports_privacy=True, supports_syntax=True
- `paste_opensuse.py` → `PasteOpenSUSE`, `"paste.opensuse.org"`, supports_expiry=True, supports_syntax=True

- [ ] **Step 3: Verify registry works**

```bash
python3 -c "from pastebinit.backends import BACKENDS; print(list(BACKENDS.keys()))"
```

Expected: `['pastebin.com', 'dpaste.com', 'paste.debian.net', 'paste.ubuntu.com', 'sprunge.us', 'paste.opendev.org', 'bpa.st', 'paste.opensuse.org']`

- [ ] **Step 4: Commit**

```bash
git add pastebinit/backends/
git commit -m "feat: add backend registry and stubs for all 8 backends

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 9: pastebin.com backend

**Files:** `pastebinit/backends/pastebin_com.py`, `tests/backends/test_pastebin_com.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/backends/test_pastebin_com.py
import pytest
from unittest.mock import patch, MagicMock
from tests.conftest import make_http_response, patch_urlopen
from pastebinit.backends.pastebin_com import PastebinCom
from pastebinit.backends.base import PasteOptions, AuthError, BackendError


@pytest.fixture
def backend():
    return PastebinCom(api_dev_key="testdevkey")


def test_paste_returns_url(backend):
    with patch_urlopen("https://pastebin.com/abc123"):
        url = backend.paste("hello world", PasteOptions())
    assert url == "https://pastebin.com/abc123"


def test_paste_with_syntax(backend):
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.return_value = make_http_response("https://pastebin.com/xyz")
        backend.paste("print('hi')", PasteOptions(format="python"))
        call_data = mock_open.call_args[0][1]
        assert b"api_paste_format=python" in call_data


def test_paste_with_private_level(backend):
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.return_value = make_http_response("https://pastebin.com/xyz")
        backend.paste("secret", PasteOptions(private=2, user_key="userkey"))
        call_data = mock_open.call_args[0][1]
        assert b"api_paste_private=2" in call_data
        assert b"api_user_key=userkey" in call_data


def test_login_returns_user_key(backend):
    with patch_urlopen("validuserkey123abc"):
        key = backend.login("myuser", "mypass")
    assert key == "validuserkey123abc"


def test_login_bad_credentials_raises(backend):
    with patch_urlopen("Bad API request, invalid login"):
        with pytest.raises(AuthError):
            backend.login("bad", "creds")


def test_paste_api_error_raises(backend):
    with patch_urlopen("Bad API request, maximum pastes per day reached"):
        with pytest.raises(BackendError):
            backend.paste("content", PasteOptions())


def test_delete_paste(backend):
    with patch_urlopen("Paste Removed"):
        result = backend.delete_paste("abc123", "userkey")
    assert result is True


def test_list_folders_parses_xml(backend):
    xml = ("<folder><folder_key>aaa</folder_key>"
           "<folder_name>MyFolder</folder_name></folder>")
    with patch_urlopen(xml):
        folders = backend.list_folders("userkey")
    assert folders == [{"key": "aaa", "name": "MyFolder"}]


def test_no_api_key_raises(monkeypatch):
    monkeypatch.delenv("PASTEBIN_API_KEY", raising=False)
    with patch("pastebinit.credentials._keyring_get", return_value=None):
        b = PastebinCom()
        with pytest.raises(AuthError):
            b.paste("x", PasteOptions())
```

- [ ] **Step 2: Run — expect failure**

```bash
pytest tests/backends/test_pastebin_com.py -v
```

- [ ] **Step 3: Write pastebin_com.py**

```python
# pastebinit/backends/pastebin_com.py
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Optional

from .base import BasePastebin, PasteOptions, AuthError, BackendError, NotSupportedError

_API = "https://pastebin.com/api/api_post.php"
_LOGIN = "https://pastebin.com/api/api_login.php"
_USER_AGENT = "pastebinit/2.0.0"

_EXPIRY = {"N", "10M", "1H", "1D", "1W", "2W", "1M", "6M", "1Y"}


class PastebinCom(BasePastebin):
    name = "pastebin.com"
    url = "https://pastebin.com"
    supports_auth = True
    supports_folders = True
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def __init__(self, api_dev_key: Optional[str] = None):
        self._api_dev_key = api_dev_key

    def _key(self) -> str:
        if self._api_dev_key:
            return self._api_dev_key
        from ..credentials import get
        key = get("pastebin.com", "api_dev_key")
        if not key:
            raise AuthError(
                "No API dev key. Set PASTEBIN_API_KEY or run: pastebinit --login"
            )
        return key

    def _post(self, url: str, params: dict) -> str:
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(url, data=data)
        req.add_header("User-Agent", _USER_AGENT)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = resp.read().decode()
        except OSError as e:
            raise BackendError(f"Network error: {e}") from e
        if result.startswith("Bad API request"):
            raise BackendError(result)
        return result

    def login(self, username: str, password: str) -> str:
        result = self._post(_LOGIN, {
            "api_dev_key": self._key(),
            "api_user_name": username,
            "api_user_password": password,
        })
        if not result or "Bad" in result:
            raise AuthError(f"Login failed: {result}")
        return result

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "text"
        expiry = opts.expiry if opts.expiry in _EXPIRY else "N"
        params: dict = {
            "api_option": "paste",
            "api_dev_key": self._key(),
            "api_paste_code": content,
            "api_paste_name": opts.title,
            "api_paste_format": fmt,
            "api_paste_private": opts.private,
            "api_paste_expire_date": expiry,
        }
        if opts.user_key:
            params["api_user_key"] = opts.user_key
        if opts.folder and opts.user_key:
            params["api_folder_key"] = self._resolve_folder(
                opts.folder, opts.user_key, create=opts.create_folder
            )
        return self._post(_API, params)

    def list_pastes(self, user_key: str, limit: int = 50) -> list[dict]:
        result = self._post(_API, {
            "api_option": "list",
            "api_dev_key": self._key(),
            "api_user_key": user_key,
            "api_results_limit": limit,
        })
        root = ET.fromstring(f"<root>{result}</root>")
        return [
            {
                "key": p.findtext("paste_key", ""),
                "title": p.findtext("paste_title", ""),
                "date": p.findtext("paste_date", ""),
                "size": p.findtext("paste_size", ""),
                "expire_date": p.findtext("paste_expire_date", ""),
                "private": p.findtext("paste_private", ""),
                "format": p.findtext("paste_format_short", ""),
                "url": p.findtext("paste_url", ""),
                "hits": p.findtext("paste_hits", ""),
            }
            for p in root.findall("paste")
        ]

    def delete_paste(self, paste_key: str, user_key: str) -> bool:
        result = self._post(_API, {
            "api_option": "delete",
            "api_dev_key": self._key(),
            "api_user_key": user_key,
            "api_paste_key": paste_key,
        })
        return result == "Paste Removed"

    def list_folders(self, user_key: str) -> list[dict]:
        result = self._post(_API, {
            "api_option": "list_folders",
            "api_dev_key": self._key(),
            "api_user_key": user_key,
        })
        root = ET.fromstring(f"<root>{result}</root>")
        return [
            {
                "key": f.findtext("folder_key", ""),
                "name": f.findtext("folder_name", ""),
            }
            for f in root.findall("folder")
        ]

    def create_folder(self, name: str, user_key: str) -> str:
        return self._post(_API, {
            "api_option": "create_folder",
            "api_dev_key": self._key(),
            "api_user_key": user_key,
            "api_folder_name": name,
        })

    def get_user_info(self, user_key: str) -> dict:
        result = self._post(_API, {
            "api_option": "userdetails",
            "api_dev_key": self._key(),
            "api_user_key": user_key,
        })
        root = ET.fromstring(result)
        return {
            "username": root.findtext("user_name", ""),
            "email": root.findtext("user_email", ""),
            "avatar_url": root.findtext("user_avatar_url", ""),
            "private": root.findtext("user_private", ""),
            "website": root.findtext("user_website", ""),
            "api_tier": root.findtext("user_api_tier", ""),
        }

    def _resolve_folder(self, name: str, user_key: str, create: bool = False) -> str:
        for f in self.list_folders(user_key):
            if f["name"] == name:
                return f["key"]
        if create:
            return self.create_folder(name, user_key)
        raise BackendError(
            f"Folder '{name}' not found on pastebin.com. Use --create-folder to create it."
        )
```

- [ ] **Step 4: Run tests — expect pass**

```bash
pytest tests/backends/test_pastebin_com.py -v
```

- [ ] **Step 5: Commit**

```bash
git add pastebinit/backends/pastebin_com.py tests/backends/test_pastebin_com.py
git commit -m "feat: implement full pastebin.com REST API backend

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 10: dpaste.com backend

**Files:** `pastebinit/backends/dpaste.py`, `tests/backends/test_dpaste.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/backends/test_dpaste.py
import pytest
from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.dpaste import DPaste
from pastebinit.backends.base import PasteOptions

_API = "https://dpaste.com/api/v2/"


@pytest.fixture
def backend():
    return DPaste()


def test_paste_returns_url(backend):
    mock_resp = make_http_response("https://dpaste.com/ABCD1234\n", url="https://dpaste.com/ABCD1234")
    with patch("urllib.request.urlopen", return_value=mock_resp):
        url = backend.paste("hello", PasteOptions())
    assert url == "https://dpaste.com/ABCD1234"


def test_paste_sends_syntax(backend):
    mock_resp = make_http_response("https://dpaste.com/XYZ\n")
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.return_value = mock_resp
        backend.paste("fn main(){}", PasteOptions(format="rust"))
        data = mock_open.call_args[0][1]
        assert b"syntax=rust" in data


def test_paste_sends_expiry(backend):
    mock_resp = make_http_response("https://dpaste.com/XYZ\n")
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.return_value = mock_resp
        backend.paste("hello", PasteOptions(expiry="1D"))
        data = mock_open.call_args[0][1]
        assert b"expiry_days=1" in data
```

- [ ] **Step 2: Write dpaste.py**

dpaste API v2: POST `https://dpaste.com/api/v2/` with fields `content`, `syntax`, `title`, `expiry_days` (1/7/30/365). Returns URL as plain text in response body.

```python
# pastebinit/backends/dpaste.py
import urllib.parse
import urllib.request
from .base import BasePastebin, PasteOptions, BackendError

_API = "https://dpaste.com/api/v2/"
_EXPIRY_MAP = {"N": "365", "1D": "1", "1W": "7", "1M": "30", "1Y": "365"}


class DPaste(BasePastebin):
    name = "dpaste.com"
    url = "https://dpaste.com"
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "text", "") else "text"
        expiry = _EXPIRY_MAP.get(opts.expiry, "7")
        params = {
            "content": content,
            "syntax": fmt,
            "title": opts.title,
            "expiry_days": expiry,
        }
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(_API, data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode().strip()
        except OSError as e:
            raise BackendError(f"dpaste.com error: {e}") from e
```

- [ ] **Step 3: Run tests — expect pass**

```bash
pytest tests/backends/test_dpaste.py -v
```

- [ ] **Step 4: Commit**

```bash
git add pastebinit/backends/dpaste.py tests/backends/test_dpaste.py
git commit -m "feat: implement dpaste.com REST API backend

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 11: paste.debian.net backend

**Files:** `pastebinit/backends/paste_debian_net.py`, `tests/backends/test_paste_debian_net.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/backends/test_paste_debian_net.py
import pytest
from unittest.mock import patch, MagicMock
from pastebinit.backends.paste_debian_net import PasteDebianNet
from pastebinit.backends.base import PasteOptions, BackendError


@pytest.fixture
def backend():
    return PasteDebianNet()


def test_paste_returns_url(backend):
    mock_proxy = MagicMock()
    mock_proxy.paste.addPaste.return_value = {
        "rc": 0, "id": 12345, "url": "https://paste.debian.net/12345/"
    }
    with patch("xmlrpc.client.ServerProxy", return_value=mock_proxy):
        url = backend.paste("hello world", PasteOptions())
    assert url == "https://paste.debian.net/12345/"


def test_paste_server_error_raises(backend):
    mock_proxy = MagicMock()
    mock_proxy.paste.addPaste.return_value = {"rc": 1}
    with patch("xmlrpc.client.ServerProxy", return_value=mock_proxy):
        with pytest.raises(BackendError):
            backend.paste("hello", PasteOptions())


def test_paste_sends_syntax(backend):
    mock_proxy = MagicMock()
    mock_proxy.paste.addPaste.return_value = {
        "rc": 0, "id": 1, "url": "https://paste.debian.net/1/"
    }
    with patch("xmlrpc.client.ServerProxy", return_value=mock_proxy):
        backend.paste("fn main(){}", PasteOptions(format="rust"))
    call_args = mock_proxy.paste.addPaste.call_args[0]
    assert call_args[1] == "rust"
```

- [ ] **Step 2: Write paste_debian_net.py**

paste.debian.net uses XML-RPC. Endpoint: `http://paste.debian.net/server.pl`. Method: `paste.addPaste(code, language, description, expire, hidden)`. expire is seconds (0=never). Returns dict `{rc, id, url}`.

```python
# pastebinit/backends/paste_debian_net.py
import xmlrpc.client
from .base import BasePastebin, PasteOptions, BackendError

_ENDPOINT = "http://paste.debian.net/server.pl"

_EXPIRY_SECONDS = {
    "N": 0, "1D": 86400, "1W": 604800, "2W": 1209600,
    "1M": 2592000, "6M": 15552000, "1Y": 31536000,
}


class PasteDebianNet(BasePastebin):
    name = "paste.debian.net"
    url = "https://paste.debian.net"
    supports_auth = True
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "Plain Text"
        expire = _EXPIRY_SECONDS.get(opts.expiry, 0)
        hidden = 1 if opts.private > 0 else 0
        try:
            proxy = xmlrpc.client.ServerProxy(_ENDPOINT)
            result = proxy.paste.addPaste(content, fmt, opts.title, expire, hidden)
        except Exception as e:
            raise BackendError(f"paste.debian.net error: {e}") from e
        if result.get("rc") != 0:
            raise BackendError(f"paste.debian.net returned error code {result.get('rc')}")
        return result.get("url", f"https://paste.debian.net/{result['id']}/")
```

- [ ] **Step 3: Run tests — expect pass**

```bash
pytest tests/backends/test_paste_debian_net.py -v
```

- [ ] **Step 4: Commit**

```bash
git add pastebinit/backends/paste_debian_net.py tests/backends/test_paste_debian_net.py
git commit -m "feat: implement paste.debian.net XML-RPC backend

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 12: Remaining simple backends

**Files:** `pastebinit/backends/paste_ubuntu_com.py`, `sprunge.py`, `paste_opendev.py`, `bpa_st.py`, `paste_opensuse.py` + matching test files

- [ ] **Step 1: Write all five backends**

```python
# pastebinit/backends/paste_ubuntu_com.py
import urllib.parse, urllib.request
from .base import BasePastebin, PasteOptions, BackendError

_EXPIRY = {"N": "year", "1D": "day", "1W": "week", "1M": "month", "1Y": "year"}
_SYNTAX_MAP = {  # Ubuntu uses different names for some
    "python": "python3", "bash": "bash", "text": "text",
    "javascript": "javascript", "css": "css", "html5": "html",
    "sql": "sql", "xml": "xml", "yaml": "yaml", "json": "json",
}


class PasteUbuntuCom(BasePastebin):
    name = "paste.ubuntu.com"
    url = "https://paste.ubuntu.com"
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "text"
        fmt = _SYNTAX_MAP.get(fmt, fmt)
        params = {
            "poster": opts.title or "pastebinit",
            "syntax": fmt,
            "expiration": _EXPIRY.get(opts.expiry, "year"),
            "content": content,
        }
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request("https://paste.ubuntu.com/", data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.url
        except OSError as e:
            raise BackendError(f"paste.ubuntu.com error: {e}") from e
```

```python
# pastebinit/backends/sprunge.py
import urllib.parse, urllib.request
from .base import BasePastebin, PasteOptions, BackendError


class Sprunge(BasePastebin):
    name = "sprunge.us"
    url = "http://sprunge.us"
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        data = urllib.parse.urlencode({"sprunge": content}).encode()
        req = urllib.request.Request("http://sprunge.us", data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                url = resp.read().decode().strip()
            # sprunge supports ?<syntax> suffix for highlighting
            if opts.format not in ("auto", "text", ""):
                url = f"{url}?{opts.format}"
            return url
        except OSError as e:
            raise BackendError(f"sprunge.us error: {e}") from e
```

```python
# pastebinit/backends/paste_opendev.py
import json, urllib.parse, urllib.request
from .base import BasePastebin, PasteOptions, BackendError

_API = "https://paste.opendev.org/api/create"
_EXPIRY_SECONDS = {
    "N": 0, "1H": 3600, "1D": 86400, "1W": 604800,
    "1M": 2592000, "1Y": 31536000,
}


class PasteOpenDev(BasePastebin):
    name = "paste.opendev.org"
    url = "https://paste.opendev.org"
    supports_auth = True
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "text"
        expire = _EXPIRY_SECONDS.get(opts.expiry, 0)
        params = {
            "text": content,
            "title": opts.title,
            "language": fmt,
            "private": "yes" if opts.private > 0 else "no",
            "expire": expire,
        }
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(_API, data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read())
            return result.get("url", "")
        except OSError as e:
            raise BackendError(f"paste.opendev.org error: {e}") from e
```

```python
# pastebinit/backends/bpa_st.py
import urllib.parse, urllib.request
from .base import BasePastebin, PasteOptions, BackendError

_EXPIRY = {"N": "never", "1H": "1hour", "1D": "1day", "1W": "1week", "1M": "1month"}


class BpaSt(BasePastebin):
    name = "bpa.st"
    url = "https://bpa.st"
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "text"
        params = {
            "content": content,
            "syntax": fmt,
            "title": opts.title,
            "expiry": _EXPIRY.get(opts.expiry, "never"),
        }
        if opts.private > 0:
            params["private"] = "1"
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request("https://bpa.st/", data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.url
        except OSError as e:
            raise BackendError(f"bpa.st error: {e}") from e
```

```python
# pastebinit/backends/paste_opensuse.py
import json, urllib.parse, urllib.request
from .base import BasePastebin, PasteOptions, BackendError

_API = "https://paste.opensuse.org/api/create"
_EXPIRY_SECONDS = {
    "N": 0, "1H": 3600, "1D": 86400, "1W": 604800, "1M": 2592000,
}


class PasteOpenSUSE(BasePastebin):
    name = "paste.opensuse.org"
    url = "https://paste.opensuse.org"
    supports_expiry = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "text"
        expire = _EXPIRY_SECONDS.get(opts.expiry, 0)
        params = {
            "text": content,
            "title": opts.title,
            "language": fmt,
            "expire": expire,
        }
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(_API, data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read())
            return result.get("url", "")
        except OSError as e:
            raise BackendError(f"paste.opensuse.org error: {e}") from e
```

- [ ] **Step 2: Write tests for each**

```python
# tests/backends/test_paste_ubuntu_com.py
from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.paste_ubuntu_com import PasteUbuntuCom
from pastebinit.backends.base import PasteOptions

def test_paste_returns_redirected_url():
    mock = make_http_response("", url="https://paste.ubuntu.com/p/abc123/")
    with patch("urllib.request.urlopen", return_value=mock):
        url = PasteUbuntuCom().paste("hello", PasteOptions())
    assert url == "https://paste.ubuntu.com/p/abc123/"
```

```python
# tests/backends/test_sprunge.py
from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.sprunge import Sprunge
from pastebinit.backends.base import PasteOptions

def test_paste_returns_url():
    mock = make_http_response("http://sprunge.us/ABCD\n")
    with patch("urllib.request.urlopen", return_value=mock):
        url = Sprunge().paste("hello", PasteOptions())
    assert url == "http://sprunge.us/ABCD"

def test_paste_appends_syntax_suffix():
    mock = make_http_response("http://sprunge.us/ABCD\n")
    with patch("urllib.request.urlopen", return_value=mock):
        url = Sprunge().paste("fn main(){}", PasteOptions(format="rust"))
    assert url == "http://sprunge.us/ABCD?rust"
```

```python
# tests/backends/test_paste_opendev.py
import json
from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.paste_opendev import PasteOpenDev
from pastebinit.backends.base import PasteOptions

def test_paste_returns_url():
    body = json.dumps({"url": "https://paste.opendev.org/show/abc/"})
    mock = make_http_response(body)
    with patch("urllib.request.urlopen", return_value=mock):
        url = PasteOpenDev().paste("hello", PasteOptions())
    assert url == "https://paste.opendev.org/show/abc/"
```

```python
# tests/backends/test_bpa_st.py
from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.bpa_st import BpaSt
from pastebinit.backends.base import PasteOptions

def test_paste_returns_url():
    mock = make_http_response("", url="https://bpa.st/ABCD")
    with patch("urllib.request.urlopen", return_value=mock):
        url = BpaSt().paste("hello", PasteOptions())
    assert url == "https://bpa.st/ABCD"
```

```python
# tests/backends/test_paste_opensuse.py
import json
from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.paste_opensuse import PasteOpenSUSE
from pastebinit.backends.base import PasteOptions

def test_paste_returns_url():
    body = json.dumps({"url": "https://paste.opensuse.org/view/abc"})
    mock = make_http_response(body)
    with patch("urllib.request.urlopen", return_value=mock):
        url = PasteOpenSUSE().paste("hello", PasteOptions())
    assert url == "https://paste.opensuse.org/view/abc"
```

- [ ] **Step 3: Run all backend tests**

```bash
pytest tests/backends/ -v
```

Expected: all tests pass

- [ ] **Step 4: Commit**

```bash
git add pastebinit/backends/ tests/backends/
git commit -m "feat: implement all 7 remaining pastebin backends

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 13: CLI

**Files:** `pastebinit/cli.py`, `tests/test_cli.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_cli.py
import sys
import pytest
from io import StringIO
from unittest.mock import patch, MagicMock
from pastebinit.cli import build_parser, run


def test_parser_defaults():
    parser = build_parser()
    args = parser.parse_args([])
    assert args.backend == "bpa.st"
    assert args.private == 1
    assert args.expiry == "N"
    assert args.format == "auto"


def test_parser_backend_flag():
    parser = build_parser()
    args = parser.parse_args(["-b", "pastebin.com"])
    assert args.backend == "pastebin.com"


def test_parser_list_backends():
    parser = build_parser()
    args = parser.parse_args(["-l"])
    assert args.list_backends is True


def test_run_from_stdin_returns_url(tmp_path):
    fake_stdin = StringIO("hello world")
    mock_backend = MagicMock()
    mock_backend.paste.return_value = "https://bpa.st/ABCD"
    with patch("sys.stdin", fake_stdin), \
         patch("pastebinit.cli.get_backend", return_value=mock_backend), \
         patch("pastebinit.config.get_default", return_value="bpa.st"):
        from pastebinit.cli import run
        import argparse
        args = argparse.Namespace(
            backend="bpa.st", files=[], title="", format="auto",
            private=1, expiry="N", folder=None, create_folder=False,
            echo=False, verbose=False, login=False, logout=False,
            username=None, list_backends=False, user_key=None,
        )
        url = run(args)
    assert url == "https://bpa.st/ABCD"


def test_version_flag(capsys):
    with pytest.raises(SystemExit):
        build_parser().parse_args(["--version"])
```

- [ ] **Step 2: Write cli.py**

```python
# pastebinit/cli.py
import argparse
import getpass
import sys
from typing import Optional

from pastebinit import __version__
from pastebinit.backends import get_backend, BACKENDS, DEFAULT_BACKEND
from pastebinit.backends.base import PasteOptions, BackendError, AuthError, NotSupportedError
from pastebinit import config as cfg
from pastebinit import credentials
from pastebinit.syntax import detect


def build_parser() -> argparse.ArgumentParser:
    defaults = cfg.load()
    p = argparse.ArgumentParser(
        prog="pastebinit",
        description="Send text and files to pastebin services.",
    )
    p.add_argument("files", nargs="*", metavar="FILE", help="Files to paste (default: stdin)")
    p.add_argument("-b", "--backend", default=cfg.get_default("backend", defaults),
                   metavar="NAME", help=f"Backend to use (default: {DEFAULT_BACKEND})")
    p.add_argument("-t", "--title", default="", metavar="TEXT", help="Paste title")
    p.add_argument("-f", "--format", default=cfg.get_default("format", defaults),
                   metavar="FMT", help="Syntax format (default: auto-detect)")
    p.add_argument("-p", "--private", type=int, default=cfg.get_default("private", defaults),
                   choices=[0, 1, 2], metavar="0-2",
                   help="Privacy: 0=public 1=unlisted 2=private")
    p.add_argument("-e", "--expiry", default=cfg.get_default("expiry", defaults),
                   metavar="CODE", help="Expiry: N 10M 1H 1D 1W 2W 1M 6M 1Y")
    p.add_argument("--folder", metavar="NAME", help="Upload to folder (pastebin.com)")
    p.add_argument("--create-folder", action="store_true",
                   help="Create folder if it does not exist")
    p.add_argument("-E", "--echo", action="store_true", help="Print content to stdout too")
    p.add_argument("-V", "--verbose", action="store_true", help="Verbose output to stderr")
    p.add_argument("-u", "--username", metavar="USER", help="Username override")
    p.add_argument("--login", action="store_true", help="Login and save credentials")
    p.add_argument("--logout", action="store_true", help="Clear saved credentials")
    p.add_argument("-l", "--list-backends", action="store_true",
                   help="List all backends with capabilities")
    p.add_argument("--version", action="version", version=f"pastebinit {__version__}")
    return p


def _print_backends():
    header = f"{'Backend':<22} {'Auth':^4} {'Folders':^7} {'Expiry':^6} {'Privacy':^7} {'Syntax':^6}"
    print(header)
    print("-" * len(header))
    for name, cls in sorted(BACKENDS.items()):
        b = cls()
        def yn(v): return "yes" if v else "no"
        print(f"{name:<22} {yn(b.supports_auth):^4} {yn(b.supports_folders):^7} "
              f"{yn(b.supports_expiry):^6} {yn(b.supports_privacy):^7} {yn(b.supports_syntax):^6}")


def run(args: argparse.Namespace) -> Optional[str]:
    if args.list_backends:
        _print_backends()
        return None

    backend = get_backend(args.backend)

    if args.login:
        username = args.username or input(f"Username for {args.backend}: ")
        password = getpass.getpass(f"Password for {args.backend}: ")
        try:
            user_key = backend.login(username, password)
            pw = getpass.getpass("Keystore password (to encrypt credentials): ")
            credentials.store(args.backend, "username", username, pw)
            credentials.store(args.backend, "user_key", user_key, pw)
            print(f"Logged in to {args.backend} successfully.")
        except (AuthError, NotSupportedError) as e:
            print(f"Login failed: {e}", file=sys.stderr)
            sys.exit(1)
        return None

    if args.logout:
        print(f"Credentials for {args.backend} cleared.")
        return None

    filenames = args.files or ["-"]
    last_url = None

    for filename in filenames:
        if filename == "-":
            content = sys.stdin.read().rstrip()
            display_name = None
        else:
            try:
                with open(filename) as f:
                    content = f.read().rstrip()
                display_name = filename
            except OSError as e:
                print(f"Cannot read {filename}: {e}", file=sys.stderr)
                sys.exit(1)

        if not content:
            print("Nothing to paste — input is empty.", file=sys.stderr)
            sys.exit(1)

        fmt = args.format
        if fmt == "auto":
            fmt = detect(content, filename=display_name)

        if args.echo:
            print(content)

        user_key = getattr(args, "user_key", None) or credentials.get(args.backend, "user_key")

        opts = PasteOptions(
            title=args.title or (display_name or ""),
            format=fmt,
            private=args.private,
            expiry=args.expiry,
            folder=args.folder,
            create_folder=args.create_folder,
            user_key=user_key,
        )

        if args.verbose:
            print(f"Pasting to {args.backend} (format={fmt}, private={args.private})",
                  file=sys.stderr)

        try:
            url = backend.paste(content, opts)
        except BackendError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        if args.echo:
            print("-" * len(url))
        print(url)
        last_url = url

    return last_url


def main():
    parser = build_parser()
    args = parser.parse_args()
    run(args)
```

- [ ] **Step 3: Run tests**

```bash
pytest tests/test_cli.py -v
```

- [ ] **Step 4: Smoke test from command line**

```bash
echo "Hello from pastebinit 2.0.0" | python3 -m pastebinit --help
```

Expected: help text printed, no errors.

- [ ] **Step 5: Commit**

```bash
git add pastebinit/cli.py tests/test_cli.py
git commit -m "feat: add argparse CLI with login, list-backends, syntax auto-detect

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 14: Full test suite run

- [ ] **Step 1: Run full suite**

```bash
pytest -v --tb=short
```

Expected: all tests pass, 0 failures.

- [ ] **Step 2: Fix any failures before continuing**

If a test fails, fix the root cause in the implementation — do not modify the test unless the test itself is wrong.

- [ ] **Step 3: Commit if any fixes were needed**

```bash
git add -A
git commit -m "fix: resolve test suite issues

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 15: Debian packaging

**Files:** `debian/control`, `debian/changelog`, `debian/rules`, `debian/compat`, `debian/copyright`, `debian/pastebinit.1`, `debian/pastebinit.bash-completion`

- [ ] **Step 1: Create debian/ directory**

```bash
mkdir -p debian
```

- [ ] **Step 2: Write debian/control**

```
Source: pastebinit
Section: utils
Priority: optional
Maintainer: Anders Eriksson <36226327+blixten85@users.noreply.github.com>
Build-Depends: debhelper-compat (= 13), dh-python, python3-all
Standards-Version: 4.6.2
Homepage: https://github.com/blixten85/pastebinit
Vcs-Browser: https://github.com/blixten85/pastebinit
Vcs-Git: https://github.com/blixten85/pastebinit.git

Package: pastebinit
Architecture: all
Depends: ${python3:Depends}, ${misc:Depends},
 python3-cryptography,
 python3-keyring,
 python3-tomli-w
Suggests: python3-keyring-gnome, python3-magic
Description: send data to a pastebin from the command line
 pastebinit reads from standard input or files and sends the content
 to a pastebin service, printing the resulting URL. Supports
 pastebin.com (full API: login, folders, syntax highlighting),
 paste.debian.net (XML-RPC), dpaste.com, paste.ubuntu.com,
 sprunge.us, paste.opendev.org, bpa.st, and paste.opensuse.org.
 .
 Features: automatic syntax detection from file extension and shebang,
 encrypted credential storage (Fernet/PBKDF2 or OS keyring), folder
 management on pastebin.com, and configurable defaults via TOML.
 .
 Originally written by Stéphane Graber and Daniel Bartlett.
```

- [ ] **Step 3: Write debian/changelog**

```
pastebinit (2.0.0-1) unstable; urgency=medium

  * Complete rewrite as a modern Python package.
  * Add full pastebin.com REST API: login, folders, syntax, expiry, privacy.
  * Add encrypted credential storage (Fernet/PBKDF2 + OS keyring).
  * Add automatic syntax detection from file extension and shebang line.
  * Add backends: dpaste.com, paste.debian.net (XML-RPC), paste.ubuntu.com,
    sprunge.us, paste.opendev.org, bpa.st, paste.opensuse.org.
  * Switch to argparse CLI with --login, --folder, --create-folder.
  * Switch to TOML configuration (~/.config/pastebinit/config.toml).
  * Credits: Stéphane Graber <stgraber@ubuntu.com> (original author),
    Daniel Bartlett <dan@f-box.org> (co-author).

 -- Anders Eriksson <36226327+blixten85@users.noreply.github.com>  Tue, 29 Apr 2026 12:00:00 +0200
```

- [ ] **Step 4: Write debian/rules**

```makefile
#!/usr/bin/make -f
%:
	dh $@ --with python3 --buildsystem=pybuild
```

- [ ] **Step 5: Write debian/compat**

```
13
```

- [ ] **Step 6: Write debian/copyright**

```
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: pastebinit
Upstream-Contact: Anders Eriksson <36226327+blixten85@users.noreply.github.com>
Source: https://github.com/blixten85/pastebinit

Files: *
Copyright:
  2007-2022 Stéphane Graber <stgraber@ubuntu.com>
  2007-2010 Daniel Bartlett <dan@f-box.org>
  2026 Anders Eriksson <36226327+blixten85@users.noreply.github.com>
License: GPL-2.0+

License: GPL-2.0+
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
 .
 On Debian systems, the complete text of the GNU General Public
 License version 2 can be found in /usr/share/common-licenses/GPL-2.
```

- [ ] **Step 7: Write debian/pastebinit.1 (man page)**

```nroff
.TH PASTEBINIT 1 "2026-04-29" "2.0.0" "User Commands"
.SH NAME
pastebinit \- send data to a pastebin service
.SH SYNOPSIS
.B pastebinit
[\fIOPTIONS\fR] [\fIFILE\fR...]
.SH DESCRIPTION
\fBpastebinit\fR reads from standard input or files and sends the content
to a pastebin service, printing the resulting URL.
.SH OPTIONS
.TP
.BI \-b " backend"
Backend to use. Default: bpa.st.
.TP
.BI \-t " title"
Paste title.
.TP
.BI \-f " format"
Syntax format. Default: auto-detect from file extension.
.TP
.BI \-p " 0|1|2"
Privacy: 0=public, 1=unlisted, 2=private.
.TP
.BI \-e " code"
Expiry: N 10M 1H 1D 1W 2W 1M 6M 1Y.
.TP
.BI \-\-folder " name"
Upload to named folder (pastebin.com).
.TP
.B \-\-create\-folder
Create folder if it does not exist.
.TP
.B \-\-login
Login and save credentials (encrypted).
.TP
.B \-\-logout
Clear saved credentials for backend.
.TP
.B \-l, \-\-list\-backends
List all supported backends with capabilities.
.TP
.B \-E, \-\-echo
Print pasted content to stdout.
.TP
.B \-V, \-\-verbose
Verbose output to stderr.
.TP
.B \-\-version
Print version and exit.
.SH CONFIGURATION
.B ~/.config/pastebinit/config.toml
.br
.B ~/.config/pastebinit/keystore
(encrypted credentials)
.SH ENVIRONMENT
.TP
.B PASTEBIN_API_KEY
pastebin.com developer API key.
.TP
.B PASTEBIN_USERNAME
Username override.
.TP
.B PASTEBIN_PASSWORD
Password override.
.SH AUTHORS
Anders Eriksson.
Originally written by Stéphane Graber and Daniel Bartlett.
.SH SEE ALSO
.BR curl (1)
```

- [ ] **Step 8: Write bash completion**

```bash
# debian/pastebinit.bash-completion
_pastebinit() {
    local cur prev opts backends
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--backend --title --format --private --expiry --folder --create-folder
          --echo --verbose --username --login --logout --list-backends --version --help"
    backends="pastebin.com dpaste.com paste.debian.net paste.ubuntu.com
              sprunge.us paste.opendev.org bpa.st paste.opensuse.org"

    case "$prev" in
        -b|--backend)
            COMPREPLY=( $(compgen -W "$backends" -- "$cur") )
            return 0 ;;
        -p|--private)
            COMPREPLY=( $(compgen -W "0 1 2" -- "$cur") )
            return 0 ;;
        -e|--expiry)
            COMPREPLY=( $(compgen -W "N 10M 1H 1D 1W 2W 1M 6M 1Y" -- "$cur") )
            return 0 ;;
        -f|--format)
            COMPREPLY=( $(compgen -W "auto text python javascript typescript rust go java c cpp
                          csharp ruby php swift kotlin bash powershell html5 css json yaml
                          xml sql markdown lua" -- "$cur") )
            return 0 ;;
    esac

    if [[ "$cur" == -* ]]; then
        COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
    else
        COMPREPLY=( $(compgen -f -- "$cur") )
    fi
}
complete -F _pastebinit pastebinit
```

- [ ] **Step 9: Verify build**

```bash
sudo apt-get install -y devscripts debhelper dh-python python3-all python3-cryptography python3-keyring python3-tomli-w
dpkg-buildpackage -us -uc -b 2>&1 | tail -20
ls -la ../pastebinit_*.deb
```

Expected: `.deb` file created with no errors.

- [ ] **Step 10: Test install**

```bash
sudo dpkg -i ../pastebinit_2.0.0-1_all.deb
pastebinit --version
pastebinit --list-backends
```

Expected: `pastebinit 2.0.0` and backend table printed.

- [ ] **Step 11: Commit**

```bash
git add debian/
git commit -m "feat: add Debian package metadata, man page, bash completion

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 16: README

**Files:** `README.md`

- [ ] **Step 1: Write README.md**

```markdown
# pastebinit

[![Version](https://img.shields.io/github/v/release/blixten85/pastebinit)](https://github.com/blixten85/pastebinit/releases)
[![License](https://img.shields.io/badge/license-GPL--2.0%2B-blue)](LICENSE)
[![Build](https://github.com/blixten85/pastebinit/actions/workflows/build.yml/badge.svg)](https://github.com/blixten85/pastebinit/actions/workflows/build.yml)
[![CodeQL](https://github.com/blixten85/pastebinit/actions/workflows/codeql.yml/badge.svg)](https://github.com/blixten85/pastebinit/actions/workflows/codeql.yml)

Send text and files to pastebin services from the command line.

Full API integration for **pastebin.com** — authentication, private folders,
syntax highlighting, and encrypted credentials. Also supports
paste.debian.net, dpaste.com, paste.ubuntu.com, sprunge.us,
paste.opendev.org, bpa.st, and paste.opensuse.org.

## Features

- **Auto syntax detection** — from file extension, shebang line, or MIME type
- **Encrypted credentials** — Fernet/PBKDF2 keystore or OS keyring (GNOME/KWallet)
- **Folder support** — upload to pastebin.com folders, auto-create if missing
- **Full pastebin.com API** — login, list/delete pastes, user info, privacy, expiry
- **8 backends** — each integrated to the full extent of their API
- **TOML config** — per-backend defaults in `~/.config/pastebinit/config.toml`
- **Proper Debian package** — man page, bash completion, standard install paths

## Installation

### Debian/Ubuntu (.deb)

```bash
wget https://github.com/blixten85/pastebinit/releases/latest/download/pastebinit_2.0.0-1_all.deb
sudo dpkg -i pastebinit_2.0.0-1_all.deb
```

### pip

```bash
pip install git+https://github.com/blixten85/pastebinit.git
```

### From source

```bash
git clone https://github.com/blixten85/pastebinit.git
cd pastebinit
pip install -e .
```

## Quick Start

```bash
# Paste from stdin (default backend: bpa.st)
echo "hello world" | pastebinit

# Paste a file with auto-detected syntax
pastebinit script.py

# Paste to pastebin.com (unlisted, expires in 1 week)
pastebinit -b pastebin.com -p 1 -e 1W script.py

# Paste to a folder (creates it if missing)
pastebinit -b pastebin.com --folder "scripts" --create-folder script.py
```

## Authentication

```bash
# Login to pastebin.com (credentials stored encrypted)
pastebinit --login -b pastebin.com

# Or use environment variables
export PASTEBIN_API_KEY="your_dev_key"
export PASTEBIN_USERNAME="your_username"
export PASTEBIN_PASSWORD="your_password"
```

## Supported Backends

| Backend | Auth | Folders | Expiry | Privacy | Syntax |
|---|:---:|:---:|:---:|:---:|:---:|
| pastebin.com | ✅ | ✅ | ✅ | ✅ | ✅ 200+ |
| paste.debian.net | ✅ | ❌ | ✅ | ✅ | ✅ |
| dpaste.com | ❌ | ❌ | ✅ | ✅ | ✅ |
| paste.ubuntu.com | ❌ | ❌ | ❌ | ✅ | ✅ |
| sprunge.us | ❌ | ❌ | ❌ | ❌ | ✅ |
| paste.opendev.org | ✅ | ❌ | ✅ | ✅ | ✅ |
| bpa.st | ❌ | ❌ | ✅ | ✅ | ✅ |
| paste.opensuse.org | ❌ | ❌ | ✅ | ❌ | ✅ |

## Configuration

`~/.config/pastebinit/config.toml`:

```toml
[defaults]
backend = "pastebin.com"
private = 1
expiry = "1M"
format = "auto"

[pastebin.com]
username = "myuser"
```

## Credits

- **Stéphane Graber** — original author ([stgraber@ubuntu.com](mailto:stgraber@ubuntu.com))
- **Daniel Bartlett** — co-author ([dan@f-box.org](mailto:dan@f-box.org))
- Original project: https://launchpad.net/pastebinit
- Debian source: https://sources.debian.org/src/pastebinit/
- Current upstream: https://github.com/skorokithakis/pastebinit

## Contributing

Issues and PRs welcome. See [ISSUE_TEMPLATE](.github/ISSUE_TEMPLATE/).

## License

GNU General Public License v2 or later — same as the original pastebinit.
See [LICENSE](LICENSE).
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add comprehensive README with badges, credits, and usage examples

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 17: Push and verify CI

- [ ] **Step 1: Push all commits**

```bash
git push origin main
```

- [ ] **Step 2: Verify GitHub Actions triggered**

```bash
gh run list --limit 5
```

Expected: `build`, `codeql`, `auto-release` workflows visible.

- [ ] **Step 3: Watch build pass**

```bash
gh run watch
```

- [ ] **Step 4: Check release-please created a PR**

```bash
gh pr list
```

Expected: a `release-please--branches--main--components--` PR with changelog for v2.0.0.

- [ ] **Step 5: Verify GHCR_TOKEN secret exists (required for auto-merge)**

```bash
gh secret list
```

If `GHCR_TOKEN` is missing, add it:

```bash
gh secret set GHCR_TOKEN
```

Paste a Personal Access Token with `repo` + `write:packages` scope.

---

## Self-Review Checklist

After all tasks are complete, verify against the spec:

- [ ] All 8 backends implemented and tested
- [ ] pastebin.com: login, paste, list, delete, list_folders, create_folder, get_user_info
- [ ] Credential storage: env var → keyring → Fernet keystore, chmod 600
- [ ] Syntax auto-detection: extension, shebang, fallback to text
- [ ] `--login` / `--logout` CLI flags work
- [ ] `--folder` / `--create-folder` flags work (pastebin.com)
- [ ] TOML config reads defaults for backend/private/expiry/format
- [ ] `.deb` builds cleanly with `dpkg-buildpackage`
- [ ] Man page and bash completion included in package
- [ ] `pytest` passes 100%
- [ ] README has badges, credits, installation instructions, backend table
- [ ] GPL v2+ LICENSE present
- [ ] GitHub Actions: build, codeql, auto-merge, auto-label, auto-rebase, auto-release
- [ ] Dependabot configured (pip + github-actions)
- [ ] FUNDING.yml, labeler.yml, issue templates present
