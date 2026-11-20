---
name: workload
description: Review the user's git commits and pull requests over a date range and write their weekly workload log (Month → Week → Day → `(2h) [Module/Sub-Module] Task`) with estimated whole hours per task. Use whenever the user asks, in Thai or English, to check what they committed, write or fill a workload, timesheet, work log, or ลงเวลา/ลงงาน/สรุปงานประจำสัปดาห์, or pastes a partly filled week — even if they don't say "workload".
argument-hint: "[project names or paths] [date range]"
---

# Workload from Commits

The user submits a weekly workload log. Use commits and pull requests to identify what they did each day and estimate whole hours per task. Read [the workload example](references/example.md) before writing.

## 1. Find the projects, the range and the draft

A typical request: `/workload web-app and mobile-app from 12 to 22 Oct`.

- **Projects**: the names (or paths) the user lists, each one passed as `--repo`. The script looks a name up as a git repo folder under the home directory, matching loosely (`mobile-app` = `Mobile App` = `mobile_app`). If it reports no match or several matches, ask the user for the path. If no project is named, use the current repo.
- **Range**: from the request or the pasted draft's week header. A date without a year means this year, or last year if that date would still be in the future. Weeks run Monday → Sunday. When the range starts or ends mid-week, the week header still shows the full Monday–Sunday dates, but write only the days inside the range.
- **Draft**: keep the user's existing lines verbatim, including meetings, UAT, leave, `Nothing`, time slots, and hours. Fill empty days or `[]` slots. If they ask to add hours to a supplied list, add only the missing hour prefixes and preserve task text, order, and any hours already recorded.

## 2. Collect commits

```bash
python3 <skill-dir>/scripts/collect_commits.py --since YYYY-MM-DD --until YYYY-MM-DD --repo web-app --repo mobile-app
```

- Run it from a few days before the range to a week after it, so the commits around an empty day at either edge are visible (step 5), but write only the days inside the range.
- Prints each day with time, repo, hash, subject, size (+added/-deleted) and the top 3 `areas` touched. An area is the file's directory path with common code-layout folders (`src`, `components`, `services`, `tests`, …) removed, so what's left is mostly the feature name. It's a hint, not the tag.
- Under each commit, its message body, indented, without `Co-Authored-By`/`Signed-off-by` trailers. Commits made with the `commit` skill have a detailed body: why, then a bullet per change, grouped under area labels (`API:`, `Web:`) in big commits. It's the best record of what a commit holds.
- Matches `git config user.name` across all branches; pass `--author` if commits were made under another name
- Times are author times (when the commit was made, even if it was rebased later) in the local timezone. Commits before 05:00 are shifted to the previous day and marked `late-night`, since that's still the previous day's work

Not every commit is work to log. Version bumps, merges, lockfile-only changes and tool-generated commits (agent session checkpoints, auto-saves, often huge or empty) are by-products of the real work around them. Don't give them entries. Subjects usually follow Conventional Commits (`type(scope): summary`): the scope hints the module, the type the kind of work, and `build(deps)` bumps, release commits and `style` (formatting-only) commits are by-products too. A squash-merge commit (on GitHub its subject ends in `(#123)`) repeats its branch's commits, so it is a by-product when those commits are in the log too.

A commit message can be vague ("wip", "update") or cover several things ("fix login" that also changed report code). When the subject and body don't explain the work, run `git show --stat <sha>` and look at what changed; the entry must describe the actual work, not the message.

## 3. Read the pull requests

A PR written with the `pull-request` skill sums up a whole branch: why, changes grouped by area, testing. For each repo with a GitHub or GitLab remote, list the user's PRs updated since the range start:

```bash
cd <repo> && gh pr list --author @me --state all --search "updated:>=YYYY-MM-DD" --limit 50 --json number,title,body,headRefName,createdAt,mergedAt,commits
cd <repo> && glab mr list --author <username> --all --per-page 50 --output json   # <username> from `glab api user`; keep MRs whose updated_at is in range
```

Use them to:
- **Name the work**: the PR's Summary and Changes describe a feature better than any single commit.
- **Group commits**: commits in one PR are one feature, so they share a tag.
- **Find the real days**: after a squash merge with the branch deleted, the local log holds only the squash commit, dated the merge day. The PR's own commits give the days the work was done (gh: `commits[].authoredDate`; GitLab: `glab api projects/:id/merge_requests/<iid>/commits`, field `authored_date`). Place the work on those days, not the merge day.

Opening or merging a PR is not an entry on its own. If `gh`/`glab` is missing, not logged in or offline, skip this step, work from commits alone, and say so in the notes.

## 4. Turn the work into entries

