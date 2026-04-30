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
