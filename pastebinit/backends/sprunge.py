from .base import BasePastebin, PasteOptions, BackendError


class Sprunge(BasePastebin):
    name = "sprunge.us"
    url = "http://sprunge.us"
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        raise NotImplementedError
