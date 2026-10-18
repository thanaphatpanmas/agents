# Git

## Start a project

```bash
git clone REPO_URL
cd REPO_NAME
```

## Create a new branch

```bash
git switch -c BRANCH_NAME
```

- Back to main: `git switch main`

## Commit work

```bash
git add .
git commit -m "feat: MESSAGE"
```

## Fix the last commit

### Add a forgotten file (keep the message)

```bash
git add FILE
git commit --amend --no-edit
```

### Undo the commit (keep the code)

```bash
git reset --soft HEAD~1
```

### Undo the commit and discard the code

```bash
git reset --hard HEAD~1
```

- Careful: uncommitted work is lost for good

## Push to remote

```bash
git push -u origin BRANCH_NAME
```

### Overwrite the remote after fixing a pushed commit

```bash
git push --force-with-lease
```

## Caveats

- Never commit `.env` → add it to `.gitignore`