**Tag** `[Mega-Module/Module/Sub-Module]`: the business feature in Title Case, read from `areas`, the subject's scope and the PR. Areas still contain project-specific folders the script can't know about, such as a workspace/package name (`web`, `server`) or a grouping folder (`settings`, `admin`). Drop those and keep the feature path: `web/sales/order/order-detail` and `server/sales/order/order-detail` → `[Sales/Order/Order Detail]`. Use as many levels as is meaningful (`[Inventory/Stock Movement]`, `[Auth]`). Two related areas in one line → `[HR/Leave Request, Payroll]`. Non-feature work gets a plain tag like `[Docs]`, `[Research]`, `[UAT dd/mm/yyyy]`. Reuse tags the user already wrote in the draft or in earlier weeks, so the same module is always named the same way.

With several projects, the reader must still tell them apart. The first project the user names is the main one, and its tags are plain module paths (`[Sales/Order]`). Every other project's tags start with its name in Title Case (`[Mobile App/Checkout]`, or just `[Mobile App]`). A line holds work from one project only.

**Task**: short English, one of the user's two styles:
- comma-separated verbs/nouns: `CRUD`, `Test, Fix, Detail`, `Re-Design, Query Optimization`
- one short past-tense phrase: `Added order export to Excel`

The whole entry must fit on one line. Keep the task to about 8 words / 60 characters. If one piece of work covered several things, name the main one, or split it into separate lines. Keep commit hashes, `type(scope):` prefixes, file names, and parenthetical explanations out of the task text.

**Lines per day**: one line per distinct piece of work, in the order it was done, usually 1–4 lines. Several commits on the same feature share one line; one big commit splits into a few lines along its body's area labels or bullets when it covers clearly separate features. A follow-up `Test, Fix, Detail` line fits when the day's commits are tests and fixes on that feature. Include only work supported by the draft or repository evidence.

## 5. Days without commits: infer, then flag

The user normally commits each task soon after finishing. Infer work on an empty weekday only when nearby commits or PR evidence support work spanning the gap.

- Look at the next commit after the gap and its PR for signs of earlier work, such as dated notes or branch activity. When the evidence supports a split, assign distinct parts to each day. Commit size alone does not establish that a task started earlier.
- Work left unfinished before the gap (a `wip` commit, a feature whose PR came later) can also continue into it.
- End every inferred line with ` (?)`, for example `(2h) [Sales/Promotion/Flash Sale] Database, API (?)`. The user checks these before submitting.
- Write `Nothing` only when nothing on either side points to the day (leave, a holiday, or work outside git).
- Weekend days appear only when they have commits or draft entries; don't infer work onto them.

## 6. Estimate hours

- Treat each distinct task's relevant commit author time as an approximate finish time. Use the gap from the preceding distinct task's finish within the same workday as a clue when tasks appear sequential. Account for known breaks, manual entries, or overlapping work. Ignore duplicate, squash, merge, and by-product timestamps when the original task commits are available. Keep the before-05:00 workday rule when comparing timestamps.
- For the first or only task of a day, or when commits cluster or have long gaps, estimate from the diff, the implementation and testing involved, and similar tasks. If one commit covers multiple entries, or a task spans multiple days, split the estimate across those entries. Count shared effort once. Use a daily hour budget only if the user supplies one.
- Pick a plausible range internally, round its midpoint to the nearest whole hour (half hours round up), and use at least 1 hour for each generated task. Output one number per task. Preserve the user's own hours and time slots verbatim. If the user asks for entries without hours, omit generated prefixes.
- Keep any day totals the user requests consistent with the displayed entries. In the notes, label generated hours as estimates and call out any particularly uncertain allocations.

## 7. Output format

Put the result in one fenced `text` block, ready to paste:

```text
June 2026
Week 1 (01/06/2026 - 07/06/2026)
Day 1 (01/06/2026)
(3h) [Sales/Order/Order List] CRUD, Filter, Pagination
(2h) [Sales/Order/Order Detail] Status Timeline, Print Receipt
Day 2 (02/06/2026)
(2h) [Sales/Order/Order Export] Database, API (?)
Day 3 (03/06/2026)
(2h) [Sales/Order/Order Export] Export Button, Excel Format
```

- Month header (`October 2026`) only when the range starts a month or the user's draft has one. A week belongs to the month of its Monday, and `Week N` means the Nth Monday of that month.
- Dates are `dd/mm/yyyy`, zero-padded. `Day N` is the weekday number (Mon = 1 … Sun = 7), so Saturday is always Day 6 even when earlier days are missing.
- Start each generated entry with `(Nh)` followed by its tag. Use a positive integer for `N`. Keep generated entries free of clock-time slots, bullets, and checkboxes.
- A week with no work at all: the week header followed by `Nothing`.
- Blank line between weeks.

After the block, add short notes in the user's language:
- each `(?)` line: which commit or PR it was inferred from, and why
- weekdays left as `Nothing`, so the user can add meetings, research or leave
- lines where the split or wording was a guess
- late-night or weekend commits you moved
- commits whose message didn't match the change, in case they want to reword them before pushing
- repos whose PRs couldn't be read
