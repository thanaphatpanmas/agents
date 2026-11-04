---
name: pull-request
description: Open or update a pull request (GitHub) or merge request (GitLab, including self-hosted) for the current branch of a repo (the current one, or a project the user names), picking the base branch from the commit graph (main, dev, or the parent branch of a stacked branch), and writing a Conventional Commits title and a reviewer-ready description from every commit and the full diff against that base. Use when the user asks, in any language, to open, create, raise, send or update a PR or MR, ask for review, or "ขอ merge / เปิด PR / สร้าง MR / ส่งรีวิว", or runs /pull-request, even if they don't say which branch to target. Not for committing (use commit), merging, approving, reviewing someone else's PR, or resolving conflicts.
argument-hint: "[project name or path] [base branch] [draft|ready] [notes for the description]"
---

# Pull Request

The user has finished work on a branch and wants it in front of reviewers without writing the PR themselves. A reviewer reads the PR once, often before the code, to decide what to look at, so it has to explain the whole branch: why it exists, what changed, how it was checked, and what could go wrong. Build it from every commit and the full diff against the base, not from the last commit or memory of the conversation; the conversation supplies the why and the testing.

Reply to the user in their language; write the title and description in English unless step 5 finds the repo uses another language.

"PR" below means a GitHub pull request or a GitLab merge request; the steps are the same.

## 1. Pick the project

The project comes first in the request: `/pull-request web-app dev draft`. With no project named, use the current repo.

- **Path**: use it as is
- **Name**: look it up. The script finds a git repo folder with that name under the home folder, matching loosely, and prints its path. If it reports no match or several, ask the user for the path.
  ```bash
  python3 <skill-dir>/scripts/find_repo.py <name>
  ```

A branch name in the request is the base the user wants (`/pull-request dev`), and `draft` / `ready` set the PR state; neither is a project. Words that read as notes go into the description.

Below, `<repo>` is the project's path. Pass it to every git command with `-C`.

## 2. Gather the facts

Fetch first, so remote branches are current, then run the context script. Pass `--base <branch>` only when the user named one.

```bash
git -C <repo> fetch --prune <remote>   # <remote> is usually origin; if fetch fails (offline), continue and say so
python3 <skill-dir>/scripts/pr_context.py <repo> [--base <branch>]
```

It prints JSON: `branch`, `on_default_branch`, `long_lived_branch` (default, or a name like `dev`, `uat`, `prod`), `in_progress`, `uncommitted_files`, `remote`, `host`, `project`, `web_url`, `platform` (`github`, `gitlab` or `unknown`), `cli` (whether `gh` and `glab` are installed and logged in to that host), `default_branch`, `push` (whether `<remote>/<branch>` exists and is tracked, unpushed and behind counts against it), `base` (suggested branch, reason, whether it is ambiguous, top candidates), and `templates` (PR/MR template files in the repo).

Stop and tell the user, without trying to fix it, when:

- the script exits with an error (not a repo, detached HEAD, no remote, `--base` not on the remote)
- `in_progress` is set: a merge, rebase, cherry-pick or revert must be finished first
- `base.suggested` is null: the base already holds every commit here, so there is nothing to review

On a long-lived branch (`long_lived_branch`), this is a promotion PR such as `dev` → `main` or `main` → `prod`, and only other long-lived branches are offered. That is fine when the user meant to promote. If instead they committed feature work straight onto it, say so: a feature PR needs its own branch, and you never create or switch branches yourself.

When `uncommitted_files` is above 0, ask whether to commit them first (with the `commit` skill if available) or open the PR without them. Don't stage anything yourself.

**CLI**: GitHub needs `gh`, GitLab needs `glab`. For `platform: unknown`, a self-hosted host neither CLI is logged in to, ask the user which one it is. When the needed CLI is missing or not logged in, tell the user how to set it up (see "Setup" at the end) and offer to write the title and description anyway, for pasting into the web form at `web_url`.

## 3. Find an existing PR and settle the base

