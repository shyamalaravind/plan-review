---
name: plan-review
description: Open the current plan (or any markdown file) in the browser so the user can highlight text and leave inline comments, then act on the feedback they send back. Use only when the user explicitly asks for a plan review (e.g. /plan-review).
disable-model-invocation: true
argument-hint: "[file.md]"
---

# Plan review

The user wants to review a plan in the browser instead of the terminal.

## 1. Pick the file

- If the user named a file, review that file.
- Otherwise review the most recent plan in this conversation. If your tool
  already saved it as a markdown file, use that file. If not, write the plan
  verbatim to a new temp file (`"$(mktemp -d)/plan.md"`). If there is no plan,
  use your last substantial message.

## 2. Open the review

`review` sits next to this SKILL.md. Run it with the absolute path to this
skill's directory:

```
<this-skill-dir>/review <file>
```

It compiles the server on first use (about a second, once) and from then on
starts instantly. It opens the browser and blocks until the user submits or
ends the review. Run it as a background command if your tool supports that,
and you'll be notified when it exits. Tell the user in one line that the
review is open, then stop and don't poll. If background commands aren't
supported, run it in the foreground with the longest timeout available.

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
- `ENDED: ...`: the user ended the review without feedback, by clicking **End
  review** or by closing the tab. Treat it as an abrupt end with no
  instructions. Say in at most one short line that the review ended with no
  feedback, and stop. Don't revise the plan, don't start implementing, don't
  guess at what they wanted, and don't ask a follow-up question — wait for them
  to say what's next.
