---
description: Commit, push, and create PR if not exists
agent: sync
subtask: true
---

Push the current branch to the remote.

## Workflow

### 1. Load project-management skill
Understand the task structure in `dev_items/`.

### 2. Identify the task
Read the current branch name (e.g. `feature/001-add-data-loader`).
Extract the task number from it (e.g. `001`).
Locate the matching `dev_items/<task-number>-*/` folder.

### 3. Read task metadata
Read `task.md` — get `type` (feature/bug/hotfix) and `title` from frontmatter.
Read `summary.md` — this will be the PR body.

### 4. Commit if needed
Check `git status`. If there are uncommitted changes:
  - `git add` the relevant files
  - `git commit -m "<type>: <title> (#<task-number>)"`

### 5. Push
Push the branch:
```bash
git push origin <current-branch>
```

### 6. Create PR if not exists
  - Check: `gh pr list --head <current-branch> --json number`
  - If no PR exists, create one:
    - PR title format: `<type>/<task-number>: <title>` (use `.opencode/templates/pr-title.md`)
    - PR body: content of `summary.md`
    - Command: `gh pr create --title "<title>" --body "<body>"`
