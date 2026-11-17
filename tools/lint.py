#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Check the workspace: page frontmatter, file names, links, the source registry, skills and
the generated sections. Errors exit 1; warnings, such as stale pages, do not.

  uv run tools/lint.py
  uv run tools/lint.py --warnings-as-errors

Allowed fields and values come from tools/schema.yaml.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import urllib.parse
from pathlib import Path

import yaml

import build_index
from common import (
    KEBAB,
    ROOT,
    WIKI_SECTIONS,
    as_date,
    dig,
    is_empty,
    iter_markdown,
    load_frontmatter,
    load_yaml,
    read_text,
    rel,
    utf8_output,
    wiki_pages,
)

TODAY = dt.date.today()
REGISTRY = "sources/registry.yaml"

LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
FENCED_CODE = re.compile(r"^(```|~~~)[^\n]*\n.*?^\1[^\n]*$", re.S | re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
HEADING = re.compile(r"^#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$", re.M)


class Report:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, str, str]] = []

    def error(self, where: str, code: str, message: str) -> None:
        self.items.append(("error", where, code, message))

    def warn(self, where: str, code: str, message: str) -> None:
        self.items.append(("warning", where, code, message))

    def count(self, level: str) -> int:
        return sum(1 for item in self.items if item[0] == level)


def check_enum(report: Report, where: str, field: str, value, allowed: list) -> None:
    if not is_empty(value) and value not in allowed:
        report.error(where, "E003", f"'{field}' is '{value}'; allowed: {', '.join(map(str, allowed))}")


def check_date(report: Report, where: str, field: str, value) -> dt.date | None:
    if is_empty(value):
        return None
    date = as_date(value)
    if date is None:
        report.error(where, "E004", f"'{field}' must be a YYYY-MM-DD date, not '{value}'")
    return date


def check_sources_field(report: Report, where: str, sources) -> None:
    if not isinstance(sources, list) or not sources:
        report.error(where, "E002", "'sources' needs at least one entry: {url, title, accessed}")
        return
    for item in sources:
        if not isinstance(item, dict) or is_empty(item.get("url")):
            report.error(where, "E002", "every entry in 'sources' needs a url")
        else:
            check_date(report, where, "sources.accessed", item.get("accessed"))


def check_pages(report: Report, schema: dict) -> None:
    stale_days = schema["stale_days"]
    part_folders = schema["part_folders"]
    for section in WIKI_SECTIONS:
        allowed_types = schema["sections"][section]
        for path in wiki_pages(section):
            where = rel(path)
            if not KEBAB.fullmatch(path.stem):
                report.error(where, "E006", "the file name must be the kebab-case slug")
            data, problem = load_frontmatter(path)
            if problem:
                report.error(where, "E001", problem)
                continue
            kind = data.get("type")
            if kind not in allowed_types:
                expected = ", ".join(allowed_types)
                report.error(where, "E005", f"type '{kind}' does not belong in wiki/{section}/ (expected: {expected})")
                continue

            rules = schema["types"][kind]
            for field in schema["common"]["required"] + rules.get("required", []):
                if is_empty(data.get(field)):
                    report.error(where, "E002", f"'{field}' is empty")
            check_enum(report, where, "evidence", data.get("evidence"), schema["common"]["evidence"])
            for field, allowed in (rules.get("enums") or {}).items():
                check_enum(report, where, field, data.get(field), allowed)
            check_sources_field(report, where, data.get("sources"))

            verified = check_date(report, where, "last_verified", data.get("last_verified"))
            limit = stale_days.get(section, stale_days["default"])
            if verified and (TODAY - verified).days > limit:
                report.warn(where, "W001", f"last verified {verified}, more than {limit} days ago")

            cost = data.get("cost")
            if isinstance(cost, dict) and not is_empty(cost.get("usd")):
                for field in ("as_of", "source"):
                    if is_empty(cost.get(field)):
                        report.error(where, "E013", f"a cost needs '{field}'")
                check_date(report, where, "cost.as_of", cost.get("as_of"))

            if kind == "part":
                folder = path.parent.name
                expected = part_folders.get(folder)
                if expected is None:
                    report.error(where, "E005", f"parts go in one of: {', '.join(part_folders)}")
                elif data.get("category") and data["category"] != expected:
                    report.error(where, "E005", f"category '{data['category']}' does not match folder '{folder}/'")


