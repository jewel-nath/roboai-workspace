"""Shared helpers for the workspace scripts: paths, YAML, frontmatter and generated sections."""

from __future__ import annotations

import datetime as dt
import os
import re
import sys
from pathlib import Path
from typing import Iterator

import yaml

ROOT = Path(__file__).resolve().parent.parent
WIKI_SECTIONS = ("robots", "parts", "tools", "software", "learning", "concepts", "guides")
SKIP_DIRS = {".git", "vendor", "node_modules", ".venv", "__pycache__"}
KEBAB = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
INDEX_START = "<!-- index:start -->"
INDEX_END = "<!-- index:end -->"
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def utf8_output() -> None:
    """Print UTF-8 even when Windows pipes output through a legacy code page."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def read_text(path: Path) -> str:
    """Read a UTF-8 file with LF line endings, whatever the checkout uses."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_yaml(path: Path):
    return yaml.safe_load(read_text(path))


def load_frontmatter(path: Path) -> tuple[dict | None, str | None]:
    """Return (data, None), or (None, what is wrong)."""
    match = _FRONTMATTER.match(read_text(path))
    if not match:
        return None, "no frontmatter block at the top of the file"
    try:
        data = yaml.safe_load(match.group(1))
    except (yaml.YAMLError, ValueError) as exc:  # ValueError: an impossible date such as 2026-13-01
        return None, "invalid YAML in frontmatter: " + str(exc).splitlines()[0]
    if not isinstance(data, dict):
        return None, "frontmatter is not a mapping"
    return data, None


def iter_markdown() -> Iterator[Path]:
    """Every Markdown file of the workspace, skipping project repos and fetched code."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        here = Path(dirpath)
        inside_projects = here == ROOT / "projects"
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not inside_projects)
        for name in sorted(filenames):
            if name.endswith(".md"):
                yield here / name


def wiki_pages(section: str) -> Iterator[Path]:
    """The pages of one wiki section, without its README."""
    for path in sorted((ROOT / "wiki" / section).rglob("*.md")):
        if path.name != "README.md":
            yield path


def as_date(value) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value)
        except ValueError:
            return None
    return None


def is_empty(value) -> bool:
    return value is None or value == "" or value == [] or value == {}


def dig(data, *keys):
    """data[k1][k2]…, or None as soon as a level is missing."""
    for key in keys:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


def replace_index(text: str, body: str) -> str | None:
    """Put body between the index markers; None when the markers are missing."""
    start = text.find(INDEX_START)
    end = text.find(INDEX_END)
    if start < 0 or end < start:
        return None
    return f"{text[: start + len(INDEX_START)]}\n{body.strip()}\n{text[end:]}"
