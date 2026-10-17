# Skill authoring guide

This guide is for designing skills that are easy to reuse and, later, to split, merge, or promote. Do not pack a skill's content into one long instruction. Aim for a shape that, given the user's request, selects the pieces it needs and points at the right procedure and references.

Skill prose in this catalog is English, except skills about Japanese such as `japanese-writing`.

## Design basics

### 1. The skill is the entry and the guide; a reference is the source of truth for an independent rule

- In the frontmatter `description`, write what the skill can do and when to use it. Do not pack the detailed procedure in. Make the description enough to recognize the request that should trigger it.
- In `SKILL.md`, write when to use it, how the work proceeds, and which material to read when.
- Put an axis of judgment, a phase of work, an output specification, or a detailed rule that can be explained on its own into `references/`.
- Do not define the same rule in several files. Put the source of truth for the body in one place. Other files refer to it or turn it into a check.
- So a reference can be read only when needed, `SKILL.md` says when to read it.

### 2. Split by independence of responsibility, not by heading count

Candidates for their own file include elements such as these.

- An independent axis of judgment (reader, purpose, weighting, risk, and so on)
- A phase or method the user can choose
- An output specification, template, or quality bar that can be used on its own
- A procedure used repeatedly, or a process that can be run mechanically

Before you split a file, check the following.

1. Can that file alone make its purpose and terms clear?
2. Can you change, move, or reuse that element without rewriting the rest?
3. Can you state when to read it?
4. Does a second source of truth for the same rule not remain in another file?

If several answers are no, the material may still be one responsibility. The reverse is also a miss: slicing sections mechanically until the pieces cannot be understood without cross-references. Prefer the balance of independence and readability.

### 3. MECE is a goal, not a mechanical split rule

Use MECE to reduce overlap and gaps. You do not have to force every element into its own file. When several elements are always used together and change for the same reason, one reference is easier to handle.

Assign each rule a file that is its source of truth. Do not copy exceptions or shared rules into several places. Link to the source of truth from where it is needed.

## Boundaries among skill, reference, and script

| Location | What goes there | How to judge |
|---|---|---|
| `SKILL.md` | Trigger conditions, the overall flow, guidance for choices and references | Is it a short instruction needed every time the skill is used? |
| `references/` | Criteria, detailed procedure, a guide for a domain, conventions | Is it knowledge a person judges by reading the context? |
| `scripts/` | Measurement, conversion, verification, and other reproducible processing | Are the input and output fixed, and is machine execution more stable? |
| `assets/` | Templates, figures, fixed material | Is it a file used in the artifact itself? |
| `checklists` | Checks before submission or after a run | Does it test whether an established rule was actually met? |

Do not make a checklist a second source of truth for the rules. Turn items into questions that can be judged, and put the detailed rule in the matching reference. A script's result also does not mechanically decide words or quality that need a judgment in context. Separate required conditions that can be measured for certain from reference information that is checked by eye.

## One skill, or a separate skill

When the source material is several skills, do not paste the files into one. First sort out the shared purpose and the differences.

### Keep them in one skill

- The user's request and the area of work are close, and the right method can be chosen from a shared entry.
- The methods can share terms, shared rules, and quality bars.
- The chosen method does not have to be run, in order, for every method, without the user asking.

In that case, make `SKILL.md` a router and put each method's guide in its own reference. Align the chapter outline of each guide, and change only what is specific to the method, such as required artifacts. Put the shared part in its own reference. **If the methods are choices, do not quietly turn them into steps that always run in order.**

### Make them separate skills

- It can be triggered by an independent request, and it has a different user intent, artifact, or procedure.
- It can be explained on its own, without depending on another skill's router or shared rules.
- Separate selection and maintenance is better, to avoid colliding trigger conditions or instructions.

When you promote a reference into its own skill, do not stop at cutting it out. Give that element its own `name`, `description`, trigger conditions, procedure, and quality bar. Do not leave an unnecessary dependency on the destination in the original skill.

Skills are sometimes distributed and used separately. Do not refer directly to another skill's internal files. If sharing is required, bundle what both need, or design a layout that can be distributed on its own. The entry point for connecting by name, and what a caller may write, has its source of truth in `skill-orchestration`. Do not copy that into this guide.

## How to create or reorganize

### 1. Inventory the request and the material

Write the following down briefly.

- What the skill should make possible
- Which requests trigger it, and which do not
- What the artifact and the success condition are
- What the branches of the work, the shared rules, and the constraints are
- What to keep from existing files or from the user's changes

When merging several skills, find the shared part and the branch points while keeping the problem each original skill solved. Do not guess a role from the file name. Read the content before you move or merge it.

### 2. Decide responsibilities and the source of truth

Split the content along the following views, and decide which file owns each item.

| View | What to decide |
|---|---|
| Routing | Which request chooses which method or phase |
| Shared principles | Which rules apply to every method |
| Guides by method | What the chosen method's artifacts and procedure are |
| Information design | What is chosen on a separate axis, such as reader, priority, or form |
| Verification | What a person checks, and what a script measures |

For each item, recording "source of truth," "when to read," and "other files it uses" makes overlap and missing references easier to find.

#### Example: reorganizing survey-report

An example of splitting material that had been mixed in one guide into methods chosen from a shared entry, and into independent axes of judgment.

| Responsibility | File | When to read |
|---|---|---|
| Choosing the phase | `references/phase-routing.md` | First |
| Artifacts specific to Phase 1 and 2 | `references/phase-1-guide.md` / `references/phase-2-guide.md` | According to the method chosen |
| Weighting and reader level | `references/gravity.md` / `references/reader-level.md` | When deciding the structure |
| Shared writing rules | `references/report-conventions.md` | While structuring and writing |
| Quality checks and measurement | `references/checklists.md` / `references/measure.py` | Before submission |

Phase 1 and Phase 2 stayed in one skill as choices in the same area, and the chapter outline of each guide was aligned. Weighting and reader level were separated as axes decided independently. This is an example of a structure, not a template to drop onto another skill as-is.

### 3. Design the read order

A typical order is **confirm the trigger → choose the method you need → read the shared rules and only the relevant detail → do the work → check quality**. Do not design it so every reference is read every time. Refer to each file by a relative path from `SKILL.md`, and write the condition for reading it.

### 4. Move and merge files

- Set one source of truth for a rule. Replace duplicates with a reference instead of copying the same wording.
- Align the chapter outline of similar guides by method: purpose, structure, detail, optional elements, and so on.
- Before deleting an old file, check what refers to it and where the content that is still needed moved.
- Keep a reference complete inside the skill's directory, so it is not missing when the skill is distributed on its own.

### 5. Do a first-look review and verify

Have a reviewer who does not know the conversation's background read `SKILL.md` and every reference. Check at least the following.

- Are the trigger conditions, and the conditions for not using it, clear?
- Is it clear what to read, in what order?
- Can required artifacts be told from optional elements?
- Is there more than one source of truth for the same rule? Do the guide and the checklist contradict each other?
- Do relative references exist, and are the files the distributed skill needs present inside it?
- Does a script mechanically decide judgments that depend on context?

Check behavior with a realistic example request that fits the skill. When the output can be verified objectively, add a test. When it is subjective, such as prose quality, weight the first-look review. Before you run a verify command, check its side effects and the artifacts it produces.

## Promises specific to this repository

The catalog rules for this repository have their source of truth in [`../AGENTS.md`](../AGENTS.md). When you add a skill, also add it to `groupings` in [`../skills.sh.json`](../skills.sh.json). When you create a new skill or a change, also check layout, metadata, release, and commit conventions, and do not copy them into this guide.
