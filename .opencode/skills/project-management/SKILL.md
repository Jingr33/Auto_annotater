---
name: project-management
description: Project management system for task tracking via GitHub Issues and GitHub Projects. Defines status lifecycle: Backlog, Ready, In progress, Blocked, Done. Load this skill when working with task issues.
license: MIT
compatibility: opencode
---

## Task Structure

Tasks are GitHub Issues in the `Jingr33/Auto_annotater` repository, tracked in GitHub Project number 3.

Each issue body follows this structure:

```markdown
## Metadata
- **Type**: feature       # feature | bug | hotfix
- **Scope**: backend      # backend | frontend | both

## Description



## Acceptance Criteria

- [ ]

## Out of Scope
```

For `bug` / `hotfix` types, the body also includes:

```markdown
## Repro Steps

1.
2.

## Expected Behavior



## Actual Behavior
```

## Configuration

- **Repository**: `Jingr33/Auto_annotater`
- **Project Number**: 3
- **Project Owner**: Jingr33

## Status Enum

Every task has exactly one status, managed via the GitHub Project "Status" field.

| Status | Meaning | Set by |
|--------|---------|--------|
| `Backlog` | Not yet prioritized | User (task creator) |
| `Ready` | Ready for implementation | User or agent |
| `In progress` | Being worked on right now | Agent when starting implementation |
| `Blocked` | Cannot proceed — depends on another task | Agent when blocked |
| `Done` | Implemented and shipped | Agent on completion |

## Status Definitions (for agents)

### `Backlog`
- This task exists but is not yet prioritized.
- No ongoing work on it.
- Do **not** start implementing a backlog task unless the user explicitly says so.

### `Ready`
- This task is ready to be picked up.
- There is **no** ongoing work on it.
- Any agent can start implementing it.
- The task description is in the issue body.

### `In progress`
- An agent has started working on this task.
- A branch `<type>/<issue-number>-<slug>` should exist.
- Other agents should **not** start working on the same task.
- If you encounter an `In progress` task, check if it is stale (no recent git activity on its branch). If stale, ask the user whether to take over.

### `Blocked`
- This task cannot proceed because it depends on another task.
- The issue body or a comment should explain what is blocking it.
- Do **not** start implementing a blocked task. Tell the user what is blocking it.

### `Done`
- Implementation is finished.
- All changes are committed and pushed.
- A summary comment exists on the issue.
- Do **not** modify a `Done` task unless the user explicitly asks.

## Status Transitions

Allowed transitions:

```
Backlog ──> Ready ──> In progress ──> Done
  │                      │
  │                      └──> Blocked
  │                            │
  └──> Ready <─────────────────┘  (user resolves blocker)
```

- `Backlog` -> `Ready`: User prioritizes the task.
- `Ready` -> `In progress`: Agent starts work. Also creates the feature branch.
- `In progress` -> `Done`: Agent finishes, commits, pushes, writes summary.
- `In progress` -> `Blocked`: Agent hits a dependency blocker.
- `Blocked` -> `Ready`: User resolves the blocker.
- `Blocked` -> `In progress`: User unblocks and agent resumes.
- `Done`: **Terminal state**. A done task is not reopened. If a new issue appears, create a new task.

## Scope Field

The `Scope` field in the issue metadata indicates which part of the codebase the task targets:

| Scope | Meaning | Coding standards |
|-------|---------|-----------------|
| `backend` | Python code in `src/backend/` | `coding-standards-python.md` |
| `frontend` | React TS code in `src/frontend_pro/` | `coding-standards-react.md` |
| `both` | Spans both backend and frontend | Both standards apply |

## dev_support/ Folder

Generated files during development (fix-cr summaries, implementation notes, etc.) go in `dev_support/<issue-number>/`. This folder is gitignored.

When a summary file is created in `dev_support/`, also post its content as a comment to the corresponding GitHub Issue:

```bash
gh issue comment <number> --repo Jingr33/Auto_annotater --body "<content of summary file>"
```

## Rules for All Agents

1. **Always read the issue body first** before acting on a task. Use the manager skill's `Fetch dev item` capability.
2. **Never change status without good reason** — each transition must follow the workflow above.
3. **Respect `In progress`** — if another agent has started the task, do not interfere unless user says so.
4. **Respect `scope`** — use the correct coding standards for the target component.
5. **Write the summary** — when reaching `Done`, create a summary file in `dev_support/<issue-number>/summary.md` using `.opencode/templates/summary.md`, then post it as a comment to the issue.
