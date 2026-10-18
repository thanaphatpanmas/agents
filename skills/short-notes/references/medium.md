# Git

## Start a project

```bash
git clone REPO_URL
cd REPO_NAME
```

- `REPO_URL` → link from the Code button on GitHub (HTTPS or SSH)
- `REPO_NAME` → folder created by the clone (same as the repo name)

## Create a new branch

```bash
git switch -c BRANCH_NAME
```

- Creates the branch from where you are and switches to it
- Name it after the work: `feature/login`, `fix/navbar`
- Back to main: `git switch main`

## Commit work

```bash
git add .
git commit -m "feat: MESSAGE"
```

- `git add .` → stages every change in the current folder (pick files: `git add FILE`)
- Start the message with the type of change: `feat`, `fix`, `docs`

## Fix the last commit

### Add a forgotten file (keep the message)

```bash
git add FILE
git commit --amend --no-edit
```

- Change the message too: `git commit --amend -m "MESSAGE"`

### Undo the commit (keep the code)

```bash
git reset --soft HEAD~1
```

- `HEAD~1` → the commit before the current one
- Changes stay staged → edit and commit again

### Undo the commit and discard the code

```bash
git reset --hard HEAD~1
```

- Careful: uncommitted work is lost for good
- Use only when you're sure you don't want that work

## Push to remote

```bash
git push -u origin BRANCH_NAME
```

- `-u` → remembers the remote branch, so next time plain `git push` works

### Overwrite the remote after fixing a pushed commit

```bash
git push --force-with-lease
```

- Use after `--amend` or `reset` on a commit that's already pushed
- Safer than `--force` → refuses if someone pushed since your last fetch

## Caveats

- Never commit `.env` → add it to `.gitignore` before `git add`
