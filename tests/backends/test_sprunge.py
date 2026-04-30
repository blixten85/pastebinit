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
