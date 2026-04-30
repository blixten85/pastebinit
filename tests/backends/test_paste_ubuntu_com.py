from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.paste_ubuntu_com import PasteUbuntuCom
from pastebinit.backends.base import PasteOptions


def test_paste_returns_redirected_url():
    mock = make_http_response("", url="https://paste.ubuntu.com/p/abc123/")
    with patch("urllib.request.urlopen", return_value=mock):
        url = PasteUbuntuCom().paste("hello", PasteOptions())
    assert url == "https://paste.ubuntu.com/p/abc123/"
