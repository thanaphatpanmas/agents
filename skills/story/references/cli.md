# Agent CLIs

Only with `cli`. Each role runs as a headless session of one of the user's agent CLIs instead of a subagent, under that CLI's own login, model and effort, so the work is spread over more than one account. The briefs, who owns which files and every rule in `SKILL.md` stay the same; only how a role is dispatched and continued changes.

## Who gets what

| Role | CLI | Why |
| --- | --- | --- |
| Dev, E2E, Evidence | `claude` | It runs commands on the machine itself, so it can start the app, reach the test database and open a browser |
| Security | `codex` | A different model from the one that built the change, and reviewing a diff needs nothing its sandbox blocks |

Codex runs every command in a sandbox that can write inside the repo but can't open a port, reach a local server or database, or launch a browser. That rules it out for Dev, E2E and Evidence.

When a CLI is left out, because the user asked for only one or the check below failed:

- no `codex`: Security goes to `claude`, in a session of its own
- no `claude`: Dev, E2E and Evidence stay subagents

## Check the CLIs

At step 1:

```bash
env -i HOME="$HOME" USER="$USER" PATH="$PATH" TERM=dumb claude auth status   # "loggedIn": true
env -i HOME="$HOME" USER="$USER" PATH="$PATH" TERM=dumb codex login status   # Logged in ...
```

When `~/.claude-cli` exists, it holds a second `claude` login (Setup): add `CLAUDE_CONFIG_DIR="$HOME/.claude-cli"` to the `env -i` list here and in every `claude` command below. Without it, `claude` uses its usual login. Tell the user the `email` the check shows, so they see which account the `claude` roles spend.

When a CLI is missing or logged out, ask whether to go on without it, saying where its roles go instead. Logging in is the user's to do: `claude auth login`, `codex login`.

## Dispatch

Run every command from the repo root. Write the filled brief to `.story/<slug>/cli/<role>.in.md`, so line breaks, backticks and `$` survive the shell, and end it with:

> This run is headless. A command that is refused, or that fails because it needs network access you don't have, stays that way: don't retry it or find another way to run it. Finish the rest and say in your reply which commands those were.

```bash
dir=.story/<slug>/cli
id=$(uuidgen | tr 'A-Z' 'a-z')   # a new one for each claude session

# claude: Dev, E2E, Evidence
env -i HOME="$HOME" USER="$USER" PATH="$PATH" TERM=dumb \
  claude -p --session-id "$id" --permission-mode acceptEdits --permission-prompts none \
  --allowedTools "Bash(<command> *)" "Bash(<command> *)" \
  < "$dir/<role>.in.md" > "$dir/<role>.out.md" 2> "$dir/<role>.log"

# codex: Security
env -i HOME="$HOME" USER="$USER" PATH="$PATH" TERM=dumb \
  codex exec -s workspace-write -o "$dir/security.out.md" - \
  < "$dir/security.in.md" > "$dir/security.log" 2>&1
```

- **Clean environment**: `env -i` keeps the main session's own variables (its session, its effort) away from the CLI, so it runs under its own login and settings. Add by name any variable the project's commands need. Never add `--model`, `--effort` or `-m`: the user picks those in each CLI
- **Permissions**: nobody can answer a prompt in a headless run. `acceptEdits` lets `claude` edit files in the repo, and each `Bash(<command> *)` rule allows one command the role's brief names: unit, integration, type-check, lint, e2e, starting the app. E2E and Evidence also get `"Bash(playwright-cli *)"`. Anything else that would prompt is refused. Never pass a flag that skips permissions or the sandbox
- **Waiting**: a role can take many minutes. Run the command in the background and wait for it to exit (Claude Code: Bash with `run_in_background`), E2E and Dev at the same time
- **Reply**: `<role>.out.md` holds the reply in the format the brief asks for. On a non-zero exit or an empty file, read `<role>.log`. A CLI that is out of quota or logged out is the user's to fix: stop and tell them
- **Record**: write each role's CLI into `progress.md`, with the session id of every `claude` session

## Continue

To send failing tests or findings back to the same agent, write the message to `<role>.in.md` and run the same `claude` command, flags included, with `--resume "$id"` in place of `--session-id "$id"`.

- A later `/story` run on the same issue continues the sessions recorded in `progress.md` the same way. Unlike subagents, they are still there
- Security starts fresh every time. When `claude` plays it, give it a new session id, never Dev's

## What Codex can't run

Tests that need the app, a database or a browser fail inside the sandbox. Codex still writes them and reports them as not run. Run those yourself, and check that each fails for the reason its finding gives before sending the findings to Dev.

## Setup

Once per machine, and only when the `claude` roles should run on a different account from the main session. The user runs it:

```bash
CLAUDE_CONFIG_DIR=~/.claude-cli claude auth login
ln -s ~/.claude/skills ~/.claude-cli/skills
ln -s ~/.claude/CLAUDE.md ~/.claude-cli/CLAUDE.md
```

A separate config folder starts without the user's skills and global instructions; the two links bring them back. Model and effort for these roles are then set in that folder, by starting `claude` once with the same variable.
