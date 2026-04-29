import xmlrpc.client
from .base import BasePastebin, PasteOptions, BackendError

_ENDPOINT = "http://paste.debian.net/server.pl"

_EXPIRY_SECONDS = {
    "N": 0, "1D": 86400, "1W": 604800, "2W": 1209600,
    "1M": 2592000, "6M": 15552000, "1Y": 31536000,
}


class PasteDebianNet(BasePastebin):
    name = "paste.debian.net"
    url = "https://paste.debian.net"
    supports_auth = True
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "Plain Text"
        expire = _EXPIRY_SECONDS.get(opts.expiry, 0)
        hidden = 1 if opts.private > 0 else 0
        try:
            proxy = xmlrpc.client.ServerProxy(_ENDPOINT)
            result = proxy.paste.addPaste(content, fmt, opts.title, expire, hidden)
        except Exception as e:
            raise BackendError(f"paste.debian.net error: {e}") from e
        if result.get("rc") != 0:
            raise BackendError(f"paste.debian.net returned error code {result.get('rc')}")
        return result.get("url", f"https://paste.debian.net/{result['id']}/")