def check_registry(report: Report, schema: dict) -> dict[str, dict]:
    try:
        data = load_yaml(ROOT / REGISTRY) or {}
    except (yaml.YAMLError, ValueError) as exc:
        report.error(REGISTRY, "E009", "invalid YAML: " + str(exc).splitlines()[0])
        return {}
    entries = data.get("sources")
    if not isinstance(entries, list):
        report.error(REGISTRY, "E009", "'sources' must be a list")
        return {}

    rules = schema["registry"]
    found: dict[str, dict] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            report.error(REGISTRY, "E009", "every entry must be a mapping")
            continue
        ident = entry.get("id")
        where = f"{REGISTRY} [{ident or '?'}]"
        for field in rules["required"]:
            if is_empty(entry.get(field)):
                report.error(where, "E009", f"'{field}' is empty")
        if ident:
            if not KEBAB.fullmatch(str(ident)):
                report.error(where, "E009", "the id must be kebab-case")
            if ident in found:
                report.error(where, "E009", "duplicate id")
            found[ident] = entry
        for field, allowed in rules["enums"].items():
            check_enum(report, where, field, entry.get(field), allowed)

        for block in ("pinned", "baseline"):
            commit = dig(entry, block, "commit")
            if not is_empty(commit) and not isinstance(commit, str):
                report.error(where, "E009", f"{block}.commit must be quoted, or YAML reads it as a number")

        checked = check_date(report, where, "last_checked", entry.get("last_checked"))
        if checked and entry.get("status") in ("trial", "in-use"):
            limit = rules["stale_check_days"]
            if (TODAY - checked).days > limit:
                report.warn(where, "W002", f"last checked {checked}, more than {limit} days ago")

        for path in entry.get("used_in") or []:
            if not (ROOT / path).exists():
                report.error(where, "E010", f"used_in path '{path}' does not exist")
        bench = dig(entry, "benchmark", "path")
        if bench and not (ROOT / "sources" / bench).exists():
            report.error(where, "E010", f"benchmark path 'sources/{bench}' does not exist")

        history = entry.get("history")
        if isinstance(history, list):
            for item in history:
                if not isinstance(item, dict) or as_date(item.get("date")) is None or is_empty(item.get("event")):
                    report.error(where, "E009", "every history entry needs a date and an event")

        adapted = entry.get("relation") in ("distilled", "copied")
        if adapted and entry.get("status") not in ("rejected", "retired") and is_empty(entry.get("notice")):
            report.error(where, "E009", "distilled and copied sources need a 'notice' for NOTICE")
    return found


def check_source_notes(report: Report, schema: dict, registry: dict[str, dict]) -> None:
    for path in sorted((ROOT / "sources").glob("*.md")):
        if path.name == "README.md":
            continue
        where = rel(path)
        if not KEBAB.fullmatch(path.stem):
            report.error(where, "E006", "the file name must be the kebab-case slug")
        data, problem = load_frontmatter(path)
        if problem:
            report.error(where, "E001", problem)
            continue
        if data.get("type") != "source":
            report.error(where, "E005", "triage notes in sources/ need 'type: source'")
        for field in schema["source_note"]["required"]:
            if is_empty(data.get(field)):
                report.error(where, "E002", f"'{field}' is empty")
        if data.get("registry") and data["registry"] not in registry:
            report.error(where, "E011", f"registry id '{data['registry']}' is not in {REGISTRY}")
        check_date(report, where, "read_on", data.get("read_on"))


