---
description: Review staged code changes — Socratic style, questions only
agent: cr
subtask: true
---

Load the **manager** skill.

If an issue number is provided in $ARGUMENTS:
- Fetch the issue: `gh issue view <number> --repo Jingr33/Auto_annotater --json title,body`
- Parse the issue body to understand the task context before reviewing.

Review the current git diff (staged and unstaged changes).

Use the Socratic method from the cr agent: questions only, escalating levels.
Start at Level 1. Only go deeper if the issue is non-trivial or the developer doesn't see it.
