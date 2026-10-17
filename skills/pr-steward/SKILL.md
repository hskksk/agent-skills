---
name: pr-steward
description: After a PR is opened, delegate watching and small fixes to a cheaper subagent. Autonomously handle lint, format, and clear CI fixes, and escalate design judgment or scope-expanding comments to the parent as a structured handoff. Use when a parent agent has opened a PR and should delegate babysitting without burning the main context on trivial follow-ups.
license: MIT
metadata:
  author: hskksk
  version: 1.7.0
---




# PR steward (a PR watcher that escalates to the parent)

The procedure for a parent agent that keeps the implementation and design context, and hands **trivial follow-up on the PR** (lint, format, obvious type errors, a one-off fix the log states explicitly, and the like) to a **steward** (a subagent or a dedicated light run).

This is not handing the whole PR to another Cloud Agent the way `/autopilot` does. Receive events with **subscribe or an equivalent wait**, **fix only what you can fix yourself**, and **send the rest back to the parent**.

## When to use

- After the parent has opened a PR, you want to keep handling red CI, bot comments, and light review comments, without putting long logs or repeated fixes into the parent's conversation
- You want a cheaper model or an isolated context to watch the PR, and to wake the parent only when judgment is required

Do not use it for:

- The implementation and design themselves, before the PR is opened (the parent's job)
- Merge, rebase, force-push, or approving a protected branch
- A request to automatically reply to a human reviewer or resolve a thread (the steward goes as far as **organizing material for the parent**. A public comment is decided by the parent or the user)

## Roles

| Role | Who | Artifact |
| --- | --- | --- |
| Parent (caller) | The main agent | PR URL, intent note, starting the steward, judgment after an escalation arrives |
| Steward | A subagent or a lightweight Cloud run | Commits for autonomous fixes, a status report, a handoff with `escalations` |

When the parent reads this skill, start at `references/parent-delegation.md`. When the steward reads it, start at `references/steward-runtime.md` and `references/triage-rubric.md`.

## Procedure (overview)

### Parent

1. Create the PR and write a short **intent note** (what changed, what not to touch, related files).
2. Start the steward. What to pass, and how to write the launch, is in `references/parent-delegation.md`.
3. **Avoid fighting over the workspace.** Editing the PR head branch is the steward's job. The parent picks one of A, B, or C in `references/workspace-isolation.md` (the same branch name is fine when the worktrees differ, or when the work is serial).
4. Repository conventions are in `references/repo-conventions.md`. Do not paste the whole text into the prompt. Pass the path and the verify commands only.
5. Until the steward returns a handoff, the parent does not edit in a way that breaks the isolation mode you chose.
6. Read `escalations` and handle design, scope, and ambiguous human comments. When autonomous fixes alone made the PR green, leave the merge decision to the user.

### Steward

1. Check the PR and the intent note you received, and check out according to the isolation mode (the PR head for a shared tree; a worktree or sub-branch as in `workspace-isolation.md`).
2. Conventions are in `repo-conventions.md`. The verify commands you were given, plus hooks and CI, are the source of truth.
3. **Set up the wait.** On a Cloud Agent, subscribe to the PR (and CI if needed) or use the `/subscribe` skill. Where those tools are missing, use the fallback in `references/steward-runtime.md`.
4. Classify each event with `references/triage-rubric.md`.
   - **Autonomous:** Tier A in the rubric. Fix with a minimal diff, run the related checks, commit, and push.
   - **Escalate:** Tier B or C. Do not change code (or investigate only), and fill the JSON in `references/handoff-format.md` for the parent.
5. Stop when the PR is merged or closed, the user says to stop, or the parent takes over. Return a final handoff before stopping.

## Reference files

| File | Contents | When to read |
| --- | --- | --- |
| `references/parent-delegation.md` | When the parent starts a steward, and what to pass | Just before the parent delegates after the PR |
| `references/steward-runtime.md` | Subscribe, subagents, and the fallback wait | Immediately after the steward starts |
| `references/triage-rubric.md` | Deciding autonomous fix versus escalate | On each CI or review event |
| `references/handoff-format.md` | The structured report returned to the parent | On escalation and at the end of the session |
| `references/workspace-isolation.md` | Worktree, serial work, and a sub-branch | When choosing the isolation mode before delegating |
| `references/repo-conventions.md` | Keeping conventions with tools and pointers | The one `conventions` line at delegation |

## Relationship to other skills

This skill is complete on its own. The general rule for the boundary that bundles several skills has its source of truth in `skill-orchestration`. Here, refer to that name only. Do not open the other skill's `references/`.
