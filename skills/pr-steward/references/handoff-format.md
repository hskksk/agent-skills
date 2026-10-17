# Handoff for the parent (structured report)

The steward returns its reply to the parent as **one JSON object** (a short summary sentence before or after is fine). The parent parses it and turns only `escalations` into implementation tasks.

## Schema

```json
{
  "schema": "pr-steward-handoff/v1",
  "pr": "https://github.com/org/repo/pull/123",
  "branch": "feature/example",
  "state": "open",
  "checks_summary": {
    "pending": ["integration"],
    "failed": [],
    "passed": ["lint", "unit"]
  },
  "autonomous_fixes": [
    {
      "id": "fix-001",
      "tier": "A",
      "summary": "Applied eslint --fix on src/foo.ts",
      "commit": "abc1234"
    }
  ],
  "escalations": [
    {
      "id": "esc-001",
      "tier": "C",
      "source": "review-comment",
      "author": "human-reviewer",
      "link": "https://github.com/org/repo/pull/123#discussion_r123",
      "summary": "Questions choice of caching layer",
      "decision_context": {
        "question": "Should we use Redis or in-process cache for session tokens?",
        "options_seen": ["Redis", "in-memory"],
        "impact": "Affects deployment and auth latency",
        "recommendation": null
      },
      "blocked": true
    }
  ],
  "steward_status": "waiting",
  "notes_for_parent": "Subscribe still active; do not start parallel edits on this branch."
}
```

## Fields

| Field | Required | Description |
| --- | --- | --- |
| `schema` | yes | Always `pr-steward-handoff/v1` |
| `pr` | yes | PR URL |
| `branch` | yes | Head branch name |
| `state` | yes | `open` / `merged` / `closed` |
| `checks_summary` | yes | Arrays of check names. Do not include detailed logs |
| `autonomous_fixes` | yes | What was pushed at Tier A. `[]` if none |
| `escalations` | yes | Tier B or C. `[]` if none |
| `steward_status` | yes | `waiting` (subscribe continues) / `idle` (green, nothing escalated) / `stopped` / `error` |
| `notes_for_parent` | no | One line of caution for the parent |

### `escalations[]`

| Field | Required | Description |
| --- | --- | --- |
| `id` | yes | Stable ID (referenced when the steward resumes) |
| `tier` | yes | `B` or `C` |
| `source` | yes | `ci` / `review-comment` / `review-body` / `bot` / `policy` / `infra` |
| `summary` | yes | One line |
| `decision_context` | Recommended for B and C | The question, options, and impact the parent needs in order to decide |
| `link` | When one exists | URL of the comment or the run |
| `blocked` | yes | `true` when the PR should not be merged until the parent decides |

Fill `recommendation` only for **Tier B where the steward is confident**. For C, set it to `null`.

## When to update

- If even one Tier B or C appears, return a handoff **at the end of that event** (foreground steward)
- Even while subscribe continues, **return a handoff each time an escalation is added**, so the parent can read it
- At the end of the session, return a final snapshot

## When the parent resumes

Include in the resume prompt:

- Which `escalations[].id` values from the previous handoff were handled
- An updated intent note, if there is one

The steward skips IDs that were already handled.
