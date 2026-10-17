# Steward runtime and waiting

The steward runs **on events**. Relying only on polling is the last resort.

## 1. Cloud Agent (a run the user owns)

When it is available, **subscribe to PR activity** after the PR is created (or immediately after launch).

- In the prompt, write "subscribe to this PR, and resume on CI, review, and push events"
- The built-in `/subscribe` skill may do the same routing
- **The steward's run or subagent** is what subscribed. The parent does not wait

Even when automatic subscribe exists (an environment that attaches CI autofix to a PR you created), **the rubric for design escalations** still follows this skill. Do not quietly fix a scope-expanding comment just because you fixed CI.

## 2. Subagent (editor / CLI / inside Cloud)

It runs in a context isolated from the parent.

- There is no history. The PR, intent note, and branch name the parent passed are the whole input
- Long CI logs stay inside the steward. Return only the handoff summary to the parent
- **Background** is recommended only when `worktree` or `sub-branch` isolation is in place. On a shared checkout, use foreground or serial work (`workspace-isolation.md`)

Prefer a light model. An escalation that needs exploration goes back to the parent as Tier C. The steward does not dig in.

## 3. Environments where subscribe is unavailable

Use one of the following. In every case **the rubric and the handoff format stay the same**.

| Situation | Fallback |
| --- | --- |
| An Automation runs as a service account | Design it so each event starts a new Automation run. Each run handles one pass of "only unhandled CI or comments" and leaves the handoff as a PR comment (draft) or a reply to the parent |
| Local, with no subscribe tool | Read state with `gh pr view` / `gh run list`, and wait until the user or the parent asks to "start the steward again." If you poll in an automatic loop, use exponential backoff and respect rate limits |
| GitHub MCP has `subscribe_pr_activity` | Subscribe to the PR with that tool, and run the same steward procedure on events |

On a fallback, **fix only Tier A**. If it is ambiguous, accumulate escalations and return them together when the parent starts.

## 4. Work loop (per event)

1. Fetch the PR's mergeable state, the check list, and unresolved review comments (`gh` or the host's PR API).
2. Note finding IDs already handled, and do not handle them again.
3. Classify each finding with `triage-rubric.md`.
4. Tier A: fix → run the related commands locally (within the lint / test scope) → commit → push.
5. Tier B or C: append to `handoff-format.md`. Do not push (only if an investigation commit is required and it meets the Tier B conditions).
6. **Do not reply** to a human reviewer's comment. Summarize it in `escalations`.

## 5. Stopping

End the steward on any of the following:

- `state` is `merged` or `closed`
- The parent or the user says to stop
- Every check has succeeded, there is no unhandled Tier B or C, and the parent has said no pull-up is needed

On exit, return a **final handoff** to the parent (an empty `escalations` is fine).
