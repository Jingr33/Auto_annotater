---
description: Stage, commit, push, and create PR
agent: sync
subtask: true
---

Stage all changes, commit with descriptive message, push, and create PR if not exists.

## Setup

1. Load the **project-management** skill.
2. Load the **manager** skill — it provides the `Fetch dev item` capability.
3. Load the **github-operations** skill.

## Workflow

### 1. Check git status

Run `git status` to see all changes.

### 2. Identify task

- Read current branch name (e.g. `feature/42-add-data-loader`)
- Extract issue number from it (e.g. `42`)
- Fetch the issue using manager skill's `Fetch dev item`:
  ```bash
  gh issue view <number> --repo Jingr33/Auto_annotater --json title,body
  ```
- Parse Type from `## Metadata` section
- Parse Title from issue title
- If `dev_support/<issue-number>/summary.md` exists, use it as PR body

### 3. Stage all changes

```bash
git add -A
```

### 4. Generate commit message

Analyze staged changes and generate a descriptive commit message:
- Use type from issue metadata (feature/bug/hotfix)
- Include issue number
- Add short description based on what changed
- Format: `<type>: <short-description> (#<issue-number>)`

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
  - PR title format: `<type>/<issue-number>: <title>` (from `.opencode/templates/pr-title.md`)
  - PR body: content of `dev_support/<issue-number>/summary.md` if it exists, otherwise issue body
  - Command: `gh pr create --title "<title>" --body "<body>"`
