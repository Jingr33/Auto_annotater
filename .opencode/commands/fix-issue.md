---
description: Fix an issue by issue number, reimplementing the broken code
subtask: true
---

Given an issue number (e.g. `001`):

1. Find the issue directory: `issues/<NNN>-*/` (match by the numeric prefix).
   - If not found, terminate with: `issue <NNN> not found in issues/`

2. Inside it, read `issue.md` **only for context** — it is a read-only specification and must never be modified.

3. Identify the component(s) that need fixing from **Root Cause** and **Possible Fixes**.

4. Read the relevant source files referenced in the issue description.

5. Implement the fix:
   - Follow the appropriate coding standards:
     - Python backend code: `instructions/coding-standards-python.md`
     - React TypeScript frontend code: `instructions/coding-standards-react.md`
   - Modify files in place in the relevant directory (`src/backend/` or `frontend/`).
   - If the fix requires a new package, add it to the relevant dependency file (do NOT install).

6. After implementation, create `fix.md` inside the same issue directory using the template at `.opencode/templates/fix.md`. Load the template file and follow its structure exactly.

7. If the fix changes anything fundamental (architecture, API, behaviour), update the relevant documentation files in `docs/`.

8. **Rules enforced by this command:**
   - NEVER modify `issue.md` inside the issue directory.
   - NEVER run git commands (no commit, no push, no branch operations).
   - Only implement the fix and create `fix.md`, then stop.
