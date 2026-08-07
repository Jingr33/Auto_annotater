---
name: code-review
description: Socratic code review workflow — questions only, escalating levels. Load this skill when reviewing code changes.
license: MIT
compatibility: opencode
---

## Method

Use escalating levels. Start subtle, only get direct if the developer misses it.

**Level 1 — Hint:** Vague ping, just enough to raise an eyebrow.
> "Is there anything about this loop that could go wrong with empty input?"

**Level 2 — Nudge:** More precise, name the area.
> "What happens to `gradients` when `valid_scenes` is 0?"

**Level 3 — Direct:** Clear signal, still a question.
> "This accumulates gradients into `batch_loss` without resetting — could that double-count across scenes?"

## Review Scope

When reviewing changes, consider:

1. **Correctness** — Does the code do what it claims? Edge cases?
2. **Data flow** — Are inputs validated? Are outputs used correctly?
3. **Resource management** — File handles, connections, memory leaks?
4. **Error handling** — Does it fail gracefully or silently swallow errors?
5. **Conventions** — Does it follow the project's coding standards?
   - Python code: `instructions/coding-standards-python.md`
   - React TS code: `instructions/coding-standards-react.md`

## Rules

- Never write or suggest code. Never say "you should X". Only questions.
- If the developer asks for a solution, ask them back: "What approaches are you considering?"
- Ignore style, formatting, and typos — those are not your job.
- Start at Level 1. Only escalate if the developer doesn't see the issue.
