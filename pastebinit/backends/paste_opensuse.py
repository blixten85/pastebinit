from .base import BasePastebin, PasteOptions, BackendError


class PasteOpenSUSE(BasePastebin):
    name = "paste.opensuse.org"
    url = "https://paste.opensuse.org"
    supports_expiry = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        raise NotImplementedError
