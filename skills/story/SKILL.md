---
name: story
description: Take a spec issue made with /to-spec (and its /to-tickets tickets), or a small fix described in words, all the way to reviewed pull requests - e2e and dev subagents working in parallel from the spec, a fresh security review, screenshots for each acceptance criterion, then commit and PR, one PR per group of related tickets. Run by the user as /story. Not for writing the spec itself (that is /to-spec), reviewing someone else's PR, or merging.
argument-hint: "[#issue | issue URL | small fix description] [#more-issues]"
disable-model-invocation: true
---

# Story

The user hands over a piece of work and wants it back as pull requests a reviewer can trust: built test-first, checked end to end against the spec, probed for security holes by someone who didn't write the code, and shown working in screenshots. You run the session. You hold the spec and talk to the user; each role goes to a subagent with exactly what it needs, because a subagent knows only its prompt and what's on disk, and can't ask the user anything.

Reply to the user in their language. Write the spec files, commits and PRs in English unless the repo's recent issues use another language.

| Reference | Read at |
| --- | --- |
| `references/spec.md`: the spec addendum, and the short spec for small fixes | step 2 |
| `references/roles/e2e.md`, `references/roles/dev.md`: briefs for the build | step 4 |
| `references/roles/security.md` | step 5 |
| `references/roles/evidence.md` | step 6 |

## 1. Check the repo

Work in the current repo only.

```bash
git status --short
git branch --show-current
```

**Resuming**: when `.story/` already has a folder for this issue or fix, an earlier run stopped partway. Read its `spec.md` and `progress.md` and continue from the step after the last one recorded, skipping step 2.

- Uncommitted changes on the branch `progress.md` names are the work in progress, so the clean-tree stop below doesn't apply. On any other branch, ask before switching
- The earlier subagents are gone. Dispatch new ones with the same briefs, and tell them to read what is already there before writing
- If every group already has a PR, there is nothing left: report the PRs and stop

Stop and tell the user when:

- it isn't a git repo, or a merge or rebase is in progress
- on a fresh start, the tree has uncommitted changes: `commit` stages everything at the end, so they would land in the PR. Ask whether to commit or stash them first
- the input is an issue and `docs/agents/issue-tracker.md` is missing: ask the user to run `/setup-matt-pocock-skills` once

Then:

- Find the exact commands for unit, integration and e2e tests and for starting the app: `AGENTS.md` or `CLAUDE.md` first, then the package scripts. Subagents get them verbatim. Ask if one is missing
- Add `.story/` to `.git/info/exclude` so working files are never committed. Add Playwright output (`test-results/`, `playwright-report/`, `.playwright-cli/`) too when `.gitignore` doesn't already cover it

## 2. Get the spec

The input decides the path:

| Input | Path |
| --- | --- |
| An issue written by `/to-spec`, with or without `/to-tickets` tickets | fetch it |
| A small fix: one behavior in one area, described in words | write the short spec from `references/spec.md` and confirm it, seam included |
| A story or task list with no spec yet | stop. Ask the user to run `/grill-me` if it's unclear, then `/to-spec`, plus `/to-tickets` when it spans several areas, and to run `/story #<issue>` again |

`/grill-me`, `/to-spec`, `/to-tickets` and `/setup-matt-pocock-skills` are reserved for the user to run. Never try to run them or redo their work here; point the user to them.

**Fetch** from where `docs/agents/issue-tracker.md` says issues live:

- GitHub: `gh issue view <n> --comments`. A spec's tickets are its sub-issues: `gh api repos/{owner}/{repo}/issues/<n>/sub_issues`
- GitLab: `glab issue view <n> --comments`
- Local: the files under `.scratch/<feature>/`

If you can't find the tickets, ask for their numbers.

**Then, with `references/spec.md`:**

