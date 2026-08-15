---
name: github-operations
description: GitHub operations for PR management — resolving comments, replying to threads, managing reviews. Load this skill when working with GitHub PRs.
license: MIT
compatibility: opencode
---

## Overview

This skill provides instructions for interacting with GitHub PRs using the `gh` CLI.

## Resolving PR Review Comments

### Method 1: Reply to a comment (REST API)

To reply to a comment:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies -f body="Your reply message"
```

### Method 2: Resolve thread via GraphQL

To resolve a thread, you need the thread ID (not comment ID):

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "THREAD_ID"}) {
    thread {
      id
      isResolved
    }
  }
}'
```

### Method 3: Get thread ID from comment

To get the thread ID for a comment:

```bash
gh api repos/{owner}/{repo}/pulls/comments/{comment_id} --jq '.node_id'
```

### Method 3: Bulk resolve all unresolved threads

```bash
# Get all unresolved thread IDs
THREAD_IDS=$(gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 100, states: UNRESOLVED) {
        nodes {
          id
        }
      }
    }
  }
}' --jq '.data.repository.pullRequest.reviewThreads.nodes[].id')

# Resolve each thread
for THREAD_ID in $THREAD_IDS; do
  gh api graphql -f query="
  mutation {
    resolveReviewThread(input: {threadId: \"$THREAD_ID\"}) {
      thread {
        id
        isResolved
      }
    }
  }"
done
```

## Replying to PR Comments

To reply to a specific comment:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies -f body="Your reply"
```

## Fetching PR Comments

### Get all comments on a PR

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --paginate
```

### Get only unresolved comments

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --paginate | jq '.[] | select(.resolved == false)'
```

## Creating PR Reviews

### Create a review with comments

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews -f event="COMMENT" -f body="Review summary"
```

### Approve a PR

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews -f event="APPROVE"
```

## Example Workflow: Resolve All Comments

```bash
# 1. Get PR number from current branch
PR_NUMBER=$(gh pr list --head $(git branch --show-current) --json number --jq '.[0].number')

# 2. Get all unresolved thread IDs
THREAD_IDS=$(gh api graphql -f query="
{
  repository(owner: \"OWNER\", name: \"REPO\") {
    pullRequest(number: $PR_NUMBER) {
      reviewThreads(first: 100, states: UNRESOLVED) {
        nodes {
          id
        }
      }
    }
  }
}" --jq '.data.repository.pullRequest.reviewThreads.nodes[].id')

# 3. Resolve each thread
for THREAD_ID in $THREAD_IDS; do
  gh api graphql -f query="
  mutation {
    resolveReviewThread(input: {threadId: \"$THREAD_ID\"}) {
      thread {
        id
        isResolved
      }
    }
  }"
done
```

## Example Workflow: Reply to All Comments

```bash
# Reply to all comments on a PR
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --jq '.[].id' | while read comment_id; do
  gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/$comment_id/replies -f body="Resolved: This comment has been addressed."
done
```

## Notes

- The `gh` CLI must be authenticated (`gh auth login`)
- Use `--paginate` for PRs with many comments
- GraphQL API is required for resolving threads (REST API doesn't support it directly)
- Thread IDs are different from comment IDs
