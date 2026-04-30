from pastebinit.syntax import detect


def test_detect_by_extension_python():
    assert detect("print('hi')", filename="script.py") == "python"


def test_detect_by_extension_rust():
    assert detect("fn main() {}", filename="main.rs") == "rust"


def test_detect_by_extension_typescript():
    assert detect("const x: number = 1", filename="app.ts") == "typescript"


def test_detect_dockerfile():
    assert detect("FROM ubuntu", filename="Dockerfile") == "bash"


def test_detect_makefile():
    assert detect("all:", filename="Makefile") == "make"


def test_detect_shebang_python():
    assert detect("#!/usr/bin/env python3\nprint('hi')") == "python"


def test_detect_shebang_bash():
    assert detect("#!/bin/bash\necho hi") == "bash"


def test_detect_shebang_node():
    assert detect("#!/usr/bin/env node\nconsole.log('hi')") == "javascript"


def test_detect_unknown_falls_back_to_text():
    assert detect("hello world") == "text"


def test_detect_explicit_format_overrides():
    assert detect("", filename="file.py") == "python"
