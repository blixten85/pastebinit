# pastebinit — Design Spec
**Date:** 2026-04-29  
**Status:** Approved  
**Author:** Anders Eriksson (blixten85)

---

## Overview

A full rewrite of `pastebinit` from scratch — a command-line tool to send text/files to pastebin services. The original codebase (v1.6.2, GPL v2+) serves as inspiration for what to do and not do, not as source material. All original authors credited. The goal is a clean, modern Python package with full API integration per backend, encrypted credential storage, and a proper Debian package — suitable for submitting upstream to Thomas Ward (current Debian maintainer, teward@ubuntu.com) for adoption into Ubuntu/Debian official repositories.

**Upstream status (verified 2026-04-29):** Actively maintained. Latest upstream: 1.8.0 (2025-11-30). This rewrite starts at **v2.0.0** — above all existing versions, no conflict. Key changes in 1.8.0 we incorporate: `argparse` instead of `getopt`, default backend `bpa.st`, OpenSUSE support, cleaned import structure.

---

## Architecture

### Package Structure

```
pastebinit/
├── pastebinit/
│   ├── __init__.py
│   ├── __main__.py              # python -m pastebinit entry point
│   ├── cli.py                   # argparse, top-level dispatch
│   ├── config.py                # TOML config read/write (~/.config/pastebinit/config.toml)
│   ├── credentials.py           # encrypted credential storage (Fernet + keyring)
│   ├── syntax.py                # auto-detect syntax from extension, shebang, magic bytes
│   └── backends/
│       ├── base.py              # BasePastebin ABC
│       ├── pastebin_com.py      # pastebin.com — full REST API
│       ├── dpaste.py            # dpaste.com — REST API
│       ├── paste_debian_net.py  # paste.debian.net — XML-RPC
│       ├── paste_ubuntu_com.py  # paste.ubuntu.com — HTTP POST
│       ├── sprunge.py           # sprunge.us — HTTP POST
│       ├── paste_opendev.py     # paste.opendev.org — REST API
│       ├── bpa_st.py            # bpa.st — default in upstream 1.8.0+
│       └── paste_opensuse.py    # paste.opensuse.org — OpenSUSE distro default
├── tests/
│   ├── test_cli.py
│   ├── test_syntax.py
│   ├── test_credentials.py
│   └── backends/
│       └── test_*.py            # one per backend (mocked HTTP)
├── pyproject.toml
├── setup.cfg
├── debian/
│   ├── control
│   ├── changelog
│   ├── rules
│   ├── copyright
│   ├── pastebinit.1
│   └── pastebinit.bash-completion
├── .github/
│   └── workflows/
│       ├── build.yml
│       ├── codeql.yml
│       ├── auto-merge.yml
│       ├── auto-label.yml
│       ├── auto-rebase.yml
│       └── auto-release.yml
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── dependabot.yml
│   ├── labeler.yml
│   └── FUNDING.yml
├── README.md
└── LICENSE                      # GPL v2+
```

---

## Backends

### Common Interface (`base.py`)

```python
class BasePastebin(ABC):
    name: str           # human-readable name
    url: str            # base URL
    supports_auth: bool = False
    supports_folders: bool = False
    supports_expiry: bool = False
    supports_privacy: bool = False
    supports_syntax: bool = False

    @abstractmethod
    def paste(self, content: str, **opts) -> str: ...

    # Optional — raise NotImplementedError if unsupported
    def login(self, username: str, password: str) -> str: ...
    def list_pastes(self, user_key: str) -> list[dict]: ...
    def delete_paste(self, paste_key: str, user_key: str) -> bool: ...
    def list_folders(self, user_key: str) -> list[dict]: ...
    def create_folder(self, name: str, user_key: str) -> str: ...
    def get_user_info(self, user_key: str) -> dict: ...
```

### Backend Capability Matrix

