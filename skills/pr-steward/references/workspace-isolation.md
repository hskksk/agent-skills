# Workspace isolation (branch and directory)

For PR follow-up, **editing the PR's head branch** is correct. What you want to forbid is not "do not touch the same branch." It is **the parent and the steward editing the same checkout (working directory) at the same time**.

## What conflicts

| What is shared | Edited at the same time | Typical result |
| --- | --- | --- |
| The same working tree (including uncommitted work) | Parent and steward in parallel | Overwrites, a half-finished merge, lint seeing a different version |
| The same branch name, different working trees | Usually safe | The push for the PR can come from the steward's side |
| A different branch, integrated into the PR branch later | Fine even while the parent continues the feature | One extra integration step |

Cursor subagents **share the parent's checkout by default**. Parallel edits can overwrite each other ([Subagents — Isolated project copies](https://cursor.com/docs/subagents)).

## Recommended patterns

### A. Serial (simple)

- The steward is **foreground**.
- While the steward is running, the parent **does not edit files on that PR branch** (another task or another branch is fine).
- The steward commits and pushes on the **PR head branch**.

This uses little context. When the parent wants to keep touching the same feature, use B or C.

### B. Isolated worktree (same branch name)

- When starting the steward, ask explicitly for **its own environment / an isolated copy / a git worktree**.
- Even in a worktree, **check out the PR's head branch** (for example `feature/foo`). The branch name may be the same as the PR.
- The parent may touch another branch or docs in the original working tree. The steward edits only the PR branch in another directory.

Example prompt:

```text
Run the PR steward in its own isolated worktree on the PR head branch <branch>. Do not edit files in the parent's working tree.
```

### C. Sub-branch (the parent keeps touching the same feature)

When the parent still has unpushed work on **the same feature branch**:

1. The steward cuts a **child branch** such as `feature/foo--steward` on a worktree (based on the PR's latest commit).
2. Commit and push Tier A fixes on the child branch.
3. **Update the PR head** in the repository's style:
   - A **merge commit** onto the PR branch, or **rebase and fast-forward push** (prefer merge when force-push is forbidden)
   - Or push the child branch as **additional commits without changing the PR base** (not possible when the PR points at the child branch — usually you integrate onto the PR head, `feature/foo`)

If force-push is forbidden, the steward does **only a normal push (merge) onto the PR head**. On a team that requires rebase, keep the steward at **foreground, and the parent does not touch the branch (A)**.

## One line the parent writes

Write the **isolation mode** as one line in the intent note:

- `isolation: serial` — the parent does not touch the PR branch
- `isolation: worktree, branch: <pr-head>` — same branch, different directory
- `isolation: sub-branch, integrate: merge-to-<pr-head>` — fix on a child branch and integrate onto the PR head

## Cloud steward

A Cloud subagent or a separate Cloud run is **another VM plus a clone** by default. Check out the PR head branch and push. There is no file conflict with the local parent.
