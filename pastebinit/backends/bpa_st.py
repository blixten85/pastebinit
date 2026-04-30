import urllib.parse
import urllib.request
from .base import BasePastebin, PasteOptions, BackendError

_EXPIRY = {"N": "never", "1H": "1hour", "1D": "1day", "1W": "1week", "1M": "1month"}


class BpaSt(BasePastebin):
    name = "bpa.st"
    url = "https://bpa.st"
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "text"
        params = {
            "content": content,
            "syntax": fmt,
            "title": opts.title,
            "expiry": _EXPIRY.get(opts.expiry, "never"),
        }
        if opts.private > 0:
            params["private"] = "1"
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request("https://bpa.st/", data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.url
        except OSError as e:
            raise BackendError(f"bpa.st error: {e}") from e
