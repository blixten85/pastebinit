from .base import BasePastebin, PasteOptions, BackendError


class DPaste(BasePastebin):
    name = "dpaste.com"
    url = "https://dpaste.com"
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        raise NotImplementedError
