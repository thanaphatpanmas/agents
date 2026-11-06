# Workload Standard

The reference output. Module names are fictional; copy the shape, not the content.

## Template

```text
Month YYYY
Week N (dd/mm/yyyy - dd/mm/yyyy)
Day N (dd/mm/yyyy)
[Mega-Module/Module/Sub-Module] Task
```

## Example

```text
June 2026
Week 1 (01/06/2026 - 07/06/2026)
Day 1 (01/06/2026)
[Sales/Order/Order List] CRUD, Filter, Pagination
[Sales/Order/Order Detail] Status Timeline, Print Receipt
Day 2 (02/06/2026)
[Sales/Order] Test, Fix, Detail
[Inventory/Stock Movement] Query Optimization
[Inventory/Stock Movement] Re-Design, Export Excel
Day 3 (03/06/2026)
Meeting Sprint Planning
[HR/Leave Request] Approval Flow, Notification
Day 4 (04/06/2026)
Nothing
Day 5 (05/06/2026)
[UAT 05/06/2026] Testing, Data Preparation
[UAT 05/06/2026] Hot Fix
Day 6 (06/06/2026)
[Auth/Two-Factor] Added TOTP setup and verification
[Auth/Two-Factor] Test, Fix, Detail

Week 2 (08/06/2026 - 14/06/2026)
Nothing

Week 5 (29/06/2026 - 05/07/2026)
Day 1 (29/06/2026)
[Docs] API Documentation, Setup Guide
[Research] Compared payment gateway providers
Day 2 (30/06/2026)
[Sales/Promotion/Coupon] Added coupon validation
[Sales/Promotion, Order] Test, Fix, Detail
Day 3 (01/07/2026)
[Sales/Promotion/Flash Sale] Database, API (?)
Day 4 (02/07/2026)
[Sales/Promotion/Flash Sale] Countdown UI, Stock Limit
[Sales/Promotion/Flash Sale] Test, Fix, Detail

July 2026
Week 1 (06/07/2026 - 12/07/2026)
Day 1 (06/07/2026)
[Report/Sales Summary] Added PDF report
```

## What each part shows

- **Plain lines**: each line is one piece of work starting with its tag, with no checkbox, times or hours; the user adds the time slots.
- **Manual lines** (`Meeting Sprint Planning` on Day 3): written by the user, not from git. Keep them as they are.
- **Inferred day** (Week 5, Day 3): no commits that day, and Day 4's one flash-sale commit had `API:` and `Web:` sections, so the API part went on Day 3 with `(?)` and the UI part stayed on Day 4. The notes say which commit it came from.
- **No work**: a weekday where nothing on either side points to work is `Nothing` (Week 1, Day 4). A week with no work at all is the week header plus `Nothing` (Week 2).
- **Weekends**: they appear only when there was work (Day 6). Sunday is skipped here.
- **Month boundary**: Week 5 starts Monday 29/06, so it stays under June even though it ends in July. July's first week is the one starting Monday 06/07.
- **Tags**: the same module keeps the same tag every time (`[Sales/Promotion/Flash Sale]`). Use a plain tag for non-feature work (`[Docs]`, `[Research]`, `[UAT dd/mm/yyyy]`).
- **Tasks**: one line, about 8 words or fewer. Write either comma-separated verbs/nouns (`Test, Fix, Detail`) or one short past-tense phrase (`Added coupon validation`).

## Not like this

```text
- [ ] [Sales/Order] CRUD                          ← no checkbox; start with the tag
(08-12) (4h) [Sales/Order] CRUD                   ← no time or hours; the user adds them
[Sales/Order] CRUD (inferred from a1b2c3d4)       ← flag with (?) only; the reason goes in the notes
Day 4 (1/10/2026)                                 ← zero-pad: 01/10/2026
[Sales/Order] Update order status display and fix validation to match the migrated data   ← too long, more than one line
[Sales/Order] feat(order): add bulk export (a1b2c3d4)   ← commit message and hash, not a task
[web/sales/order] CRUD                            ← package folder in tag; use [Sales/Order]
```
