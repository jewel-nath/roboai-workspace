#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Compare every source registry entry, or every Robot Atlas page, with its upstream today.

Registry mode asks the GitHub API about each GitHub source and reports what changed since the
recorded baseline: new commits or releases, archived or moved repos, licence changes, and repos
with no push for 180 days. Page mode (--pages) checks each robot page in wiki/robots/ against its
`links.repo`: moved or deleted, archived, a licence on GitHub the page does not list, commits newer
than `maturity.last_commit`, and `maturity.active` against the last push. It changes nothing unless
asked:

  uv run tools/check_sources.py                  report in the terminal
  uv run tools/check_sources.py --report         also write sources/reports/<today>.md
  uv run tools/check_sources.py --record         also set last_checked to today in the registry
  uv run tools/check_sources.py --rebaseline ID  record today's upstream state as ID's baseline
  uv run tools/check_sources.py --only ID ...    check only these entries
  uv run tools/check_sources.py --json           print the results as JSON

  uv run tools/check_sources.py --pages                 check the robot pages instead
  uv run tools/check_sources.py --pages --only SLUG ... check only these pages
  uv run tools/check_sources.py --pages --report        add a pages section to today's report
  uv run tools/check_sources.py --pages --record-pages  set maturity.last_commit, stars and active

Retired entries are skipped. Without GITHUB_TOKEN the API allows 60 requests an hour: about 15
sources or 30 pages. Page mode skips the pages it has no requests left for and says which. The
token is read from the environment and never stored.
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
from pathlib import Path

import yaml

from common import ROOT, as_date, dig, load_frontmatter, load_yaml, read_text, utf8_output, wiki_pages, write_text

API = "https://api.github.com"
REGISTRY = ROOT / "sources" / "registry.yaml"
REPORTS = ROOT / "sources" / "reports"
GITHUB_REPO = re.compile(r"^https://github\.com/([^/\s]+)/([^/\s#?]+?)(?:\.git)?/?$")
# Page links may point into a repo (…/tree/main/hardware); the repo is what gets checked.
GITHUB_LINK = re.compile(r"^https?://(?:www\.)?github\.com/([^/\s]+)/([^/\s#?]+?)(?:\.git)?(?:[/#?].*)?$")
STALE_PUSH_DAYS = 180
COUNT_WINDOW = 30  # newest commits searched for our reference commit
REQUESTS_PER_PAGE = 2  # the repo, and its newest commit
REPORT_SECTIONS = {"registry": "## Registry sources", "pages": "## Robot Atlas pages"}
MATURITY_LINE = re.compile(r"^maturity:\s*\{(?P<body>.*)\}\s*(?P<comment>#.*)?$")
SPDX_WORD = re.compile(r"[A-Za-z0-9.+-]+")
TODAY = dt.date.today()
NETWORK_ERRORS = (urllib.error.URLError, TimeoutError, http.client.HTTPException, json.JSONDecodeError)


class RateLimited(Exception):
    """The GitHub API has no requests left this hour."""


class GitHub:
    def __init__(self, token: str | None) -> None:
        self.token = token
        self.remaining: str | None = None
        self.reset: str | None = None

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
                self._note_limit(response.headers)
                return response.status, json.load(response)
        except urllib.error.HTTPError as exc:
            self._note_limit(exc.headers)
            if exc.code in (403, 429) and self.remaining == "0":
                raise RateLimited("GitHub API rate limit reached: set GITHUB_TOKEN or try again in an hour.")
            return exc.code, None

    def _note_limit(self, headers) -> None:
        self.remaining = headers.get("X-RateLimit-Remaining")
        self.reset = headers.get("X-RateLimit-Reset")

    def check_limit(self) -> None:
        """Ask how many requests are left; this call does not count against the limit."""
        code, body = self.get("/rate_limit")
        core = dig(body, "resources", "core")
        if code == 200 and isinstance(core, dict):
            self.remaining, self.reset = str(core.get("remaining")), str(core.get("reset"))

    def requests_left(self) -> int | None:
        return int(self.remaining) if self.remaining and self.remaining.isdigit() else None

    def reset_time(self) -> str:
        """When the hourly limit resets, as local time."""
        if not (self.reset and self.reset.isdigit()):
            return "within the hour"
        return "at " + dt.datetime.fromtimestamp(int(self.reset)).strftime("%H:%M")


def plain_version(value) -> str:
    return str(value or "").strip().lstrip("vV")


def same_commit(a, b) -> bool:
    a, b = str(a or ""), str(b or "")
    return bool(a and b) and (a.startswith(b) or b.startswith(a))


