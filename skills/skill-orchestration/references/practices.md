# Why the combination works this way

The reasons for the procedure in `SKILL.md` live here. Other skills do not open this file directly. This skill's `SKILL.md` says to read it when the reasons are needed.

## Published practice

### Disclosure has three stages

The Agent Skills specification does not read a whole skill at once. At startup it sees only `name` and `description`. It reads `SKILL.md` after the task matches. It reads a supporting file only when that `SKILL.md` says to open it now.

If the caller opens another skill's `references/` directly, it skips the middle stage. The condition for when to read, and the warnings that exist only in `SKILL.md`, drop out. If the other skill moves a file, the caller's path stays behind and breaks.

### One skill, one job

Skill-authoring guidance asks you to cut a skill at the same granularity as a function. Too narrow, and several skills load at once for one job and their instructions collide. Too broad, and the skill does not trigger when it is needed.

What the caller may add is order, and constraints that exist only on the caller. If the caller summarizes the other skill's procedure and absorbs it, that skill owns both jobs and drifts on every update.

### Read only the skills you need

Composite-skill examples (APM composite skills) do not load every dependency into context. The body is a routing table that says when and which skill to read. When another job's procedure would mix in, name the skills you will not read. Do not copy components into the caller's directory. Keep them as separate skills.

The Agent Skills specification does not resolve `kind` or `dependencies`. Unknown frontmatter is ignored, so write dependencies in a table in the body. Do not use install-time dependency resolution.

A cycle is a defect in the dependency. Do not build a shape where A calls B and B calls A. A skill does not write its procedure on the assumption that another skill was read first. Only the caller knows the order.

### Selection uses description

If a person cannot pick the right skill by reading `description`, an agent cannot either. That is true both for search over a large skill set and for a small hand-written routing table. Automatic assignment of hundreds of skills is heavy while the skill count is still small. Until then, a table is enough.

What `description` may contain is when to use the skill and the names of skills it combines. Adding internal file names does not improve startup selection. At startup, only `description` is read.

### The skill that owns the check owns the check

Skill-authoring guidance recommends a loop: verify after the work, and fix until it passes. The skill that owns the verification is the one that knows the items and the commands. What the caller may own is only the gate: do not continue while a failure remains. If you copy the items, an old list stays after the other skill changes them.

## Decisions adopted here

### One source of truth for the boundary

The caller's prohibitions and the callable entry point are the same reading of the boundary. If you split them into separate skills, the question "may I write a path?" has two homes, and only one of them goes stale. The callable side lives in `references/callable-skill.md`. The caller lives in `references/caller.md`. Write `description` so this skill triggers for either task.

### Writing a path is the same coupling as bundling

Even if you do not copy the other skill's `references/`, a path depends on its internal layout. When the other skill renames a file, the caller breaks. That is the same kind of failure as a copy that diverges.

The references you allow are the skill name and, as the other skill's entry point, `SKILL.md`. `SKILL.md` is the published procedure. Supporting files are implementation.

### Do not put the other skill's paths in the permission list

If `allowed-tools` names another skill's script path, the permission scope becomes that skill's directory layout. Only the `SKILL.md` of the skill that owns the script holds the command string. The caller writes "run the command written in that skill." When permission is required, allow a capability such as `python3`.

If the other skill's script says "see `references/checklists.md`", that path is relative to the other skill's directory. Copying that sentence into the caller's procedure makes it unclear which skill's `references/` is meant.

### Pick one source of truth by role

When two skills hold the same judgment, the caller does not have both files read and reconciled. It writes one sentence by role. Survey execution is `how-to-survey`. The shape of the deliverable is `survey-report`. Which supporting file is longer is not material the caller uses to choose.

### Do not write local concerns into an imported skill

Constraints that exist only in the caller's repository, such as save location, publish steps, and output format, are written in the caller. Writing them into an imported file means the next install erases them, or the file diverges from upstream.

### A symlink shows the same skill to another harness

A link that shows the same skill from another harness points at the install directory. A link that points at another skill's `references/` is the same coupling as a path reference, so do not add it.

### Name the handoff by the artifact

"Write the report after the survey notes and source list exist" is a caller sentence. "Fill the table in the other skill's search-plan file, then write the layer in the other skill's structure guide" is the other skill's internal structure. Do not write section names, layer numbers, or script flags.

### Do not invent the rules of a missing skill

When a needed skill is not installed, the caller does not summarize its rules as a substitute. A substitute becomes a one-off copy. Write "when the skill is present, follow its `SKILL.md`." When it is absent, either skip that job or tell the user the missing skill name.

### Do not point at another skill's internal rules as an exception

Writing "use this skill except for the other skill's particular template" depends on a name inside the other skill. After that template disappears, only the exception sentence remains. Write the scope of application as your own job. If the other skill's artifact needs a special case, the special case belongs in that skill's `SKILL.md`.

## Sources

- Progressive disclosure in the Agent Skills specification, and [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) (granularity, context, when to open supporting files, the verification loop)
- [APM Composite Skills](https://docs.apm.orthg.nl/docs/composite-skills) (routing tables, do not copy components, do not create cycles, do not read everything at once)
- [Progressive Disclosure for Layered Agent Definitions](https://agentpatterns.ai/patterns/agent-design/progressive-disclosure-agents/) (skills are self-contained and do not assume a hidden read order)
- [Compositional Skill Routing](https://agentpatterns.ai/context-engineering/compositional-skill-routing/) (a skill a person cannot choose from `description` is one an agent cannot choose either; while the skill count is small, do not use large-scale automatic assignment)
