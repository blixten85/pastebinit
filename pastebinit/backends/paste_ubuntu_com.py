import urllib.parse
import urllib.request
from .base import BasePastebin, PasteOptions, BackendError

_EXPIRY = {"N": "year", "1D": "day", "1W": "week", "1M": "month", "1Y": "year"}
_SYNTAX_MAP = {
    "python": "python3", "bash": "bash", "text": "text",
    "javascript": "javascript", "css": "css", "html5": "html",
    "sql": "sql", "xml": "xml", "yaml": "yaml", "json": "json",
}


class PasteUbuntuCom(BasePastebin):
    name = "paste.ubuntu.com"
    url = "https://paste.ubuntu.com"
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "text"
        fmt = _SYNTAX_MAP.get(fmt, fmt)
        params = {
            "poster": opts.title or "pastebinit",
            "syntax": fmt,
            "expiration": _EXPIRY.get(opts.expiry, "year"),
            "content": content,
        }
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request("https://paste.ubuntu.com/", data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.url
        except OSError as e:
            raise BackendError(f"paste.ubuntu.com error: {e}") from e
