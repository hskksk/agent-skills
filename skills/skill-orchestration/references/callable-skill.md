# Callable side

Read this when the table in `SKILL.md` says you are writing a skill that others call. The caller's prohibitions are in `references/caller.md`. Here, write an entry point that finishes the job without the caller looking inside.

## What to publish

The entry point is only `description` and `SKILL.md`.

- In `description`, write when to use the skill, when not to, and the artifact it returns. Do not name supporting files.
- In `SKILL.md`, write the artifact you receive, the procedure, when to read your own supporting files, and the artifact you return.
- Put measurement commands, how to run checks, and the rule that you fix failures before finishing in your own `SKILL.md`. The caller should not have to copy the commands.
- Point at your own `references/`, `scripts/`, and `assets/` with relative paths from your own `SKILL.md`. Those paths are not a published entry point.

## What not to assume

- That a particular caller has already been read
- The caller's save location, length limits, publish steps, or diagram notation
- Paths to another skill's supporting files or scripts
- That the other side has pinned your section numbers or file names

When another skill is needed, name it and say to read it only when it is present. When it is absent, do not reimplement its rules on the spot.

## One job

A callable skill returns one artifact that a caller can point at from a single row of a table. A survey returns survey notes and sources. A prose pattern returns that prose. Cut the job that way. Saving and publishing are the caller's constraints. Do not make them required steps of the callable skill.

Name the returned thing as an artifact, not as a file name. The caller should not have to write "fill this table in that file."

## Script output

When a script prints a relative path, say in `SKILL.md` that the path is from this skill's directory. The caller does not copy that sentence into its own procedure.

## After writing

- Can you tell, from `description` alone, when to use the skill and what comes back?
- Does `SKILL.md` alone contain no paths other than this skill's supporting files?
- Does a path sit immediately after another skill's name?
- Has a save location or product name from a particular repository become a required condition of the procedure?
