---
name: story
description: >-
  Take an idea, task list, existing spec or small change to reviewed pull requests.
  Choose a proportional workflow before planning: handle small low-risk features
  directly, delegate independent work when useful, and require security review for
  sensitive changes. Coordinate missing planning, focused verification and reusable
  UI evidence. Resume without repeating approved work. Run by the user as /story.
  Not for reviewing someone else's PR or merging.
argument-hint: "[idea | task list | #issue | issue URL | spec path | small change] [#more-issues] [cli]"
disable-model-invocation: true
---

# Story

The user hands over work and wants it back as pull requests a reviewer can trust. Match planning, tests and delegation to the behavior and risk of the change. You hold the spec and user decisions, own final verification and coordinate any delegated roles. A small feature should not inherit the full ceremony of a cross-module change.

Own the transitions between planning and delivery. Invoke the installed planning skills in the main session when needed; the user should not have to run each command separately. Carry their answers and approvals forward. Keep business decisions and required confirmations with the user, and never treat silence as approval.

`cli` in the request (or asking in words to hand the work to agent CLIs) sends the roles to the user's `claude` and `codex` CLIs instead of subagents: follow `references/cli.md` wherever a step dispatches or continues an agent.

Reply to the user in their language. Write the spec files, commits and PRs in English unless the repo's recent issues use another language.

| Reference | Read at |
| --- | --- |
| `references/planning.md`: planning skills, approvals, checkpoints and publication recovery | steps 1 and 2 |
| `references/verification.md`: check ownership, shared execution slot, evidence reuse and timing | steps 1, 3 and before running checks |
| `references/spec.md`: the spec addendum, and the short spec for small changes | step 2 |
| `references/roles/e2e.md`, `references/roles/dev.md`: briefs for the build | step 4 |
| `references/roles/security.md` | step 5 |
| `references/roles/evidence.md` | step 6 |
| `references/cli.md`: roles on the `claude` and `codex` CLIs | steps 1 and 4 to 6, with `cli` |

## 1. Check the repo

Work in the current repo only.

```bash
git status --short
git branch --show-current
```

**Resuming**: look for an existing `.story/` folder matching the issue, source path or request. Read its `progress.md` and `spec.md` if present. Follow `references/planning.md`: resume the first unfinished step, including planning; skip step 2 only when its approved output is still current. If several runs could match, ask which one to continue.

- Recorded changes from this run on the branch `progress.md` names are work in progress, including setup files; the clean-tree stop below doesn't apply to them. Ask about unrelated changes and before switching to a different recorded branch
- Restore only the roles still needed by the current route. Continue a live agent when available; otherwise dispatch a replacement with the recorded work. CLI sessions recorded in `progress.md` can be continued (`references/cli.md`)
- If every group already has a PR and the request adds no new scope, report the PRs and stop

Stop and tell the user when:

- it isn't a git repo, or a merge or rebase is in progress
- on a fresh start, the tree has uncommitted changes: `commit` stages everything at the end, so they would land in the PR. Ask whether to commit or stash them first

Then:

- Find the commands and mandatory checks in `AGENTS.md` or `CLAUDE.md`, then package scripts. Discover commands for the work actually needed; don't block a non-UI change on a missing browser command. Give any agents the exact scoped commands from step 3
- Bound each test command: test runs, the app, its database and the agents all share one machine. Cap the runner's workers at 2 (Playwright `--workers=2`, Jest or Vitest `--maxWorkers=2`), and give Playwright `--reporter=line` to avoid an interactive HTML reporter. Pass flags through package scripts correctly or call the runner directly. Select relevant Playwright projects explicitly; exclude separate UAT/visual runs only when neither the verification plan nor repo/user requirements call for them, and report exclusions. Every step and brief uses these bounded commands and the shared execution slot
- Add `.story/` to `.git/info/exclude` so working files are never committed. Add Playwright output (`test-results/`, `playwright-report/`, `.playwright-cli/`) too when `.gitignore` doesn't already cover it
- Before planning, create `.story/<slug>/progress.md` using `references/planning.md`. Use `<issue>-<short-name>` when an issue is known, otherwise `<short-name>`; keep that folder when an issue is created later. Record the current branch, request and next step before calling any planning skill

**Choose the route before writing a spec.** Inspect the requested behavior and affected callers first; read a supplied issue/spec as needed. Classify by scope and risk, not whether the user calls it a feature, supplies an issue or has a long spec:

- **Small, low risk**: one localized behavior using established components and contracts, without changing authorization, tenant isolation, destructive behavior, money calculations, schema/data migrations or a trust boundary. Examples: add an informational dialog using the existing component, or a local display option. Use a short spec; the main session builds, reviews, verifies and captures UI evidence. No role agents by default
- **Standard**: broader scope, uncertain impact, or any sensitive change above. Use the planning steps needed for that scope. Delegate only separable work that avoids more overhead than it creates; a single implementation owner is the default. A one-button delete or permissions dialog is not low risk
- **Multiple groups**: split genuinely separate deliverables and apply the appropriate route to each group, steps 4 to 7 in dependency order

