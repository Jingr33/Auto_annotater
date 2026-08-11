---
description: Fix all code review comments on current PR
agent: dev
subtask: true
---

Fix all code review comments for the current branch's PR.

## Setup

1. Load the **project-management** skill.
2. Load the **code-review** skill.
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

### 6. Implement ALL Changes (NO PAUSE YET)

**DO NOT show preview or ask for confirmation yet.** Implement everything first.

For code fixes:
1. Read the file at the specified line
2. Understand the reviewer's concern
3. Implement the fix following coding standards
4. Stage the changes (git add)

For questions:
1. Analyze the question
2. Formulate clear explanation
3. Reply using: `gh api repos/{owner}/{repo}/pulls/comments/<comment-id>/replies -f body="<explanation>"`
4. Resolve thread

For acknowledgments:
1. Reply with brief acknowledgment if needed
2. Resolve thread

For outdated:
1. Verify the issue is actually fixed
2. Reply: "This has been addressed in commit <hash>"
3. Resolve thread

### 7. PAUSE for Confirmation (AFTER all implementations)

**Show user counts only:**

```
=== CR-FIX COMPLETE (NOT COMMITTED YET) ===

Threads processed: N

Code fixes applied: N
Questions answered: N
Threads resolved: N

Files modified: N

Type "continue" to commit and push, "cancel" to stop.
```

### 8. Resolve ALL Processed Threads

**Every comment that was fixed, answered, or acknowledged MUST be resolved.**

For each processed thread, mark as resolved:
```bash
gh api repos/{owner}/{repo}/pulls/comments/<comment-id>/resolve -X PATCH
```

**Skipped comments:**
- If you skip a comment (don't fix/answer), you MUST provide a reason
- Add skipped comments to the `fix-cr.md` under "Skipped Comments" section

### 9. Commit and Push (only on "continue")

- Commit all staged changes with descriptive messages
- Push to branch: `git push origin <branch>`
- Verify push succeeded

### 9. On "cancel"

- Stop without committing
- Inform user changes are staged but not committed

### 10. Create fix-cr.md

- Location: `dev_items/<task-folder>/fix-cr.md`
- For multiple CR rounds, name sequentially: `fix-cr.md`, `fix-cr-1.md`, `fix-cr-2.md`, etc.
- Check existing files to determine the next number
- Use template: `.opencode/templates/fix-cr.md`
- Fill all sections with actual data

### 11. Report Summary

Report to user:
- Number of threads processed
- Number of code fixes applied
- Number of explanations provided
- Number of threads resolved
- Link to PR

## Rules

- NEVER commit before user confirmation
- NEVER pause before implementing fixes
- Process ALL threads before showing summary
- NEVER modify `task.md` or `summary.md`
- Follow coding standards for all fixes
- All replies must be professional and clear
- Always resolve threads after processing
- ALL processed threads MUST be resolved (fixed, answered, or acknowledged)
- If skipping a comment, provide a reason in fix-cr.md
- Document everything in `fix-cr.md`
- Update existing PR, never create new one
