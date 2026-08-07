---
description: Analyze an error from runtime logs and create structured issue file(s) in issues/
subtask: true
---

Given the error/log output in the prompt:

1. Parse the output into distinct problems.
2. For each problem, read relevant source files in `src/backend/` or `frontend/`.
3. For each problem, create a directory `issues/<NNN>-<short-description>/` with a single file `issue.md` inside it, using the template at `.opencode/templates/issue.md`.
   - Example: `issues/001-yolo-prediction-crash/issue.md`
4. Number them sequentially starting from the next available number. First check the highest existing `NNN` prefix in `issues/`, then start from `NNN+1`. NEVER reuse an existing number.
5. If re-analyzing an issue that already has a `fix.md` in its directory, rename `fix.md` -> `fix-obsolete.md` before making any changes to `issue.md`.
6. **SCOPE RULE:** Analyze only what is in the provided log output. Do not invent extra problems.
