---
name: skill-orchestration
description: Decide how a caller and a callable skill are written when several skills are combined into one job. The boundary is the skill name and the other skill's procedure only; do not point at another skill's files. Use when writing or reviewing a skill that calls other skills, or a skill that other skills should be able to call.
license: MIT
metadata:
  author: hskksk
  version: 1.7.0
---



# Combining skills

Set the boundary for connecting skills by name. Use this both when writing a caller and when writing a skill that others call. Both sides are the same reading of the boundary, so this skill is the source of truth. Do not split it into another skill.

Do not use this when the only task is to revise prose that neither calls other skills nor is called by them.

Decide which side the current task is, then read only the matching file. Do not read both sides in full at once.

| When | Read |
| --- | --- |
| Writing, revising, or reviewing a caller | `references/caller.md`. Read `references/practices.md` when you need the reasons |
| Writing, revising, or reviewing a skill that others call | `references/callable-skill.md`. Read `references/practices.md` when you need the reasons |
| Checking that the caller and the callable side match | `references/caller.md` and `references/callable-skill.md` |

## Boundary

The only things you may write across skills are these:

- The skill name
- When to read that skill
- The artifact you pass, and the condition for moving on after it returns
- One sentence that says to read that skill's `SKILL.md` and follow its procedure

The callable side puts an entry point that finishes the job with these four items in `description` and `SKILL.md`. The caller writes nothing beyond these four. Supporting files, scripts, section numbers, and template names do not leave that skill.
