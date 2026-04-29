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
        data = mock_open.call_args[0][0].data
        assert b"syntax=rust" in data


def test_paste_sends_expiry(backend):
    mock_resp = make_http_response("https://dpaste.com/XYZ\n")
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.return_value = mock_resp
        backend.paste("hello", PasteOptions(expiry="1D"))
        data = mock_open.call_args[0][0].data
        assert b"expiry_days=1" in data
