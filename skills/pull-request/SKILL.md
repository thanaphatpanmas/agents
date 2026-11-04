---
name: pull-request
description: Open or update a GitHub pull request or GitLab merge request (including self-hosted) for the current branch, choosing the base from the commit graph (main, dev, or a stacked parent) and writing a Conventional Commits title and reviewer-ready description from the whole branch. Use when the user asks, in any language, to open, create or update a PR or MR, ask for review, or runs /pull-request. Not for committing, merging or reviewing PRs.
argument-hint: "[project name or path] [base branch] [draft|ready] [delete-branch] [notes for the description]"
---

# Pull Request

The user has finished work on a branch and wants it in front of reviewers without writing the PR themselves. A reviewer reads the PR once, often before the code, so it has to explain the whole branch: why it exists, what changed, how it was checked, and what could go wrong. Build it from every commit and the full diff against the base, not from the last commit or memory of the conversation; the conversation supplies the why and the testing.

Reply to the user in their language; write the title and description in English unless the repo's recent PRs use another language. "PR" means a GitHub pull request or a GitLab merge request; the steps are the same.

| Reference | Read at |
| --- | --- |
| `references/base-branch.md`: how the base is chosen and checked | step 3 |
| `references/cli.md`: every `gh` / `glab` command, and CLI setup | steps 2, 3, 5, 8 |
| `references/templates.md`: title and description rules, sizes, examples | step 6 |

## 1. Pick the project

The project comes first in the request: `/pull-request web-app dev draft`. With no project named, use the current repo. A name is looked up with the script below; if it reports no match or several, ask for the path.

```bash
python3 <skill-dir>/scripts/find_repo.py <name>
```

A branch name in the request is the base the user wants, `draft` / `ready` set the PR state, `delete-branch` (or asking in words to delete the branch after merge) turns on deleting the source branch when the PR merges, and other words are notes for the description. Below, `<repo>` is the project's path; pass it to every git command with `-C`.

## 2. Gather the facts

```bash
git -C <repo> fetch --prune <remote>   # usually origin; if it fails (offline), continue and say so
python3 <skill-dir>/scripts/pr_context.py <repo> [--base <branch>]   # --base only when the user named one
```

The JSON gives the branch and its push state, `platform` (`github`, `gitlab`, `unknown`), whether `gh` / `glab` are logged in to the host, the suggested base, and any PR/MR templates.

Stop and tell the user, without trying to fix it, when the script exits with an error, `in_progress` is set (finish the merge or rebase first), or `base.suggested` is null (nothing to review).

- `uncommitted_files` above 0: ask whether to commit first (with the `commit` skill) or open the PR without them. Don't stage anything yourself
- `platform: unknown`: ask whether the host is GitHub or GitLab
- the needed CLI missing or not logged in: give the setup from `cli.md`, and offer to write the title and description for pasting into the web form at `web_url`

## 3. Settle the base

Find an open PR from this branch (`cli.md`, "Find PRs"): if one exists, this run updates it instead of opening a duplicate. Then settle the base with `references/base-branch.md`: stacked bases, ambiguous ones and promotion PRs each need a check before you trust the suggestion.

## 4. Push the branch

The PR is built from what is on the remote. The counts compare with `<remote>/<branch>`, not the upstream, because `git checkout -b feat origin/main` tracks `main`:

- `push.remote_branch_exists` or `push.tracks_remote_branch` false → `git -C <repo> push -u <remote> <branch>`
- `push.unpushed` above 0 → `git -C <repo> push <remote> <branch>`
- `push.behind` above 0 → never force-push: stop, and offer `git -C <repo> pull --rebase <remote> <branch>`, run only if they agree

Any other rejection (authentication, protected branch): show the error and stop.

## 5. Read the whole branch

Compare against `<remote>/<base>`, so a stale local base can't add or hide commits. The three-dot diff is exactly what reviewers will see; if it is very large, go area by area from the stat.

```bash
git -C <repo> log --reverse --no-merges --format='%h %s%n%b' <remote>/<base>..HEAD
git -C <repo> diff --stat <remote>/<base>...HEAD
git -C <repo> diff <remote>/<base>...HEAD
```

Also gather: 3–5 recently merged PRs, to match language and shape (`cli.md`, "Recent merged PRs"); the repo template listed in `templates`, whose sections replace the standard ones; and what was actually tested in this session or by CI, including screenshots of UI changes.

## 6. Write the title and description

Follow `references/templates.md`. The title is a Conventional Commits subject, since squash-merging turns it into the commit on the base. The description puts the why first and lists only checks that really ran.

## 7. Ask before creating

Ask one question, with AskUserQuestion if available (otherwise in chat, and wait). Each option's preview shows the full title and description, and its label names the direction, e.g. "Open PR: `feature/b` → `dev`":

- **Open as ready for review** / **Open as draft**, or **Update PR #12** for an existing one (say if the state or base would change, and whether the source branch will be deleted after merge)
- When the base is ambiguous or looked wrong, ask for it in the same call, recommended branch first

Skip the question only when the request set `draft` / `ready` and the base is certain. If the user edits the text, revise and ask again; if they cancel, nothing is created.

## 8. Create or update

Run the create or update command from `cli.md`, passing the description through a temporary file. Attach screenshots where the CLI can. With `delete-branch`, also set delete-after-merge (`cli.md`, "Delete branch after merge"). Never merge, approve, enable auto-merge, close, or delete branches yourself. If the command fails, show the error and stop.

## 9. Report

Keep it short: the PR URL, `head` → `base`, ready or draft; for a stacked PR, which PR must merge first; what the user still has to do (screenshots to drag in, a base you chose, checks you couldn't run); the full text only if they didn't see it in step 7.
