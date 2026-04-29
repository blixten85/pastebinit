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
        call_data = mock_open.call_args[0][0].data  # Request object's data
        assert b"api_paste_format=python" in call_data


def test_paste_with_private_level(backend):
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.return_value = make_http_response("https://pastebin.com/xyz")
        backend.paste("secret", PasteOptions(private=2, user_key="userkey"))
        call_data = mock_open.call_args[0][0].data
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
