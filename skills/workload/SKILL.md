---
name: workload
description: Review the user's git commits over a date range and write their weekly workload timesheet in their own template (Month → Week → Day → `- [ ] (08-12) (4h) [Module/Sub-Module] Task`), filling each working day to 8 hours. Use whenever the user asks, in Thai or English, to check/review what they committed in a period, write or fill a workload, timesheet, work log, or ลงเวลา/ลงงาน/สรุปงานประจำสัปดาห์, or pastes a partly filled week with empty `[]` slots — even if they don't say "workload".
argument-hint: "[project names or paths] [date range]"
---

# Workload from Commits

The user submits a weekly workload log. Git history is the evidence of what they did; this skill turns it into entries in their exact format so they can paste it without editing. Read `references/example.md` once before writing: it is the standard every output must match, including the "Not like this" mistakes to avoid.

## 1. Find the projects, the range and the draft

A typical request: `/workload web-app and mobile-app from 12 to 22 Oct`.

- **Projects**: the names (or paths) the user lists, each one passed as `--repo`. The script looks a name up as a git repo folder under the home directory, matching loosely (`mobile-app` = `Mobile App` = `mobile_app`). If it reports no match or several matches, ask the user for the path. If no project is named, use the current repo.
- **Range**: from the request or the pasted draft's week header. A date without a year means this year, or last year if that date would still be in the future. Weeks run Monday → Sunday. When the range starts or ends mid-week, the week header still shows the full Monday–Sunday dates, but write only the days inside the range.
- **Draft**: if the user pasted a partly filled week, that draft is the skeleton. Keep every line they already wrote verbatim (meetings, UAT, leave, "Nothing") and fill only the empty `[]` slots. Their manual entries record things git can't see.

## 2. Collect commits

```bash
python3 <skill-dir>/scripts/collect_commits.py --since YYYY-MM-DD --until YYYY-MM-DD --repo web-app --repo mobile-app
```

- Prints each day with time, repo, hash, subject, size (+added/-deleted) and the top 3 `areas` touched. An area is the file's directory path with common code-layout folders (`src`, `components`, `services`, `tests`, …) removed, so what's left is mostly the feature name. It's a hint, not the tag.
- Under each commit, its message body, indented, without `Co-Authored-By`/`Signed-off-by` trailers. Commits made with the `commit` skill (the user's own work, written up by an agent) have a detailed body: why, then a bullet per change, grouped under area labels (`API:`, `Web:`) in big commits. It's the best record of what a commit holds.
- Matches `git config user.name` across all branches; pass `--author` if commits were made under another name
- Times are author times (when the commit was made, even if it was rebased later) in the local timezone. Commits before 05:00 are shifted to the previous day and marked `late-night`, since that's still the previous day's work

Not every commit is work to log. Version bumps, merges, lockfile-only changes and tool-generated commits (agent session checkpoints, auto-saves, often huge or empty) are by-products of the real work around them. Don't give them entries or hours. Subjects usually follow Conventional Commits (`type(scope): summary`): the scope hints the module, the type the kind of work, and `build(deps)` bumps, release commits and `style` (formatting-only) commits are by-products too.

A commit message can be vague ("wip", "update") or cover several things ("fix login" that also changed report code). When the subject and body don't explain the work, run `git show --stat <sha>` and look at what changed; the entry must describe the actual work, not the message.

## 3. Turn commits into entries

**Tag** `[Mega-Module/Module/Sub-Module]`: the business feature in Title Case, read from `areas` and the subject's scope. Areas still contain project-specific folders the script can't know about, such as a workspace/package name (`web`, `server`) or a grouping folder (`settings`, `admin`). Drop those and keep the feature path: `web/sales/order/order-detail` and `server/sales/order/order-detail` → `[Sales/Order/Order Detail]`. Use as many levels as is meaningful (`[Inventory/Stock Movement]`, `[Auth]`). Two related areas in one slot → `[HR/Leave Request, Payroll]`. Non-feature work gets a plain tag like `[Docs]`, `[Research]`, `[UAT dd/mm/yyyy]`. Reuse tags the user already wrote in the draft or in earlier weeks, so the same module is always named the same way.

With several projects, the reader must still tell them apart. The first project the user names is the main one, and its tags are plain module paths (`[Sales/Order]`). Every other project's tags start with its name in Title Case (`[Mobile App/Checkout]`, or just `[Mobile App]`). A slot holds work from one project only.

**Task**: short English, one of the user's two styles:
- comma-separated verbs/nouns: `CRUD`, `Test, Fix, Detail`, `Re-Design, Query Optimization`
- one short past-tense phrase: `Added order export to Excel`

The whole entry must fit on one line: keep the task to about 8 words / 60 characters. If a slot covered several things, name the main one, or split them into separate slots. Never cram them into one task. No commit hashes, `type(scope):` prefixes, file names or parentheses.

**Time slots**: a full day is 8h: 08-12 and 13-17, with lunch at 12-13 not counted. If the user's draft or request uses other working hours, follow those instead.
- Default: two 4h blocks, `(08-12) (4h)` then `(13-17) (4h)`. Morning comes first.
- Split into 2h/1h blocks only when the user asks for detail, or when one 4h label would hide clearly separate work. Slot hours always equal the range (`(08-10) (2h)`), and a day's slots never overlap.
- When the draft already has some slots filled, the new slots fill only the hours that are left.

**Allocating work to slots.** A commit's time is when the work was saved, not when it started. A 12:03 commit is the morning's work, an 18:08 commit is the afternoon's, and evening commits belong to that day's slots. Give each block the work closest in time, and give big or complex commits more hours. The user often commits once at the end of a session, so one commit can hold a whole morning, afternoon or day: spread it over the slots between the previous commit (or the start of the day) and its own time, splitting it along its body's area labels or bullets. If a day's commits look thin for 8h, fill the rest with the testing/fixing/detailing that naturally goes with that work (that's how the user writes it), not with invented features.

**Days without commits.** Write `Nothing` on weekdays with no commits and no draft entry; don't make up work. List those days in the reply so the user can add meetings or research, and say when a big commit on the next working day may include that day's work. Weekend days appear only if they have commits or draft entries.

## 4. Output format

Put the result in one fenced `text` block, ready to paste:

```text
June 2026
Week 1 (01/06/2026 - 07/06/2026)
Day 1 (01/06/2026)
- [ ] (08-12) (4h) [Sales/Order/Order List] CRUD, Filter, Pagination
- [ ] (13-17) (4h) [Sales/Order/Order Detail] Status Timeline, Print Receipt
Day 2 (02/06/2026)
Nothing
```

- Month header (`October 2026`) only when the range starts a month or the user's draft has one. A week belongs to the month of its Monday, and `Week N` means the Nth Monday of that month.
- Dates are `dd/mm/yyyy`, zero-padded. `Day N` is the weekday number (Mon = 1 … Sun = 7), so Saturday is always Day 6 even when earlier days are missing.
- A week with no work at all: the week header followed by `Nothing`.
- Checkbox: new entries are `- [ ]` (the user ticks them after submitting). Keep `[x]` on lines they already ticked.
- Blank line between weeks.

After the block, add short notes in the user's language:
- entries where the slot split or wording was a guess
- weekdays left as `Nothing`, and late-night or weekend commits you moved
- commits whose message didn't match the change, in case they want to reword them before pushing
