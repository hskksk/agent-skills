---
name: survey-report
description: Route a research request to Phase 1 (exploratory) or Phase 2 (verification and structuring), choose front, middle, or rear weighting and a reader level, and write the report. Deliver a map plus three questions, or a conclusion tied to its evidence. Use when routing research requests and writing landscape or decision-oriented survey reports.
license: MIT
metadata:
  author: hskksk
  version: 1.7.0
---



# Survey report (phase × weighting × reader level)

Choose Phase 1 (exploratory) or Phase 2 (verification and structuring) for the request, decide weighting (front, middle, or rear) and reader level (introductory, practitioner, or specialist) separately, and write the report. The three axes are independent. The detailed rules live in `references/`. This file only guides the order of work and where to read.

## When to use

- You receive a research or survey request and will summarize it as a report
- You need to decide whether the job is a landscape and issue map (exploration) or a comparison, hypothesis check, or conclusion for a decision (verification)

Do not use this for a bare link list or a glossary alone.

## Procedure

1. **Choose the phase.** Follow the decision flow in `references/phase-routing.md`.
2. **Decide weighting and reader level.** Read `references/gravity.md` and `references/reader-level.md`, and choose each axis independently. Do not put the working note of why you chose them into the body.
3. **Read the matching phase guide and the shared rules.** For Phase 1 use `references/phase-1-guide.md`. For Phase 2 use `references/phase-2-guide.md`. Both follow `references/report-conventions.md`.
4. **Check before submission.** Run the common tests in `references/checklists.md` and the tests for the phase and weighting you chose. Optionally measure with `references/measure.py`.

## Reference files

| File | Contents | When to read |
| --- | --- | --- |
| `references/phase-routing.md` | How to choose Phase 1 or 2 | First |
| `references/gravity.md` | How to choose front, middle, or rear weighting, and where information goes | Before writing |
| `references/reader-level.md` | What introductory, practitioner, and specialist readers already know, and where the explanation starts | Before writing |
| `references/phase-1-guide.md` | Phase 1 artifacts and a structure sketch | When the phase is 1 |
| `references/phase-2-guide.md` | How Phase 2 ties the answer to its evidence | When the phase is 2 |
| `references/report-conventions.md` | Output rules shared by every phase | While structuring and writing |
| `references/checklists.md` | Pre-submission tests: common, by phase, and by weighting | Before submission |
| `references/measure.py` | Counts the shared metrics that can be counted (TL;DR, `[n]`, sources, length) | Before submission (optional) |

When the report is in Japanese, and the `japanese-writing` skill is available, read it before drafting and before revision, and follow its procedure.

## What this skill does not cover

It does not include how to run primary research (search-query design, API calls, interview design), or a particular organization's internal templates, save locations, or TTS/PR steps. The output is limited to the structure of a Markdown report and the shape of the argument.
