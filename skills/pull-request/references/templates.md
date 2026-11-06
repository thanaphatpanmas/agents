# Pull Request Templates

Every PR uses the same skeleton. Size only decides which parts appear, so a typo fix and a new module still read the same way. When the repo has its own PR/MR template, its sections replace these; the rules for what goes in each still apply.

## Title

Conventional Commits, the same rules as a commit subject. Many teams squash-merge, which turns the PR title into the commit on the base branch.

- `type(scope): summary`, imperative, lower-case verb after the colon, 72 characters at most, no trailing period
- `type` by the first that applies: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `style`, `chore`, `revert`. A feature with its tests is `feat`
- `scope`: the main module, reusing scopes from `git log`; leave it out when the branch spans many areas
- A breaking change gets `!` after the type or scope
- A one-commit branch can reuse that commit's subject

## Description

Covers the whole branch at the depth its size calls for.

- **Why first**: the problem or goal and the approach, from the conversation when you have it. Don't invent motivation
- **Changes**: what changed, grouped by area for large branches. Name modules, endpoints, commands and config keys, not line edits
- **Testing**: only what was really run and what it showed, plus steps a reviewer can follow. Never claim a check passed when you don't know; say what wasn't tested
- **Always call out**: behavior users will notice, migrations, new env vars or config and how to apply them, dependency changes, risks, follow-ups left undone, and merge order for a stacked PR
- **Keep out**: diff stats, file-by-file trivia, conversation chatter, tool or agent names, secrets and personal data from logs or screenshots
- **Issue links** (`Closes #123`) only when the number appears in the branch name, commits, conversation or user's notes
- **Checkboxes** in a repo template: tick only what you verified
- **Attribution**: add any lines your own instructions require (for example a "Generated with" footer) as the last line

## Skeleton

```text
type(scope): summary                       title, all sizes

## Summary                                 all sizes: why, then the approach (1–3 sentences)
Depends on #12, which must merge first.    stacked PRs only

## Changes                                 medium: one flat list; large: one ### group per area
- change

## Testing                                 all sizes: what was run and what it showed, then reviewer steps
- [x] `npm test`: 142 passed
- Not tested: ...

## Screenshots                             UI changes only
![Settings page after saving](./<path>)    GitHub: one per image, same path as its `--attach` (cli.md); GitLab: none, glab appends them

## Notes                                   only when needed: migrations, config, risks, follow-ups

BREAKING CHANGE: ...                       only with `!` in the title: what breaks, how to migrate
Closes #123                                only when the number is known
```

## Pick the size

Decide by scope, not line count. When torn between two sizes, pick the larger.

| Size | When | Description |
| --- | --- | --- |
| small | one change in one area: typo, one-line fix, version bump | Summary of 1–2 sentences + Testing |
| medium | one feature or fix across several files | Summary + 2–8 flat Changes bullets + Testing (+ Screenshots, Notes) |
| large | several areas or layers, a new module, a migration or a breaking change | Summary + Changes grouped by area + Testing + Notes |

## Small

```text
fix(cart): round line totals to 2 decimal places

## Summary
Line totals showed values like 19.999999 for some discounts because
they were rounded after summing instead of per line.

## Testing
- [x] `npm test -- cart`: passed, including a new case for 3 × 6.6667
```

## Medium

```text
fix(staff-evaluation): disable round-locked actions with a reason

## Summary
Once an evaluation round started, some add/edit/delete/save buttons
disappeared, so users could not tell why the action was missing. They
now stay visible but disabled, and hovering says whether the round is
in progress or already closed.

## Changes
- Add `useEvaluationFormsLockedReason()` returning an in-progress or
  closed reason for locked Part 1/2/3 forms
- Form detail page: Edit/Delete disabled with a tooltip instead of hidden
- Committee page: Save disabled with a tooltip once the round closes
- `DataTable`: show `disabledTooltip` on disabled overflow-menu items,
  only when one is given, so other tables are unchanged
- th/en strings for both round states

## Testing
- [x] New e2e spec `evaluation-round-lock`: 2 passed locally, covering an
  active round and a closed one (browser clock moved past the end date)
- [x] Frontend type-check clean
- Not tested: mobile layouts

## Screenshots
![Edit and Delete disabled with a tooltip while the round runs](./screenshots/form-detail-locked.png)
![Save disabled with a tooltip after the round closes](./screenshots/committee-closed.png)

## Notes
The server still accepts participant/committee changes after a round
closes; only the UI blocks them. Follow-up needed.
```

## Large (stacked)

```text
feat(auth)!: replace session cookies with JWT access and refresh tokens

## Summary
The mobile app can't share cookie sessions with the web app, and
server-side sessions made scaling past one instance hard. Move both
clients to short-lived JWT access tokens with rotating refresh tokens.

Depends on #41 (refresh_tokens table), which must merge first; this PR
targets its branch `feat/refresh-token-table`.

## Changes
### API
- Add `POST /auth/login`, `/auth/refresh` and `/auth/logout`
- 15-minute access tokens; 30-day refresh tokens that rotate on every
  use and detect reuse
- Replace the session middleware with JWT verification

### Web
- Keep the access token in memory and refresh it before expiry
- Redirect to login when a refresh fails

### Tests
- Integration tests for login, rotation, reuse and logout

## Testing
- [x] `npm run test:integration`: 38 passed
- [x] Logged in on web and mobile against a local API, waited past
  token expiry, confirmed silent refresh
- Reviewer: run `npm run db:migrate`, then log in and call
  `/auth/refresh` twice with the same token; the second call must 401

## Notes
- Set `JWT_SECRET` and `REFRESH_TOKEN_TTL_DAYS` (default 30) before deploying
- Every user is logged out once after the deploy

BREAKING CHANGE: protected endpoints now require an
`Authorization: Bearer <token>` header; cookie sessions are rejected.
```

## Not like this

| Wrong | Why | Right |
| --- | --- | --- |
| title `Fix/staff` or `update` | the branch name says nothing to a reviewer | `fix(staff-evaluation): disable round-locked actions with a reason` |
| a description that repeats only the last commit | the PR is the whole branch | read every commit and the full diff against the base |
| `- [x] All tests pass` when none were run | a false claim a reviewer will trust | list what was run, and say what wasn't |
| `Changes: updated 12 files` | stats, not meaning | name what changed and why |
| a stacked PR with no "Depends on" | the reviewer merges it first and breaks the base | link the parent PR and state the order |
