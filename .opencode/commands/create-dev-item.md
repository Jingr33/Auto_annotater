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

5. Read `.opencode/templates/task.md` and write it to `dev_items/<NNN>-<slug>/task.md` with filled frontmatter.

6. Create and switch to the branch:
   ```bash
   git checkout -b <type>/<NNN>-<slug>
   ```

7. Print confirmation: created path, branch name, and basic info.

8. **Stop.** Do not implement the PBI. Do not change its status to `commited`. Do not edit any source code, write tests, or otherwise work on the task described in the dev item. Only the creation above is requested.
