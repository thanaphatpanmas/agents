# Prepare the Branch Before Push

Fetching updates remote-tracking refs; it doesn't integrate code. Keep fetching, choosing an integration strategy and pushing separate so local pull configuration cannot silently choose merge or rebase. Use the remote, current branch and settled PR base from steps 2–3, not an upstream that may point at another branch.

## Preconditions

- Use a successful fresh fetch. If it fails, prepare PR text only; report that synchronization and mergeability were not verified, and don't integrate, push or create/update the PR.
- Confirm the base before changing history. For stacked work, use the confirmed parent branch, not the default branch.
- Check `git -C <repo> status --porcelain` before integration. Require a clean index and worktree, including untracked files, and no operation in progress. Don't auto-stash, discard or commit user changes. If the user excludes uncommitted work from the PR, read-only checks may continue, but integration must wait until that work is preserved and the worktree is clean.
- Record the starting HEAD before every integration, including fast-forward, merge and rebase, so the final result can be reviewed against it.

## 1. Synchronize the Same-Named Remote Branch

Use `push.behind` and `push.unpushed` against `<remote>/<branch>`, not against the PR base:

| State | Action |
| --- | --- |
| Remote branch absent, or `push.behind` is 0 | Nothing to integrate from this ref |
| Behind, with no local-only commits | `git -C <repo> merge --ff-only <remote>/<branch>` |
| Both behind and ahead | Merge `<remote>/<branch>` by default, using the procedure below; resolve clear conflicts without asking |

If the remote branch was force-updated or the history is unexpected, inspect it and ask before combining histories. Don't use a merge to conceal a rewritten history.

## 2. Check Against the PR Base

Check the merge in PR direction without changing HEAD, the index or the worktree:

```bash
git -C <repo> merge-tree --write-tree <remote>/<base> HEAD
```

Exit 0 means no textual conflicts; exit 1 means conflicts, whose paths and messages are in the output. Other failures are errors, not evidence of a conflict. If this command is unsupported, use an isolated temporary worktree for the check or report the limitation; don't trial-merge into a dirty worktree. A clean merge doesn't prove runtime compatibility.

- **No conflicts, and no repo/user requirement to update the branch:** continue without integrating the base just because it advanced.
- **Conflicts, or an explicit requirement to include the latest base:** integrate `<remote>/<base>` into an ordinary feature branch using the strategy below.
- **Promotion PR from a long-lived branch, such as `dev` → `main`:** check and report conflicts, but don't merge or rebase the target back into the source automatically. If integration is needed, explain the consequence and ask for the team's strategy first.

## 3. Choose the Strategy

Default to **merge**, especially for a published or shared branch, because it preserves existing commit IDs. A PR request authorizes necessary local integration and its integration commit; don't ask again just because an unambiguous merge is needed.

Use **rebase** only when requested by the user or required by the repo's documented workflow, and after confirming that every commit it would rewrite is unpublished and that no shared or stacked branch depends on those commits. Then run `git -C <repo> rebase <ref>`, with `<ref>` being the remote branch or base being integrated. Don't infer that commits are unpublished merely because this branch has no remote ref. If publication or dependent branches are uncertain, or rebase would rewrite published commits, explain the issue and ask how to proceed before rebasing. Don't force-push under this skill; a workflow requiring it needs separate explicit authorization.

For a merge, use:

```bash
git -C <repo> merge --no-commit --no-ff <ref>
```

This leaves a successful non-fast-forward merge available for review before committing. An already integrated ref is a no-op; don't create an empty commit. Inspect errors before deciding that a nonzero exit is a resolvable conflict.

## 4. Resolve Conflicts or Ask

Read each conflicting hunk, both sides' changes and the affected callers/tests before editing.

- **Resolve without asking** when the intended combined result is established by code, tests and requirements, such as independent additions that both need to remain, or adapting a call to an explicitly renamed API while preserving both changes. Regenerate generated files with the repo's existing tool after resolving their sources.
- **Ask before deciding** when the sides imply different business rules, API contracts, permissions, data/migration semantics, delete-versus-keep choices or unclear requirements. Name the paths, explain the competing behaviors, recommend an option and wait before applying a disputed resolution. Resolve other independent, clear hunks while waiting, but don't finish integration or push until the decision arrives.

Don't choose an entire side with `ours`/`theirs`, drop changes or weaken tests just to clear conflicts. If the user cancels integration, abort only the merge/rebase started by this run; don't reset or abort a pre-existing operation.

## 5. Verify and Finish

After any integration, including fast-forward, review the full result against the recorded starting HEAD and run affected tests and required repo checks. For pending resolutions, stage only files changed by this integration, with explicit paths. Check that `git -C <repo> diff --name-only --diff-filter=U` is empty, inspect the staged diff, and run `git -C <repo> diff --cached --check`. For rebase, check each resolved step before `git -C <repo> rebase --continue`, then verify the final result; don't use `--skip` to bypass a conflict.

For a pending merge, commit only after verification, using the repo's merge-message convention or `chore: merge <ref> into <branch>`. Don't invoke the `commit` skill to stage unrelated files. If checks fail, investigate within scope and don't push; if checks can't run, report the limitation and ask before pushing the unverified integration.

After completion, confirm a clean worktree and no operation in progress, rerun the base conflict check and refresh `pr_context.py <repo> --base <base>`. Read the final branch diff for the PR description and record the integration, any meaningful resolutions and the checks actually run.
