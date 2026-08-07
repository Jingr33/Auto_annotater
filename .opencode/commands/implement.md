---
description: Implement a task from dev_items/ (e.g. /implement 001)
agent: dev
subtask: true
---

Implement task $ARGUMENTS from `dev_items/`.

## Setup

1. First, load the **project-management** skill — it defines the status system and rules.
2. Identify the task folder: find `dev_items/$ARGUMENTS-*` (e.g. `001-*`).

## Workflow

### 1. Pre-flight
- Read `task.md` frontmatter. Respect the status rules from the skill.

### 2. Git setup
- `git checkout master` (if this fails, stop and tell the user).
- Create branch: `git checkout -b feature/<TASK>-<short-description>` (kebab-case).
  Example: `feature/001-add-data-loader`

### 3. Implement
- Transition status to `commited`.
- Follow the appropriate coding standards:
  - Python backend code: `instructions/coding-standards-python.md`
  - React TypeScript frontend code: `instructions/coding-standards-react.md`
- You may introduce new packages. **Do not** install them. Add every new dependency to the relevant requirements/package file.

### 4. Document
- Review the changes you made. Update relevant documentation in `docs/` if anything changed.

### 5. Finish
- Transition status to `done`.
- Write `summary.md` in the task folder using `.opencode/templates/summary.md`.
- `git add` + `git commit` with a descriptive message.

### 6. Push & PR (only if user says "force")
- `git push origin <branch>`
- Check `gh pr list --head <branch>` — skip if PR exists.
- Create PR with `gh pr create --title "<title>" --body "<summary.md content>"`
