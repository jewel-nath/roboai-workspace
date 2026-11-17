#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Compare every source registry entry with its upstream today.

Asks the GitHub API about each GitHub source and reports what changed since the recorded
baseline: new commits or releases, archived or moved repos, licence changes, and repos with no
push for 180 days. It changes nothing unless asked:

  uv run tools/check_sources.py                  report in the terminal
  uv run tools/check_sources.py --report         also write sources/reports/<today>.md
  uv run tools/check_sources.py --record         also set last_checked to today in the registry
  uv run tools/check_sources.py --rebaseline ID  record today's upstream state as ID's baseline
  uv run tools/check_sources.py --only ID ...    check only these entries
  uv run tools/check_sources.py --json           print the results as JSON

Retired entries are skipped. Without GITHUB_TOKEN the API allows 60 requests an hour, about 15
sources; the token is read from the environment and never stored.
"""

from __future__ import annotations

import argparse
import datetime as dt
import http.client
import json
import os
import re
import sys
import urllib.error
import urllib.request

from common import ROOT, as_date, dig, load_yaml, read_text, utf8_output, write_text

API = "https://api.github.com"
REGISTRY = ROOT / "sources" / "registry.yaml"
GITHUB_REPO = re.compile(r"^https://github\.com/([^/\s]+)/([^/\s#?]+?)(?:\.git)?/?$")
STALE_PUSH_DAYS = 180
COUNT_WINDOW = 30  # newest commits searched for our reference commit
TODAY = dt.date.today()
NETWORK_ERRORS = (urllib.error.URLError, TimeoutError, http.client.HTTPException, json.JSONDecodeError)


class GitHub:
    def __init__(self, token: str | None) -> None:
        self.token = token
        self.remaining: str | None = None

    def get(self, path: str) -> tuple[int, object]:
        request = urllib.request.Request(
            API + path,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "roboai-workspace-source-check",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                self.remaining = response.headers.get("X-RateLimit-Remaining")
                return response.status, json.load(response)
        except urllib.error.HTTPError as exc:
            self.remaining = exc.headers.get("X-RateLimit-Remaining")
            if exc.code in (403, 429) and self.remaining == "0":
                raise SystemExit("GitHub API rate limit reached: set GITHUB_TOKEN or try again in an hour.")
            return exc.code, None


def plain_version(value) -> str:
    return str(value or "").strip().lstrip("vV")


def same_commit(a, b) -> bool:
    a, b = str(a or ""), str(b or "")
    return bool(a and b) and (a.startswith(b) or b.startswith(a))


def check(gh: GitHub, entry: dict) -> dict:
    result = {"id": entry.get("id"), "status": entry.get("status"), "flags": [], "now": {}, "ok": False}
    match = GITHUB_REPO.match(str(entry.get("url") or ""))
    if not match:
        result["flags"].append("not on GitHub: check by hand")
        return result
    full_name = f"{match.group(1)}/{match.group(2)}"

    code, meta = gh.get(f"/repos/{full_name}")
    if code == 404:
        result["flags"].append("repo not found: deleted or made private")
        return result
    if code != 200 or not isinstance(meta, dict):
        result["flags"].append(f"GitHub answered {code}")
        return result

    now = {
        "full_name": meta.get("full_name"),
        "stars": meta.get("stargazers_count"),
        "archived": bool(meta.get("archived")),
        "license": (meta.get("license") or {}).get("spdx_id"),
        "pushed": (meta.get("pushed_at") or "")[:10],
    }
    code, commits = gh.get(f"/repos/{now['full_name']}/commits?per_page=1")
    if code == 200 and isinstance(commits, list) and commits:
        now["head"] = commits[0]["sha"]
        now["commit"] = commits[0]["sha"][:7]
        now["commit_date"] = commits[0]["commit"]["committer"]["date"][:10]
    code, release = gh.get(f"/repos/{now['full_name']}/releases/latest")
    now["release"] = release.get("tag_name") if code == 200 and isinstance(release, dict) else None
    result["now"] = now
    result["ok"] = True

    flags = result["flags"]
    base = entry.get("baseline") or {}
    pinned = entry.get("pinned") or {}
    if str(now["full_name"]).lower() != full_name.lower():
        flags.append(f"moved to {now['full_name']}")
    if now["archived"] and not base.get("archived"):
        flags.append("archived")
    if base.get("archived") and not now["archived"]:
        flags.append("no longer archived")
    if now["license"] and now["license"] != "NOASSERTION" and entry.get("license") and now["license"] != entry["license"]:
        flags.append(f"licence is now {now['license']} (registry: {entry['license']})")

    reference = pinned.get("commit") or base.get("commit")
    label = "pin" if pinned.get("commit") else "baseline"
    if reference and now.get("head") and not same_commit(reference, now["head"]):
        # The commits list is far lighter than the compare endpoint, which returns whole diffs.
        code, recent = gh.get(f"/repos/{now['full_name']}/commits?sha={now['head']}&per_page={COUNT_WINDOW}")
        shas = [c.get("sha", "") for c in recent] if code == 200 and isinstance(recent, list) else []
        position = next((i for i, sha in enumerate(shas) if same_commit(reference, sha)), None)
        if position is not None:
            flags.append(f"{position} new commit(s) since {label}")
        elif len(shas) == COUNT_WINDOW:
            flags.append(f"more than {COUNT_WINDOW} new commits since {label}")
        else:
            flags.append(f"head moved since {label}; {label} commit not found upstream")

    latest = plain_version(now["release"])
    known = {plain_version(base.get("release")), plain_version(pinned.get("version"))} - {""}
    if latest and latest not in known:
        flags.append(f"new release {now['release']}")

    pushed = as_date(now["pushed"])
    if pushed and (TODAY - pushed).days > STALE_PUSH_DAYS:
        flags.append(f"no push since {pushed}")
    return result


def stars_text(entry: dict, now: dict) -> str:
    before, after = dig(entry, "baseline", "stars"), now.get("stars")
    if after is None:
        return "—"
    if isinstance(before, int):
        return f"{after} ({after - before:+d})"
    return str(after)


def report_markdown(results: list[dict], entries: dict[str, dict]) -> str:
    lines = [
        f"# Source check {TODAY}",
        "",
        f"Checked {len(results)} source(s) against the baselines in `sources/registry.yaml` with "
        "`tools/check_sources.py`. Flagged entries go to `/review-sources`.",
        "",
        "| Source | Status | Flags | Commit (baseline → now) | Latest release | Stars | Last push |",
        "|---|---|---|---|---|---|---|",
    ]
    for result in results:
        entry, now = entries[result["id"]], result["now"]
        commit = f"{dig(entry, 'baseline', 'commit') or '—'} → {now.get('commit') or '—'}"
        flags = "; ".join(result["flags"]) or "no change"
        lines.append(
            f"| {result['id']} | {result['status']} | {flags} | {commit} | {now.get('release') or '—'} | "
            f"{stars_text(entry, now)} | {now.get('pushed') or '—'} |"
        )
    return "\n".join(lines) + "\n"


def entry_span(lines: list[str], ident: str) -> tuple[int, int] | None:
    """The registry lines of one entry: from its '- id:' line to the next entry or comment."""
    start = next((i for i, line in enumerate(lines) if line.rstrip() == f"  - id: {ident}"), None)
    if start is None:
        return None
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("  - id: ") or lines[i].startswith("  #")),
        len(lines),
    )
    return start, end


def set_field(lines: list[str], span: tuple[int, int], key: str, value: str) -> bool:
    for i in range(*span):
        if lines[i].startswith(f"    {key}:"):
            lines[i] = f"    {key}: {value}"
            return True
    return False


def append_history(lines: list[str], span: tuple[int, int], event: str, note: str) -> None:
    last = max((i for i in range(*span) if lines[i].startswith("      - {date:")), default=None)
    if last is not None:
        lines.insert(last + 1, f"      - {{date: {TODAY}, event: {event}, note: {note}}}")


def flow(mapping: dict) -> str:
    """A one-line YAML mapping in the registry's style, with commits quoted."""
    parts = []
    for key, value in mapping.items():
        if value is None or value == "":
            parts.append(f"{key}: ")
        elif isinstance(value, bool):
            parts.append(f"{key}: {'true' if value else 'false'}")
        elif key == "commit":
            parts.append(f'{key}: "{value}"')
        else:
            parts.append(f"{key}: {value}")
    return "{" + ", ".join(parts) + "}"


