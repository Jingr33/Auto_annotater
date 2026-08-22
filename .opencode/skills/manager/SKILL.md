---
name: manager
description: Manages the dev item lifecycle via GitHub Issues. Creates issues, adds them to the GitHub Project, sets status, and creates feature branches.
license: MIT
compatibility: opencode
---

## Configuration

- **GitHub Project Number**: 3
- **Project Owner**: Jingr33

## Capabilities

### Create dev item

1. Build the issue body using the template at `.opencode/templates/task.md`:
   - `## Metadata` section with Type and Scope
   - `## Description` from the user input
   - `## Acceptance Criteria` with empty checkbox
   - `## Out of Scope` empty
   - For `bug` / `hotfix` types, include the bug-only sections (`## Repro Steps`, `## Expected Behavior`, `## Actual Behavior`). For `feature`, omit them.

2. Create the GitHub Issue:
   ```bash
   gh issue create --repo Jingr33/Auto_annotater --title "<title>" --body "<body>"
   ```
   Capture the issue number from the output.

3. Add the issue to the GitHub Project:
   ```bash
   gh project item-add 3 --owner Jingr33 --url <issue_url>
   ```

4. Set initial status to "Ready":
   ```bash
   gh project item-edit 3 --owner Jingr33 --url <issue_url> --field "Status" --value "Ready"
   ```

5. Build the slug from the title: lowercase, spaces -> hyphens, strip special chars.

6. Create and switch to the branch:
   ```bash
   git checkout -b <type>/<issue-number>-<slug>
   ```

7. Print a summary: issue number, issue URL, branch name.

### Fetch dev item

Used by commands that need to read task details (implement, cr-fix, ship, etc.).

**Two methods, with fallback:**

1. **By issue number** (preferred): `gh issue view <number> --repo Jingr33/Auto_annotater --json title,body,state`
2. **By branch name** (fallback): extract issue number from branch pattern `<type>/<number>-<slug>`, then fetch the issue.

**Parsing issue body:**

The issue body contains metadata as markdown sections:
```markdown
## Metadata
- **Type**: feature
- **Scope**: backend

## Description
...

## Acceptance Criteria
- [ ] ...

## Out of Scope
...
```

Parse the `## Metadata` section to extract `Type` and `Scope`. The `## Description` and `## Acceptance Criteria` sections contain the task details.

### Set project status

Update the status field on the GitHub Project for an issue:

```bash
gh project item-edit 3 --owner Jingr33 --url <issue_url> --field "Status" --value "<status>"
```

Valid status values: `Backlog`, `Ready`, `In progress`, `Blocked`, `Done`.

### Get project status

Check the current status of an issue in the project:

```bash
gh issue view <number> --repo Jingr33/Auto_annotater --json projectItems --jq '.projectItems[] | select(.project.number == 3) | .fieldValues.nodes[] | select(.field.name == "Status") | .optionId'
```

Or more reliably, list project items and find the status:
```bash
gh project item-list 3 --owner Jingr33 --format json
```
