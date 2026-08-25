---
description: Commit, push, and create PR if not exists
agent: sync
subtask: true
---

Push the current branch to the remote.

## Setup

1. Load the **project-management** skill.
2. Load the **manager** skill — it provides the `Fetch dev item` capability.

## Workflow

### 1. Identify the task

- Read the current branch name (e.g. `feature/42-add-data-loader`).
- Extract the issue number from it (e.g. `42`).
- Fetch the issue using manager skill's `Fetch dev item`:
  ```bash
  gh issue view <number> --repo Jingr33/Auto_annotater --json title,body
  ```
- Parse Type and Title from the issue.

### 2. Read task metadata

- If `dev_support/<issue-number>/summary.md` exists, this will be the PR body.

### 3. Commit if needed

Check `git status`. If there are uncommitted changes:
  - `git add` the relevant files
  - `git commit -m "<type>: <title> (#<issue-number>)"`

### 4. Push

Push the branch:
```bash
git push origin <current-branch>
```

### 5. Create PR if not exists
  - Check: `gh pr list --head <current-branch> --json number`
  - If no PR exists, create one:
    - PR title format: `<type>/<issue-number>: <title>` (use `.opencode/templates/pr-title.md`)
    - PR body: content of `dev_support/<issue-number>/summary.md` if it exists, otherwise issue body
    - Command: `gh pr create --title "<title>" --body "<body>"`
