from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


class BackendError(Exception):
    pass


class NotSupportedError(BackendError):
    pass


class AuthError(BackendError):
    pass


@dataclass
class PasteOptions:
    title: str = ""
    format: str = "text"
    private: int = 1
    expiry: str = "N"
    folder: Optional[str] = None
    create_folder: bool = False
    user_key: Optional[str] = None


class BasePastebin(ABC):
    name: str
    url: str
    supports_auth: bool = False
    supports_folders: bool = False
    supports_expiry: bool = False
    supports_privacy: bool = False
    supports_syntax: bool = False

    @abstractmethod
    def paste(self, content: str, opts: PasteOptions) -> str: ...

    def login(self, username: str, password: str) -> str:
        raise NotSupportedError(f"{self.name} does not support authentication")

    def list_pastes(self, user_key: str) -> list[dict]:
        raise NotSupportedError(f"{self.name} does not support listing pastes")

    def delete_paste(self, paste_key: str, user_key: str) -> bool:
        raise NotSupportedError(f"{self.name} does not support deleting pastes")

    def list_folders(self, user_key: str) -> list[dict]:
        raise NotSupportedError(f"{self.name} does not support folders")

    def create_folder(self, name: str, user_key: str) -> str:
        raise NotSupportedError(f"{self.name} does not support creating folders")

    def get_user_info(self, user_key: str) -> dict:
        raise NotSupportedError(f"{self.name} does not support user info")
