# Classification rubric (autonomous vs escalate)

Split each finding (CI failure, bot comment, review comment) into **Tier A / B / C**. When unsure, move to the **higher tier** (escalation is the safe side).

## Tier A — the steward may fix autonomously and push

Tier A only when all of the following hold:

1. **It does not contradict the PR intent note** (touch only files inside the scope)
2. The fix is **unique** (the line a lint, formatter, or type-error message points at, an obvious typo, a string the test expects, and the like)
3. It does not change a **public API, schema, migration, or security boundary**
4. It does not weaken a check (adding a skip, relaxing a threshold, or abusing `eslint-disable` is Tier B or higher)
5. A human reviewer has not attached an **approval or an explicit "fix this"** (bots and CI only)

Examples:

- `eslint` / `ruff` / `prettier` / `gofmt` / `cargo fmt` and the like
- Import cleanup or unused-variable removal in a single file
- Fixing an expected value a unit test shows, without changing the intent of production logic
- A merge conflict that **resolves mechanically** (no change of meaning on the same line)

## Tier B — the parent decides, then someone fixes (the steward only investigates and summarizes)

Applies when:

- There are several legitimate fixes (naming, level of abstraction, error-handling policy)
- The scope **widens** the PR intent (a large set of new files, a new dependency, a proposed refactor)
- The path to green is deleting tests, skipping them, or changing CI configuration
- A bot comment **might be a false positive**, but domain knowledge is required
- **Contradictory comments** inside the same PR (fixing one makes the other worse)

The steward: put candidate diffs in a **list**. It may write a recommendation. It **does not commit**.

## Tier C — always to the parent (or the user)

Applies when:

- Architecture, domain model, compatibility, or a performance tradeoff
- Security (authorization, input validation, secrets)
- A **human reviewer's** question, design comment, or "why did you do it this way?"
- Infrastructure failure, a permission error, or a flaky check that keeps failing (past the retry limit)
- A merge block (required review, a policy failure)

The steward: put the original link, a quotation, and the blast radius in the handoff, and **does not push at all**.

## CI special cases

| Signal | Treatment |
| --- | --- |
| A single cause in lint / format / typecheck | Tier A (B if the message shows a design problem across files) |
| An integration or e2e failure | B by default. A if the log is a one-line configuration mistake |
| A merge conflict with `main` | A if mechanical, B or C if the meaning has to be interpreted |
| An external service 5xx or rate limit | C (infrastructure) |

## Recording

Give each handled finding a stable ID (tool name + file + line + a short hash, or the review comment id). Do not handle the same ID again on the next event.
