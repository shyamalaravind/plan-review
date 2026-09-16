---
name: plan-review
description: Open the current plan (or any markdown file) in the browser so the user can highlight text and leave inline comments, then act on the feedback they send back. Only runs when the user invokes /plan-review.
disable-model-invocation: true
argument-hint: "[file.md]"
---

# Plan review

The user wants to review a plan in the browser instead of the terminal.

## 1. Pick the file

- If the user gave a path (`$ARGUMENTS`), review that file.
- Otherwise review the most recent plan in this conversation:
  - If plan mode saved it under `~/.claude/plans/`, use that file.
  - If not, write that plan verbatim to a new temp file
    (`"$(mktemp -d)/plan.md"`). If there is no plan in the conversation,
    use your last substantial message.

## 2. Open the review

Run this with Bash, **with `run_in_background: true`**. It blocks until the user submits:

```
python3 ~/.claude/skills/plan-review/review.py <file>
```

Tell the user in one line that the review is open in their browser, then end
your turn. Don't poll; you'll be notified when it finishes.

## 3. Act on the feedback

The command prints one of:

- `APPROVED: ...`: the user approved with no notes. Treat it as the user saying
  "looks good", and continue with whatever the plan was for.
- `APPROVED WITH NOTES: ...`: approved. Fold the notes in as you go.
- `CHANGES REQUESTED: ...`: numbered comments, each quoting the passage it
  refers to, plus an optional general comment. Address every comment and
  revise the plan. If the plan came from a file, update that file. Show what
  changed, one line per comment. Don't start implementing; the user will review
  again or approve.
