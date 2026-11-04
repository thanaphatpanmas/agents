# Commit Message Templates

Every commit uses the same skeleton. Size only decides which parts appear, so a one-line fix and a mega feature still read the same way.

## Convention

Every repo uses Conventional Commits, so messages look the same across all projects. The rules below already pass commitlint's `config-conventional`.

- If the repo enforces its own rules (a commitlint config such as `commitlint.config.*`, `.commitlintrc*` or a `commitlint` key in `package.json`, or commit rules in `CONTRIBUTING.md`, `AGENTS.md` or `CLAUDE.md`), they win wherever they differ
- Read recent history only to reuse the scope names already in use, so the same module always gets the same scope
- Always write in English

## Subject line

- Imperative mood, completing "If applied, this commit will …": `Add`, `Fix`, `Remove`, never `Added` or `Adds`
- 50 characters or fewer when possible, 72 at most, no trailing period
- Names the overall outcome, not a list of files
- Format `type(scope): summary`. The summary starts with a lower-case verb; acronyms and names keep their case (`add CSV export`)
  - `type`: `feat` new behavior, `fix` bug fix, `perf`, `refactor` (no behavior change), `docs`, `test`, `build` (build system, dependencies), `ci`, `style` (formatting only), `chore` (anything else), `revert`. A commit that mixes kinds takes the first that applies in this order, so a feature with its tests and docs is `feat`
  - `scope`: the main module or area touched, in lower-case kebab-case (`order-detail`); leave it out when the change spans many areas

## Body

The body must cover everything in the commit, at the depth its size calls for. Separate it from the subject with one blank line and wrap lines at 72 characters.

- **Why first**: 1–3 sentences on the problem or goal and the approach taken. Take this from the conversation when you have it; don't invent motivation that neither the diff nor the conversation supports.
- **Then what**: `- ` bullets for every meaningful change: one flat list for medium, grouped under `Area:` labels for large. Each says what changed and, when it isn't obvious, why. Name modules, functions, endpoints, commands and config keys, not line-level edits.
- **Always call out**: behavior changes users will notice; new or changed env vars, config or migrations and how to apply them; dependencies added, removed or upgraded (with versions); removed features; known limitations or follow-up work left undone. Put setup steps and limits in the notes paragraph after the bullets.
- **Keep out**: diff stats, file-by-file trivia, phrases like "this commit", conversation chatter, tool or agent names, emoji (unless the convention uses them). Lockfile and generated changes get one bullet at most.

## Footer

- Breaking change: add `!` after the type or scope and a `BREAKING CHANGE: <what breaks and how to migrate>` footer
- Issue references (`Refs: #123`, `Closes #123`) only when the number appears in the branch name, the conversation or the user's notes
- Other trailers, such as `Co-Authored-By`, only when the user's or the agent's own instructions require them

## Skeleton

```text
type(scope): summary                 all sizes

Why paragraph.                       medium, large (small: only if the why isn't obvious)

- change                             medium: one flat list
Area:                                large: one labelled list per area
- change

Notes paragraph.                     only when needed: how to upgrade, limits, follow-ups

BREAKING CHANGE: ...                 footers: only when needed, always the last paragraph
Refs: #123
```

## Pick the size

Decide by scope, not line count. When torn between two sizes, pick the larger.

| Size | When | Body |
| --- | --- | --- |
| small | one change in one area, and the subject says it all: typo, one-line fix, rename, formatting, version bump | none, or 1–2 sentences when the why isn't obvious |
| medium | one feature or fix across several files, or a small change whose why needs explaining | why paragraph + 2–8 flat bullets |
| large | several areas or layers (database + API + UI), a new module, a migration or a breaking change | why paragraph + bullets grouped under area labels + notes |

## Small

```text
fix(cart): round line totals to 2 decimal places
```

```text
fix(auth): treat expired session cookies as logged out

Requests with an expired cookie returned 500 instead of redirecting
to the login page.
```

```text
build(deps): bump axios from 1.7.2 to 1.7.9
```

## Medium

```text
feat(orders): add CSV export to the order list

Sales staff copied orders into spreadsheets by hand for monthly
reports. Export uses the filters already applied on the list, so
the file matches what is on screen.

- Add GET /orders/export returning text/csv for the current filters
- Add an Export button to the order list toolbar
- Format dates as dd/mm/yyyy and amounts with 2 decimal places
- Add tests for filtered export and an empty result
```

```text
refactor(reports): extract date range parsing into a shared helper

Three report endpoints parsed ?from/?to differently, and one
accepted an end date before the start date.

- Add parseDateRange() in lib/date-range with one validation rule
- Use it in the sales, stock and payroll report endpoints
- Return 400 with a clear message for an invalid or reversed range
```

## Large

```text
feat(auth)!: replace session cookies with JWT access and refresh tokens

The mobile app can't share cookie sessions with the web app, and
server-side sessions made scaling past one instance hard. Move to
short-lived JWT access tokens with rotating refresh tokens, used by
both clients.

API:
- Add POST /auth/login, /auth/refresh and /auth/logout
- Issue 15-minute access tokens and 30-day refresh tokens that
  rotate on every use and detect reuse
- Replace the session middleware with JWT verification on all
  protected routes

Database:
- Add refresh_tokens table with per-device expiry and revocation
- Drop the sessions table

Web:
- Store the access token in memory and refresh it before expiry
- Redirect to login when a refresh fails

Tests:
- Add integration tests for login, rotation, reuse and logout
- Update protected route tests to send a bearer token

Run `npm run db:migrate` before deploying. Set JWT_SECRET and
REFRESH_TOKEN_TTL_DAYS (default 30). Existing users are logged out
once after the deploy.

BREAKING CHANGE: protected endpoints now require an
`Authorization: Bearer <token>` header; cookie sessions are no longer
accepted.
```

## Not like this

| Wrong | Why | Right |
| --- | --- | --- |
| `update code` | no type, says nothing | `fix(cart): round line totals to 2 decimal places` |
| `feat: Added export feature.` | past tense, capitalized, trailing period | `feat(orders): add CSV export to the order list` |
| `fix: fix bug in login.ts, auth.ts, session.ts` | lists files instead of the outcome | `fix(auth): treat expired session cookies as logged out` |
| `feat: add CSV export and fix rounding and update deps` | crams everything into the subject | subject names the main outcome; the rest goes in body bullets |
| a large change with a one-line body | the reader can't tell what changed | use the large template |
| a typo fix with a three-paragraph body | noise | subject only |
