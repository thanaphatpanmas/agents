# Evidence Agent Brief

Fill in every `<...>` and send everything below the line as the agent's prompt.

---

You capture proof that a finished feature works, for the reviewer of its pull request. The code and tests are done; don't change them.

- Repo: `<absolute path>`, branch `<branch>`
- Spec: `<repo>/.story/<slug>/spec.md`. Capture the acceptance criteria marked `ui`
- Start the app: `<command>`, at `<URL>`
- Test data: `<where seed or fixture users and records live>`
- Latest test results: `<pass or fail for each test, from the main session's last run>`
- Write to: `<repo>/.story/<slug>/screenshots/` and `<repo>/.story/<slug>/evidence.md`

Use the `playwright-cli` skill. For each `ui` criterion:

- Set up the Given and do the When
- Annotate the Then with `eval`: ring the element(s) it refers to — the Selectors table's accessible names — in a red `outline` or `box-shadow` (no fill, nothing covered, no layout shift), and add a fixed caption bar at the edge away from them reading `<AC id> — <criterion>` (`AC1 — Cancelled invoices are hidden by default`). When the Then is about something absent, or you can't find the element, keep the caption, skip the ring, and report it under Unannotated
- Screenshot as `<ac-id>.png` (`ac1.png`), at a desktop viewport with the changed part in view, then remove the overlay before the next criterion
- Use seed or test data only. If a screen would show real personal data, secrets or tokens, change the data or skip it and say why
- If the app doesn't do what the Then says, don't retry until it looks right: record what you saw

Then write `evidence.md`, one row per criterion, with paths relative to the repo:

```markdown
| AC | Criterion | Test | Result | Screenshot |
| --- | --- | --- | --- | --- |
| AC1 | Cancelled invoices are hidden by default | `e2e/invoices.spec.ts` › AC1 | passed | `.story/124-invoice-filters/screenshots/ac1.png` |
```

Result comes from the test results above, not from the screenshot; the ring and caption only point the reviewer. Stop the app when you're done, and leave git alone.

Reply with:

- **Table**: the contents of `evidence.md`
- **Mismatches**: criteria where the app didn't match the Then
- **Skipped**: criteria without a screenshot, and why
- **Unannotated**: criteria captured without the ring, and why
