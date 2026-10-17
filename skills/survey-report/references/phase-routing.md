# Choosing the report type (phase routing)

This guide routes a survey report to Phase 1 (exploratory) or Phase 2 (verification and structuring) by how far the request's question is already fixed. Weighting and reader level are separate axes. Choose them in [`gravity.md`](gravity.md) and [`reader-level.md`](reader-level.md).

## Decision flow

```
[Request from the user]
          │
          ▼
   Is there a concrete issue or hypothesis?
    ├── YES ──> Phase 2: verification and structuring
    └── NO  ──> Is the goal a landscape or the latest developments?
                  ├── YES ──> Phase 1: exploratory
                  └── unclear ─> Phase 1: exploratory
```

For an ambiguous request, choose Phase 1 and end with concrete questions that Phase 2 could verify. Confirm the question with the user when you need to. Do not assume that Phase 2 will follow Phase 1.

## How to judge

| | Phase 1: exploratory | Phase 2: verification and structuring |
|---|---|---|
| The request | A broad theme, a landscape, trends, or an unfamiliar field | Comparing options, analyzing causes, checking a hypothesis, or material for a decision |
| The question | "What is the problem?" or "What is the state now?" is still unspecified | Concrete, such as "A or B?" or "Why did this happen?" |
| The artifact | A map of the field, and three questions to solve next | An answer to the question, and the evidence that supports it |

### Example requests that choose Phase 1

- "Survey the landscape of this field"
- "I want the latest developments and the main issues"
- "Give me an overview from the basics"

### Example requests that choose Phase 2

- "Compare the tradeoffs of A and B"
- "Identify the bottleneck and its cause"
- "Summarize the evidence for whether we should adopt this"

For each phase's artifacts and structure, see [`phase-1-guide.md`](phase-1-guide.md) or [`phase-2-guide.md`](phase-2-guide.md).
