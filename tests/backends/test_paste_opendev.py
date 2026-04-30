import json
from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.paste_opendev import PasteOpenDev
from pastebinit.backends.base import PasteOptions


def test_paste_returns_url():
    body = json.dumps({"url": "https://paste.opendev.org/show/abc/"})
    mock = make_http_response(body)
    with patch("urllib.request.urlopen", return_value=mock):
        url = PasteOpenDev().paste("hello", PasteOptions())
    assert url == "https://paste.opendev.org/show/abc/"
