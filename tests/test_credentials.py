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