def read_upstream(gh: GitHub, full_name: str) -> tuple[dict | None, str | None]:
    """A GitHub repo's state today with its newest commit, or (None, why it could not be read)."""
    code, meta = gh.get(f"/repos/{full_name}")
    if code == 404:
        return None, "repo not found: deleted or made private"
    if code != 200 or not isinstance(meta, dict):
        return None, f"GitHub answered {code}"
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
    return now, None


# --- Registry entries ------------------------------------------------------------------------


def check(gh: GitHub, entry: dict) -> dict:
    result = {"id": entry.get("id"), "status": entry.get("status"), "flags": [], "now": {}, "ok": False}
    match = GITHUB_REPO.match(str(entry.get("url") or ""))
    if not match:
        result["flags"].append("not on GitHub: check by hand")
        return result
    full_name = f"{match.group(1)}/{match.group(2)}"

    now, problem = read_upstream(gh, full_name)
    if problem:
        result["flags"].append(problem)
        return result
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


def registry_section(results: list[dict], entries: dict[str, dict]) -> str:
    lines = [
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
    return "\n".join(lines)


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


# --- Robot Atlas pages -----------------------------------------------------------------------


def robot_pages() -> dict[str, tuple[Path, dict]]:
    """Every robot page by slug; pages whose frontmatter cannot be read are left to the lint."""
    pages = {}
    for path in wiki_pages("robots"):
        data, _ = load_frontmatter(path)
        if data and data.get("type") == "robot":
            pages[path.stem] = (path, data)
    return pages


def normal_licence(spdx: str) -> str:
    # GitHub reports GPL-3.0 for both GPL-3.0-only and GPL-3.0-or-later.
    return re.sub(r"(-ONLY|-OR-LATER|\+)$", "", spdx.upper())


def licence_ids(expression) -> set[str]:
    """The licence ids in an SPDX expression such as 'CC-BY-NC-4.0 AND MIT'."""
    words = SPDX_WORD.findall(str(expression or ""))
    return {normal_licence(w) for w in words if w.upper() not in ("AND", "OR", "WITH")}


def licence_flag(page: dict, detected: str | None) -> str | None:
    """A flag when GitHub's licence is neither the page's software nor its hardware licence."""
    if not detected or detected == "NOASSERTION":
        return None
    listed = {kind: dig(page, "license", kind) for kind in ("software", "hardware")}
    listed = {kind: value for kind, value in listed.items() if value}
    if any(normal_licence(detected) in licence_ids(value) for value in listed.values()):
        return None
    if not listed:
        return f"GitHub licence is {detected}; the page lists no software or hardware licence"
    return f"GitHub licence is {detected} (page: {', '.join(f'{k} {v}' for k, v in listed.items())})"


def check_page(gh: GitHub, slug: str, page: dict) -> dict:
    url = str(dig(page, "links", "repo") or "")
    result = {"page": slug, "repo": url, "flags": [], "now": {}, "ok": False}
    match = GITHUB_LINK.match(url)
    if not match:
        result["flags"].append("repo not on GitHub: check by hand")
        return result
    full_name = f"{match.group(1)}/{match.group(2)}"

    now, problem = read_upstream(gh, full_name)
    if problem:
        result["flags"].append(problem)
        return result
    pushed = as_date(now["pushed"])
    now["active"] = not now["archived"] and pushed is not None and (TODAY - pushed).days <= STALE_PUSH_DAYS
    result["now"] = now
    result["ok"] = True

    flags = result["flags"]
    active = dig(page, "maturity", "active")
    if str(now["full_name"]).lower() != full_name.lower():
        flags.append(f"moved to {now['full_name']}")
    if now["archived"] and active is not False:
        flags.append("archived")
    licence = licence_flag(page, now["license"])
    if licence:
        flags.append(licence)

    recorded, newest = as_date(dig(page, "maturity", "last_commit")), as_date(now.get("commit_date"))
    if newest and not recorded:
        flags.append("no maturity.last_commit on the page")
    elif newest and newest > recorded:
        flags.append(f"new commits since {recorded}")

    if active is True and pushed and (TODAY - pushed).days > STALE_PUSH_DAYS:
        flags.append(f"no push since {pushed}, but the page says active")
    if active is False and now["active"]:
        flags.append(f"pushed on {pushed}, but the page says inactive")
    return result


def check_pages(gh: GitHub, slugs: list[str], pages: dict) -> tuple[list[dict], list[str]]:
    """Check pages while the API has requests left; return the results and the skipped slugs."""
    try:
        gh.check_limit()
    except (RateLimited, *NETWORK_ERRORS):
        pass  # the loop below stops at the limit either way
    results = []
    for index, slug in enumerate(slugs):
        left = gh.requests_left()
        if left is not None and left < REQUESTS_PER_PAGE:
            return results, slugs[index:]
        try:
            results.append(check_page(gh, slug, pages[slug][1]))
        except RateLimited:
            return results, slugs[index:]
        except NETWORK_ERRORS as exc:
            repo = dig(pages[slug][1], "links", "repo")
            results.append({"page": slug, "repo": repo, "flags": [f"network error: {exc}"], "now": {}, "ok": False})
    return results, []


def bool_text(value) -> str:
    return "true" if value is True else "false" if value is False else "—"


def change_text(before, after) -> str:
    """'before → after', with the difference when both are counts."""
    if isinstance(before, int) and not isinstance(before, bool) and isinstance(after, int):
        return f"{before} → {after} ({after - before:+d})"
    return f"{'—' if before in (None, '') else before} → {'—' if after is None else after}"


def pages_section(results: list[dict], pages: dict, skipped: list[str], no_repo: list[str]) -> str:
    lines = [
        f"Checked {len(results)} robot page(s) in `wiki/robots/` against their `links.repo` with "
        "`tools/check_sources.py --pages`. New commits mean the page's `maturity` and `last_verified` "
        f"are out of date; \"active\" means a push in the last {STALE_PUSH_DAYS} days and not archived. "
        "Flagged pages go to `/review-sources`.",
        "",
    ]
    if skipped:
        lines += [f"Skipped near the API rate limit, {len(skipped)} page(s): {', '.join(skipped)}.", ""]
    if no_repo:
        lines += [f"No `links.repo`, so not checked: {', '.join(no_repo)}.", ""]
    lines += [
        "| Page | Flags | Last commit (page → now) | Active (page → now) | Stars (page → now) | GitHub licence | Last push |",
        "|---|---|---|---|---|---|---|",
    ]
    for result in results:
        page, now = pages[result["page"]][1], result["now"]
        flags = "; ".join(result["flags"]) or "no change"
        pushed = (now.get("pushed") or "—") + (" (archived)" if now.get("archived") else "")
        lines.append(
            f"| {result['page']} | {flags} | {change_text(dig(page, 'maturity', 'last_commit'), now.get('commit_date'))} | "
            f"{bool_text(dig(page, 'maturity', 'active'))} → {bool_text(now.get('active'))} | "
            f"{change_text(dig(page, 'maturity', 'stars'), now.get('stars'))} | {now.get('license') or '—'} | {pushed} |"
        )
    return "\n".join(lines)


def update_maturity(path: Path, values: dict) -> list[str] | None:
    """Edit a page's one-line `maturity: {…}`; return the keys changed, or None without that line."""
    lines = read_text(path).split("\n")
    end = next((i for i in range(1, len(lines)) if lines[i] == "---"), 0)
    for i in range(1, end):
        match = MATURITY_LINE.match(lines[i])
        if match:
            break
    else:
        return None
    current = yaml.safe_load("{" + match.group("body") + "}") or {}
    changed = [key for key, value in values.items() if value is not None and current.get(key) != value]
    if changed:
        merged = {**current, **{key: values[key] for key in changed}}
        comment = f"  {match.group('comment')}" if match.group("comment") else ""
        lines[i] = f"maturity: {flow(merged)}{comment}"
        write_text(path, "\n".join(lines))
    return changed


def record_pages(results: list[dict], pages: dict) -> list[str]:
    notes = []
    for result in results:
        if not result["ok"]:
            continue
        now = result["now"]
        values = {"last_commit": as_date(now.get("commit_date")), "stars": now.get("stars"), "active": now.get("active")}
        changed = update_maturity(pages[result["page"]][0], values)
        if changed is None:
            notes.append(f"{result['page']}: no one-line `maturity: {{…}}` in the frontmatter; update it by hand")
        elif changed:
            notes.append(f"{result['page']}: {', '.join(changed)}")
    return notes


# --- Report and command line -----------------------------------------------------------------


def report_text(sections: dict[str, str]) -> str:
    lines = [f"# Source check {TODAY}"]
    for kind, heading in REPORT_SECTIONS.items():
        if sections.get(kind):
            lines += ["", heading, "", sections[kind].strip()]
    return "\n".join(lines) + "\n"


def report_sections(text: str) -> dict[str, str]:
    """The sections of a report; text before any section heading is the registry's (older reports)."""
    kinds = {heading: kind for kind, heading in REPORT_SECTIONS.items()}
    sections, kind, body = {}, "registry", []
    for line in text.split("\n")[1:]:
        if line.strip() in kinds:
            sections[kind] = "\n".join(body).strip()
            kind, body = kinds[line.strip()], []
        else:
            body.append(line)
    sections[kind] = "\n".join(body).strip()
    return {k: v for k, v in sections.items() if v}


def write_report(kind: str, body: str) -> Path:
    """Write one section of today's report, keeping the other section if it is there."""
    path = REPORTS / f"{TODAY}.md"
    sections = report_sections(read_text(path)) if path.exists() else {}
    sections[kind] = body
    write_text(path, report_text(sections))
    return path


def run_registry(args: argparse.Namespace, gh: GitHub) -> int:
    registry = load_yaml(REGISTRY) or {}
    entries = {e["id"]: e for e in registry.get("sources") or [] if isinstance(e, dict) and e.get("id")}
    wanted = set(args.only or []) | set(args.rebaseline)
    unknown = wanted - set(entries)
    if unknown:
        print(f"not in the registry: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2
    ids = [i for i in entries if (i in wanted if wanted else entries[i].get("status") != "retired")]

    results = []
    for ident in ids:
        try:
            results.append(check(gh, entries[ident]))
        except RateLimited as exc:
            raise SystemExit(str(exc)) from None
        except NETWORK_ERRORS as exc:
            results.append({"id": ident, "status": entries[ident].get("status"), "flags": [f"network error: {exc}"], "now": {}, "ok": False})

    section = registry_section(results, entries)
    print(json.dumps(results, indent=2, default=str) if args.json else report_text({"registry": section}))
    if args.report:
        print(f"wrote {write_report('registry', section).relative_to(ROOT).as_posix()}", file=sys.stderr)
    if args.record or args.rebaseline:
        for change in update_registry(results, args.record, set(args.rebaseline)):
            print(f"registry: {change}", file=sys.stderr)
    return 0


def run_pages(args: argparse.Namespace, gh: GitHub) -> int:
    pages = robot_pages()
    unknown = set(args.only or []) - set(pages)
    if unknown:
        print(f"not a robot page in wiki/robots/: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2
    slugs = [s for s in pages if s in args.only] if args.only else list(pages)
    no_repo = [s for s in slugs if not dig(pages[s][1], "links", "repo")]
    slugs = [s for s in slugs if s not in no_repo]

    results, skipped = check_pages(gh, slugs, pages)
    section = pages_section(results, pages, skipped, no_repo)
    if args.json:
        print(json.dumps({"pages": results, "skipped": skipped, "no_repo": no_repo}, indent=2, default=str))
    else:
        print(report_text({"pages": section}))
    if skipped:
        print(
            f"skipped {len(skipped)} of {len(slugs)} page(s): the GitHub API limit resets {gh.reset_time()}. "
            "Set GITHUB_TOKEN, or run again later with --only.",
            file=sys.stderr,
        )
    if args.report:
        print(f"wrote {write_report('pages', section).relative_to(ROOT).as_posix()}", file=sys.stderr)
    if args.record_pages:
        for note in record_pages(results, pages):
            print(f"page: {note}", file=sys.stderr)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pages", action="store_true", help="check the robot pages in wiki/robots/ instead of the registry")
    parser.add_argument("--only", nargs="+", metavar="ID", help="check only these registry ids (with --pages: page slugs)")
    parser.add_argument("--report", action="store_true", help="write this check's section of sources/reports/<today>.md")
    parser.add_argument("--record", action="store_true", help="set last_checked to today for checked entries")
    parser.add_argument("--rebaseline", nargs="+", metavar="ID", default=[], help="record today's state as the baseline")
    parser.add_argument("--record-pages", action="store_true", help="with --pages: set maturity.last_commit, stars and active")
    parser.add_argument("--json", action="store_true", help="print the results as JSON")
    args = parser.parse_args()
    if args.pages and (args.record or args.rebaseline):
        parser.error("--record and --rebaseline are for registry entries; pages use --record-pages")
    if args.record_pages and not args.pages:
        parser.error("--record-pages needs --pages")
    utf8_output()

    gh = GitHub(os.environ.get("GITHUB_TOKEN"))
    status = run_pages(args, gh) if args.pages else run_registry(args, gh)
    if gh.remaining is not None:
        print(f"GitHub API requests left this hour: {gh.remaining}", file=sys.stderr)
    return status


if __name__ == "__main__":
    sys.exit(main())
