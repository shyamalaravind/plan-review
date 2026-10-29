# plan-review

Review coding-agent plans in your browser, with inline comments. It's an [Agent Skill](https://agentskills.io), so it works in Claude Code, Codex, Gemini CLI, Cursor and any other tool that reads `SKILL.md`.

The plan opens as a document in your browser. Select text → **Comment**. Add an optional general comment, then **Approve** or **Request changes**.
The agent receives each comment with the passage it's about, and revises the plan.

Don't want to say anything? **End review without feedback** — or just close the review — ends it. The agent is told the review stopped with no instructions, and waits for you instead of guessing.

Everything runs locally and offline, from `127.0.0.1`, with the renderer bundled.

Want the plan as a canvas of diagrams instead, with every function it names one hover or click away from the code? That's its sibling, [graphify-review](https://github.com/shyamalaravind/graphify-review), in a repository of its own. Ask for it by name, and in plan mode it takes this skill's place, so the plan isn't reviewed twice.

## How it works

Ask for a plan review (`/plan-review`, or `/plan-review path/to/file.md`), and the plan opens in a local page. It also runs on its own before an agent leaves plan mode, as a human checkpoint in front of the host's plan-approval gate (`exit_plan_mode` in Claude Code), not a replacement for it.

- The agent runs one command, `review`, and reads one block of text back: `APPROVED`, `APPROVED WITH NOTES`, `CHANGES REQUESTED` with numbered comments, or `ENDED`.
- The page is served in a single response, with the plan and the markdown renderer built into the HTML, so the tab makes no other request.
- There's one way back, `POST submit`, and the server exits once it has the verdict.

To use a browser other than your default, set `PLAN_REVIEW_BROWSER` (see [Install](#install)).

## Install

Clone the repo, then link the skill into your tool's skills directory:

```sh
git clone https://github.com/shyamalaravind/plan-review.git
ln -s "$PWD/plan-review/skill/plan-review" ~/.claude/skills/plan-review   # Claude Code
ln -s "$PWD/plan-review/skill/plan-review" ~/.codex/skills/plan-review    # Codex (Cursor reads this too)
ln -s "$PWD/plan-review/skill/plan-review" ~/.gemini/skills/plan-review   # Gemini CLI
```

Create the skills directory first if it doesn't exist. Requires a C++17 compiler — `clang++` from the Xcode command line tools on macOS (`xcode-select --install`), or `g++` on Linux. No packages, no runtime.

The skill builds its binary on its first review (~1s); after that it starts in a few milliseconds. To build it ahead of time: `make -C skill/plan-review`.

To pick the browser reviews open in:

```sh
export PLAN_REVIEW_BROWSER="Brave Browser"   # macOS; brave-browser on Linux. graphify-review reads it too
```

Put it in `~/.zshenv` (or your shell's equivalent), not `~/.zshrc`. Agents run commands in non-interactive shells, and those skip `~/.zshrc`.

You can also run it without an agent: `skill/plan-review/review plan.md` prints the feedback to stdout. `--title` names the review (`review resume.md --title "Apollo.io Resume Senior Software Engineer"`), so another skill that hands its document over can ask for a title.

## Layout

- `skill/plan-review/`: the skill.
  - `SKILL.md`: instructions the agent follows.
  - `review`: launcher. Compiles the server on first use (or after `review.cpp` changes) into `bin/review`, then runs it.
  - `review.cpp`: the server — C++17, standard library and POSIX sockets only. It serves the page, blocks until you submit or end the review, and prints the feedback.
  - `page.html`: the review page.
  - `marked.min.js`: a bundled copy of [marked](https://github.com/markedjs/marked) v12.0.2 (MIT) that renders the markdown.

graphify-review lived here until it moved to its own repository, which kept its history.
