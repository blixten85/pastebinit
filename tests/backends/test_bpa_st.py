from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.bpa_st import BpaSt
from pastebinit.backends.base import PasteOptions


def test_paste_returns_url():
    mock = make_http_response("", url="https://bpa.st/ABCD")
    with patch("urllib.request.urlopen", return_value=mock):
        url = BpaSt().paste("hello", PasteOptions())
    assert url == "https://bpa.st/ABCD"
