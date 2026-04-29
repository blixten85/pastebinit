from pathlib import Path
from typing import Optional

EXTENSION_MAP: dict[str, str] = {
    ".py": "python", ".pyw": "python",
    ".js": "javascript", ".mjs": "javascript", ".cjs": "javascript",
    ".ts": "typescript", ".tsx": "typescript",
    ".jsx": "javascript",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".c": "c", ".h": "c",
    ".cpp": "cpp", ".cxx": "cpp", ".cc": "cpp", ".hpp": "cpp",
    ".cs": "csharp",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin", ".kts": "kotlin",
    ".scala": "scala",
    ".sh": "bash", ".bash": "bash", ".zsh": "bash", ".fish": "bash",
    ".ps1": "powershell",
    ".html": "html5", ".htm": "html5",
    ".css": "css", ".scss": "css", ".sass": "css",
    ".json": "json",
    ".yaml": "yaml", ".yml": "yaml",
    ".toml": "ini", ".ini": "ini", ".cfg": "ini", ".conf": "ini",
    ".xml": "xml",
    ".sql": "sql",
    ".md": "markdown", ".markdown": "markdown",
    ".lua": "lua",
    ".r": "rsplus", ".R": "rsplus",
    ".dart": "dart",
    ".ex": "erlang", ".exs": "erlang", ".erl": "erlang",
    ".hs": "haskell",
    ".ml": "ocaml", ".mli": "ocaml",
    ".vim": "vim",
    ".pl": "perl", ".pm": "perl",
    ".tf": "ini",
    ".env": "ini",
    ".mk": "make",
    ".groovy": "groovy",
    ".gradle": "groovy",
    ".clj": "clojure",
    ".nim": "nim",
    ".zig": "text",
}

SHEBANG_MAP: dict[str, str] = {
    "python": "python", "python3": "python", "python2": "python",
    "node": "javascript", "nodejs": "javascript",
    "bash": "bash", "sh": "bash", "zsh": "bash", "dash": "bash",
    "ruby": "ruby",
    "perl": "perl",
    "php": "php",
    "lua": "lua",
    "rscript": "rsplus",
}

_SPECIAL_NAMES: dict[str, str] = {
    "dockerfile": "bash",
    "makefile": "make",
    "gnumakefile": "make",
    "gemfile": "ruby",
    "rakefile": "ruby",
    "vagrantfile": "ruby",
    "cmakelists.txt": "cmake",
}


def detect(content: str, filename: Optional[str] = None) -> str:
    """Return pastebin syntax format for content, using filename hint if given."""
    if filename:
        p = Path(filename)
        name_lower = p.name.lower()
        if name_lower in _SPECIAL_NAMES:
            return _SPECIAL_NAMES[name_lower]
        ext = p.suffix.lower()
        if ext in EXTENSION_MAP:
            return EXTENSION_MAP[ext]

    lines = content.splitlines()
    if lines and lines[0].startswith("#!"):
        parts = lines[0].lstrip("#!").strip().split()
        if parts:
            interpreter = Path(parts[-1]).name.lower()
            if interpreter in SHEBANG_MAP:
                return SHEBANG_MAP[interpreter]

    return "text"
