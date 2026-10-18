# Argument skeleton contract

Read this before drawing. It is the source of truth for what the diagram contains. How to draw it — engine, palette, dashes, legend syntax — stays with the diagram skill the caller already has, when one is present.

## Where it sits

After the opening and before the first section of the body. The opening still answers the question on its own. The skeleton shows how the supporting claims relate. It adds no fact that appears nowhere else in the report, and it does not defer a fact the opening already answered.

## When a list is enough

Two claims in a straight line, with no ruled-out branch that changes how the chain reads, do not need a rendered diagram. Write one line per claim, in document order, then the same caption the diagram would have had. A branch, a join, or a ruled-out hypothesis sends it back to a diagram.

## Nodes

Every node carries three things and nothing else: a tag naming its place on the path, one line stating what it says, and the figures that line stands on. A node that holds a paragraph is a section that escaped.

Tags are positions on one path, not categories. The path is Question, then Finding, then Mechanism, then Claim, then Action. Ruled-out branches sit off the path. Scope frames the path. It is not a step on it.

| Tag | Japanese label | Count | What it carries | Failure it invites |
| --- | --- | --- | --- | --- |
| Question | 問い | exactly 1, the root | What changed to make the question live, and the decision waiting on the answer | Names the method ("we analyzed") and omits the decision |
| Finding | 所見 | one per section that carries a claim | One observed fact, with the figures behind it | Copies the section heading and becomes a table of contents |
| Mechanism | 機構 | 0 or 1 | How the findings produce the result. If the caller has a confidence scale, name the level here. This skill does not define the scale | Stops at "A affects B" and never says how |
| Claim | 主張 | exactly 1 | The position the report takes, in the words the opening uses | Restates a finding. A reader could not disagree with it |
| Action | 打ち手 | exactly 1 | The next move. Any of owner, date, or success measure that is missing is written as missing | Rounds a hole up into a recommendation |
| Ruled out | 棄却 | 0 or more, off the path | A branch investigated and dropped, with the figures that dropped it. Points at the appendix section that holds the branch | Leaves the dead end only in the appendix, so the next reader digs it again |
| Scope | 適用範囲 | 0 or 1, a frame | The limit the whole chain holds within, and only when that limit changes how the chain is read | Repeats the opening's range when it changes nothing |

When the report is Japanese, the label the reader sees is the Japanese label. The block's heading is 論の骨格. 分析の骨格 is acceptable when the document is an analysis rather than an argument about one question. Either heading names the block. It does not state the conclusion.

A Finding node states what its section concludes. The section heading names the section. When the node's line is the heading, the skeleton has become a table of contents.

## Edges

Every edge carries the relation as its label. An unlabelled edge says "related somehow".

| Relation | English label | Japanese label |
| --- | --- | --- |
| narrows | narrows | 絞り込み |
| explains | explains | 説明する |
| joins | joins | 合流 |
| therefore | therefore | だから |
| so do | so do | 打つ手 |

The edge from the question to the first finding may say where the question comes from (どこで起きているか) when that is the narrowing. Write the label in the report's language.

## Caption

One sentence under the figure names which of these the relations are:

- a chain — each claim depends on the one before
- parallel supports — independent evidence converging on one answer
- a contrast

It also lists the appendices. Name the relation honestly. Forcing a chain onto independent findings distorts the argument in the same way as reading a chain as parallel supports. A reader who mistakes a chain for parallel supports will think any one claim could be dropped.

## Index

The skeleton is an index only when the number of Finding nodes equals the number of sections that carry a claim. Count the nodes, then count the sections. A section with no Finding node is a section the reader cannot navigate to.

## Nothing extra

Chain nodes come from the opening and the body. A Ruled-out node points at the appendix section for that branch. Scope compresses the range already stated in the opening. A figure or a finding with no home elsewhere in the report does not go here.

## Position, not palette

The position on the path must be visible without reading the tag. Ruled-out branches sit off the path. This skill does not choose colors, dash patterns, or a diagram language.

## Shape, not content

The listing below is a shape to copy. Build the skeleton from the report's own claims. Do not reuse the words.

```
[Question]  Paging volume rose 1.6x after the May release; decide by the next review whether to
            roll the release back        340 -> 540 pages per week
     | where it comes from
[Finding 1] The volume comes from one alert rule, not from the estate as a whole
            168 of the 200 extra pages        --- ruled out ---> [Ruled out] Not the new service:
     | narrows                                                    its own page count is flat
[Finding 2] That rule fires on a metric that is noisy overnight, when nobody acts on it
            71% of its pages fire between 01:00 and 05:00
     | explains
[Mechanism] The metric is a per-host gauge that the client library resets on reconnect, so an
            overnight reconnect storm reads as a threshold breach
     | therefore
[Claim]     The paging problem is one library's reconnect behaviour, not alert coverage
     | so do
[Action]    Pin the two services to the fixed client version   owner and date not yet identified
[Scope]     Holds for the May-June window; two nights are missing from the runner logs
```

Caption for that shape:

> 1 → 2 is a chain of narrowing, not two parallel grounds. 2 explains what changed inside the rule that 1 identified. The ruled-out branch sits off the chain. Appendices: A alert classification, B ruled-out hypotheses, C missing nights.
