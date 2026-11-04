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

- **Screenshots**: on GitLab, attach each file with `--attach <path>` on `glab mr create` (needs a recent glab; if the flag is unknown, skip it). The GitHub CLI can't upload images: list the files in the report so the user can drag them into the PR
- **Reviewers, assignees, labels**: only when the user names them (`--reviewer`, `--assignee`, `--label` on both CLIs)

## Setup

What the user needs once per machine, when `pr_context.py` reports the CLI missing or not logged in:

- **GitHub**: `brew install gh`, then `gh auth login` (GitHub Enterprise: `gh auth login --hostname <host>`)
- **GitLab**: `brew install glab`, then `glab auth login` (self-hosted: `glab auth login --hostname <host>`, signing in with a personal access token that has the `api` and `write_repository` scopes)

On other systems, see https://cli.github.com and https://gitlab.com/gitlab-org/cli. Tell the user to paste tokens at the CLI prompt, never on the command line or in chat.
