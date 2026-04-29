from .base import BasePastebin, PasteOptions, BackendError


class BpaSt(BasePastebin):
    name = "bpa.st"
    url = "https://bpa.st"
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        raise NotImplementedError
