# Git

## Start a project

```bash
git clone REPO_URL
cd REPO_NAME
```

- `REPO_URL` → link from the Code button on GitHub (HTTPS or SSH)
- `REPO_NAME` → folder created by the clone (same as the repo name)
- Cloning over SSH needs your SSH key added to GitHub first, otherwise `Permission denied (publickey)`

## Create a new branch

```bash
git switch -c BRANCH_NAME
```

- Creates the branch from where you are and switches to it
- Name it after the work: `feature/login`, `fix/navbar`
- Back to main: `git switch main`
- Alternative: `git checkout -b BRANCH_NAME` (older command, same result)

### Check which branch you're on

```bash
git branch
```

```text
* feature/login
  main
```

- `*` → current branch

## Commit work

```bash
git add .
git commit -m "feat: MESSAGE"
```

- `git add .` → stages every change in the current folder (pick files: `git add FILE`)
- Start the message with the type of change: `feat`, `fix`, `docs`

### Check before committing

```bash
git status
```

```text
On branch feature/login
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   src/login.ts
```

- Files under `Changes to be committed` → go into this commit
- Unstage a file: `git restore --staged FILE`

## Fix the last commit

### Add a forgotten file (keep the message)

```bash
git add FILE
git commit --amend --no-edit
```

- Change the message too: `git commit --amend -m "MESSAGE"`
- Already pushed → push again with `--force-with-lease`

### Undo the commit (keep the code)

```bash
git reset --soft HEAD~1
```

- `HEAD~1` → the commit before the current one (`HEAD~2` = two back)
- Changes stay staged → edit and commit again

### Undo the commit and discard the code

```bash
git reset --hard HEAD~1
```

> [!WARNING]
> Uncommitted work is lost for good and can't be recovered

- The dropped commit itself is recoverable: find its hash with `git reflog`, then `git reset --hard HASH`
- Already pushed → use `git revert HEAD` instead: a new commit that undoes it without rewriting history

## Push to remote

```bash
git push -u origin BRANCH_NAME
```

- `-u` → remembers the remote branch, so next time plain `git push` works

### Push rejected because the remote has new commits

```text
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'REPO_URL'
```

```bash
git pull --rebase
git push
```

- `--rebase` → replays your commits on top of the new ones, no extra merge commit
- On conflict: fix the files → `git add FILE` → `git rebase --continue`

### Overwrite the remote after fixing a pushed commit

```bash
git push --force-with-lease
```

- Use after `--amend` or `reset` on a commit that's already pushed
- Safer than `--force` → refuses if someone pushed since your last fetch
- Never on a shared branch like `main`

## Caveats

- Never commit `.env` → add it to `.gitignore` before `git add`
- Already committed `.env` → `git rm --cached .env`, then commit; the values stay in history → rotate the keys

## References

- [git switch](https://git-scm.com/docs/git-switch)
- [git reset](https://git-scm.com/docs/git-reset)
- [git push](https://git-scm.com/docs/git-push)
