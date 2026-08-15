---
name: manager
description: Manages the dev item (PBI) lifecycle. Can create new work items, set their status, and generate the required directory structure.
license: MIT
compatibility: opencode
---

## Capabilities

### Create dev item

1. Find the highest numeric prefix in `dev_items/` (e.g. `003-*` -> highest is 3).
2. Next number = highest + 1, formatted as `NNN` (3 digits, zero-padded, e.g. `004`).
3. Create directory `dev_items/<NNN>-<slug>/` where `<slug>` is the title converted to kebab-case.
4. Write `task.md` inside it using the template at `.opencode/templates/task.md`:
   - `title:` from the user input (keep original wording)
   - `type:` default `feature` (or `bug` / `hotfix` if specified)
   - `status:` default `new` (or `commited` / `done` / `block` if specified)
   - `scope:` default `backend` (or `frontend` / `both` if specified)
   - If `type` is `feature`, **omit** the bug-only section (`## Repro Steps`, `## Expected Behavior`, `## Actual Behavior`). Include it only for `bug` / `hotfix` types.
5. Create a git branch: `git checkout -b <type>/<NNN>-<slug>` (e.g. `feature/004-my-task`).
6. Print a summary of what was created.
