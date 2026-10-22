# Commit Message Templates

Every commit uses the same skeleton. Size only decides which parts appear, so a one-line fix and a mega feature still read the same way.

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
