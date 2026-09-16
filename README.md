# plan-review

Review Claude Code plans in the browser with inline comments, invoked on demand with `/plan-review`.

`/plan-review` opens the latest plan (or `/plan-review path/to/file.md`) in a local page.
Select text → **Comment**. Add an optional general comment, then **Approve** or **Request changes**.
Claude receives the comments, each quoting the passage it refers to, and revises the plan.

## Layout

- `skill/plan-review/SKILL.md`: the skill Claude follows.
- `skill/plan-review/review.py`: a Python server with no dependencies beyond the standard library. It serves the page on `127.0.0.1`, blocks until you submit, and prints the feedback.
- `skill/plan-review/page.html`: the review page. It loads `marked` from jsDelivr to render markdown and falls back to plain text when offline.

## Install

```sh
ln -s ~/work-space/Solenya/plan-review/skill/plan-review ~/.claude/skills/plan-review
```

Requires `python3`. No packages.
