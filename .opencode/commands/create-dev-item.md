---
description: Create a new dev item as a GitHub Issue with feature branch
subtask: true
---

Load the `manager` skill.

Parse the prompt:

- Everything after `/create-dev-item` is the task description.
- Extract the title (first line or first sentence).
- Optionally look for `--type <type>` to override default `feature`.
- Optionally look for `--scope <backend|frontend|both>` to set the target component.

### 1. Build the issue body

Read `.opencode/templates/task.md` and fill it with:
- `Type` from parsed `--type` (default `feature`)
- `Scope` from parsed `--scope` (default `backend`)
- `Description` from the task description text

If the resolved type is `feature`, drop the bug-only sections (`## Repro Steps`, `## Expected Behavior`, `## Actual Behavior`) from the body. Keep them only for `bug` / `hotfix` types.

### 2. Create the GitHub Issue

```bash
gh issue create --repo Jingr33/Auto_annotater --title "<title>" --body "<body>"
```

Capture the issue number from the output.

### 3. Add issue to GitHub Project

```bash
gh project item-add 3 --owner Jingr33 --url <issue_url>
```

### 4. Set initial status

```bash
gh project item-edit 3 --owner Jingr33 --url <issue_url> --field "Status" --value "Ready"
```

### 5. Create and switch to branch

Build the slug from the title: lowercase, spaces -> hyphens, strip special chars.

```bash
git checkout -b <type>/<issue-number>-<slug>
```

### 6. Print confirmation

Show: issue number, issue URL, branch name, type, scope.

### 7. STOP. NEVER IMPLEMENT.
The `/create-dev-item` command ONLY creates the issue and branch. Implementation is a separate step done later by the user or in a different session.
