---
name: argument-skeleton
description: Draw a report's reasoning as a tagged diagram between the opening and the first section, and return that diagram plus one caption naming a chain, parallel supports, or a contrast. Use when two or more claims must be related, including branches that were ruled out. Do not use it for a single claim, a comparison table, or a landscape that is not an argument.
license: MIT
metadata:
  author: hskksk
  version: 1.0.0
---


# Argument skeleton

Draw the reasoning of a report as a diagram the reader can use as an index. Place it after the opening and before the first section. The opening still answers the question on its own. The diagram shows how the supporting claims relate, including the branches that were ruled out.

`references/contract.md` is the source of truth for the nodes, the edges, the caption, and the index check. Read it before drawing. This file only says when to draw and what comes back.

## When to use

- A report has two or more claims, and the reader has to see how they connect
- A branch was investigated and dropped, and hiding it would make the next reader dig it again

Do not use it for:

- A single claim
- A comparison whose value is a table, not a chain of claims
- A landscape or a map that is not an argument from a question to an action

## Procedure

1. Read `references/contract.md`.
2. If the claims are two, in a straight line, with no ruled-out branch that changes how the chain reads, write one line per claim and the caption. Otherwise draw the diagram.
3. Apply the index check in that file. Count the Finding nodes, then count the sections that carry a claim.
4. Return the diagram, or the short list, and the caption.

When a diagram skill is present, follow that skill for syntax. This skill does not choose an engine, a palette, or a dash pattern. When no diagram skill is present, still return the nodes, the labelled edges, and the caption in the report's language. Do not invent a notation on the spot.

## What this skill does not cover

It does not decide the opening's slots, how many claims a report may have, how long the report may be, how a recommendation is worded beyond the Action node, or which heading style the sections use. It does not define a confidence scale. If the caller has one, name the level on the Mechanism node. The section heading names the section. The Finding node states what that section concludes.
