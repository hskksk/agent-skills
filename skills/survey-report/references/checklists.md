# Checks before submission

Use this immediately before you output or save the report. Run the common tests first, then the tests for the primary weighting you chose. Do not estimate countable metrics by eye. Run the helper script `measure.py` (optional; still do the visual tests below if it is missing).

```bash
python3 <path-to-survey-report>/references/measure.py \
  --model <front|middle|rear> \
  <report-file>
```

Report the script's output as it is. Whether the structure fits is not decided by numbers alone, so judge the weighting tests by pointing at the relevant places in the manuscript. **Do not rewrite the numbers by hand.**

## Common tests

### 1. Question and reader

- Can you state the question the report answers in one sentence?
- Can you state what the main reader will be able to do after reading?
- Have you chosen one assumed level: introductory, practitioner, or specialist?
- Have you separated terms the reader may use without explanation from terms the body introduces?
- Is there a reason for the reader to spend time, beyond the theme being interesting?

If there are several questions, decide which is primary. If the reader is unspecified, choose introductory. Organizing the table of contents without narrowing the subject does not fix it.

### 2. Separating the axes

- Can you state in one sentence why you chose Phase 1 or 2?
- Have you chosen one primary weighting: front, middle, or rear?
- Can you point at one artifact that is the center of value?
- Is there at most one secondary weighting?
- Do page space, primary sources, and the best figures gather on the primary weighting?
- Has a fixed frame from another model lingered out of habit?
- Do the working terms "front weighting", "middle weighting", "rear weighting", and "center of value" stay out of the body?

"Everything is important" means you have not chosen. Make the part you can least cut the primary weighting.

### 3. Opening

Is there `## TL;DR` immediately after the title, so the main conclusions can be grasped in 3–5 items? Is each item one sentence? Does it state content rather than method or chapter structure, and does it keep conditions and serious reservations?

Can the question, scope, and why it is worth reading be understood from the opening that follows? For front weighting, also check the answer and conditions. For middle weighting, the axes of classification. For rear weighting, how the work will be evaluated.

Do not fix the overview's heading count or sentence count. Rewrite an opening that is only a preview of each section, a report that you surveyed, or an explanation of this skill's structure.

For an introductory reader, check the material after the TL;DR in this order.

1. Did you show a concrete situation the reader could be in?
2. Did you explain what used to collide, and what was difficult?
3. Did you make what the new mechanism changed understandable without technical terms?
4. Did you introduce technical terms and the internal mechanism after that?

A term that appeared in the TL;DR is explained again at its first use in the body. The check fails if an unknown term is defined only by another unknown term.

### 4. Table of contents

Does the table of contents support the main way of reading?

- Reading only `##`, can you see the path of the report, such as background, mechanism, constraints, and operations?
- Reading through `###`, can you follow concrete findings, questions, and comparison targets?
- Have you split with `###` wherever the explanatory role changes, regardless of length?
- Has a long `##` section become one block of explanation with no subheadings?
- Does front weighting move from the point to the evidence, middle weighting from comparison axes to the subjects, and rear weighting from the question to the evidence and the discussion?

Not every heading has to be a conclusion sentence. Also fix a heading that cannot be told apart from its neighbor, such as `## Details`, and a long heading that stuffs the body into the heading.

### 5. Evidence and interpretation

- Do `[n]` and `## Appendix: Sources` correspond?
- Have you distinguished what a source says from this report's interpretation?
- Is it clear what is still unchecked?
- Is it clear where you have not read the primary source?
- Are counterexamples, limits of application, and bias in the sources placed where they arrive in time for the judgment?

### 6. Evidence survives

Does the appendix keep the following?

- The core sources for each section
- **Important branches you investigated and did not adopt, and why**
- Timelines, people, and adjacent fields cut from the body that would help a later survey
- Identifying information for sources whose URL cannot be checked

Shortening means moving material down a layer. It does not mean deleting evidence.

### 7. Choice of form

- Is reasoning written as prose?
- Are elements, angles, and conditions whose reading order does not change the meaning in a list?
- Do list items share grammar and level of abstraction, without packing several points into one item?
- If four or more subjects share the same columns, did you consider a table?
- Do you use a figure only to show a relationship such as cause, dependency, or order?
- Is there no fact that exists only in a figure?

A landscape figure is not required. Place one only when a figure makes the relationship clearer.

