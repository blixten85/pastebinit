import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Optional

from .base import BasePastebin, PasteOptions, AuthError, BackendError, NotSupportedError

_API = "https://pastebin.com/api/api_post.php"
_LOGIN = "https://pastebin.com/api/api_login.php"
_USER_AGENT = "pastebinit/2.0.0"

_EXPIRY = {"N", "10M", "1H", "1D", "1W", "2W", "1M", "6M", "1Y"}


class PastebinCom(BasePastebin):
    name = "pastebin.com"
    url = "https://pastebin.com"
    supports_auth = True
    supports_folders = True
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def __init__(self, api_dev_key: Optional[str] = None):
        self._api_dev_key = api_dev_key

    def _key(self) -> str:
        if self._api_dev_key:
            return self._api_dev_key
        from ..credentials import get
        key = get("pastebin.com", "api_dev_key")
        if not key:
            raise AuthError(
                "No API dev key. Set PASTEBIN_API_KEY or run: pastebinit --login"
            )
        return key

    def _post(self, url: str, params: dict) -> str:
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(url, data=data)
        req.add_header("User-Agent", _USER_AGENT)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = resp.read().decode()
        except OSError as e:
            raise BackendError(f"Network error: {e}") from e
        if result.startswith("Bad API request"):
            raise BackendError(result)
        return result

    def login(self, username: str, password: str) -> str:
        try:
            result = self._post(_LOGIN, {
                "api_dev_key": self._key(),
                "api_user_name": username,
                "api_user_password": password,
            })
        except BackendError as e:
            raise AuthError(f"Login failed: {e}") from e
        if not result:
            raise AuthError("Login returned empty response")
        return result

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "text"
        expiry = opts.expiry if opts.expiry in _EXPIRY else "N"
        params: dict = {
            "api_option": "paste",
            "api_dev_key": self._key(),
            "api_paste_code": content,
            "api_paste_name": opts.title,
            "api_paste_format": fmt,
            "api_paste_private": opts.private,
            "api_paste_expire_date": expiry,
        }
        if opts.user_key:
            params["api_user_key"] = opts.user_key
        if opts.folder and opts.user_key:
            params["api_folder_key"] = self._resolve_folder(
                opts.folder, opts.user_key, create=opts.create_folder
            )
        return self._post(_API, params)

    def list_pastes(self, user_key: str, limit: int = 50) -> list[dict]:
        result = self._post(_API, {
            "api_option": "list",
            "api_dev_key": self._key(),
            "api_user_key": user_key,
            "api_results_limit": limit,
        })
        root = ET.fromstring(f"<root>{result}</root>")
        return [
            {
                "key": p.findtext("paste_key", ""),
                "title": p.findtext("paste_title", ""),
                "date": p.findtext("paste_date", ""),
                "size": p.findtext("paste_size", ""),
                "expire_date": p.findtext("paste_expire_date", ""),
                "private": p.findtext("paste_private", ""),
                "format": p.findtext("paste_format_short", ""),
                "url": p.findtext("paste_url", ""),
                "hits": p.findtext("paste_hits", ""),
            }
            for p in root.findall("paste")
        ]

    def delete_paste(self, paste_key: str, user_key: str) -> bool:
        result = self._post(_API, {
            "api_option": "delete",
            "api_dev_key": self._key(),
            "api_user_key": user_key,
            "api_paste_key": paste_key,
        })
        return result == "Paste Removed"

    def list_folders(self, user_key: str) -> list[dict]:
        result = self._post(_API, {
            "api_option": "list_folders",
            "api_dev_key": self._key(),
            "api_user_key": user_key,
        })
        root = ET.fromstring(f"<root>{result}</root>")
        return [
            {
                "key": f.findtext("folder_key", ""),
                "name": f.findtext("folder_name", ""),
            }
            for f in root.findall("folder")
        ]

    def create_folder(self, name: str, user_key: str) -> str:
        return self._post(_API, {
            "api_option": "create_folder",
            "api_dev_key": self._key(),
            "api_user_key": user_key,
            "api_folder_name": name,
        })

    def get_user_info(self, user_key: str) -> dict:
        result = self._post(_API, {
            "api_option": "userdetails",
            "api_dev_key": self._key(),
            "api_user_key": user_key,
        })
        root = ET.fromstring(result)
        return {
            "username": root.findtext("user_name", ""),
            "email": root.findtext("user_email", ""),
            "avatar_url": root.findtext("user_avatar_url", ""),
            "private": root.findtext("user_private", ""),
            "website": root.findtext("user_website", ""),
            "api_tier": root.findtext("user_api_tier", ""),
        }

    def _resolve_folder(self, name: str, user_key: str, create: bool = False) -> str:
        for f in self.list_folders(user_key):
            if f["name"] == name:
                return f["key"]
        if create:
            return self.create_folder(name, user_key)
        raise BackendError(
            f"Folder '{name}' not found on pastebin.com. Use --create-folder to create it."
        )
