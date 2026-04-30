from unittest.mock import MagicMock, patch


def make_http_response(body: str, url: str = "https://example.com/abc123") -> MagicMock:
    """Return a mock that behaves like urllib.request.urlopen()'s context manager."""
    mock = MagicMock()
    mock.read.return_value = body.encode()
    mock.url = url
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


def patch_urlopen(body: str, url: str = "https://example.com/abc123"):
    """Patch urllib.request.urlopen to return a fake response."""
    return patch(
        "urllib.request.urlopen",
        return_value=make_http_response(body, url),
    )
