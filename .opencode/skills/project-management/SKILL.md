---
name: project-management
description: Project management system for task tracking via dev_items/ folder. Defines status lifecycle: new, commited, done, block. Load this skill when working with dev_items/ tasks.
license: MIT
compatibility: opencode
---

## Task Folder Structure

Tasks live in `dev_items/` at the project root. Each task has its own folder:

```
dev_items/
  001-add-data-loader/
    task.md       # Task metadata + description (YAML frontmatter)
    summary.md    # Implementation summary (created by agent on completion)
  002-fix-memory-leak/
    task.md
    summary.md
  ...
```

Folders are named `NNN-short-description`. The leading number is the **task ID** — this is how agents identify the task. The rest is human-readable.

Use `.opencode/templates/task.md` as the canonical template for `task.md`. The file uses YAML frontmatter:

```markdown
---
title: <task title>
type: feature       # feature | bug | hotfix
status: new         # new | commited | done | block
scope: backend      # backend | frontend | both
---

## Description



## Acceptance Criteria

- [ ]

## Out of Scope
```

## Status Enum

Every task has exactly one status. The status field must contain one of these four values (lowercase only):

| Status | Meaning | Set by |
|--------|---------|--------|
| `new` | Ready for implementation | User (task creator) |
| `commited` | Being worked on right now | Agent when starting implementation |
| `done` | Implemented and committed | Agent on completion |
| `block` | Cannot proceed — depends on another task | Agent when blocked |

## Status Definitions (for agents)

### `new`
- This task is ready to be picked up.
- There is **no** ongoing work on it.
- Any agent can start implementing it.
- The task description is in the body of `task.md`.

### `commited`
- An agent has started working on this task.
- A branch `feature/<TASK>-<desc>` should exist.
- Other agents should **not** start working on the same task.
- If you encounter a `commited` task, check if it is stale (no recent git activity on its branch). If stale, ask the user whether to take over.

### `done`
- Implementation is finished.
- All changes are committed on the feature branch.
- `summary.md` exists in the task folder with a description of what was done.
- Do **not** modify a `done` task unless the user explicitly asks.

### `block`
- This task cannot proceed because it depends on another task.
- The `task.md` body or a note in the folder should explain what is blocking it.
- Do **not** start implementing a blocked task. Tell the user what is blocking it.

## Status Transitions

Allowed transitions:

```
new ──> commited ──> done
  │                    │
  └──> block           └──> (no further transitions)
```

- `new` -> `commited`: Agent starts work. Also creates the feature branch.
- `commited` -> `done`: Agent finishes, commits, writes summary.
- `new` -> `block`: Agent discovers a dependency is missing.
- `commited` -> `block`: During work, agent hits an external blocker.
- `block` -> `new`: User resolves the blocker and resets the status.
- `block` -> `commited`: User unblocks and agent resumes.
- `done`: **Terminal state**. A done task is not reopened. If a new issue appears, create a new task.

## Scope Field

The `scope` field in task frontmatter indicates which part of the codebase the task targets:

| Scope | Meaning | Coding standards |
|-------|---------|-----------------|
| `backend` | Python code in `src/backend/` | `coding-standards-python.md` |
| `frontend` | React TS code in `frontend/` | `coding-standards-react.md` |
| `both` | Spans both backend and frontend | Both standards apply |

## Rules for All Agents

1. **Always read `task.md` frontmatter first** before acting on a task.
2. **Never change status without good reason** — each transition must follow the workflow above.
3. **Respect `commited`** — if another agent has `commited` the task, do not interfere unless user says so.
4. **Respect `scope`** — use the correct coding standards for the target component.
5. **Write the summary** — when reaching `done`, create `summary.md` using `.opencode/templates/summary.md`. Fill every relevant section. This file also serves as the PR description body when pushing.
