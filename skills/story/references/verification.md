# Verification, execution and elapsed time

Use this when choosing checks and before starting test, build, lint, type-check or browser commands. The main session owns the plan and final evidence; separate agents do not each need their own full-suite run.

## Select checks by impact

Record a compact table in `progress.md`: check/command, covered behavior or package, owner, result/log path and the code state it verified. Include repo/user-mandated checks even on the small route. A full suite is appropriate for a shared foundation change with uncertain dependents, not automatically for every local UI addition. Never weaken assertions, disable tests, change timeouts or skip mandatory checks to make the run shorter or green.

Choose the smallest existing boundary that reliably proves the behavior, plus affected regression tests. An unchanged backend contract does not require new server tests just because a dialog calls it. A changed authorization or deletion rule does require the relevant server-side checks, even when the UI diff is tiny. Use existing type-check/lint scripts at their supported scope; if only a package-wide command is reliable, run that once at final verification.

Record omitted suites and why the selected checks cover the change. Do not call scoped results a full-suite pass. If impact cannot be bounded with confidence, broaden verification instead of guessing.

## One shared execution slot

The main session schedules heavy commands across all roles on the machine:

- One test/build/type-check/lint/browser-verification run at a time. Retain the existing worker caps (at most 2; Playwright uses `--reporter=line`). Source reading and writing may run in parallel when files do not overlap
- During implementation, Dev alone may run scoped red/green tests. An E2E author writes test files and returns them unrun; the main session executes them after Dev finishes. This also works for headless CLI roles without a permission-message loop
- Security receives the slot only after build/test runs finish; it can run its in-scope finding tests. Return the slot before sending fixes to Dev. Evidence receives it only for missing captures after verification
- Reuse a healthy app/test database when compatible. Record the process owner; only stop processes this story started, and only when no remaining checks need them. Never stop a user's server or reset shared fixtures while another run uses them
- If an unrelated run is already consuming resources, defer your heavy command and report the queue wait. Do not kill it or increase worker counts

Grant the slot in each brief as `scoped tests now` or `author only; return commands unrun`. This is a scheduling rule, not a new lock service or dependency. A role without the slot returns work and pending commands; it does not poll or start its own server.

## Avoid duplicate checks without using stale results

Dev's scoped passes support implementation progress. The main session reads the raw output and diff rather than repeating every pass at the handoff. Final verification belongs to the main session after implementation and review fixes are complete, using the recorded plan; preserve CI and hooks required by the repo.

A passing main-session check can count toward final verification if no relevant code, dependency, configuration, fixture or environment changed after it ran. Record the file set or diff/commit identity with its result; commit SHA alone is insufficient for uncommitted edits. If relevance is unclear, rerun the check. Invalidate affected checks after a fix, not every unrelated result. A hook that modifies code also invalidates affected results and evidence.

When a test fails, distinguish a behavior regression from app startup, fixture or resource failure using the output. Fix the cause before retrying; do not loop until a flaky run passes. Keep the original failure in the report, give the reason for a rerun and verify under the original test configuration. After three unresolved fix/verification rounds, stop and show the user the evidence. Timings never justify ignoring a failure.

## Capture evidence during verification

For UI changes, use the same browser pass to verify behavior and capture its relevant visible states. Save selected screenshots under `.story/<slug>/screenshots/` before ephemeral test output is cleared. Use `roles/evidence.md` for evidence quality and reporting. Existing captures remain usable only while the relevant code, test state and viewport still match; a screenshot is not proof of an API assertion.

## Measure the phases

In `progress.md`, record phase/owner, start and end timestamps with timezone, elapsed duration and outcome. Start/end entries belong at phase transitions, command execution, agent dispatch/completion and user wait/resume; don't add timing tool calls around every file read or test case. Use actual clock/tool timestamps. A missing interval stays `unknown`, not an estimate presented as fact.

Distinguish active work, command runtime, queue waits and user waits. Attach command durations from the runner when available, and explain each repeated command. For parallel agents, their durations overlap: report wall-clock elapsed and their individual durations rather than summing them as total elapsed. Existing runs without timestamps cannot provide a measured speed comparison.
