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