def check_skills(report: Report, schema: dict, registry: dict[str, dict]) -> None:
    rules = schema["skill"]
    prefixes = tuple(prefix + "-" for prefix in rules["prefixes"])
    declared: dict[str, set] = {}

    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        name = path.parent.name
        skill = f"skills/{name}"
        where = rel(path)
        data, problem = load_frontmatter(path)
        if problem:
            report.error(where, "E001", problem)
            continue
        if data.get("name") != name:
            report.error(where, "E014", "'name' must match the folder name")
        if not name.startswith(prefixes):
            report.warn(where, "W003", "the name has no known category prefix (see skills/README.md)")
        for field in rules["required"]:
            if is_empty(data.get(field)):
                report.error(where, "E002", f"'{field}' is empty")

        meta = data.get("metadata")
        if not isinstance(meta, dict):
            report.error(where, "E002", "'metadata' with sources, evidence and last_verified is missing")
            continue
        if not isinstance(meta.get("sources"), list):
            report.error(where, "E002", "'metadata.sources' must be a list ([] when written here)")
        for field in ("evidence", "last_verified"):
            if is_empty(meta.get(field)):
                report.error(where, "E002", f"'metadata.{field}' is empty")
        check_enum(report, where, "metadata.evidence", meta.get("evidence"), rules["evidence"])
        check_date(report, where, "metadata.last_verified", meta.get("last_verified"))

        ids = meta.get("sources") if isinstance(meta.get("sources"), list) else []
        declared[skill] = set(ids)
        for ident in ids:
            entry = registry.get(ident)
            if entry is None:
                report.error(where, "E011", f"source '{ident}' is not in {REGISTRY}")
            elif not any(p.rstrip("/") == skill or p.startswith(skill + "/") for p in entry.get("used_in") or []):
                report.error(where, "E012", f"registry entry '{ident}' does not list {skill} in used_in")

    for ident, entry in registry.items():
        for used in entry.get("used_in") or []:
            parts = used.strip("/").split("/")
            if len(parts) >= 2 and parts[0] == "skills":
                skill = f"skills/{parts[1]}"
                if skill in declared and ident not in declared[skill]:
                    report.error(
                        f"{REGISTRY} [{ident}]",
                        "E012",
                        f"lists {skill} in used_in, but that skill's metadata.sources does not name '{ident}'",
                    )


def strip_code(text: str) -> str:
    text = FENCED_CODE.sub("", text)
    text = HTML_COMMENT.sub("", text)
    return INLINE_CODE.sub("", text)


def heading_slug(heading: str) -> str:
    """The anchor GitHub gives a heading."""
    heading = re.sub(r"<[^>]+>", "", heading).strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading)
    return heading.replace(" ", "-")


def anchors(path: Path, cache: dict[Path, set]) -> set:
    if path not in cache:
        seen: dict[str, int] = {}
        found = set()
        for heading in HEADING.findall(strip_code(read_text(path))):
            slug = heading_slug(heading)
            count = seen.get(slug, 0)
            found.add(slug if count == 0 else f"{slug}-{count}")
            seen[slug] = count + 1
        cache[path] = found
    return cache[path]


def check_links(report: Report) -> None:
    cache: dict[Path, set] = {}
    for path in iter_markdown():
        where = rel(path)
        for match in LINK.finditer(strip_code(read_text(path))):
            target = match.group(1)
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            file_part, _, anchor = target.partition("#")
            dest = (path.parent / urllib.parse.unquote(file_part)).resolve() if file_part else path
            if not dest.exists():
                report.error(where, "E007", f"broken link: {target}")
            elif anchor and dest.is_file() and dest.suffix == ".md" and anchor.lower() not in anchors(dest, cache):
                report.error(where, "E007", f"no heading for '#{anchor}' in {file_part or path.name}")


def check_generated(report: Report) -> None:
    try:
        stale = build_index.out_of_date()
    except (Exception, SystemExit) as exc:  # a broken registry or page must not hide the other findings
        report.error("tools/build_index.py", "E008", f"could not build the generated sections: {exc}")
        return
    for path in stale:
        report.error(rel(path), "E008", "generated section is out of date: run uv run tools/build_index.py")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--warnings-as-errors", action="store_true", help="exit 1 on warnings too")
    args = parser.parse_args()
    utf8_output()

    schema = load_yaml(ROOT / "tools" / "schema.yaml")
    report = Report()
    registry = check_registry(report, schema)
    check_pages(report, schema)
    check_source_notes(report, schema, registry)
    check_skills(report, schema, registry)
    check_links(report)
    check_generated(report)

    for level, where, code, message in sorted(report.items, key=lambda item: (item[0] != "error", item[1], item[2])):
        print(f"{level.upper():7} {code} {where}: {message}")
    errors, warnings = report.count("error"), report.count("warning")
    print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.warnings_as_errors and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
