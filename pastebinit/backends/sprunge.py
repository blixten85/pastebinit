import urllib.parse
import urllib.request
from .base import BasePastebin, PasteOptions, BackendError


class Sprunge(BasePastebin):
    name = "sprunge.us"
    url = "http://sprunge.us"
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        data = urllib.parse.urlencode({"sprunge": content}).encode()
        req = urllib.request.Request("http://sprunge.us", data=data)
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                url = resp.read().decode().strip()
            if opts.format not in ("auto", "text", ""):
                url = f"{url}?{opts.format}"
            return url
        except OSError as e:
            raise BackendError(f"sprunge.us error: {e}") from e
