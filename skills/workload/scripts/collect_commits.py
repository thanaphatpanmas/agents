#!/usr/bin/env python3
"""Group the user's git commits by work day for writing a workload timesheet.

Usage:
  collect_commits.py --since 2026-10-12 --until 2026-10-18 [--repo PATH_OR_NAME ...] [--author PATTERN]

--repo takes a path, or a project name that is looked up as a git repo under the home folder.
Commits made before 05:00 count toward the previous day (late-night work).
"""
import argparse
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

LATE_NIGHT_CUTOFF_HOUR = 5
# Common code-layout directory names across ecosystems; they say where code lives, not which feature it is
NOISE_DIRS = {
    # repo / source roots
    "packages", "apps", "libs", "lib", "src", "app", "source", "main", "internal", "pkg", "cmd",
    # feature grouping
    "features", "modules", "domain", "domains",
    # UI layers
    "components", "pages", "views", "screens", "layouts", "routes", "router", "hooks",
    "store", "stores", "styles", "assets", "public", "static", "templates",
    # backend layers
    "controllers", "handlers", "services", "repositories", "models", "entities",
    "schemas", "dto", "dtos", "middleware", "api",
    # shared code
    "utils", "helpers", "types", "interfaces", "constants",
    # i18n
    "locales", "i18n", "translations",
    # tests
    "test", "tests", "__tests__", "spec", "specs", "fixtures", "mocks", "__mocks__",
    # misc
    "scripts", "screenshots", "images",
}
# Attribution trailers say who helped, not what was done
TRAILER = re.compile(r"(co-authored-by|signed-off-by):", re.IGNORECASE)
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SEARCH_DEPTH = 4
SKIP_SEARCH_DIRS = {"node_modules", "Library", "Applications", "Pictures", "Music", "Movies"}


def normalize(name):
    # "my-app", "my_app" and "My App" all name the same project
    return re.sub(r"[\s_.-]", "", name).lower()


def find_repos(name, root):
    target, found = normalize(name), []
    for dirpath, dirnames, _ in os.walk(root):
        if os.path.exists(os.path.join(dirpath, ".git")):
            if normalize(os.path.basename(dirpath)) == target:
                found.append(dirpath)
            dirnames.clear()
            continue
        if len(Path(dirpath).relative_to(root).parts) >= SEARCH_DEPTH:
            dirnames.clear()
            continue
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in SKIP_SEARCH_DIRS]
    return found


def resolve_repo(value):
    path = Path(value).expanduser()
    if path.is_dir():
        return path
    root = Path.home()
    matches = find_repos(value, root)
    if len(matches) == 1:
        return Path(matches[0])
    if not matches:
        sys.exit(f"No git repo named '{value}' under {root} (depth {SEARCH_DEPTH}); pass its path instead")
    sys.exit(f"Several repos match '{value}': {', '.join(matches)}; pass the path instead")


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout


def area_of(path):
    # numstat writes a rename as "dir/{old => new}/file" or "old => new"; the work is at the new path
    path = re.sub(r"\{[^{}]* => ([^{}]*)\}", r"\1", path).split(" => ")[-1]
    parts = [p for p in Path(path).parent.parts if p.lower() not in NOISE_DIRS]
    if not parts:
        return Path(path).name
    return "/".join(parts)


def read_commits(repo, author, since, until):
    # The stash ref holds uncommitted work, not commits. --since checks the committer date, which is never
    # earlier than the author date, so it only bounds the search; the range itself is applied below
    log = git(
        repo, "log", "--exclude=refs/stash", "--all", "--no-merges", f"--author={author}",
        f"--since={since.isoformat()}",
        "--date=iso-strict", "--numstat", "--pretty=format:%x1e%H%x09%ad%x09%s%x1f%b%x1f",
    )
    commits = []
    for record in log.split("\x1e")[1:]:
        header, body, numstat = record.split("\x1f", 2)
        sha, when, subject = header.split("\t", 2)
        # Commits may carry any timezone (e.g. UTC "Z"); the work day is the user's local day
        when = datetime.fromisoformat(when.replace("Z", "+00:00")).astimezone()
        # Author date, not committer date: a rebase days later must not move the work out of its week
        if not since <= when < until:
            continue
        current = {
            "repo": Path(repo).resolve().name, "sha": sha[:8], "subject": subject, "when": when,
            "body": [line for line in body.splitlines() if line.strip() and not TRAILER.match(line)],
            "added": 0, "deleted": 0,
            "areas": Counter(),
        }
        commits.append(current)
        for line in numstat.splitlines():
            m = re.match(r"(\d+|-)\t(\d+|-)\t(.+)", line)
            if not m:
                continue
            added = int(m[1]) if m[1] != "-" else 0
            deleted = int(m[2]) if m[2] != "-" else 0
            current["added"] += added
            current["deleted"] += deleted
            current["areas"][area_of(m[3])] += added + deleted or 1
    return commits


def work_day(when):
    if when.hour < LATE_NIGHT_CUTOFF_HOUR:
        return (when - timedelta(days=1)).date()
    return when.date()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", required=True, type=date.fromisoformat)
    parser.add_argument("--until", required=True, type=date.fromisoformat, help="inclusive")
    parser.add_argument("--repo", action="append", default=[], help="path or project name; repeatable; default: cwd")
    parser.add_argument("--author", help="default: git config user.name of each repo")
    args = parser.parse_args()

    # Widen the window so late-night commits land on the right day
    since = (datetime.combine(args.since, datetime.min.time()) + timedelta(hours=LATE_NIGHT_CUTOFF_HOUR)).astimezone()
    until = (datetime.combine(args.until + timedelta(days=1), datetime.min.time()) + timedelta(hours=LATE_NIGHT_CUTOFF_HOUR)).astimezone()

    by_day, seen = defaultdict(list), set()
    repos = [resolve_repo(r) for r in args.repo] or [Path(".")]
    for repo in repos:
        author = args.author or git(repo, "config", "user.name").strip()
        for c in read_commits(repo, author, since, until):
            # Rebased/cherry-picked copies on other branches share subject and time
            key = (c["subject"], c["when"])
            if key in seen:
                continue
            seen.add(key)
            by_day[work_day(c["when"])].append(c)

    day = args.since
    while day <= args.until:
        commits = sorted(by_day.get(day, []), key=lambda c: c["when"])
        print(f"## {day.strftime('%d/%m/%Y')} {WEEKDAYS[day.weekday()]}"
              + ("" if commits else "  (no commits)"))
        for c in commits:
            late = " late-night" if c["when"].date() != day else ""
            areas = ", ".join(a for a, _ in c["areas"].most_common(3))
            print(f"- {c['when'].strftime('%H:%M')}{late} [{c['repo']}] {c['sha']} {c['subject']}"
                  f"  (+{c['added']}/-{c['deleted']})  areas: {areas}")
            for line in c["body"]:
                print(f"    {line}")
        day += timedelta(days=1)


if __name__ == "__main__":
    main()
