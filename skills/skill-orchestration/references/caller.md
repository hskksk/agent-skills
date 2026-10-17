# Caller

Read this when the table in `SKILL.md` says you are writing a caller. The callable entry point is in `references/callable-skill.md`. The reasons are in `references/practices.md`.

## Interface

The only things you may write about another skill are the four items in the boundary section of `SKILL.md`.

Do not name another skill's `references/`, `scripts/`, `assets/`, measurement scripts, checklist file names, section numbers, or internal template names. Do not put another skill's file paths in `allowed-tools` either.

When to open a supporting file is decided by the other skill's `SKILL.md`. The caller does not descend into it. Pointing at your own `references/` from your own `SKILL.md` is not part of this prohibition.

## Procedure

1. Cut the job into one piece. The caller owns order, handoff, and constraints that exist only in the caller's repository. It does not own the other skill's procedure.
2. Check whether an existing skill's `description` is enough. If it is, call it by name. If it is not, add a skill. Do not copy the other skill's prose in to fill the gap.
3. Write a routing table. The columns are only "when" and "skill to read." Say which skills not to read when the current job does not need them.
4. When the same judgment lives in two skills, write one sentence that names which role is the source of truth. Do not decide by which file is longer.
5. Write constraints that exist only in the caller's repository (save location, publish steps, output format) in the caller. Do not edit files of an imported skill.
6. For measurement and checks, follow the procedure of the skill that owns them. The caller may add only a gate: do not continue while the check is unmet. Do not copy the command string. When you need to allow execution, allow a capability such as `python3`, not the other skill's path.
7. When a skill is not installed, do not reimplement its rules on the spot. Write that it is read only when present.
8. Check for cycles. Do not let A call B and B call A.
9. After writing, search for a path that follows another skill's name. References to `references/` stay inside your own directory.

## Routing table

```markdown
| When | Skill to read |
|------|-----------|
| From before search through the survey check | `how-to-survey` |
| Before drafting the body and before submission | `survey-report` |
| When the output is Japanese, before drafting and before revision | `japanese-writing` |
```

After the table, write the artifact you pass and the local constraints in prose. Do not put the other skill's file names in table cells.

## What stays in the caller

- Save location and frontmatter
- Publish steps
- Output format that exists only in this environment (for example diagram notation, or a length cap for speech)

Do not restate headings, citation style, or search counts that the other skill already decides.

## Install location

The source of truth for the install location is that environment's skills directory (often `.agents/skills/<name>/`). A symlink for another harness is only for pointing at the same directory. It is not for exposing another skill's contents. Install an external skill and read it by name. Do not bundle or link the other skill's `references/`.
