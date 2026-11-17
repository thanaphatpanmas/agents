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
- Before/after comparison: `<off | on: pages or runs to compare, and where the before side is>`
- Write to: `<repo>/.story/<slug>/screenshots/` and `<repo>/.story/<slug>/evidence.md`

Prefer captures from the passing test or current browser session. Use `playwright-cli` for missing states. For each required visible state:

- Set up the Given and do the When
- Annotate before capturing. Ring each element the Then refers to (the Selectors table's accessible names) in red, with a short numbered note beside it saying what it shows (`1. Paid tile still selected after reload`). Add a red caption bar along the bottom edge reading `<AC id> — <criterion>` (`AC1 — Cancelled invoices are hidden by default`). Use the repo's annotation helper when it has one, adding the caption bar if it lacks one; otherwise inject the overlay with `eval`: red `outline` or `box-shadow`, no fill, nothing covered, no layout shift. When the Then is about something absent, or you can't find the element, keep the caption bar, skip the ring and report it under Unannotated
- Wait for loading states to settle, then screenshot at a viewport appropriate to the change with the changed part in view. Remove the overlay before the next capture
- Reuse one screenshot for several criteria when it clearly demonstrates them, naming each in its caption bar; capture distinct states only when they add evidence. Include responsive states when the layout change needs them
- Use seed or test data only. If a screen would show real personal data, secrets or tokens, change the data or skip it and say why
- If the app doesn't do what the Then says, don't retry until it looks right: record what you saw
- For a criterion a screenshot can't show, capture a short text sample from a real run against test data instead: a trimmed request and response, a before/after query result, the stored value, or the log line or record a job created. Strip tokens, passwords and personal data, and save it as `<ac-id>.md` beside the screenshots

Then write `evidence.md`, one row per criterion, with paths relative to the repo (with the comparison on, add a `## Before / after` list: name, page or run, change):

```markdown
| AC | Criterion | Test | Result | Screenshot or sample |
| --- | --- | --- | --- | --- |
| AC1 | Cancelled invoices are hidden by default | `e2e/invoices.spec.ts` › AC1 | passed | `.story/124-invoice-filters/screenshots/ac1.png` |
| AC2 | A teacher can't cancel another school's invoice | `invoice.e2e-spec.ts` › AC2 | passed | `.story/124-invoice-filters/screenshots/ac2.md` |
```

Result comes from the supplied test results, not from the screenshot; the rings, notes and caption bar only point the reviewer. Label a manual browser check explicitly and never imply it was an automated test. Screenshots do not prove API assertions; their test and sample do. A criterion with no test says how it was checked (manual run, code reading); one with neither test nor sample is marked unverified. Keep captures tied to the verified code/state. Record durations, release the execution slot and leave git alone. Stop only a process this story started, and only when the main session confirms no further checks need it.

## Before/after comparison

Only when the main session turned it on (SKILL.md step 1). Both sides are the same pages or runs, against the same data, with the same marks; only the code differs.

- **One capture script, two runs.** Write it once in a git-excluded folder such as `.story/<slug>/capture/`, starting from `<skill-dir>/scripts/capture-template.js`, and run it with `MODE` `before`, then `after`, into `screenshots/before/` and `screenshots/after/`. AC annotations whose notes quote new values run in `after` only
- **Same data.** Create the records the pages need through the API or fixtures at the start of each run and delete them at the end, so both sides start from the same state. Same users, viewport, locale and steps, including typed input: typing `8.5` on both sides shows what each version does with it
- **Same marks.** Find each target by something both versions share: a regex on its stable label (`/^Total:/`), its structure (`p:has(> strong)` when label and value are split into separate text nodes) or its role, never by the value that changed. Notes name the thing (`3. total`), not its value; values go in the pair's caption. Fit a full-width block's ring to its text and put the note beside it, so no note covers content. Leave out look-alikes that aren't part of the change, such as a `2/3` submitted count next to `5.6/7` scores
- **Before side on the base code.** It is normally captured right after branching, before the first edit (SKILL.md step 4). When it is needed later:
  - Nothing has to run from this checkout (functions, CLI, scripts): use a `git worktree add <tmp> <base>` checkout
  - The app runs from this checkout (dev servers that reload on change): save `git diff` and copies of new files outside the repo; drop intent-to-add entries (`git reset -q -- <paths>`), since `git stash` refuses them; `git stash push -u`; rebuild shared packages and wait for the servers to reload; capture; `git stash pop`; re-add the intent-to-add entries; check that `git diff` matches the saved copy. Never leave the stash behind
- **Pairs.** `python3 <skill-dir>/scripts/compare.py <repo>/.story/<slug>/screenshots --captions <captions.json>` writes one side-by-side page per name, before left and after right, using the ringed `marked/` shots when present, plus a render script; run that with `playwright-cli run-code` to get `screenshots/compare/<name>.png`. Each caption states the change in values (`06 Part 1 card: 6 of 7 → 5.6 of 7`), or `no change` for a page included to show nothing regressed
- **Without UI**, compare text. Send the same request, call or command to both code states and put the outputs side by side in `screenshots/compare.md`, as a two-column table or a `diff` block: an API pair shows status and the trimmed body (`POST score 7.25: 201 saved → 400 refused`), a calculation an input → output table, a migration the schema diff and row counts, a performance change timings over the same data and run count. A refactor's pair shows identical output. Strip tokens, passwords and personal data

Reply with:

- **Table**: the contents of `evidence.md`
- **Mismatches**: criteria where the app didn't match the Then
- **Skipped**: criteria without a screenshot, and why
- **Unannotated**: criteria captured without a ring, and why
- **Run**: browser checks performed, automated versus manual, and duration
- **Comparison**: pairs made, their captions, and any mark that didn't land on one side
