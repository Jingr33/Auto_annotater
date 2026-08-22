---
description: Fix all code review comments on current PR
agent: dev
subtask: true
---

Fix all code review comments for the current branch's PR.

**Parameters:**
- `force` — Skip confirmation pause and commit/push immediately after implementation.

## Setup

1. Load the **project-management** skill.
2. Load the **manager** skill — it provides the `Fetch dev item` capability.
3. Load the **code-review** skill.
4. Load the **github-operations** skill (for resolving threads).
5. Identify the current branch and task.

## Workflow

### 0. Parse Parameters

- Check if prompt contains the word `force`
- Set `FORCE_PUSH` flag accordingly

### 1. Fetch the issue

- Get current branch: `git branch --show-current`
- Extract issue number from branch name (`<type>/<number>-<slug>`)
- If no issue number found, stop and inform user.
- Fetch the issue using manager skill's `Fetch dev item`:
  ```bash
  gh issue view <number> --repo Jingr33/Auto_annotater --json title,body
  ```
- Parse metadata from issue body.

### 2. Identify PR

- Find PR: `gh pr list --head <branch> --json number,title,url`
- If no PR found, stop and inform user.

### 3. Fetch Pipeline Status

- Check CI checks: `gh pr checks <pr-number>`
- Document pass/fail status.

### 4. Fetch All Review Threads

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

### 5. Group into Threads

Group comments by thread:
- Root comment: `in_reply_to_id` is null
- Replies: `in_reply_to_id` points to root

Identify unresolved threads:
- Thread is unresolved if any comment is unresolved
- Include outdated threads (code changed since comment)

### 6. Categorize Each Thread

For each unresolved thread, determine action:
- **Code fix** — requires code change
- **Question** — needs explanation reply
- **Acknowledgment** — trivial, resolve without reply
- **Outdated** — already fixed by other changes, just resolve

### 7. Implement ALL Changes (NO PAUSE YET)

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

### 8. PAUSE for Confirmation (AFTER all implementations, skip if force)

If `FORCE_PUSH` is NOT set:

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

If `FORCE_PUSH` IS set: Skip pause, proceed directly to step 9.

### 9. Resolve ALL Processed Threads

**Every comment that was fixed, answered, or acknowledged MUST be resolved.**

Use the **github-operations** skill to resolve threads:

```bash
# Get all unresolved thread IDs (use query.graphql file)
gh api graphql -F query=@query.graphql

# Create mutation file for each thread
echo 'mutation { resolveReviewThread(input: {threadId: "THREAD_ID"}) { thread { id isResolved } } }' | Out-File "q.txt" -Encoding ascii -NoNewline

# Resolve thread
gh api graphql -F query=@q.txt
```

**Important:** Use `-F query=@file.txt` format, not `-F query=-` to avoid encoding issues.

**Skipped comments:**
- If you skip a comment (don't fix/answer), you MUST provide a reason
- Add skipped comments to the fix-cr summary under "Skipped Comments" section

### 10. Commit and Push (only on "continue" or if force)

- Commit all staged changes with descriptive messages
- Push to branch: `git push origin <branch>`
- Verify push succeeded

### 10a. On "cancel" (only when not force)

- Stop without committing
- Inform user changes are staged but not committed

### 11. Create fix-cr summary

- Create `dev_support/<issue-number>/` directory if it doesn't exist
- Create `dev_support/<issue-number>/fix-cr.md`
- For multiple CR rounds, name sequentially: `fix-cr.md`, `fix-cr-1.md`, `fix-cr-2.md`, etc.
- Check existing files to determine the next number
- Use template: `.opencode/templates/fix-cr.md`
- Fill all sections with actual data

### 12. Post fix-cr summary as issue comment

```bash
gh issue comment <issue-number> --repo Jingr33/Auto_annotater --body "<content of fix-cr.md>"
```

### 13. Report Summary

Report to user:
- Number of threads processed
- Number of code fixes applied
- Number of explanations provided
- Number of threads resolved
- Link to PR

## Rules

- NEVER commit before user confirmation (unless `force` parameter is used)
- NEVER pause before implementing fixes
- Process ALL threads before showing summary
- Follow coding standards for all fixes
- All replies must be professional and clear
- Always resolve threads after processing
- ALL processed threads MUST be resolved (fixed, answered, or acknowledged)
- If skipping a comment, provide a reason in fix-cr.md
- Document everything in `dev_support/<issue-number>/fix-cr.md`
- Update existing PR, never create new one
- When `force` is used, skip confirmation and commit/push immediately
