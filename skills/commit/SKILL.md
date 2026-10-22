---
name: commit
description: Stage every change in the current git repo, write a detailed Conventional Commits message from the actual diff, sized to the change (small, medium or large), then ask whether to commit only or commit and push. Use when the user asks, in any language, to commit, commit and push, or save their work to git, or runs /commit. Not for amending, rebasing, squashing, splitting commits, or opening pull requests.
argument-hint: "[push|no-push] [notes for the message]"
---

# Commit

The user finishes a working session and wants all of it in one commit, with a message that tells a future reader exactly what changed and why, without writing it themselves. The message is the permanent record, so build it from the diff, not from memory of the conversation; the conversation supplies the why.

Reply to the user in their language; write the commit message in English (step 3).

## 1. Check the repo state

```bash
git status
git branch --show-current
git log -n 20 --format='%s'
```

Stop and tell the user, without trying to fix it, when:

- it's not a git repo
- the working tree is clean: there is nothing to commit
- a merge, rebase, cherry-pick or revert is in progress, or there are unmerged paths (`git status` says so)
- HEAD is detached (`git branch --show-current` prints nothing)

Commit on the current branch, whatever it is. Never create or switch branches. In a new repo `git log` fails because there are no commits yet; carry on, this is the first commit.

## 2. Stage everything, safely

Everything goes in: new files, modifications and deletions, except what must never be committed:

- **Secrets**: `.env*` (except templates like `.env.example`), `*.pem`, `*.key`, `*.p12`, `id_rsa*`, credential or service-account JSON, `*.tfstate`
- **Generated or local files** that `.gitignore` misses: `node_modules/`, `dist/`, `build/`, `.next/`, `__pycache__/`, `.venv/`, `.DS_Store`, IDE folders, logs, local database files and dumps
- **Large binaries**: over 5 MB

Before staging, ask about anything on the list that `git status` from step 1 already shows, especially an untracked generated folder such as `?? node_modules/`, which would stage thousands of files. `git status` folds each new folder into one line, so stage and then check every file:

```bash
git add -A
git diff --cached --stat
git diff --cached
```

1. Check every path in the stat against the list. It lists each file inside new folders and shows binary sizes (`Bin 0 -> 6000000 bytes`).
2. Read the full diff. If it is very large, go through it file by file or area by area from the stat; lockfiles and generated files only need their names. Watch for secrets inside files too: private key blocks, API keys, tokens, passwords, connection strings with credentials.

Unstage anything that matches with `git reset -q -- <path>` and ask the user per file: leave it out, add it to `.gitignore`, or include it anyway. Never repeat a secret's value in your reply.

## 3. Write the message

Read `references/templates.md` before writing. It holds the one skeleton every commit uses, how to pick small, medium or large, and examples of each.

### Convention

Every repo uses Conventional Commits, so messages look the same across all projects. The rules below already pass commitlint's `config-conventional`.

- If the repo enforces its own rules (a commitlint config such as `commitlint.config.*`, `.commitlintrc*` or a `commitlint` key in `package.json`, or commit rules in `CONTRIBUTING.md`, `AGENTS.md` or `CLAUDE.md`), they win wherever they differ
- Read recent history only to reuse the scope names already in use, so the same module always gets the same scope
- Always write in English

### Subject line

- Imperative mood, completing "If applied, this commit will …": `Add`, `Fix`, `Remove`, never `Added` or `Adds`
- 50 characters or fewer when possible, 72 at most, no trailing period
- Names the overall outcome, not a list of files
- Format `type(scope): summary`. The summary starts with a lower-case verb; acronyms and names keep their case (`add CSV export`)
  - `type`: `feat` new behavior, `fix` bug fix, `perf`, `refactor` (no behavior change), `docs`, `test`, `build` (build system, dependencies), `ci`, `style` (formatting only), `chore` (anything else), `revert`. A commit that mixes kinds takes the first that applies in this order, so a feature with its tests and docs is `feat`
  - `scope`: the main module or area touched, in lower-case kebab-case (`order-detail`); leave it out when the change spans many areas

### Body

The body must cover everything in the commit, at the depth its size calls for (see the templates). Separate it from the subject with one blank line and wrap lines at 72 characters.

- **Why first**: 1–3 sentences on the problem or goal and the approach taken. Take this from the conversation when you have it; don't invent motivation that neither the diff nor the conversation supports.
- **Then what**: `- ` bullets for every meaningful change: one flat list for medium, grouped under `Area:` labels for large. Each says what changed and, when it isn't obvious, why. Name modules, functions, endpoints, commands and config keys, not line-level edits.
- **Always call out**: behavior changes users will notice; new or changed env vars, config or migrations and how to apply them; dependencies added, removed or upgraded (with versions); removed features; known limitations or follow-up work left undone. Put setup steps and limits in the notes paragraph after the bullets.
- **Keep out**: diff stats, file-by-file trivia, phrases like "this commit", conversation chatter, tool or agent names, emoji (unless the convention uses them). Lockfile and generated changes get one bullet at most.

### Footer

- Breaking change: add `!` after the type or scope and a `BREAKING CHANGE: <what breaks and how to migrate>` footer
- Issue references (`Refs: #123`, `Closes #123`) only when the number appears in the branch name, the conversation or the user's notes
- Other trailers, such as `Co-Authored-By`, only when the user's or the agent's own instructions require them

## 4. Ask: commit only, or commit and push

Skip the question when the request already decides it (`/commit push`, `/commit no-push`, "commit and push", "don't push").

Otherwise ask one question, with AskUserQuestion if available (if not, show the message, ask in chat and wait), showing the full message as the preview of each option:

- **Commit and push**: say where it goes, e.g. "Push `main` to `origin/main`". Leave this option out when the repo has no remote (`git remote` prints nothing) and say why.
- **Commit only**

If the user answers with changes to the message, revise it and ask again. If they cancel, leave the changes staged and tell them `git reset -q` unstages them.

## 5. Commit

Pass the message through a quoted heredoc so `$`, backticks and line breaks are kept exactly:

```bash
git commit -F - <<'EOF'
<message>
EOF
```

- Never use `--no-verify` or `--amend`, change git config, or turn off commit signing
- If a hook auto-fixed files (formatter, linter), run `git add -A` and commit again with the same message, once
- If a hook fails with real errors (tests, type errors, lint it can't fix), or the commit fails for any other reason (signing, missing `user.name`), stop and show the error. Fix code only if the user asks; the changes stay staged

## 6. Push (if chosen)

```bash
git rev-parse --abbrev-ref --symbolic-full-name '@{u}' # fails when there is no upstream
git push                                               # upstream exists
git push -u origin <branch>                            # no upstream yet
```

- No upstream: push to `origin`, or ask which remote when there are several and none is `origin`
- Rejected because the remote has new commits: never force-push. Tell the user, and offer `git pull --rebase` followed by `git push`; run it only after they agree. If the rebase hits conflicts, stop and hand back, mentioning `git rebase --abort`
- Rejected for any other reason (authentication, protected branch, server hook): show the error and stop. The commit stays local

## 7. Report

Keep it short:

- short hash, branch and subject line
- pushed to `<remote>/<branch>`, or committed locally only
- files you excluded, hook auto-fixes, and anything else the user should know
- the full message, only if the user didn't already see it in step 4
