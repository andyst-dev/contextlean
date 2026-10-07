"""Shared offline evidence checks; dataset-specific expectations stay in tests."""

import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import sys
from unittest.mock import patch
import zipfile


def extract_archive(source, destination):
    """Validate all members before extracting published source or solutions."""
    with zipfile.ZipFile(source) as archive:
        for member in archive.infolist():
            path = Path(member.filename)
            if path.is_absolute() or ".." in path.parts:
                raise AssertionError("archive contains an unsafe path")
            if stat.S_ISLNK(member.external_attr >> 16):
                raise AssertionError("archive contains a symlink")
        archive.extractall(destination)


def load_frozen_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    with patch.object(sys, "dont_write_bytecode", True):
        spec.loader.exec_module(module)
    return module


def assert_checksums(test, ledger):
    checksums = json.loads(ledger.read_text())
    for name, expected in checksums.items():
        with test.subTest(ledger=str(ledger), artifact=name):
            path = Path(name)
            test.assertFalse(path.is_absolute())
            test.assertNotIn("..", path.parts)
            test.assertEqual(
                hashlib.sha256((ledger.parent / path).read_bytes()).hexdigest(), expected
            )
    return checksums


def assert_usage(test, run, parsed):
    for key, value in parsed["usage"].items():
        test.assertEqual(run["metrics"][key], value)
    test.assertEqual(run["metrics"]["command_calls"], parsed["commands"])
    test.assertEqual(
        run["metrics"]["total_tokens"],
        parsed["usage"]["input_tokens"] + parsed["usage"]["output_tokens"],
    )


def fingerprint(path):
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    digest = hashlib.sha256()
    for item in sorted(p for p in path.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
        digest.update(item.relative_to(path).as_posix().encode() + b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()
