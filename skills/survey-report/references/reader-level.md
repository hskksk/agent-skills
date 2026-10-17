# Choose the reader level

Reader level decides where the explanation starts. It is independent of weighting, which decides where the report's value sits. Front weighting does not mean a specialist reader, and rear weighting does not mean an introductory reader. For weighting, see [`gravity.md`](gravity.md).

## Assumed level

| Level | You may assume | Scaffolding the body still needs |
|---|---|---|
| **Introductory** | The name of the subject, a familiar use, neighboring everyday concepts | What happens, what used to go wrong, and which problem a technical term names |
| **Practitioner** | Basic operations, the main settings, terms that come up often | The mechanism behind an operation, failure conditions, exceptions |
| **Specialist** | Internal mechanisms, standard terminology, the representative prior debate | What is different this time, the evidence, objections, open points |

If the user does not specify, choose **introductory**. That does not mean "a reader who knows nothing." For example, you may assume that SQLite is a database that stores an application's data. You may not use rollback journal, WAL frame, end mark, or checkpoint mode without explaining them.

## Opening for an introductory reader

After the `TL;DR` that follows the title, the body uses this order as the default.

1. **A familiar situation** — show a situation the reader could be in.
2. **The old problem** — explain what collided, and what was inconvenient.
3. **The change** — explain how the new mechanism changes the problem.
4. **Names and internal mechanism** — define technical terms here, then go into detail.

A technical term that appeared in the `TL;DR` is still explained at its first use in the body. Do not pack background history into the opening. Put only the cause and effect the next explanation needs.

Before writing, leave this sentence in the working note.

> The reader's assumed level is **<introductory, practitioner, or specialist>**. **<known concepts>** are not explained. **<unknown concepts>** are introduced from **<a situation and the old problem>**.

Do not include this note in the finished manuscript.