Look for an open PR from this branch, because a second push of the same work should update it, not open a duplicate:

```bash
gh pr list --head <branch> --state open --json number,url,title,baseRefName,isDraft    # GitHub
glab mr list --source-branch <branch> --output json                                       # GitLab (open only)
```

If one exists, this run updates it. Its base stays unless the user named another.

Otherwise the base is, in order: the branch the user named, then `base.suggested`. The script picks the remote branch this one has the fewest commits beyond, which follows how the branch was actually cut:

- cut from `main` → `main`; cut from `dev` while `dev` is ahead of `main` → `dev`
- stacked on another feature branch → that branch, so the PR shows only this branch's own commits
- on a long-lived branch → the nearest other long-lived branch (`dev` → `main`, `main` → `prod`), always confirmed with the user

Check the suggestion before trusting it:

- **Stacked base** (not the default branch or a long-lived one like `dev`): look up that branch's own PR with the list command above using its name. If it is open, link it in the description ("Depends on #12" / "Depends on !12") and say it must merge first. If it was already merged, its branch is dead: suggest the branch it merged into instead.
- **`base.ambiguous`**: the graph can't tell the team's flow: two long-lived branches sit at the same fork point (`dev` == `main`), or this is a promotion PR. Look at where recent PRs went (`gh pr list --state merged --limit 10 --json headRefName,baseRefName` / `glab mr list --merged --per-page 10 --output json`, field `target_branch`): if feature branches usually go to `dev`, or `dev` usually goes to `main`, recommend that. Then ask in step 7 instead of guessing.
- **Too many commits**: if the range holds commits that clearly aren't this work (dozens of unrelated subjects), the base is wrong. Show the candidates and ask.

## 4. Push the branch

The PR is built from what is on the remote, so push before writing it. The counts compare with `<remote>/<branch>`, not the upstream, because a branch made with `git checkout -b feat origin/main` tracks `main`:

- `push.remote_branch_exists` or `push.tracks_remote_branch` is false → `git -C <repo> push -u <remote> <branch>`
- `push.unpushed` above 0 → `git -C <repo> push <remote> <branch>`
- `push.behind` above 0 → the remote branch has commits this clone lacks. Never force-push: stop and tell the user (offer `git -C <repo> pull --rebase <remote> <branch>`, run it only if they agree)

If the push is rejected for any other reason (authentication, protected branch), show the error and stop.

## 5. Read the whole branch

Compare against the remote base, `<remote>/<base>`, so a stale local copy of the base can't add or hide commits:

```bash
git -C <repo> log --reverse --no-merges --format='%h %s%n%b' <remote>/<base>..HEAD
git -C <repo> diff --stat <remote>/<base>...HEAD
git -C <repo> diff <remote>/<base>...HEAD
```

The three-dot diff is exactly what reviewers will see in the PR. If it is very large, go area by area from the stat; lockfiles and generated files only need their names.

Also gather:

- **Language and shape**: glance at 3–5 recently merged PRs (`gh pr list --state merged --limit 5 --json title,body` / `glab mr list --merged --per-page 5 --output json`) to match their language, section names and title style
- **Template**: if `templates` lists a file, read it. On GitHub one `pull_request_template.md` is used automatically; on GitLab `.gitlab/merge_request_templates/Default.md` is the default. Fill the template's sections instead of the standard ones
- **Testing**: what was actually run in this session or by CI (commands, test results), and screenshots taken of UI changes

## 6. Write the title and description

Read `references/templates.md` before writing. It holds the skeleton, how to pick small, medium or large, and examples.

**Title**: Conventional Commits, the same rules as a commit subject. Many teams squash-merge, which turns the PR title into the commit on the base branch.

- `type(scope): summary`, imperative, lower-case verb after the colon, 72 characters at most, no trailing period
- `type` by the first that applies: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `style`, `chore`, `revert`. A feature with its tests is `feat`
- `scope`: the main module, reusing scopes from `git log`; leave it out when the branch spans many areas
- A breaking change gets `!` after the type or scope
- A one-commit branch can reuse that commit's subject

