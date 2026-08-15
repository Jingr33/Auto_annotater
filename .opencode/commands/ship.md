---
description: Stage, commit, push, and create PR
agent: sync
subtask: true
---

Stage all changes, commit with descriptive message, push, and create PR if not exists.

## Setup

1. Load the **project-management** skill.
2. Load the **github-operations** skill.

## Workflow

### 1. Check git status

Run `git status` to see all changes.

### 2. Identify task

- Read current branch name (e.g. `feature/001-add-data-loader`)
- Extract task number from it (e.g. `001`)
- Locate matching `dev_items/<task-number>-*/` folder
- Read `task.md` — get `type` and `title` from frontmatter
- Read `summary.md` — this will be the PR body (if exists)

### 3. Stage all changes

```bash
git add -A
```

### 4. Generate commit message

Analyze staged changes and generate a descriptive commit message:
- Use type from task.md (feature/bug/hotfix)
- Include task number
- Add short description based on what changed
- Format: `<type>: <short-description> (#<task-number>)`

### 5. Commit

```bash
git commit -m "<generated-message>"
```

### 6. Push

```bash
git push origin <current-branch>
```

### 7. Create PR if not exists

- Check: `gh pr list --head <current-branch> --json number`
- If no PR exists, create one:
  - PR title format: `<type>/<task-number>: <title>` (from `.opencode/templates/pr-title.md`)
  - PR body: content of `summary.md`
  - Command: `gh pr create --title "<title>" --body "<body>"`
