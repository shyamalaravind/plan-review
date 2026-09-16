# plan-review

Review coding-agent plans in the browser with inline comments. It's an [Agent Skill](https://agentskills.io), so it works in Claude Code, Codex, Gemini CLI, Cursor and any other tool that reads `SKILL.md`.

Ask for a plan review (`/plan-review`, or `/plan-review path/to/file.md`), and the plan opens in a local page.
Select text → **Comment**. Add an optional general comment, then **Approve** or **Request changes**.
The agent receives each comment with the passage it quotes, and revises the plan.

Everything runs locally and offline. The page is served from `127.0.0.1` in a single response, with the plan and the markdown renderer built into the HTML, so there are no network requests.

## Layout

- `skill/plan-review/SKILL.md`: instructions the agent follows.
- `skill/plan-review/review.py`: a Python server with no dependencies beyond the standard library. It serves the page, blocks until you submit, and prints the feedback.
- `skill/plan-review/page.html`: the review page.
- `skill/plan-review/marked.min.js`: a bundled copy of [marked](https://github.com/markedjs/marked) v12.0.2 (MIT) that renders the markdown.

## Install

Clone the repo, then link the skill into your tool's skills directory:

```sh
git clone https://github.com/shyamalaravind/plan-review.git
SKILL="$PWD/plan-review/skill/plan-review"

ln -s "$SKILL" ~/.claude/skills/plan-review   # Claude Code
ln -s "$SKILL" ~/.codex/skills/plan-review    # Codex (Cursor reads this too)
ln -s "$SKILL" ~/.gemini/skills/plan-review   # Gemini CLI
```

Create the skills directory first if it doesn't exist. Requires `python3`. No packages.

You can also run it without an agent: `python3 skill/plan-review/review.py plan.md` prints the feedback to stdout.