def update_registry(results: list[dict], record: bool, rebaseline: set[str]) -> list[str]:
    lines = read_text(REGISTRY).split("\n")
    changed = []
    for result in results:
        if not result["ok"]:
            continue
        span = entry_span(lines, result["id"])
        if span is None:
            continue
        if record and set_field(lines, span, "last_checked", str(TODAY)):
            changed.append(f"{result['id']}: last_checked")
        if result["id"] in rebaseline:
            now = result["now"]
            baseline = {
                "as_of": TODAY,
                "commit": now.get("commit"),
                "commit_date": now.get("commit_date"),
                "release": now.get("release"),
                "stars": now.get("stars"),
                "archived": now.get("archived"),
            }
            if set_field(lines, span, "baseline", flow(baseline)):
                span = entry_span(lines, result["id"])
                append_history(lines, span, "rebaselined", "upstream state recorded as the new baseline")
                changed.append(f"{result['id']}: baseline")
    write_text(REGISTRY, "\n".join(lines))
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", nargs="+", metavar="ID", help="check only these registry ids")
    parser.add_argument("--report", action="store_true", help="write sources/reports/<today>.md")
    parser.add_argument("--record", action="store_true", help="set last_checked to today for checked entries")
    parser.add_argument("--rebaseline", nargs="+", metavar="ID", default=[], help="record today's state as the baseline")
    parser.add_argument("--json", action="store_true", help="print the results as JSON")
    args = parser.parse_args()
    utf8_output()

    registry = load_yaml(REGISTRY) or {}
    entries = {e["id"]: e for e in registry.get("sources") or [] if isinstance(e, dict) and e.get("id")}
    wanted = set(args.only or []) | set(args.rebaseline)
    unknown = wanted - set(entries)
    if unknown:
        print(f"not in the registry: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2
    ids = [i for i in entries if (i in wanted if wanted else entries[i].get("status") != "retired")]

    gh = GitHub(os.environ.get("GITHUB_TOKEN"))
    results = []
    for ident in ids:
        try:
            results.append(check(gh, entries[ident]))
        except NETWORK_ERRORS as exc:
            results.append({"id": ident, "status": entries[ident].get("status"), "flags": [f"network error: {exc}"], "now": {}, "ok": False})

    if args.json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print(report_markdown(results, entries))
    if args.report:
        path = ROOT / "sources" / "reports" / f"{TODAY}.md"
        write_text(path, report_markdown(results, entries))
        print(f"wrote {path.relative_to(ROOT).as_posix()}", file=sys.stderr)
    if args.record or args.rebaseline:
        for change in update_registry(results, args.record, set(args.rebaseline)):
            print(f"registry: {change}", file=sys.stderr)
    if gh.remaining is not None:
        print(f"GitHub API requests left this hour: {gh.remaining}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
