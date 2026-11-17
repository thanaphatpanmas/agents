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
- Save a plain screenshot with the changed part in view, at a viewport appropriate to the change. Add a concise criterion/state caption to the evidence table and PR. In-image rings/caption bars are optional unless requested; if used, don't cover content or alter layout, and remove them afterward
- Reuse one screenshot for several criteria when it clearly demonstrates them; capture distinct states only when they add evidence. Include responsive states when the layout change needs them
- Use seed or test data only. If a screen would show real personal data, secrets or tokens, change the data or skip it and say why
- If the app doesn't do what the Then says, don't retry until it looks right: record what you saw

Then write `evidence.md`, one row per criterion, with paths relative to the repo:

```markdown
| AC | Criterion | Test | Result | Screenshot |
| --- | --- | --- | --- | --- |
| AC1 | Cancelled invoices are hidden by default | `e2e/invoices.spec.ts` › AC1 | passed | `.story/124-invoice-filters/screenshots/ac1.png` |
```

Result comes from the supplied test results; label a manual browser check explicitly and never imply it was an automated test. Screenshots do not prove API assertions. Keep captures tied to the verified code/state. Record durations, release the execution slot and leave git alone. Stop only a process this story started, and only when the main session confirms no further checks need it.

Reply with:

- **Table**: the contents of `evidence.md`
- **Mismatches**: criteria where the app didn't match the Then
- **Skipped**: criteria without a screenshot, and why
- **Run**: browser checks performed, automated versus manual, and duration
