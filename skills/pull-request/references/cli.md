# gh and glab Commands

GitHub uses `gh`, GitLab (gitlab.com or self-hosted) uses `glab`. Run every command from the repo (`cd <repo> &&`) so the CLI picks the project from the remote. When the remote isn't `origin`, add `--repo <host>/<project>` (gh) or `-R <web_url>` (glab).

## Find PRs

Open PRs from a branch, to update instead of opening a duplicate, or to find a stacked base's own PR:

```bash
gh pr list --head <branch> --state open --json number,url,title,baseRefName,isDraft
glab mr list --source-branch <branch> --output json          # open only by default
```

## Recent merged PRs

To match the repo's language, section names and title style, and to see where branches usually merge:

```bash
gh pr list --state merged --limit 10 --json title,body,headRefName,baseRefName
glab mr list --merged --per-page 10 --output json            # fields: title, description, source_branch, target_branch
```

## Create, update, draft

Write the description to a temporary file so line breaks, backticks and `$` survive the shell, and quote the title in single quotes (escape any `'` inside it as `'\''`). Remove the file when done.

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

- **Screenshots**: add `--attach ./<path>` per file to the create or update command. Commands run from the repo, so `<path>` is relative to it. If the CLI rejects the flag (`gh` before 2.99, an older `glab`), leave it off and list the files in the report so the user can drag them into the PR
  - **GitHub**: also place each image in the description as `![alt](./<path>)`, the same path as its `--attach`; `gh` replaces it with the uploaded URL. If some uploads fail, `gh` still creates or updates the PR and exits non-zero: don't run it again, and list the failed files in the report
  - **GitLab**: `glab` appends each file to the description itself (the flag is experimental there), so don't reference them in the body
- **Reviewers, assignees, labels**: only when the user names them (`--reviewer`, `--assignee`, `--label` on both CLIs)

## Delete branch after merge

Only with `delete-branch`. Nothing is deleted now; the host removes the source branch when the PR merges.

- **GitLab create**: add `--remove-source-branch=true` to `glab mr create`
- **GitLab update**: `glab mr update <n> --remove-source-branch` toggles the setting, so first check `glab mr view <n> --output json` and run it only when `force_remove_source_branch` is not already `true`
- **GitHub**: there is no per-PR setting. Check `gh repo view --json deleteBranchOnMerge`. If it is `false`, tell the user that only the repo-wide setting can do this (`gh repo edit --delete-branch-on-merge`, or Settings → General → "Automatically delete head branches"), and that it affects every PR. Don't change it yourself

## Setup

What the user needs once per machine, when `pr_context.py` reports the CLI missing or not logged in:

- **GitHub**: `brew install gh`, then `gh auth login` (GitHub Enterprise: `gh auth login --hostname <host>`)
- **GitLab**: `brew install glab`, then `glab auth login` (self-hosted: `glab auth login --hostname <host>`, signing in with a personal access token that has the `api` and `write_repository` scopes)

On other systems, see https://cli.github.com and https://gitlab.com/gitlab-org/cli. Tell the user to paste tokens at the CLI prompt, never on the command line or in chat.
