# Choosing the Base Branch

The base decides which commits reviewers see. A wrong base either buries the work under unrelated commits or hides part of it, so check the suggestion before trusting it.

## Order

1. An open PR from this branch already exists: keep its base, unless the user named another
2. The branch the user named
3. `base.suggested` from `pr_context.py`

## How the script suggests

It picks the remote branch this one has the fewest commits beyond, which follows how the branch was actually cut:

| Situation | Suggested base |
| --- | --- |
| cut from `main` | `main` |
| cut from `dev` while `dev` is ahead of `main` | `dev` |
| stacked on another feature branch | that branch, so the PR shows only this branch's own commits |
| on a long-lived branch (`main`, `dev`, `uat`, `prod`, …) | the nearest other long-lived branch (`dev` → `main`, `main` → `prod`), always marked ambiguous |

On a tie, long-lived branches beat feature branches cut from the same commit, then the branch whose tip sits at the fork point wins. Feature branches left on the remote after merging are never offered from a long-lived branch.

## Checks

- **Stacked base** (not the default branch or a long-lived one): find that branch's own PR (see `cli.md`, "Find PRs"). If it is open, link it in the description ("Depends on #12" / "Depends on !12") and say it must merge first. If it was already merged, its branch is dead: suggest the branch it merged into instead.
- **`base.ambiguous`**: the graph can't tell the team's flow: two long-lived branches sit at the same fork point (`dev` == `main`), or this is a promotion PR. Look at where recent PRs went (`cli.md`, "Recent merged PRs"): if feature branches usually go to `dev`, or `dev` usually goes to `main`, recommend that. Then ask the user instead of guessing.
- **Promotion PR on a long-lived branch**: fine when the user meant to promote (`dev` → `main`, `main` → `prod`). If they committed feature work straight onto it, say so: a feature PR needs its own branch, and you never create or switch branches yourself.
- **Too many commits**: if the range holds commits that clearly aren't this work (dozens of unrelated subjects), the base is wrong. Show `base.candidates` and ask.
