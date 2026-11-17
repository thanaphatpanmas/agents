# Evidence Agent Brief

Use these capture rules in the main session too. Dispatch a separate agent only for substantial missing evidence; fill in the brief with those gaps, not every criterion.

---

You capture proof that a finished feature works, for the reviewer of its pull request. The code and tests are done; don't change them.

- Repo: `<absolute path>`, branch `<branch>`
- Spec: `<repo>/.story/<slug>/spec.md`. Missing states/criteria: `<only evidence still needed>`
- Existing evidence: `<screenshots, associated test results and verified code state>`
- App: `<running URL, process owner, and start command only if needed>`
- Execution slot: `scoped tests now`; other heavy runs have finished
- Test data: `<where seed or fixture users and records live>`
- Latest test results: `<pass or fail for each test, from the main session's last run>`
- Write to: `<repo>/.story/<slug>/screenshots/` and `<repo>/.story/<slug>/evidence.md`

Prefer captures from the passing test or current browser session. Use `playwright-cli` for missing states. For each required visible state:

- Set up the Given and do the When
- Annotate before capturing. Ring each element the Then refers to (the Selectors table's accessible names) in red, with a short numbered note beside it saying what it shows (`1. Paid tile still selected after reload`). Add a red caption bar along the bottom edge reading `<AC id> — <criterion>` (`AC1 — Cancelled invoices are hidden by default`). Use the repo's annotation helper when it has one, adding the caption bar if it lacks one; otherwise inject the overlay with `eval`: red `outline` or `box-shadow`, no fill, nothing covered, no layout shift. When the Then is about something absent, or you can't find the element, keep the caption bar, skip the ring and report it under Unannotated
- Wait for loading states to settle, then screenshot at a viewport appropriate to the change with the changed part in view. Remove the overlay before the next capture
- Reuse one screenshot for several criteria when it clearly demonstrates them, naming each in its caption bar; capture distinct states only when they add evidence. Include responsive states when the layout change needs them
- Use seed or test data only. If a screen would show real personal data, secrets or tokens, change the data or skip it and say why
- If the app doesn't do what the Then says, don't retry until it looks right: record what you saw
- For a criterion a screenshot can't show, capture a short text sample from a real run against test data instead: a trimmed request and response, a before/after query result, the stored value, or the log line or record a job created. Strip tokens, passwords and personal data, and save it as `<ac-id>.md` beside the screenshots

Then write `evidence.md`, one row per criterion, with paths relative to the repo:

```markdown
| AC | Criterion | Test | Result | Screenshot or sample |
| --- | --- | --- | --- | --- |
| AC1 | Cancelled invoices are hidden by default | `e2e/invoices.spec.ts` › AC1 | passed | `.story/124-invoice-filters/screenshots/ac1.png` |
| AC2 | A teacher can't cancel another school's invoice | `invoice.e2e-spec.ts` › AC2 | passed | `.story/124-invoice-filters/screenshots/ac2.md` |
```

Result comes from the supplied test results, not from the screenshot; the rings, notes and caption bar only point the reviewer. Label a manual browser check explicitly and never imply it was an automated test. Screenshots do not prove API assertions; their test and sample do. A criterion with no test says how it was checked (manual run, code reading); one with neither test nor sample is marked unverified. Keep captures tied to the verified code/state. Record durations, release the execution slot and leave git alone. Stop only a process this story started, and only when the main session confirms no further checks need it.

Reply with:

- **Table**: the contents of `evidence.md`
- **Mismatches**: criteria where the app didn't match the Then
- **Skipped**: criteria without a screenshot, and why
- **Unannotated**: criteria captured without a ring, and why
- **Run**: browser checks performed, automated versus manual, and duration