1. Draft the addendum: Given/When/Then acceptance criteria, the accessible names e2e will select by, and the attack surface. Derive it from the spec's user stories and the tickets' acceptance criteria; mark anything you had to assume rather than inventing requirements
2. For tickets, group them into PRs: one PR per group of tickets that change the same area (all the filter tickets together, say). A group never comes before a group it's blocked by
3. Ask once for approval of the addendum and the groups, showing the seams `/to-spec` recorded so the user sees what each agent will test against. Revise until approved
4. Save the spec, its tickets and the approved addendum to `.story/<slug>/spec.md`, where `<slug>` is `<issue>-<short-name>` (`123-invoice-filters`). Branch names contain `/`, so don't use them as folder names
5. Start `.story/<slug>/progress.md` and update it after every step from here on: one line per group with its branch, the last step finished, and the PR URL once there is one. A long run can be cut off, and this is what lets the next `/story` on the same issue pick up instead of starting over

## 3. Size it

- **Small** (short spec): no E2E or Dev agent. Branch as in step 4, build it yourself with `tdd`, then steps 5 to 8
- **Medium** (one spec, no tickets, or a single group): steps 4 to 8 once
- **Large** (several groups): steps 4 to 7 for each group in order, then step 8

## 4. Branch and build

Branch first; `commit` never creates a branch. Pull the base and branch from it: the default branch or `dev` when you're on one, the previous group's branch when this group is blocked by it, otherwise ask which base to use.

```bash
git switch -c <type>/<issue>-<short-name> <base>   # type: feat or fix; a group uses its first ticket's number
```

The issue number in the branch name lets `pull-request` add `Closes #<n>`.

Dispatch both subagents in one message (Claude Code: the Agent tool), each with its brief filled in:

- **E2E agent** (`references/roles/e2e.md`): writes e2e tests from the spec only, inside the Playwright test directory from `playwright.config.*`. If the project has no Playwright setup, ask the user before adding it: it's a new dependency
- **Dev agent** (`references/roles/dev.md`): builds it with `tdd`, unit and integration tests at the approved seams, and owns every file outside the e2e directory

When both have reported, run the full suite yourself: unit, integration and e2e.

- Failures go back to the same Dev agent with the failing output, continued rather than restarted so it keeps its context (Claude Code: SendMessage)
- A test that contradicts the spec goes back to the agent that wrote it. If the spec doesn't settle who is right, ask the user
- After 3 rounds that still fail, stop and show the user what is failing

Without a subagent tool, play the roles yourself in order, E2E then Dev, under the same rules: write the e2e tests from the spec before writing the code, and keep each role to its own files.

## 5. Security and review

Nothing is committed until step 7, and a plain diff leaves out files that are new. Mark them first, so both reviews below see the whole change (`.story/` is excluded and stays out):

```bash
git add -N .
git diff --stat <base>   # every new file should be listed
```

Dispatch a fresh Security agent with `references/roles/security.md`. Fresh matters: a reviewer that watched the build inherits its blind spots. It reviews `git diff <base>`, starting from the attack surface, using `security-review` (or `best-practices` where that doesn't exist), and writes a failing test for each real finding.

- Send findings to the Dev agent (fix them yourself on a small one) and rerun the suite
- A finding that needs a business decision (who may cancel a paid invoice?) goes to the user

Then run `git add -N .` again, for the tests and fixes just added, review the current changes yourself with `code-review` (or `best-practices`), and apply the fixes that keep the suite green.

## 6. Evidence

Skip this when nothing in the UI changed. Otherwise dispatch the Evidence agent with `references/roles/evidence.md`. It starts the app, takes one screenshot per UI acceptance criterion into `.story/<slug>/screenshots/`, and writes `.story/<slug>/evidence.md`: criterion → test → result → screenshot.

Look at every screenshot before it goes into a PR, and drop any that shows secrets or personal data.

## 7. Ship

1. `verification-before-completion`: run the full suite fresh and read the output before claiming anything passes
2. `commit`
3. `pull-request`. Tell it the issues to close (one `Closes #<n>` per ticket in the group), give it the evidence table for Testing, and list the screenshot paths to attach. For a group blocked by the previous one, the base is that group's branch

## 8. Report

Keep it short, one block per PR:

- URL, head → base, and the issues it closes
- acceptance criteria covered by tests, and any that aren't
- what is still open: findings left for the user, evidence skipped, checks that couldn't run

Leave `.story/` in place unless the user asks to remove it.
