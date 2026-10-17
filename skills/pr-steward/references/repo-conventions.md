# Repository conventions (without eating context)

Do not paste a long style guide into the steward's prompt. Push conventions onto **the repository's source of truth** and **mechanical gates**, and give the agent only **where to look and what to run**.

## Layers (higher means fewer tokens)

| Layer | Example | How the steward uses it |
| --- | --- | --- |
| Auto-format and lint | `eslint --fix`, `prettier`, `ruff format`, `gofmt` | **Run the same command** before and after Tier A. Do not read the rule text |
| Commit hooks | `husky`, `pre-commit`, `commitlint` | If `git commit` fails, fix it. Message rules are checked here too |
| CI | GitHub Actions lint / test | Push until green; put only a summary of the CI log in the handoff |
| Static config | `commitlint.config.*`, `.editorconfig`, `biome.json` | Read the relevant file, **only the lines you need**, and only when something failed |
| Docs for people | `AGENTS.md`, `CONTRIBUTING.md` | Pass **the path only**. "Before committing, follow the Commits section of `AGENTS.md`" |

Add a **convention pointer** to the parent's intent note (do not include the full text):

```yaml
conventions:
  agent: AGENTS.md
  commits: conventional commits; scope optional
  verify: npm run lint && npm test -- --related
```

## Cursor / agent side (keep it short)

- Write commit format and prohibitions in **Project Rules** (`.cursor/rules`) or **`AGENTS.md`**. Always Apply is token-heavy, so narrow the scope with **globs** (for example `**/*.{ts,tsx}`) or the equivalent of `apply when committing`.
- Optionally put 5–10 lines in **`.cursor/agents/pr-steward.md`**: about the level of "follow `AGENTS.md` and `commitlint`. Verify with `npm run lint`." Do not duplicate the skill body.
- The **steward skill** (`pr-steward`) is only the procedure and the rubric. Repository-specific type names and exceptions have their source of truth in **the repository's `AGENTS.md`**.

## Commit messages

1. The parent puts one line in `conventions.commits` (for example `type(scope): imperative subject`).
2. The steward runs `git commit` and, **if commitlint or a hook fails**, fixes it from the error message alone (do not restate the full rules).
3. When a Tier A summary push would be several commits, use **one issue per commit** only when the team requires it. Otherwise a single commit such as `fix: address lint on PR` is fine, within what commitlint allows.

## Coding style

- **The formatter or linter is the source of truth.** The steward does not make style judgments; it runs the tool.
- Send only comments the tool cannot fix to Tier B or C via the triage rubric.
- Do not make the steward read a huge `STYLE.md` every time. Asking an Explore subagent to "summarize the overrides in the `eslint` config" is fine **after an escalation**.

## What to put in the handoff

In `notes_for_parent`, only when you stopped on a convention violation:

- Which gate failed (`commitlint`, `eslint`, the CI name)
- **The last 20 lines or fewer** of the log, or a one-line error

Do not include the full conventions or a long diff.
