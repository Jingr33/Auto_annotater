---
description: Create or update documentation
agent: docs
subtask: true
---

Document or update $ARGUMENTS in the `docs/` folder.

- If `$ARGUMENTS` is `agents`, `commands`, `skills`, `instructions`, or `templates` — update the corresponding page in `docs/.opencode/`.
- If `$ARGUMENTS` is `project` or a specific topic (e.g. `architecture`, `backend`, `frontend`) — update the page in `docs/project/`.
- If `$ARGUMENTS` is `all` — review and update all documentation pages.
- If `$ARGUMENTS` starts with `implemented` — the user just completed a task; scan the git diff and update relevant docs.

Read existing files in the relevant section first, then update. Use `docs/templates/` for consistent formatting.