Record the route, risk and reason in `progress.md` and tell the user briefly; choosing a route is not an extra approval gate. Reclassify if exploration or a requirement change expands the impact. With `cli`, check only CLIs for roles actually being dispatched, immediately before they are needed.

## 2. Get the spec

Read `references/planning.md`. The input decides which work is missing:

| Input | Path |
| --- | --- |
| An existing spec issue or local spec, with or without tickets | fetch/read it, reuse it and its recorded approvals; resolve only missing decisions |
| A small low-risk feature or fix | reuse the supplied spec or write and confirm the short spec from `references/spec.md`, seam included; skip tracker setup and ticket publication unless needed or requested |
| An idea or task list without a usable spec | coordinate setup if needed, `grill-me` when unclear, then `to-spec`; use `to-tickets` when the work spans several areas |

Call the planning skills yourself under their own instructions and the coordination rules in `references/planning.md`. Do not rewrite their procedures inside Story or restart planning that is already complete.

**Fetch** from the supplied local path, or from where `docs/agents/issue-tracker.md` says issues live (run setup first if a tracker is needed and not configured):

- GitHub/GitLab: fetch the named issue and related tickets through the configured CLI/API. Page comments and ticket lists with a capped page size (at most 100), process one page at a time and follow pagination until the needed context is found; do not assume the first page is complete
- Local: the files under `.scratch/<feature>/`

If the request or spec references tickets you can't find, ask for their numbers or paths. If tickets have not been created yet, follow the planning rules instead.

**Then, with `references/spec.md`:**

1. Draft the addendum: Given/When/Then acceptance criteria, the accessible names e2e will select by, and the attack surface. Derive it from the spec's user stories and the tickets' acceptance criteria; mark anything you had to assume rather than inventing requirements
2. For tickets, group them into PRs: one PR per group of tickets that change the same area (all the filter tickets together, say). A group never comes before a group it's blocked by
3. Show the addendum and groups for approval. Reuse approved seams and ticket breakdowns; ask only about additions or changes not already approved. Revise until approved
4. Save the current spec, ticket references and approved addendum to the existing `.story/<slug>/spec.md`. Keep ticket details in their tracker or local files and read them per group rather than copying the whole collection
5. Update `progress.md` with planning approvals and each group's branch, last completed step and PR URL. Update it after every later step too; never dispatch build agents against an unapproved revision

## 3. Plan verification and ownership

Read `references/verification.md`. Record the checks, their scope, owner and why they cover the change, plus the browser states needed as evidence. Honor repo/user-required checks on every route. Prefer the existing test boundary that proves the behavior; do not automatically require unit, integration and e2e coverage of the same behavior.

For new non-trivial behavior and bug fixes, use `tdd` at the approved seam. For trivial copy/style edits, use the relevant existing checks and a visual check rather than inventing tests that mirror the edit. For a dialog, verify opening/closing, keyboard/focus behavior and any changed submit/error path. Add e2e tests for important journeys or browser-only behavior when lower-level tests cannot establish it; preserve existing relevant regression coverage.

## 4. Branch and build

Branch first; `commit` never creates a branch. Pull the base and branch from it: the default branch or `dev` when you're on one, the previous group's branch when this group is blocked by it, otherwise ask which base to use.

```bash
git switch -c <type>/<issue>-<short-name> <base>   # type: feat or fix; a group uses its first ticket's number
```

Use a real issue number when one exists so `pull-request` can add `Closes #<n>`. For a small fix or local spec without tracker issues, use `<type>/<short-name>` and omit issue-closing directives. Carry this run's recorded setup changes into its branch and delivery; if switching or updating the base would overwrite them, stop and resolve that with the user.

For the small route, implement directly in the main session. Otherwise use a Dev agent only when delegation is useful, with `references/roles/dev.md`. Add a separate E2E agent only when there is enough independent browser-test work to justify the handoff. When both are needed, they may write in parallel under these boundaries:

- **E2E agent** (`references/roles/e2e.md`): writes e2e tests from the spec only, inside the Playwright test directory from `playwright.config.*`. If the project has no Playwright setup, ask the user before adding it: it's a new dependency
- **Dev agent** (`references/roles/dev.md`): builds it with `tdd`, unit and integration tests at the approved seams, and owns every file outside the e2e directory

Follow `references/verification.md`: Dev owns the execution slot during implementation; E2E authors tests without starting the app or running them concurrently. When Dev yields the slot, the main session runs the pending browser/integration checks. Do not rerun passing Dev checks merely because of the handoff; inspect their raw output and changed files, and reserve final verification for step 7. Never treat an expected pre-implementation failure as a post-implementation pass.

