import json
import urllib.parse
import urllib.request
from .base import BasePastebin, PasteOptions, BackendError

_API = "https://paste.opensuse.org/api/create"
_EXPIRY_SECONDS = {
    "N": 0, "1H": 3600, "1D": 86400, "1W": 604800, "1M": 2592000,
}


class PasteOpenSUSE(BasePastebin):
    name = "paste.opensuse.org"
    url = "https://paste.opensuse.org"
    supports_expiry = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "text"
        expire = _EXPIRY_SECONDS.get(opts.expiry, 0)
        params = {
            "text": content,
            "title": opts.title,
            "language": fmt,
            "expire": expire,
        }
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(_API, data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read())
            return result.get("url", "")
        except OSError as e:
            raise BackendError(f"paste.opensuse.org error: {e}") from e
