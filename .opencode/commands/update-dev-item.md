---
description: Update an existing GitHub Issue (title, body, status, type, scope) — never creates new issues
subtask: true
---

Load the `manager` skill.

Parse the prompt:
- First token after `/update-dev-item` is the **issue number** (required).
- Remaining tokens are update flags.

## Supported flags

| Flag | Example | Effect |
|------|---------|--------|
| `--title` | `--title "New title"` | Update issue title |
| `--status` | `--status "In progress"` | Set project status |
| `--type` | `--type bug` | Update Type in Metadata |
| `--scope` | `--scope frontend` | Update Scope in Metadata |
| `--description` | `--description "..."` | Replace Description section body |
| `--acceptance-criteria` | `--acceptance-criteria "..."` | Replace Acceptance Criteria body |
| `--out-of-scope` | `--out-of-scope "..."` | Replace Out of Scope body |
| `--comment` | `--comment "..."` | Post a comment on the issue |

## Rules

1. **NEVER create a new issue.** If the issue number does not exist, error and stop.
2. If no flags are provided, error with usage hint.
3. When updating body sections, fetch the current body first, then surgically replace only the target section.
4. Status values must be one of: `Backlog`, `Ready`, `In progress`, `Blocked`, `Done`.

## Workflow

### 1. Validate issue exists

```bash
gh issue view <number> --repo Jingr33/Auto_annotater --json number,title,body,state
```

If this fails, report "Issue #<number> not found" and stop.

### 2. Handle --title

```bash
gh issue edit <number> --repo Jingr33/Auto_annotater --title "<new title>"
```

### 3. Handle body updates (--description, --acceptance-criteria, --out-of-scope, --type, --scope)

a. Fetch current body:
```bash
gh issue view <number> --repo Jingr33/Auto_annotater --json body --jq '.body'
```

b. Parse the body as markdown sections delimited by `## `.

c. Replace the content of the targeted section(s). For --type and --scope, update the corresponding line in `## Metadata`.

d. Reconstruct the body and update:
```bash
gh issue edit <number> --repo Jingr33/Auto_annotater --body "<new body>"
```

### 4. Handle --status

```bash
gh project item-edit 3 --owner Jingr33 --url <issue_url> --field "Status" --value "<status>"
```

To get the issue URL, use:
```bash
gh issue view <number> --repo Jingr33/Auto_annotater --json url --jq '.url'
```

### 5. Handle --comment

```bash
gh issue comment <number> --repo Jingr33/Auto_annotater --body "<comment>"
```

### 6. Print confirmation

Show: issue number, which fields were updated, new values.

### 7. STOP. NEVER IMPLEMENT.
After updating the dev item, you MUST NOT implement, change status to "In progress" (unless explicitly asked), edit source code, write tests, or continue working on the task.
