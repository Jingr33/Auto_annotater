---
description: Migrate existing dev_items/ to GitHub Issues
subtask: true
---

Migrate all tasks from the local `dev_items/` folder to GitHub Issues.

## Setup

1. Load the **manager** skill.
2. Load the **project-management** skill.

## Workflow

### 1. Discover dev_items

List all directories in `dev_items/`:
```powershell
Get-ChildItem -Path "dev_items" -Directory -Name
```

Filter to directories matching the pattern `NNN-*` (3-digit prefix).

### 2. Process each item

For each dev_item directory (in order):

#### a. Read task.md

Read `dev_items/<folder>/task.md` and parse YAML frontmatter:
- `title`
- `type` (feature/bug/hotfix)
- `status` (new/commited/done/block)
- `scope` (backend/frontend/both)

Read the body content (everything after the frontmatter).

#### b. Build GitHub Issue body

Convert the task.md content to GitHub Issue format:

```markdown
## Metadata
- **Type**: <type>
- **Scope**: <scope>

<body content from task.md, preserving all sections>
```

If type is `feature`, keep only sections relevant to features (Description, Acceptance Criteria, Out of Scope).
If type is `bug` or `hotfix`, include all sections (Repro Steps, Expected Behavior, Actual Behavior).

#### c. Create GitHub Issue

```bash
gh issue create --repo Jingr33/Auto_annotater --title "<title>" --body "<body>"
```

Capture the issue number from the output.

#### d. Add to GitHub Project

```bash
gh project item-add 3 --owner Jingr33 --url <issue_url>
```

#### e. Map and set status

Map the old status to GitHub Project status:

| Old Status | New Status |
|------------|------------|
| `new` | `Ready` |
| `commited` | `In progress` |
| `done` | `Done` |
| `block` | `Blocked` |

```bash
gh project item-edit 3 --owner Jingr33 --url <issue_url> --field "Status" --value "<mapped_status>"
```

#### f. Handle summary.md

If `dev_items/<folder>/summary.md` exists:
- Create `dev_support/<issue-number>/` directory
- Copy summary.md to `dev_support/<issue-number>/summary.md`
- Post summary as issue comment:
  ```bash
  gh issue comment <number> --repo Jingr33/Auto_annotater --body "<summary content>"
  ```

#### g. Handle fix-cr.md

If `dev_items/<folder>/fix-cr.md` exists:
- Create `dev_support/<issue-number>/` directory if needed
- Copy fix-cr.md to `dev_support/<issue-number>/fix-cr.md`
- Post fix-cr as issue comment:
  ```bash
  gh issue comment <number> --repo Jingr33/Auto_annotater --body "<fix-cr content>"
  ```

### 3. Print migration table

After all items are processed, print a summary table:

```
Migration Complete!

| Old Folder | Old Status | Issue # | Issue URL | New Status |
|------------|-----------|---------|-----------|------------|
| 001-implement-react... | done | #12 | https://... | Done |
| 002-material-ui... | done | #13 | https://... | Done |
| ... | ... | ... | ... | ... |
```

### 4. Verify

- Check that all issues were created successfully.
- Report any failures.
- Do NOT delete or modify the `dev_items/` folder — it is kept as archive.
