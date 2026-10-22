# Workload Standard

The reference output. Module names are fictional; copy the shape, not the content.

## Template

```text
Month YYYY
Week N (dd/mm/yyyy - dd/mm/yyyy)
Day N (dd/mm/yyyy)
- [ ] (HH-HH) (Nh) [Mega-Module/Module/Sub-Module] Task
```

## Example

```text
June 2026
Week 1 (01/06/2026 - 07/06/2026)
Day 1 (01/06/2026)
- [x] (08-12) (4h) [Sales/Order/Order List] CRUD, Filter, Pagination
- [x] (13-17) (4h) [Sales/Order/Order Detail] Status Timeline, Print Receipt
Day 2 (02/06/2026)
- [x] (08-10) (2h) [Sales/Order] Test, Fix, Detail
- [x] (10-12) (2h) [Inventory/Stock Movement] Query Optimization
- [x] (13-17) (4h) [Inventory/Stock Movement] Re-Design, Export Excel
Day 3 (03/06/2026)
- [x] (08-12) (4h) Meeting Sprint Planning
- [x] (13-17) (4h) [HR/Leave Request] Approval Flow, Notification
Day 4 (04/06/2026)
Nothing
Day 5 (05/06/2026)
- [x] (08-12) (4h) [UAT 05/06/2026] Testing, Data Preparation
- [x] (13-17) (4h) [UAT 05/06/2026] Hot Fix
Day 6 (06/06/2026)
- [x] (08-12) (4h) [Auth/Two-Factor] Added TOTP setup and verification
- [x] (13-17) (4h) [Auth/Two-Factor] Test, Fix, Detail

Week 2 (08/06/2026 - 14/06/2026)
Nothing

Week 5 (29/06/2026 - 05/07/2026)
Day 1 (29/06/2026)
- [ ] (08-12) (4h) [Docs] API Documentation, Setup Guide
- [ ] (13-17) (4h) [Research] Compared payment gateway providers
Day 2 (30/06/2026)
- [ ] (08-12) (4h) [Sales/Promotion/Coupon] Added coupon validation
- [ ] (13-17) (4h) [Sales/Promotion, Order] Test, Fix, Detail

July 2026
Week 1 (06/07/2026 - 12/07/2026)
Day 1 (06/07/2026)
- [ ] (08-12) (4h) [Sales/Promotion/Flash Sale] CRUD
- [ ] (13-17) (4h) [Report/Sales Summary] Added PDF report
```

## What each part shows

- **8h days**: every working day adds up to 8h, either 4h + 4h or smaller blocks (Day 2). Lunch 12-13 is never a slot.
- **Manual lines** (`Meeting Sprint Planning` on Day 3): written by the user, not from git. Keep them as they are.
- **No work**: a weekday with no work is `Nothing` (Day 4). A week with no work at all is the week header plus `Nothing` (Week 2).
- **Weekends**: they appear only when there was work (Day 6). Sunday is skipped here.
- **Month boundary**: Week 5 starts Monday 29/06, so it stays under June even though it ends in July. July's first week is the one starting Monday 06/07.
- **Checkboxes**: `[x]` for weeks already submitted, `[ ]` for the newly written week.
- **Tags**: the same module keeps the same tag every time (`[Sales/Promotion/Coupon]`). Use a plain tag for non-feature work (`[Docs]`, `[Research]`, `[UAT dd/mm/yyyy]`).
- **Tasks**: one line, about 8 words or fewer. Write either comma-separated verbs/nouns (`Test, Fix, Detail`) or one short past-tense phrase (`Added coupon validation`).

## Not like this

```text
- [ ] [14-15] (1h) ...                                  ← time uses ( ), not [ ]
- [ ] (08-12) (3h) ...                                  ← 08-12 is 4h
Day 4 (1/10/2026)                                       ← zero-pad: 01/10/2026
- [ ] (08-12) (4h) [Sales/Order] Update order status display and fix validation to match the migrated data   ← too long, more than one line
- [ ] (08-12) (4h) [Sales/Order] feat(order): add bulk export (a1b2c3d4)   ← commit message and hash, not a task
- [ ] (08-12) (4h) [web/sales/order] CRUD               ← package folder in tag; use [Sales/Order]
```
