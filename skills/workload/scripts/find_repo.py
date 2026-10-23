#!/usr/bin/env python3
"""Print the path of the git repo the user named.

Usage:
  find_repo.py PATH_OR_NAME

A name is looked up as a git repo folder under the home folder, matching loosely.
Exits with an error when nothing or several repos match.
Kept identical in skills/commit and skills/workload, which are installed separately; edit both.
"""
import os
import re
import sys
from pathlib import Path

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
        return path.resolve()
    root = Path.home()
    matches = find_repos(value, root)
    if len(matches) == 1:
        return Path(matches[0])
    if not matches:
        sys.exit(f"No git repo named '{value}' under {root} (depth {SEARCH_DEPTH}); pass its path instead")
    sys.exit(f"Several repos match '{value}': {', '.join(matches)}; pass the path instead")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(resolve_repo(sys.argv[1]))
