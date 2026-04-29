from .base import BasePastebin, PasteOptions, BackendError


class PasteUbuntuCom(BasePastebin):
    name = "paste.ubuntu.com"
    url = "https://paste.ubuntu.com"
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        raise NotImplementedError
