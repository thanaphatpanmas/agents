# Planning and checkpoints

Read this before starting or resuming planning. Story coordinates the installed skills; each skill still owns its procedure. Keep planning in the main session, where the user's conversation and decisions are available, including when build roles use `cli`.

## Invoke only what is needed

Use the runtime's skill invocation tool when available. Otherwise locate and read the installed `SKILL.md` and follow it and its references in the main session. If a required skill is missing or model invocation is disabled, report that specific blocker; do not bypass it or silently invent a replacement workflow. Read only the skills required by the current step.

| Skill | Call when | Carry forward |
| --- | --- | --- |
| `setup-matt-pocock-skills` | Planning needs a tracker and `docs/agents/issue-tracker.md` is missing or unusable | Existing repo configuration and any tracker choice already supplied; confirm only unresolved choices |
| `grill-me` | The request leaves material behavior, scope or business decisions unresolved after reading the repo | Known requirements and unanswered decisions; finish when shared understanding is confirmed |
| `to-spec` | The request needs a full spec and none is usable yet | Agreed requirements and seams; confirm the proposed spec before publishing and record its issue URL or local path |
| `to-tickets` | The spec spans several areas and lacks a usable breakdown | The approved spec and existing tickets; confirm only new or changed slices and dependencies before publication |

Choose the scope/risk route in step 1 before calling planning skills. For a local spec, read its supplied path directly; setup is needed only if a later step needs a tracker. A small low-risk feature or fix uses the short spec without forcing setup, an interview or tickets. An existing issue or long spec alone does not force a heavier route. With an existing spec, resolve substantive gaps before building, but do not publish a duplicate spec just to fit this flow.

Calling a skill is not a new approval gate. Pass explicit prior approvals into it, with the content they covered. A confirmed seam need not be confirmed again unchanged. An approval of ticket breakdowns does not automatically approve new acceptance criteria or a different PR grouping. Bundle related decisions when practical; ask only about what remains unsettled.

## Save from the start

Create `.story/<slug>/progress.md` before calling setup or planning skills. Choose the issue number plus a short name when known, otherwise just a short name; use the same folder for the whole run. Store:

- The original request, source issue URL or local path, and current branch
- Current phase and next action: setup, clarification, spec, tickets, addendum, build, review, evidence or ship
- Route and risk reason; selected checks/owners and phase timestamps from `verification.md`
- Decisions and pending questions, plus what the user actually approved; associate approvals with a local spec revision number, starting at 1
- Created artifact references: setup file paths, spec issue/path, and ticket IDs or links per group
- A pending publication before each external create operation; replace it with the returned ID/URL immediately after success
- Per-group progress: branch, last completed step and PR URL; CLI session IDs when applicable

Save drafts and decisions in `spec.md` even before approval, clearly marked as drafts. Update the checkpoint before waiting for the user and after each completed step or publication. Include setup files changed by this run in its recorded work, so resume does not mistake them for unrelated changes.

Keep the checkpoint concise: store decisions and references, not transcripts, logs or full ticket bodies. Read ticket details for the active group. For any tracker lookup or recovery search, request capped pages (at most 100), filter on the server and inspect one page at a time. If the tracker cannot page, report that limit rather than silently loading its entire collection.

## Resume and changed requirements

Read the saved request, decisions and references before dispatching work. Check the referenced artifacts and continue at the first unfinished step; an unfinished spec or partial ticket publication must not jump straight to building. Existing runs without planning checkpoints may reuse an explicitly approved saved spec, but do not infer approval merely because a file exists.

When a publication's result is uncertain, check the tracker for the pending artifact using the recorded source, parent and title before retrying. Reuse the existing ID if found. If absence cannot be established, ask the user rather than creating a possible duplicate. Apply this to each ticket and PR, not only the parent spec.

If requirements changed, increment the local spec revision, identify affected tickets, groups, tests and evidence, and mark those steps for rework. Retain approvals for unchanged decisions; obtain approval for the changed scope before publishing updates or resuming affected implementation. Preserve existing issue and PR identities. If the original skill only creates artifacts, make the explicitly approved update through the configured tracker tools instead of running its create step again. Never close or replace parent issues as part of replanning.
