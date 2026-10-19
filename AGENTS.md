# Coding Principles

Global defaults for every project. Explicit user requests and project-level AGENTS.md / CLAUDE.md take precedence. For trivial tasks, use judgment.

When principles conflict: correctness & security > not breaking existing behavior > task scope > readability > brevity & DRY.

## 1. Think Before Coding

**Investigate first. Don't assume. Surface tradeoffs.**

- Before editing, read the relevant code and conventions, and identify affected callers, tests, fixtures, configuration, and exports.
- Don't pick an interpretation silently. Ask when ambiguity materially affects correctness or design; otherwise state your assumption and proceed.
- If a simpler approach exists, say so. Push back when warranted.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features, flexibility, or configurability beyond what was asked (YAGNI).
- Reuse existing utilities and patterns first. Extract shared code only for real duplication that changes for the same reason (DRY) — no abstractions for single-use code.
- Prefer the standard library, platform, or existing dependencies over adding new ones for straightforward functionality.
- Fewer lines is a benefit, not a goal. If 200 lines could clearly be 50, rewrite — but never trade readability or completeness for brevity.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Readability & Style

**Match the surrounding code.**

- Follow the project's existing style and conventions (formatting, naming, structure), even if you'd do it differently.
- Names explain what things do. Avoid vague names and unclear abbreviations; conventional ones (`id`, `url`, `i`, `ctx`) are fine.
- Avoid deep nesting. Prefer guard clauses and early returns.
- Give new modules a single clear responsibility. Don't split existing code unless the task needs it.
- Comments explain WHY, not WHAT, in one short line. No multi-line blocks unless the project's doc-comment convention (JSDoc, docstrings) calls for them.

## 4. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

- Make the smallest complete change: update everything it affects, nothing more.
- Don't "improve" adjacent code, comments, or formatting. Don't refactor what isn't broken.
- Remove imports/variables/functions that YOUR changes made unused. Mention unrelated dead code — don't delete it.

The test: every changed line should trace directly to the user's request.

## 5. Correctness & Security

**Correct and safe before short or clever.**

- Handle errors at system boundaries (user input, I/O, external APIs). No error handling or fallbacks for scenarios that can't happen.
- Preserve existing validation, error handling, security, and accessibility behavior.
- Validate untrusted input; use parameterized queries and context-aware output encoding (OWASP Top 10).
- Never hardcode, log, or commit secrets, tokens, or personal data.
- Ask before destructive or irreversible actions (`rm -rf`, `git reset --hard`, force-push, dropping data).

## 6. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

Test new non-trivial logic with the project's existing test setup and check that affected behavior still works. No test setup? Verify another way (run it, type-check, lint) — don't add a framework unasked. Never weaken, skip, or delete a test to make it pass; if a test looks wrong, say so.

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

When done, briefly state what changed, what wasn't verified, and any known limitations or risks.