**Description**: covers the whole branch at the depth its size calls for.

- **Why first**: the problem or goal and the approach, from the conversation when you have it. Don't invent motivation
- **Changes**: what changed, grouped by area for large branches. Name modules, endpoints, commands and config keys, not line edits
- **Testing**: only what was really run and what it showed, plus steps a reviewer can follow. Never claim a check passed when you don't know; say what wasn't tested
- **Always call out**: behavior users will notice, migrations, new env vars or config and how to apply them, dependency changes, risks, follow-ups left undone, and merge order for a stacked PR
- **Keep out**: diff stats, file-by-file trivia, conversation chatter, tool or agent names, secrets and personal data from logs or screenshots
- **Issue links** (`Closes #123`) only when the number appears in the branch name, commits, conversation or user's notes
- **Checkboxes** in a repo template: tick only what you verified

Add any attribution lines your own instructions require (for example a "Generated with" footer) as the last line.

## 7. Ask before creating

Show the user one question, with AskUserQuestion if available (if not, show the text in chat and wait). The preview of each option shows the full title and description, and the labels name the direction, e.g. "Open PR: `feature/b` → `dev`":

- **Open as ready for review**
- **Open as draft**
- For an existing PR: **Update PR #12** (and say if the state or base would change)

When `base.ambiguous` is true or the base looked wrong in step 3, ask for the base in the same call, recommended branch first.

Skip the question only when the request already decided the state (`draft` / `ready`), and the base is certain (named by the user, or not ambiguous). If the user edits the text, revise it and ask again; if they cancel, nothing is created, and the pushed branch stays.

## 8. Create or update

Write the description to a temporary file so line breaks, backticks and `$` survive the shell, and quote the title in single quotes (escape any `'` inside it as `'\''`):

```bash
body=$(mktemp) && cat > "$body" <<'EOF'
<description>
EOF
```

| | GitHub (`gh`) | GitLab (`glab`) |
| --- | --- | --- |
| Create | `gh pr create --base <base> --head <branch> --title '<title>' --body-file "$body" [--draft]` | `glab mr create --source-branch <branch> --target-branch <base> --title '<title>' --description-file "$body" [--draft] --yes` |
| Update | `gh pr edit <n> --title '<title>' --body-file "$body" [--base <base>]` | `glab mr update <n> --title '<title>' --description-file "$body" [--target-branch <base>] --yes` |
| Draft ↔ ready | `gh pr ready <n>` / `gh pr ready <n> --undo` | `glab mr update <n> --ready` / `--draft` |

Run them from `<repo>` (`cd <repo> &&`) so the CLI picks the right project from the remote. When the remote isn't `origin`, add `--repo <host>/<project>` (gh) or `-R <web_url>` (glab).

- **Screenshots**: on GitLab, attach each file with `--attach <path>` on `glab mr create` (needs a recent glab; if the flag is unknown, skip it). The GitHub CLI can't upload images: list the files in the report so the user can drag them into the PR
- Add reviewers, assignees or labels only when the user names them (`--reviewer`, `--assignee`, `--label` on both CLIs)
- Never merge, approve, enable auto-merge, close, or delete branches

If the command fails (permissions, a PR already open, validation), show the error and stop. Remove the temporary file when done.

## 9. Report

Keep it short:

- the PR URL, `head` → `base`, and ready or draft
- for a stacked PR, which PR must merge first
- what the user still has to do: screenshots to drag in, an ambiguous base you chose, checks you couldn't run
- the full title and description only if the user didn't already see them in step 7

## Setup

What the user needs once per machine, to tell them when step 2 finds a CLI missing:

- **GitHub**: `brew install gh`, then `gh auth login` (GitHub Enterprise: `gh auth login --hostname <host>`)
- **GitLab**: `brew install glab`, then `glab auth login` (self-hosted: `glab auth login --hostname <host>`, with a personal access token that has the `api` scope)

On other systems, see https://cli.github.com and https://gitlab.com/gitlab-org/cli.
