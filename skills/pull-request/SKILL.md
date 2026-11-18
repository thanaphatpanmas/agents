---
name: pull-request
description: Open or update a GitHub pull request or GitLab merge request (including self-hosted) for the current branch, choosing the base from the commit graph, checking conflicts and resolving clear ones before push, and writing a Conventional Commits title and reviewer-ready description from the whole branch. Use when the user asks, in any language, to open, create or update a PR or MR, ask for review, or runs /pull-request. Not for standalone commits, merging or reviewing PRs.
argument-hint: "[project name or path] [base branch] [draft|ready] [reviewer names] [delete-branch|keep-branch] [notes for the description]"
---

# Pull Request

The user has finished work on a branch and wants it in front of reviewers without writing the PR themselves. A reviewer reads the PR once, often before the code, so it has to explain the whole branch: why it exists, what changed, how it was checked, and what could go wrong. Build it from every commit and the full diff against the base, not from the last commit or memory of the conversation; the conversation supplies the why and the testing.

Reply to the user in their language; write the title and description in English unless the repo's recent PRs use another language. "PR" means a GitHub pull request or a GitLab merge request; the steps are the same.

| Reference | Read at |
| --- | --- |
| `references/base-branch.md`: how the base is chosen and checked | step 3 |
| `references/integration.md`: branch synchronization, conflict checks and resolution | step 4 |
| `references/cli.md`: every `gh` / `glab` command, and CLI setup | steps 2, 3, 5, 7, 8 |
| `references/templates.md`: title and description rules, sizes, examples | step 6 |

## 1. Pick the project

The project comes first in the request: `/pull-request web-app dev draft`. With no project named, use the current repo. A name is looked up with the script below; if it reports no match or several, ask for the path.

```bash
python3 <skill-dir>/scripts/find_repo.py <name>
```

A branch name in the request is the base the user wants, `draft` / `ready` set the PR state, people named as reviewers or assignees answer those questions in step 7, `delete-branch` / `keep-branch` (or saying in words whether to delete the branch after merge) answers the delete question, and other words are notes for the description. Below, `<repo>` is the project's path; pass it to every git command with `-C`.

## 2. Gather the facts

```bash
git -C <repo> fetch --prune <remote>   # usually origin; on failure, only prepare text and report the failed fetch
python3 <skill-dir>/scripts/pr_context.py <repo> [--base <branch>]   # --base only when the user named one
```

The JSON gives the branch and its push state, `platform` (`github`, `gitlab`, `unknown`), whether `gh` / `glab` are logged in to the host, the suggested base, and any PR/MR templates.

Stop and tell the user, without trying to fix it, when the script exits with an error, `in_progress` is set (finish the merge or rebase first), or `base.suggested` is null (nothing to review).

- `uncommitted_files` above 0: ask whether to commit first (with the `commit` skill) or open the PR without them. Don't stage user changes, stash them or integrate branches over them; if integration is needed, wait for a clean worktree
- `platform: unknown`: ask whether the host is GitHub or GitLab
- the needed CLI missing or not logged in: give the setup from `cli.md`, and offer to write the title and description for pasting into the web form at `web_url`

## 3. Settle the base

Find an open PR from this branch (`cli.md`, "Find PRs"): if one exists, this run updates it instead of opening a duplicate. Then settle the base with `references/base-branch.md`: stacked bases, ambiguous ones and promotion PRs each need a check before you trust the suggestion.

Resolve an ambiguous base before any integration or push; don't defer this decision to step 7.

## 4. Prepare and push the branch

Follow `references/integration.md` before pushing: synchronize with the same-named remote branch, then check conflicts against the settled base. Merge is the default when integration is needed; use rebase only under the conditions in that reference. Resolve conflicts without asking when code, tests and requirements establish the intended result; ask before choosing between different behaviors. Promotion PRs need a separate decision before integrating the base backwards.

After integration, rerun `pr_context.py <repo> --base <base>` and use the refreshed push counts. Don't push with unresolved conflicts, an unfinished operation or failed required checks.

The PR is built from what is on the remote. The counts compare with `<remote>/<branch>`, not the upstream, because `git checkout -b feat origin/main` tracks `main`:

- `push.behind` above 0 → return to synchronization in `references/integration.md` before either push command below
- `push.remote_branch_exists` or `push.tracks_remote_branch` false → `git -C <repo> push -u <remote> <branch>`
- `push.unpushed` above 0 → `git -C <repo> push <remote> <branch>`

Never force-push. If a concurrent update rejects the push, fetch again and repeat synchronization, conflict checks and verification; if updates keep racing, report it and stop. Any other rejection (authentication, protected branch): show the error and stop.

## 5. Read the whole branch

Compare against `<remote>/<base>`, so a stale local base can't add or hide commits. The three-dot diff is exactly what reviewers will see; if it is very large, go area by area from the stat.

```bash
git -C <repo> log --reverse --no-merges --format='%h %s%n%b' <remote>/<base>..HEAD
git -C <repo> diff --stat <remote>/<base>...HEAD
git -C <repo> diff <remote>/<base>...HEAD
```

Also gather: 3–5 recently merged PRs, to match language and shape and to see who usually reviews (`cli.md`, "Recent merged PRs"); the repo template listed in `templates`, whose sections replace the standard ones; and what was actually tested in this session or by CI, including screenshots of UI changes. Include material conflict resolutions and checks run after integration; earlier checks alone don't verify the integrated result.

## 6. Write the title and description

Follow `references/templates.md`. The title is a Conventional Commits subject, since squash-merging turns it into the commit on the base. The description puts the why first and lists only checks that really ran.

## 7. Ask before creating

Ask in one AskUserQuestion call with up to four questions (otherwise in chat, and wait). Skip a question the request already answered (State only when the base is also certain); for an existing PR, show its current reviewers, assignees and delete setting as the first option of each.

1. **State**: each option's preview shows the full title and description, and its label names the direction, e.g. "Open PR: `feature/b` → `dev`": **Open as ready for review** / **Open as draft**, or **Update PR #12** for an existing one (say if the state or base would change)
2. **Reviewers** (multi-select): up to three people who reviewed recent merged PRs, excluding the author, plus **No reviewer**; the user can type other names
3. **Assignee**: **Same as reviewers** / **Me** / **None**
4. **Delete source branch after merge**: **No** / **Yes**, GitLab only. GitHub has no per-PR setting: don't ask, and state the repo-wide setting in the preview (`cli.md`, "Delete branch after merge")

Typed names are checked against the host before creating (`cli.md`, "Reviewers and assignees"). If the user changes the base during preview, return to steps 3–5 before creating. If the user edits the text, revise and ask again; if they cancel, nothing is created.

## 8. Create or update

Run the create or update command from `cli.md`, passing the description through a temporary file. Attach screenshots where the CLI can. Pass the reviewers and assignees chosen in step 7, and set delete-after-merge to the answer (`cli.md`, "Delete branch after merge"). Never merge a PR/MR, approve, enable auto-merge, close, or delete branches yourself; local branch integration in step 4 is separate. If the command fails, show the error and stop.

## 9. Report

Keep it short: the PR URL, `head` → `base`, ready or draft, reviewers, assignees and whether the branch is deleted after merge; for a stacked PR, which PR must merge first; what the user still has to do (screenshots to drag in, a base you chose, checks you couldn't run); the full text only if they didn't see it in step 7.
