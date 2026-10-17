# Parent agent (the delegating side)

The parent keeps the design and implementation context. Hand PR watching to a **cheaper runner**.

## Artifacts to pass

Always include these in the steward's launch prompt:

1. **PR identifier** — URL, number, or `owner/repo#number`
2. **Intent note** — the purpose of the change, acceptance criteria, and **files or areas not to touch**
3. **What remains for the parent** — one line on what the parent should do when the steward escalates (for example, "breaking API changes are decided here")
4. **Scope of permission** — usually "commit and push to the PR head branch is allowed." Merge and force-push are not. Rebase depends on the team and the isolation mode (`workspace-isolation.md`).
5. **Isolation mode** — one of `serial`, `worktree`, or `sub-branch` (`workspace-isolation.md`). **Separating worktrees on the same branch name** is the usual pattern for PR follow-up.
6. **Convention pointer** — the one `conventions:` line from `repo-conventions.md` (path to `AGENTS.md`, verify commands). Do not paste the full conventions.

Optional:

- Names of checks known to be flaky
- A policy for telling human reviewers from bots (human comments escalate by default)

## How to launch (Cursor)

### Subagent (preferred: inside the same session)

The parent starts the steward with **Task / a subagent** and puts the items above in the prompt.

- You may specify a lighter model than the parent (cost isolation).
- If there is a dedicated steward definition, summarize this skill's steward procedure in `.cursor/agents/pr-steward.md` and launch it with `/pr-steward` or by name.
- Launch it in the **foreground**. Until the handoff JSON returns, the parent does not fix the PR head within the isolation mode you chose (`serial`). With `worktree` or `sub-branch`, the parent may work in another tree or on another branch.

Example of one sentence to include in the prompt:

```text
You are the PR steward. Follow the pr-steward skill: subscribe to this PR, fix only Tier A issues per triage-rubric, escalate Tier B/C to the parent using handoff-format. Do not merge or force-push.
```

### Just after the parent opened the PR with a Cloud Agent

If the parent run created the PR, **do not hand the whole thing to another full autopilot**. Instead:

- Start a subagent steward inside the same run, or
- If the user allows it, cut a **separate Cloud run** on a light model that is dedicated to the steward (separate from the parent's conversation ID; the parent reads the handoff from a PR comment or a shared note)

The parent does not have to subscribe itself. Subscribe is **the steward's responsibility**.

## When an escalation arrives

1. Read `escalations` in the handoff in priority order.
2. The parent fixes items that `decision_context` is enough for. When it is not enough, ask the user.
3. Decide whether to **resume** the steward or **stop** it. On resume, pass that the previous escalation IDs were marked handled.

## What not to do

- The parent and the steward editing the **same working tree** at the same time (allowed when worktrees are separate, even if the branch name is the same)
- Pasting the full conventions into the steward prompt (a path and `npm run …` are enough)
- Telling the steward to "just fix" an architecture decision
- Running `/autopilot` and the steward in parallel on the same PR (the roles overlap)
