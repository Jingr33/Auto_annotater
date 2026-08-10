---
description: Fix all code review comments on current PR (dry-run first)
agent: dev
subtask: true
---

Fix all code review comments for the current branch's PR.

## Setup

1. Load the **project-management** skill.
2. Load the **code-review** skill (for review context).
3. Identify the current branch and task.

## Workflow

### 1. Identify PR

- Get current branch: `git branch --show-current`
- Find PR: `gh pr list --head <branch> --json number,title,url`
- If no PR found, stop and inform user.

### 2. Fetch Pipeline Status

- Check CI checks: `gh pr checks <pr-number>`
- Document pass/fail status.

### 3. Fetch All Review Threads

Get ALL comments (including resolved/outdated):
```bash
gh api repos/{owner}/{repo}/pulls/<pr-number>/comments --paginate
```

Parse each comment:
- `id` — comment ID
- `path` — file path
- `body` — comment text
- `user.login` — reviewer username
- `line` / `original_line` — line number
- `in_reply_to_id` — parent comment (for threads)
- `resolved` — resolution status
- `minimized` — if minimized by author

### 4. Group into Threads

Group comments by thread:
- Root comment: `in_reply_to_id` is null
- Replies: `in_reply_to_id` points to root

Identify unresolved threads:
- Thread is unresolved if any comment is unresolved
- Include outdated threads (code changed since comment)

### 5. Categorize Each Thread

For each unresolved thread, determine action:
- **Code fix** — requires code change
- **Question** — needs explanation reply
- **Acknowledgment** — trivial, resolve without reply
- **Outdated** — already fixed by other changes, just resolve

### 6. DRY-RUN: Preview Changes

**DO NOT commit or push yet.** Show user what will be changed:

```
=== CR-FIX DRY-RUN ===

Threads to process: N

1. [CODE FIX] <file>:<line>
   - @<reviewer>: "<comment>"
   - Fix: <description>
   - Commit: <commit message>

2. [QUESTION] <file>:<line>
   - @<reviewer>: "<comment>"
   - Reply: "<explanation>"

3. [ACKNOWLEDGE] <file>:<line>
   - @<reviewer>: "<comment>"
   - Action: Resolve without reply

4. [OUTDATED] <file>:<line>
   - @<reviewer>: "<comment>"
   - Action: Already fixed, resolve

Files to modify:
- <file1> (<N> changes)
- <file2> (<N> changes)

Commits to create:
- <commit message 1>
- <commit message 2>

=== END DRY-RUN ===
```

### 7. Wait for User Confirmation

**STOP here.** Wait for user to review the dry-run output.

User options:
- **"continue"** — Apply changes, commit, push
- **"edit"** — User wants to modify the plan
- **"cancel"** — Stop without making changes

### 8. Apply Changes (only on "continue")

For each thread marked as code fix:
1. Read the file at the specified line
2. Understand the reviewer's concern
3. Implement the fix following coding standards
4. Stage the changes (do not commit yet)

For each thread marked as question:
1. Analyze the question
2. Formulate clear explanation
3. Reply using: `gh api repos/{owner}/{repo}/pulls/comments/<comment-id>/replies -f body="<explanation>"`
4. Resolve thread

For each thread marked as acknowledgment:
1. Reply with brief acknowledgment if needed
2. Resolve thread

For each thread marked as outdated:
1. Verify the issue is actually fixed
2. Reply: "This has been addressed in commit <hash>"
3. Resolve thread

### 9. Commit and Push

- Commit all staged changes with descriptive messages
- Push to branch: `git push origin <branch>`
- Verify push succeeded

### 10. Resolve All Threads

For each processed thread, mark as resolved:
```bash
gh api repos/{owner}/{repo}/pulls/comments/<comment-id>/resolve -X PATCH
```

### 11. Create cr-fix.md

- Location: `dev_items/<task-folder>/cr-fix.md`
- Use template: `.opencode/templates/cr-fix.md`
- Fill all sections with actual data

### 12. Report Summary

Report to user:
- Number of threads processed
- Number of code fixes applied
- Number of explanations provided
- Number of threads resolved
- Link to PR

## Rules

- NEVER commit automatically — always show dry-run first
- NEVER modify `task.md` or `summary.md`
- Follow coding standards for all fixes
- All replies must be professional and clear
- Always resolve threads after processing
- Document everything in `cr-fix.md`
- Update existing PR, never create new one
