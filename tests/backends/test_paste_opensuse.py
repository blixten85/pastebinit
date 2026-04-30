import json
from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.paste_opensuse import PasteOpenSUSE
from pastebinit.backends.base import PasteOptions


def test_paste_returns_url():
    body = json.dumps({"url": "https://paste.opensuse.org/view/abc"})
    mock = make_http_response(body)
    with patch("urllib.request.urlopen", return_value=mock):
        url = PasteOpenSUSE().paste("hello", PasteOptions())
    assert url == "https://paste.opensuse.org/view/abc"
