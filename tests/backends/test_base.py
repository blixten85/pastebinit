import pytest
from pastebinit.backends.base import (
    BasePastebin, PasteOptions, BackendError, NotSupportedError, AuthError
)


class MinimalBackend(BasePastebin):
    name = "test"
    url = "https://test.example.com"

    def paste(self, content: str, opts: PasteOptions) -> str:
        return "https://test.example.com/abc"


def test_paste_options_defaults():
    opts = PasteOptions()
    assert opts.title == ""
    assert opts.format == "text"
    assert opts.private == 1
    assert opts.expiry == "N"
    assert opts.folder is None


def test_concrete_backend_paste():
    b = MinimalBackend()
    url = b.paste("hello", PasteOptions())
    assert url == "https://test.example.com/abc"


def test_unsupported_raises():
    b = MinimalBackend()
    with pytest.raises(NotSupportedError):
        b.login("user", "pass")
    with pytest.raises(NotSupportedError):
        b.list_pastes("key")
    with pytest.raises(NotSupportedError):
        b.delete_paste("key", "ukey")
    with pytest.raises(NotSupportedError):
        b.list_folders("ukey")
    with pytest.raises(NotSupportedError):
        b.create_folder("name", "ukey")
    with pytest.raises(NotSupportedError):
        b.get_user_info("ukey")
