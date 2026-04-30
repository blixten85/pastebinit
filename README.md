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

## Bash Completion

Included in the `.deb` package. To install manually:

```bash
source debian/pastebinit.bash-completion
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
