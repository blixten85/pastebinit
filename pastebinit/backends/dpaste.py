import urllib.parse
import urllib.request
from .base import BasePastebin, PasteOptions, BackendError

_API = "https://dpaste.com/api/v2/"
_EXPIRY_MAP = {"N": "365", "1D": "1", "1W": "7", "1M": "30", "1Y": "365"}


class DPaste(BasePastebin):
    name = "dpaste.com"
    url = "https://dpaste.com"
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "text", "") else "text"
        expiry = _EXPIRY_MAP.get(opts.expiry, "7")
        params = {
            "content": content,
            "syntax": fmt,
            "title": opts.title,
            "expiry_days": expiry,
        }
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(_API, data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode().strip()
        except OSError as e:
            raise BackendError(f"dpaste.com error: {e}") from e
