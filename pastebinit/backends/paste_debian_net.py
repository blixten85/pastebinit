from .base import BasePastebin, PasteOptions, BackendError


class PasteDebianNet(BasePastebin):
    name = "paste.debian.net"
    url = "https://paste.debian.net"
    supports_auth = True
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        raise NotImplementedError
