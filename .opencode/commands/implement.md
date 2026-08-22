---
description: Implement a task from GitHub Issues (e.g. /implement 42)
agent: dev
subtask: true
---

Implement task from GitHub Issue $ARGUMENTS.

## Setup

1. First, load the **project-management** skill — it defines the status system and rules.
2. Load the **manager** skill — it provides the `Fetch dev item` capability.

## Workflow

### 1. Fetch the issue

Identify the task using the manager skill's `Fetch dev item` capability:

- **Primary**: Use the issue number from `$ARGUMENTS`.
- **Fallback**: If no argument given, extract issue number from current branch name (`<type>/<number>-<slug>`).

Fetch the issue:
```bash
gh issue view <number> --repo Jingr33/Auto_annotater --json title,body,state
```

Parse the issue body to extract:
- Type and Scope from `## Metadata` section
- Description, Acceptance Criteria from the body

### 2. Pre-flight

- Check the current project status via the manager skill's `Get project status`.
- Respect the status rules from the project-management skill.
- If status is `Blocked`, stop and tell the user.
- If status is `Done`, stop and tell the user.

### 3. Git setup

- Before starting implementation, set the GitHub Project status to `In progress`:
  ```bash
  gh project item-edit 3 --owner Jingr33 --url <issue_url> --field "Status" --value "In progress"
  ```
- Verify the status update when possible. If the status update cannot be made, tell the user before continuing.
- Once set to `In progress`, leave the issue in that status throughout investigation, implementation, testing, documentation, and completion.
- `git checkout master` (if this fails, stop and tell the user).
- Create branch: `git checkout -b feature/<issue-number>-<slug>` (kebab-case).
  Example: `feature/42-add-data-loader`

### 4. Implement

- Follow the appropriate coding standards:
  - Python backend code: `instructions/coding-standards-python.md`
  - React TypeScript frontend code: `instructions/coding-standards-react.md`
- You may introduce new packages. **Do not** install them, except `@mui/material`, which you **may** install via npm. Add every new dependency to the relevant requirements/package file.

### Styling
- Use **Material UI only** (`@mui/material`).

### 5. Document

- Review the changes you made. Update relevant documentation in `docs/` if anything changed.

### 6. Finish

- Leave the GitHub Project status as `In progress`.
- Create `summary.md` in `dev_support/<issue-number>/` using `.opencode/templates/summary.md`.
- Post the summary as a comment to the issue:
  ```bash
  gh issue comment <number> --repo Jingr33/Auto_annotater --body "<summary content>"
  ```
- **Never commit** — leave the changes uncommitted in the working tree.

### 7. Push & PR (only if user says "force")

- `git push origin <branch>`
- Check `gh pr list --head <branch>` — skip if PR exists.
- Create PR with `gh pr create --title "<title>" --body "<summary content>"`

## Important: no commits
- Never run `git commit`. The implementation must be left as uncommitted working-tree changes for the user to review and commit themselves.
