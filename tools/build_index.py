#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Write the workspace's generated sections.

Generated: the index table in each wiki section's README, the summary in sources/README.md, and
NOTICE (from the registry's distilled and copied entries). The text between the index markers and
the whole of NOTICE are overwritten, so edit the pages and the registry, never the output.

  uv run tools/build_index.py           write whatever changed
  uv run tools/build_index.py --check   report only; exit 1 when anything is out of date
"""

from __future__ import annotations

import argparse
import os
import sys
import textwrap
from pathlib import Path
from typing import Callable

from common import (
    ROOT,
    dig,
    load_frontmatter,
    load_yaml,
    read_text,
    rel,
    replace_index,
    utf8_output,
    wiki_pages,
    write_text,
)

STATUS_TITLES = {
    "in-use": "In use",
    "trial": "Trial",
    "planned": "Planned",
    "watching": "Watching",
    "rejected": "Rejected",
    "retired": "Retired",
}


def cell(value) -> str:
    """One table cell: lists joined, pipes escaped, empty shown as a dash."""
    if value is None or value == "" or value == [] or value == {}:
        return "—"
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def table(headers: list[str], rows: list[list[str]], empty: str = "_No pages yet._") -> str:
    if not rows:
        return empty
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines)


def href(target: Path, base: Path) -> str:
    return os.path.relpath(target, base).replace(os.sep, "/")


def pages(section: str) -> list[tuple[Path, dict]]:
    """Pages whose frontmatter reads; the lint reports the others."""
    found = []
    for path in wiki_pages(section):
        data, _ = load_frontmatter(path)
        if data:
            found.append((path, data))
    return found


def by(*keys: str) -> Callable:
    return lambda item: tuple(str(item[1].get(key) or "").lower() for key in keys)


def name_link(path: Path, data: dict, base: Path) -> str:
    return f"[{cell(data.get('name') or path.stem)}]({href(path, base)})"


def cost_text(cost) -> str:
    if not isinstance(cost, dict) or cost.get("usd") in (None, ""):
        return "—"
    parts = [str(cost["usd"])]
    if cost.get("type"):
        parts.append(str(cost["type"]))
    if cost.get("as_of"):
        parts.append(f"({cost['as_of']})")
    return cell(" ".join(parts))


def strings_in(value) -> set[str]:
    """Every string anywhere inside a nested value, such as a robot's stack."""
    if isinstance(value, dict):
        value = list(value.values())
    if isinstance(value, list):
        return set().union(*(strings_in(item) for item in value))
    return {value.strip()} if isinstance(value, str) else set()


def robots_index() -> str:
    base = ROOT / "wiki" / "robots"
    rows = [
        [
            name_link(path, d, base),
            cell(d.get("category")),
            cell(d.get("tier")),
            cell(d.get("openness")),
            cell(dig(d, "specs", "dof")),
            cell(dig(d, "specs", "payload_kg")),
            cost_text(d.get("cost")),
            cell(d.get("evidence")),
            cell(d.get("last_verified")),
        ]
        for path, d in sorted(pages("robots"), key=by("category", "name"))
    ]
    headers = ["Robot", "Category", "Tier", "Openness", "DOF", "Payload (kg)", "Cost (USD)", "Evidence", "Verified"]
    return table(headers, rows)


def parts_index() -> str:
    base = ROOT / "wiki" / "parts"
    users: dict[str, list[tuple[str, Path]]] = {}
    for path, d in pages("robots"):
        for slug in strings_in(d.get("stack")):
            users.setdefault(slug, []).append((str(d.get("name") or path.stem), path))
    rows = []
    for path, d in sorted(pages("parts"), key=by("category", "name")):
        used = ", ".join(f"[{cell(name)}]({href(robot, base)})" for name, robot in sorted(users.get(path.stem, [])))
        rows.append(
            [
                name_link(path, d, base),
                cell(d.get("category")),
                cell(d.get("subcategory")),
                cell(d.get("interfaces")),
                cost_text(d.get("cost")),
                used or "—",
                cell(d.get("last_verified")),
            ]
        )
    return table(["Part", "Category", "Subcategory", "Interfaces", "Cost (USD)", "Used in", "Verified"], rows)


def tools_index(section: str) -> Callable[[], str]:
    def build() -> str:
        base = ROOT / "wiki" / section
        rows = [
            [
                name_link(path, d, base),
                cell(d.get("kind")),
                cell(d.get("area")),
                cell(d.get("support")),
                cell(d.get("license")),
                cell(dig(d, "version", "tested")),
                cell(d.get("agent_access")),
                cell(d.get("last_verified")),
            ]
            for path, d in sorted(pages(section), key=by("area", "name"))
        ]
        return table(["Name", "Kind", "Area", "Support", "Licence", "Tested", "Agent access", "Verified"], rows)

    return build


def concepts_index() -> str:
    base = ROOT / "wiki" / "concepts"
    rows = [
        [name_link(path, d, base), cell(d.get("area")), cell(d.get("summary"))]
        for path, d in sorted(pages("concepts"), key=by("area", "name"))
    ]
    return table(["Concept", "Area", "Summary"], rows)


def guides_index() -> str:
    base = ROOT / "wiki" / "guides"
    rows = [
        [name_link(path, d, base), cell(d.get("question")), cell(d.get("recommendation"))]
        for path, d in sorted(pages("guides"), key=by("name"))
    ]
    return table(["Guide", "Question", "Recommendation"], rows)


def registry() -> dict:
    return load_yaml(ROOT / "sources" / "registry.yaml") or {}


def first_sentence(text, limit: int = 140) -> str:
    text = " ".join(str(text or "").split())
    end = text.find(". ")
    if end >= 0:
        text = text[: end + 1]
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def sources_summary() -> str:
    entries = registry().get("sources") or []
    blocks = []
    for status, title in STATUS_TITLES.items():
        group = sorted(
            (e for e in entries if e.get("status") == status),
            key=lambda e: (str(e.get("area")), str(e.get("id"))),
        )
        if not group:
            continue
        rows = [
            [
                f"[{cell(e.get('id'))}]({e.get('url')})",
                cell(e.get("kind")),
                cell(e.get("area")),
                cell(e.get("relation")),
                cell(e.get("license")),
                cell(dig(e, "pinned", "version") or dig(e, "pinned", "commit")),
                cell(e.get("last_checked")),
                cell(first_sentence(e.get("notes"))),
            ]
            for e in group
        ]
        headers = ["Source", "Kind", "Area", "Relation", "Licence", "Pinned", "Checked", "Notes"]
        blocks.append(f"### {title} ({len(group)})\n\n" + table(headers, rows))

    notes = []
    for path in sorted((ROOT / "sources").glob("*.md")):
        if path.name == "README.md":
            continue
        data, _ = load_frontmatter(path)
        if data and data.get("type") == "source":
            notes.append(
                [
                    f"[{cell(data.get('name') or path.stem)}]({path.name})",
                    cell(data.get("read_on")),
                    cell(dig(data, "counts", "entries")),
                    cell(dig(data, "counts", "pages")),
                    cell(dig(data, "counts", "waiting")),
                    cell(dig(data, "counts", "index_only")),
                    cell(dig(data, "counts", "deferred")),
                    cell(dig(data, "counts", "rejected")),
                ]
            )
    headers = ["Source", "Read on", "Entries", "Pages", "Waiting", "Index only", "Deferred", "Rejected"]
    blocks.append("### Triage notes\n\n" + table(headers, notes, empty="_None yet._"))
    return "\n\n".join(blocks)


def wrap(text: str, first: str, rest: str) -> list[str]:
    return textwrap.wrap(
        " ".join(text.split()),
        76,
        initial_indent=first,
        subsequent_indent=rest,
        break_long_words=False,
        break_on_hyphens=False,
    )


def notice() -> str:
    reg = registry()
    lines = [str(reg.get("notice_header") or "").strip(), ""]
    adapted = [
        e
        for e in reg.get("sources") or []
        if e.get("relation") in ("distilled", "copied")
        and e.get("status") not in ("rejected", "retired")
        and e.get("notice")
    ]
    if adapted:
        lines += ["This product includes material adapted from the projects below.", ""]
        for e in adapted:
            lines += wrap(f"{e['id']} ({e.get('url')}), {e.get('license')}.", "- ", "  ")
            lines += wrap(str(e["notice"]), "  ", "  ")
            lines.append("")
    footer = (
        "Every outside source is recorded in sources/registry.yaml. This file is generated "
        "from it by tools/build_index.py: edit the registry, not this file."
    )
    lines += wrap(footer, "", "")
    return "\n".join(lines) + "\n"


SECTIONS: dict[str, Callable[[], str]] = {
    "wiki/robots/README.md": robots_index,
    "wiki/parts/README.md": parts_index,
    "wiki/tools/README.md": tools_index("tools"),
    "wiki/software/README.md": tools_index("software"),
    "wiki/learning/README.md": tools_index("learning"),
    "wiki/concepts/README.md": concepts_index,
    "wiki/guides/README.md": guides_index,
    "sources/README.md": sources_summary,
}


def render_all() -> dict[Path, str]:
    """The full new text of every file with a generated part."""
    rendered = {}
    for relpath, build in SECTIONS.items():
        path = ROOT / relpath
        text = replace_index(read_text(path), build())
        if text is None:
            raise SystemExit(f"{relpath}: the index markers are missing")
        rendered[path] = text
    rendered[ROOT / "NOTICE"] = notice()
    return rendered


def out_of_date(rendered: dict[Path, str] | None = None) -> list[Path]:
    rendered = rendered if rendered is not None else render_all()
    return [path for path, text in rendered.items() if not path.exists() or read_text(path) != text]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="report only; exit 1 when anything is out of date")
    args = parser.parse_args()
    utf8_output()

    rendered = render_all()
    stale = out_of_date(rendered)
    if args.check:
        for path in stale:
            print(f"out of date: {rel(path)}")
        return 1 if stale else 0
    for path in stale:
        write_text(path, rendered[path])
        print(f"updated: {rel(path)}")
    if not stale:
        print("all generated sections are up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
