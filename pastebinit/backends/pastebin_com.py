from .base import BasePastebin, PasteOptions, BackendError, AuthError


class PastebinCom(BasePastebin):
    name = "pastebin.com"
    url = "https://pastebin.com"
    supports_auth = True
    supports_folders = True
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        raise NotImplementedError
