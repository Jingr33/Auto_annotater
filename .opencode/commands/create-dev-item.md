---
description: Create a new dev item (PBI) with task.md and feature branch
subtask: true
---

Load the `manager` skill.

Parse the prompt:

- Everything after `/create-dev-item` is the task description.
- Extract the title (first line or first sentence).
- Optionally look for `--type <type>` to override default `feature`.
- Optionally look for `--status <status>` to override default `new`.
- Optionally look for `--scope <backend|frontend>` to set the target component.

1. Find the highest existing NNN prefix in `dev_items/`:
   ```powershell
   Get-ChildItem -Path "dev_items" -Directory -Name | Select-String -Pattern "^\d{3}" | ForEach-Object { [int]$_.Matches.Value } | Measure-Object -Maximum | ForEach-Object { $_.Maximum }
   ```
   If no items exist yet, start from 1.

2. Compute next number as NNN (3-digit zero-padded).

3. Build the slug from the title: lowercase, spaces -> hyphens, strip special chars.

4. Create the directory:
   ```powershell
   New-Item -ItemType Directory -Path "dev_items/<NNN>-<slug>" -Force
   ```

5. Read `.opencode/templates/task.md` and write it to `dev_items/<NNN>-<slug>/task.md` with filled frontmatter. If the resolved `type` is `feature`, drop the bug-only section (`## Repro Steps`, `## Expected Behavior`, `## Actual Behavior`) from the written file. Keep it only for `bug` / `hotfix` types.

6. Create and switch to the branch:
   ```bash
   git checkout -b <type>/<NNN>-<slug>
   ```

7. Print confirmation: created path, branch name, and basic info.

8. **STOP. NEVER IMPLEMENT.** After creating the PBI, you MUST NOT:
   - Implement the feature or task described in the dev item
   - Change its status to `commited`
   - Edit any source code, write tests, or install dependencies
   - Continue working on the task in any way

   The `/create-dev-item` command ONLY creates the PBI structure and branch. Implementation is a separate step done later by the user or in a different session.
