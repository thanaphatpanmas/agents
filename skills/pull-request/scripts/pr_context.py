#!/usr/bin/env python3
"""Print, as JSON, what the pull-request skill needs to open a PR/MR for the current branch.

Usage:
  pr_context.py REPO [--base BRANCH]

Reports the branch and its push state, the remote and its hosting platform, whether
gh/glab are installed and logged in for that host, PR/MR templates, and the base branch.
Without --base, the base is read from the commit graph: the remote branch that HEAD has
the fewest commits beyond, so a stacked branch (feature-b on feature-a on dev) gets
feature-a, and a branch cut from dev gets dev while dev is ahead of main. From a
long-lived branch (main, dev, uat, prod...) only other long-lived branches are offered,
always marked ambiguous, since promotion order (dev -> main -> prod) is a team choice.
Run `git fetch --prune <remote>` first so remote branches are current.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

# Long-lived branches win a tie over feature branches cut from the same commit.
INTEGRATION_BRANCHES = (
    "main", "master", "develop", "dev", "development",
    "staging", "test", "testing", "uat", "release", "prod", "production",
)
MAX_CANDIDATES = 5
IN_PROGRESS = {
    "MERGE_HEAD": "merge",
    "rebase-merge": "rebase",
    "rebase-apply": "rebase",
    "CHERRY_PICK_HEAD": "cherry-pick",
    "REVERT_HEAD": "revert",
}
TEMPLATE_PATTERNS = [
    re.compile(r"^(\.github/|docs/)?pull_request_template\.md$", re.I),
    re.compile(r"^\.github/pull_request_template/[^/]+\.md$", re.I),
    re.compile(r"^\.gitlab/merge_request_templates/[^/]+\.md$", re.I),
]


def git(repo, *args):
    """Run git in repo; return stdout, or None when the command fails."""
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def parse_remote(url):
    """Host and project path from an https or ssh remote URL, without credentials."""
    scp = re.match(r"^(?:[^@/]+@)?([^:/]+):(?!//)(.+)$", url)
    if scp and "://" not in url:
        host, path = scp.groups()
    else:
        parts = urlsplit(url)
        host, path = parts.hostname or "", parts.path
    path = re.sub(r"\.git$", "", path.strip("/"))
    return host, path


def cli_status(tool, host):
    if not shutil.which(tool):
        return {"installed": False, "authenticated": False}
    try:
        result = subprocess.run(
            [tool, "auth", "status", "--hostname", host], capture_output=True, text=True, timeout=30
        )
        authenticated = result.returncode == 0
    except subprocess.TimeoutExpired:
        authenticated = None
    return {"installed": True, "authenticated": authenticated}


def detect_platform(host, cli):
    if host == "github.com":
        return "github"
    if host == "gitlab.com":
        return "gitlab"
    # Self-hosted: trust whichever CLI is logged in to this host, then the host name.
    if cli["gh"]["authenticated"]:
        return "github"
    if cli["glab"]["authenticated"]:
        return "gitlab"
    if "github" in host:
        return "github"
    if "gitlab" in host:
        return "gitlab"
    return "unknown"


def pick_remote(repo, branch):
    remotes = (git(repo, "remote") or "").split()
    configured = git(repo, "config", f"branch.{branch}.remote")
    if configured in remotes:
        return configured
    if "origin" in remotes:
        return "origin"
    return remotes[0] if len(remotes) == 1 else None


def default_branch(repo, remote):
    head = git(repo, "symbolic-ref", "--short", f"refs/remotes/{remote}/HEAD")
    if head:
        return head.removeprefix(f"{remote}/")
    for name in ("main", "master"):
        if git(repo, "rev-parse", "--verify", "--quiet", f"refs/remotes/{remote}/{name}"):
            return name
    return None


def ahead_behind(repo, ref):
    """(commits only in HEAD, commits only in ref)."""
    counts = git(repo, "rev-list", "--left-right", "--count", f"{ref}...HEAD")
    if not counts:
        return None
    behind, ahead = (int(n) for n in counts.split())
    return ahead, behind


def rank_bases(repo, remote, branch, default):
    prefix = f"refs/remotes/{remote}/"
    refs = (git(repo, "for-each-ref", "--format=%(refname)", prefix) or "").splitlines()
    candidates = []
    for ref in refs:
        name = ref.removeprefix(prefix)
        if name in ("HEAD", branch):
            continue
        counts = ahead_behind(repo, f"{remote}/{name}")
        # ahead == 0: the branch already holds everything here (merged, or stacked on top of it).
        if not counts or counts[0] == 0:
            continue
        ahead, behind = counts
        rank = 0 if name == default else 1 if name in INTEGRATION_BRANCHES else 2
        candidates.append({"branch": name, "ahead": ahead, "behind": behind, "rank": rank})
    # Fewest commits beyond wins; on a tie, long-lived branches beat feature branches,
    # then the one whose tip is nearest the fork point (dev contains main, but a branch cut from main sits on main).
    candidates.sort(key=lambda c: (c["ahead"], c["rank"] == 2, c["behind"], c["rank"], c["branch"]))
    return candidates


def suggest_base(candidates, total):
    if not candidates:
        return None, "no remote branch is behind this branch: it is already merged or has no commits of its own", False
    best = candidates[0]
    tied = [c for c in candidates if c["ahead"] == best["ahead"] and c["rank"] < 2]
    # Unless exactly one tied long-lived branch still sits at the fork point (dev == main, or both moved on),
    # the graph can't tell which one the branch was cut from.
    ambiguous = len(tied) > 1 and sum(c["behind"] == 0 for c in tied) != 1
    reason = (
        f"{best['ahead']} commit(s) here are not on {best['branch']}, "
        f"the fewest of {total} remote branches"
    )
    if ambiguous:
        reason += f"; tied with {', '.join(c['branch'] for c in tied if c is not best)}"
    return best["branch"], reason, ambiguous


def git_path_exists(repo, name):
    path = git(repo, "rev-parse", "--git-path", name)
    return bool(path) and (Path(repo) / path).exists()


def find_templates(repo):
    files = (git(repo, "ls-files") or "").splitlines()
    return [f for f in files if any(p.match(f) for p in TEMPLATE_PATTERNS)]


def main():
    args = sys.argv[1:]
    base_arg = None
    if "--base" in args:
        i = args.index("--base")
        if i + 1 >= len(args):
            sys.exit(__doc__)
        base_arg = args[i + 1]
        del args[i : i + 2]
    if len(args) != 1:
        sys.exit(__doc__)

    repo = git(args[0], "rev-parse", "--show-toplevel")
    if not repo:
        sys.exit(f"Not a git repository: {args[0]}")
    branch = git(repo, "branch", "--show-current")
    if not branch:
        sys.exit("HEAD is detached: check out a branch first")

    in_progress = next((op for marker, op in IN_PROGRESS.items() if git_path_exists(repo, marker)), None)
    dirty = len((git(repo, "status", "--porcelain") or "").splitlines())

    remote = pick_remote(repo, branch)
    if not remote:
        sys.exit("No remote to open a pull request on (none, or several and none is 'origin')")
    host, project = parse_remote(git(repo, "remote", "get-url", remote) or "")
    cli = {"gh": cli_status("gh", host), "glab": cli_status("glab", host)}
    default = default_branch(repo, remote)

    # Compare with the same-named remote branch, not @{u}: `checkout -b feat origin/main` tracks main.
    remote_branch = f"{remote}/{branch}"
    upstream = git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    remote_branch_exists = bool(git(repo, "rev-parse", "--verify", "--quiet", f"refs/remotes/{remote_branch}"))
    push = {
        "remote_branch_exists": remote_branch_exists,
        "tracks_remote_branch": upstream == remote_branch,
        "unpushed": None,
        "behind": None,
    }
    if remote_branch_exists:
        push["unpushed"], push["behind"] = ahead_behind(repo, remote_branch)

    long_lived = branch == default or branch in INTEGRATION_BRANCHES
    all_candidates = rank_bases(repo, remote, branch, default)
    # From a long-lived branch, feature branches left on the remote after merging are not targets.
    candidates = [c for c in all_candidates if c["rank"] < 2] if long_lived else all_candidates

    if base_arg:
        if not git(repo, "rev-parse", "--verify", "--quiet", f"refs/remotes/{remote}/{base_arg}"):
            sys.exit(f"Base branch '{base_arg}' is not on {remote}; push it or pick another")
        if any(c["branch"] == base_arg for c in all_candidates):
            suggested, reason, ambiguous = base_arg, "named by the user", False
        else:
            suggested, reason, ambiguous = None, f"{base_arg} already holds every commit on {branch}", False
    else:
        suggested, reason, ambiguous = suggest_base(candidates, len(candidates))
        if long_lived and suggested:
            reason = f"{branch} is a long-lived branch, so this is a promotion PR; confirm the target. {reason}"
            ambiguous = True

    print(json.dumps({
        "repo": repo,
        "branch": branch,
        "on_default_branch": branch == default,
        "long_lived_branch": long_lived,
        "in_progress": in_progress,
        "uncommitted_files": dirty,
        "remote": remote,
        "host": host,
        "project": project,
        "web_url": f"https://{host}/{project}" if host and project else None,
        "platform": detect_platform(host, cli),
        "cli": cli,
        "default_branch": default,
        "push": push,
        "base": {
            "suggested": suggested,
            "reason": reason,
            "ambiguous": ambiguous,
            "candidates": [{k: c[k] for k in ("branch", "ahead", "behind")} for c in candidates[:MAX_CANDIDATES]],
        },
        "templates": find_templates(repo),
    }, indent=2))


if __name__ == "__main__":
    main()