| Backend | Auth | Folders | Expiry | Privacy | Syntax | Protocol |
|---|---|---|---|---|---|---|
| pastebin.com | ✅ | ✅ | ✅ | ✅ | ✅ 200+ | REST |
| paste.debian.net | ✅ | ❌ | ✅ | ✅ | ✅ | XML-RPC |
| dpaste.com | ❌ | ❌ | ✅ | ✅ | ✅ | REST |
| paste.ubuntu.com | ❌ | ❌ | ❌ | ✅ | ✅ | HTTP POST |
| sprunge.us | ❌ | ❌ | ❌ | ❌ | ✅ | HTTP POST |
| paste.opendev.org | ✅ | ❌ | ✅ | ✅ | ✅ | REST |
| bpa.st | ❌ | ❌ | ✅ | ✅ | ✅ | HTTP POST |
| paste.opensuse.org | ❌ | ❌ | ✅ | ✅ | ✅ | HTTP POST |

### pastebin.com (full treatment)

Implements the complete Pastebin REST API (`https://pastebin.com/api/api_post.php`):

- **Login** → `api_user_key` (cached encrypted, TTL handled)
- **Create paste** — title, format, privacy (0/1/2), expiry (N/10M/1H/1D/1W/2W/1M/6M/1Y), folder key
- **List pastes** — all pastes for authenticated user
- **Delete paste** — by paste key
- **Get raw** — own private pastes via authenticated raw endpoint
- **List folders** — retrieve user's folders with keys
- **Create folder** — create new folder, return folder key
- **Upload to folder** — resolve folder name → key, create if `--create-folder` passed
- **User info** — account details, limits, quota

---

## CLI Interface

```
pastebinit [OPTIONS] [FILE...]

Input:
  FILE...               One or more files (stdin if omitted)
  -i, --input FILE      Explicit input file

Authentication:
  --login               Prompt for credentials, save encrypted
  --logout              Clear saved credentials for backend
  -u, --username TEXT   Username (overrides config/keystore)

Backend:
  -b, --backend NAME    Backend to use (default: pastebin.com)
  -l, --list-backends   List all backends with capability table

Paste options:
  -t, --title TEXT      Paste title/filename
  -f, --format TEXT     Syntax format (default: auto)
  -p, --private INT     0=public 1=unlisted 2=private
  -e, --expiry CODE     N 10M 1H 1D 1W 2W 1M 6M 1Y (default: N)
  --folder TEXT         Folder name to upload into
  --create-folder       Create folder if it doesn't exist
  -E, --echo            Print content to stdout as well
  -V, --verbose         Verbose output to stderr
  -v, --version         Print version
  -h, --help            Print help
```

---

## Credential Storage

Three layers, checked in priority order:

### Layer 1 — Environment variables (highest priority)
```
PASTEBIN_API_KEY       pastebin.com developer key
PASTEBIN_USERNAME      username
PASTEBIN_PASSWORD      password
```
Suitable for CI/automation/scripts.

### Layer 2 — OS Keyring
Via Python `keyring` library. Works transparently on systems with GNOME Keyring, KWallet, or macOS Keychain. No interaction needed after first login.

### Layer 3 — Encrypted config file (fallback, headless servers)
`~/.config/pastebinit/keystore` — Fernet symmetric encryption.

- Key derived from user passphrase via PBKDF2-HMAC-SHA256 (600,000 iterations)
- Salt stored alongside encrypted blob
- File created on first `--login`, permissions set to `600` automatically
- Passphrase prompted once per session (or on every invocation if no keyring available)
- Encrypted fields: `api_dev_key`, `password`, `user_key` (cached login token)

### Config file (`~/.config/pastebinit/config.toml`)
```toml
[defaults]
backend = "pastebin.com"
private = 1
expiry = "1M"
format = "auto"

[pastebin.com]
# Sensitive values stored in keystore, not here
username = "myuser"

[dpaste.com]
expiry = "1W"
```

---

## Syntax Auto-Detection (`syntax.py`)

Priority order:
1. `--format` CLI argument (explicit override)
2. File extension mapping (`.py` → `python`, `.rs` → `rust`, `.ts` → `typescript`, etc.)
3. Shebang line parsing (`#!/usr/bin/env python3` → `python`)
4. Magic bytes (e.g. ELF header → `asm`)
5. `python-magic` MIME type if installed
6. Fallback: `text`