### 8. When the report is in Japanese

- Are source names not biased toward being the grammatical subject?
- Do sentences not end with "X states" or "X writes" (「〜は述べる」「〜は書く」)?
- Are calques and coined words that `japanese-writing` rejects still present?
- Do the working terms 「前重心」「中重心」「後重心」「価値の中心」 stay out of the body?
- Does the body expose production process the reader does not need, such as revision history, comparison with an old draft, or the writing session?
- Did you fix repetition, nominalization, and empty prefaces with the `japanese-writing` revision procedure?
- Do headings, paragraph breaks, tables, figures, and bold give a reader scanning on a diagonal something to hold onto?

### 9. Measurement

Check the common metrics from `measure.py`. When a required metric is missed, look at the manuscript and fix it. Do not overwrite the numbers by hand. Candidate-word hits are a reference display, so judge them in context.

For a Japanese body the script reports characters. For other bodies it reports words. Body length is a reference value and has no minimum. Judge a thin survey by distinct sources, the share of primary sources, and whether opposing sources are present, not by length.

## Tests by phase

### Phase 1 (exploratory)

1. Does the L1 overview or the opening contain a summary of the landscape?
2. **Have you presented three "questions to solve next"?** Does each question have one sentence on why it matters?
3. Is the landscape structured as relationships among elements, axes of conflict, and players? A figure is not required.
4. Has it not become a mere glossary or link list?
5. If the work will continue to Phase 2, is it shown which question to start from?

### Phase 2 (verification and structuring)

1. Does `## Overview` contain the answer (one sentence), the axes of judgment, and the survey scope?
2. Do the claims that support the answer correspond to chapters in the body? The count is not fixed.
3. Does each claim mention evidence, a concrete example, and a limit?
4. Can the conclusion be followed by reading the headings alone?
5. If you include `## Summary`, does it not contradict the answer in `## Overview`?

## Tests by weighting

### Front weighting

1. Can the opening yield the answer, the main reasons, the conditions, and the scope?
2. If the reader stops after the opening, do dropped reservations not create a misunderstanding?
3. For an introductory reader, did you place a foothold for understanding instead of jumping from the conclusion straight into the internal mechanism?
4. Does the body add evidence, counterexamples, and limits of application, rather than paraphrasing the opening?
5. If there is a recommendation, did the user ask for it, and does the evidence support its strength?
6. Is the ending not a long restatement of the opening?

### Middle weighting

1. Does the opening make the scope and the axes of comparison or classification clear?
2. Can the reader find, from the body, the set of options, the differences, the exceptions, and bias in the evidence?
3. Do the table columns match the comparison axes, without changing conveniently per subject?
4. Have you not dropped cases that do not fit a single conclusion?
5. Is the wrap-up not merely reading the body's tables aloud again?

### Rear weighting

1. Does the opening make the question, why it matters, the scope, and the method of evaluation clear?
2. Can source selection, method, results, and interpretation be followed as distinct?
3. Is the final discussion derived only from evidence shown in the body?
4. Have you treated counterevidence, alternative explanations, and the limits of generalization?
5. Is the provisional answer in the opening not an assertion made before the argument?

## Mixed-weighting test

Run this only when you set a secondary weighting.

1. Can you state the role of the primary weighting and the secondary weighting in separate sentences?
2. Is the secondary weighting a path into the primary weighting, or a path for reuse?
3. Have page space and figures not split in half, erasing the primary weighting?
4. Have you not added a third weighting?

## Order for repairing a manuscript that is too long

1. Write the reader's purpose and the center of value, one sentence each.
2. Mark sections that do not support the primary weighting.
3. Move important evidence to the appendix, and delete only duplication.
4. Rebuild the table of contents in the order of the primary weighting.
5. Write the TL;DR in 3–5 items. One sentence per item, and only the main conclusions.
6. Rewrite the opening to match the model.
7. Move independent enumerations to lists, and comparisons that share columns to tables.
8. Split long sections where the explanatory role changes — question, mechanism, condition, exception — not by length.
9. Replace source names with `[n]`, and put the subject back on the topic.
10. When the report is in Japanese, fix repetition, nominalization, and empty prefaces with the `japanese-writing` revision procedure.
11. Run `measure.py`.
12. Run the common tests and the tests for the weighting you chose once more.
