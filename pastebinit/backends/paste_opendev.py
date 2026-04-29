from .base import BasePastebin, PasteOptions, BackendError


class PasteOpenDev(BasePastebin):
    name = "paste.opendev.org"
    url = "https://paste.opendev.org"
    supports_auth = True
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        raise NotImplementedError
