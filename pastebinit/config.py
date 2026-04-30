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