- Failures go back to the same Dev agent with the failing output, continued rather than restarted so it keeps its context (Claude Code: SendMessage; with `cli`: resume its session)
- A test that contradicts the spec goes back to the agent that wrote it. If the spec doesn't settle who is right, ask the user
- After 3 rounds that still fail, stop and show the user what is failing

Without subagents, implement and verify in the main session under the same test plan. Do not simulate extra roles just to reproduce the handoffs.

## 5. Security and review

Nothing is committed until step 7, and a plain diff leaves out files that are new. Mark them first, so both reviews below see the whole change (`.story/` is excluded and stays out):

```bash
git add -N .
git diff --stat <base>   # every new file should be listed
```

Require a fresh Security agent when the change affects authorization/tenant isolation, destructive actions, money logic, schema/data migrations, a trust boundary (such as uploads, untrusted rendering or external input), or when the user/repo requires it. Use `references/roles/security.md` and grant its execution slot only after other test runs finish. For other changes, the main session performs a focused security check during code review. If an independent reviewer is required but unavailable, report that check as blocked rather than claiming an independent review.

- Send in-scope findings to the implementation owner, then rerun the checks affected by the fix, including the regression test that demonstrated the finding
- A finding that needs a business decision (who may cancel a paid invoice?) goes to the user

Then run `git add -N .` again if files were added and review the final diff and directly affected callers yourself. Use relevant `code-review` or `best-practices` guidance for this scoped review; do not launch a whole-site audit unless required by the task. Fix defects introduced, exposed or made reachable by the change. Record unrelated pre-existing issues briefly for follow-up; don't write reproducer tests, refactor or fix them in this story. A serious existing issue that makes this change unsafe is still a blocker and must be reported.

## 6. Evidence

Screenshots do three jobs: the user sees the finished result, each image shows exactly what changed and where, and once the user confirms them they go into the PR so the reviewer sees what it does. Skip screenshots only when nothing in the UI changed; every UI change gets them, on every route. Criteria a screenshot can't show still get evidence, below.

Capture during the planned browser verification, preferably from the passing test or the same live session. Use `references/roles/evidence.md` for the capture rules, whether the main session or an agent captures it. Every screenshot is annotated: a red ring with a short numbered note on each element that proves the criterion, and a red caption bar reading `<AC id> — <criterion>`. Use the repo's own annotation helper when it has one, adding the caption bar to it if it lacks one; otherwise draw the overlay with `playwright-cli` `eval`. One screenshot may prove several criteria when it clearly does; its caption names each.

Criteria a screenshot can't show (API responses, permissions, stored data, migrations, background jobs, browser storage) need evidence the reviewer can read instead: the passing test that proves each one, plus a short text sample from a real run against test data — a trimmed request and response, a before/after query result, the stored value, or the log line or record a job created. Strip tokens, passwords and personal data. A criterion backed only by reading the code says so; one with neither a test nor a sample is reported as unverified, never as done.

Dispatch an Evidence agent only for missing or invalid evidence substantial enough to justify a separate handoff; give it only those gaps.

Look at every screenshot yourself first: exclude secrets/personal data, and replace stale captures or ones whose ring, note or caption marks the wrong spot. Then show the user the screenshots (Claude Code: `SendUserFile`; otherwise list the paths) together with the evidence table and the text samples, and wait for their confirmation before step 7; recapture or rerun what they ask to change. Never open the PR with evidence the user hasn't confirmed. When later fixes change a visible state, recapture that state and show it again.

## 7. Ship

1. `verification-before-completion`: the main session owns the final verification plan from step 3. Run its commands against the final code, one at a time, and read the actual output before claiming success. A check already run by the main session after the last relevant edit can count; a summary from an agent alone cannot. Run the full suite when required by the repo/user or when shared changes cannot be covered reliably by scoped checks. Follow `references/verification.md` for invalidating results after edits, handling failures and reporting checks not run
2. `commit`
3. `pull-request`. Tell it the real tracker issues to close (one `Closes #<n>` per ticket in the group; local ticket numbers are not tracker issues), give it the evidence table for Testing, the confirmed screenshot paths and text samples, and have it put each piece under its own criterion: a visible `<AC id> — <criterion>` line, then the image (the same text as alt text) or the sample in a code block: `.story/` is excluded from git, so a path left as text is a dead link, and an unreferenced attachment just piles up at the end of the PR. For a group blocked by the previous one, the base is that group's branch

## 8. Report

Keep it short, one block per PR:

- URL, head → base, and the issues it closes
- acceptance criteria covered by tests, and any that aren't
- what is still open: findings left for the user, evidence skipped, checks that couldn't run or were left out
- route chosen and observed elapsed time by phase, including user waits and repeated commands; distinguish estimates or unavailable timings from measured ones

Leave `.story/` in place unless the user asks to remove it.