Full mapping table covers all 200+ pastebin.com format codes, plus equivalents for backends with fewer options (best-effort mapping to closest match).

---

## Debian Packaging

### `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]

[project]
name = "pastebinit"
version = "2.0.0"
requires-python = ">=3.10"
dependencies = [
    "cryptography>=41",
    "keyring>=24",
    "tomllib; python_version < '3.11'",
    "tomli-w>=1.0",
]
```

### `debian/control` (key fields)
```
Package: pastebinit
Architecture: all
Depends: python3, python3-cryptography, python3-keyring, python3-tomli-w
Suggests: python3-keyring-gnome, python3-magic
Description: send data to a pastebin from the command line
```

### CI `.deb` build
`build.yml` runs `dpkg-buildpackage -us -uc` on Ubuntu Noble, uploads resulting `.deb` as a GitHub Release asset on every tagged release. Users can `dpkg -i pastebinit_2.0.0_all.deb` immediately.

Man page (`pastebinit.1`) and bash-completion (`pastebinit.bash-completion`) included in the package.

---

## GitHub Repository Setup

Repository: `github.com/blixten85/pastebinit`

### Workflows (matching existing repos exactly)

| Workflow | Trigger | Purpose |
|---|---|---|
| `build.yml` | push/release | run tests + build .deb |
| `codeql.yml` | push/PR/weekly | Python security analysis |
| `auto-merge.yml` | PR opened | dependabot/claude/release-please auto-merge |
| `auto-label.yml` | PR opened | label by changed files |
| `auto-rebase.yml` | push to main | rebase PRs with auto-merge label |
| `auto-release.yml` | push to main | release-please version bump + changelog |

### Dependabot
Weekly, Monday 09:00 Europe/Stockholm. Ecosystems: `pip` + `github-actions`. Labels: `dependencies`/`ci` + `auto-merge`.

### Labels
`bug`, `enhancement`, `dependencies`, `ci`, `documentation`, `auto-merge`, `auto-rebase`

### Issue Templates
- Bug report (with environment, steps, logs)
- Feature request (with use case, alternatives)

### Branch protection / ruleset
- `claude/*` branches auto-merge once checks pass (via `GHCR_TOKEN`)
- Required checks: `build`, `CodeQL`

---

## README Structure

```markdown
# pastebinit

[version badge] [license badge] [build badge] [CodeQL badge]

Send text and files to pastebin services from the command line.
Full API integration with pastebin.com — authentication, folders,
syntax highlighting auto-detection, and encrypted credential storage.
Also supports paste.debian.net, dpaste.com, paste.ubuntu.com,
sprunge.us, and paste.opendev.org.

## Features
## Installation
  ### Debian/Ubuntu (.deb)
  ### pip
  ### From source
## Quick Start
## Authentication
## Supported Backends (capability table)
## Configuration
## Syntax Auto-Detection
## Bash Completion
## Contributing
## Credits
  - Stéphane Graber <stgraber@ubuntu.com> — original author
  - Daniel Bartlett <dan@f-box.org> — co-author
  - Original project: https://launchpad.net/pastebinit
  - Debian source: https://sources.debian.org/src/pastebinit/
## License
  GPL v2+ — same as original pastebinit
```

---

## What the Original Code Taught Us (Do's and Don'ts)

**Don'ts (from v1.6.2):**
- Single 474-line monolithic script — impossible to test backends in isolation
- XML config files with no schema validation
- `except:` bare except clauses swallowing all errors silently
- No type hints anywhere
- `distutils`-era packaging (no `pyproject.toml`)
- Credentials stored in plaintext XML

**Do's (kept from v1.6.2):**
- `socket.setdefaulttimeout()` to avoid hanging forever
- Distribution-aware default backend selection
- Support stdin (`-`) as implicit input when no file given
- Echo mode (`-E`) for confirming what was sent
- Verbose mode (`-V`) to stderr for debugging

---

## Out of Scope

- GUI / TUI interface
- Windows-specific packaging
- Hosting own pastebin service
- Paste editing (not supported by any backend API)
