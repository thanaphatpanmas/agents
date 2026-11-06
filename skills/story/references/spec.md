# Spec Addendum

`/to-spec` writes the problem, user stories, seams and testing decisions. The agents need three more things it doesn't pin down: what "done" looks like as checkable behavior, the names the e2e tests select by, and where to look for holes. Append them to the spec in `.story/<slug>/spec.md`.

Derive every line from the spec's user stories and the tickets' acceptance criteria. Where you had to fill a gap, end the line with `(assumed)` so the user sees it at approval.

## Acceptance criteria

One per observable behavior. Number them in order across the whole spec so tests, screenshots and the PR can refer to `AC3`.

```markdown
## Acceptance criteria

- **AC1** Cancelled invoices are hidden by default `ui` (#124)
  - Given invoices with the statuses paid, pending cancel and cancelled
  - When the user opens the invoice list
  - Then only the paid invoice is listed and "Hide cancelled" is checked
- **AC2** A teacher can't cancel another school's invoice `api` (#126)
  - Given an invoice that belongs to another school
  - When a teacher sends the cancel request for it
  - Then the request is refused and the invoice is unchanged
```

- `ui`: a user can see it, so it gets an e2e test and a screenshot. `api`: server behavior, covered by integration tests
- Then lines describe what someone could check from outside: text on screen, a response, a stored record. Not "the function is called"
- The source in brackets: a ticket, or a user story number when there are no tickets

## Selectors

Only for `ui` criteria. The E2E agent writes tests against these names while the Dev agent builds the screens, so both must use the same ones.

```markdown
## Selectors

| Element | Role | Accessible name |
| --- | --- | --- |
| Hide cancelled filter | checkbox | Hide cancelled |
| Invoice date filter | textbox | Invoice date |
| Cancel button on a row | button | Cancel invoice |
```

Reuse names that already exist in the UI and the spec's own wording. For a multilingual app, use the language the e2e tests run in.

## Attack surface

What the change opens up, so the Security agent starts in the right place. Leave out a heading that doesn't apply, and write `none` when nothing does.

```markdown
## Attack surface

- Input: the invoice-date filter and student-code search reach a database query
- Access: only staff of the invoice's school may cancel it, paid or not
- Output: Excel export writes names typed by users into cells
- State: a paid invoice can be cancelled once; cancelling again must fail
```

## PR groups

Only when there are tickets. One PR per group of tickets that change the same area. A group goes after any group it's blocked by and branches from it.

```markdown
## PR groups

| Group | Tickets | Area | Blocked by | Branch |
| --- | --- | --- | --- | --- |
| 1 | #124, #125 | invoice list filters | none | feat/124-invoice-filters |
| 2 | #126 | cancel paid invoices | 1 | feat/126-cancel-paid-invoice |
```

## Short spec for a small fix

No `/to-spec` issue, so write the whole thing to `.story/<slug>/spec.md`. Use the issue number in `<slug>` when there is one, otherwise just the short name.

```markdown
# <What changes>

## Problem
What happens now and what should happen instead.

## Seam
Where the test goes: the function, endpoint or component whose behavior changes, tested through its public interface.

## Acceptance criteria
## Selectors
## Attack surface

## Out of scope
```

The last three sections follow the formats above; drop Selectors when nothing in the UI changes.
