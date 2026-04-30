from .pastebin_com import PastebinCom
from .dpaste import DPaste
from .paste_debian_net import PasteDebianNet
from .paste_ubuntu_com import PasteUbuntuCom
from .sprunge import Sprunge
from .paste_opendev import PasteOpenDev
from .bpa_st import BpaSt
from .paste_opensuse import PasteOpenSUSE

BACKENDS: dict[str, type] = {
    "pastebin.com": PastebinCom,
    "dpaste.com": DPaste,
    "paste.debian.net": PasteDebianNet,
    "paste.ubuntu.com": PasteUbuntuCom,
    "sprunge.us": Sprunge,
    "paste.opendev.org": PasteOpenDev,
    "bpa.st": BpaSt,
    "paste.opensuse.org": PasteOpenSUSE,
}

DEFAULT_BACKEND = "bpa.st"


def get_backend(name: str):
    """Return instantiated backend by name, raise ValueError if unknown."""
    cls = BACKENDS.get(name)
    if cls is None:
        known = ", ".join(sorted(BACKENDS))
        raise ValueError(f"Unknown backend '{name}'. Known backends: {known}")
    return cls()
