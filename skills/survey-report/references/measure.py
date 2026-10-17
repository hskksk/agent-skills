#!/usr/bin/env python3
"""Count the shared metrics that can be counted for a survey-report.

    python3 references/measure.py \\
      --model front|middle|rear \\
      <report-file>

Judge whether the structure fits in references/checklists.md. This script
checks shared metrics that can be counted without forcing weighting back into
a fixed table of contents. Words whose fitness depends on context stay a
reference display. Report the output as it is. Do not rewrite the numbers by
hand, and do not ignore a missed required metric.

Japanese bodies are measured in characters, with Japanese prose checks. Other
bodies are measured in words. Marker headings stay English either way.
"""

import argparse
import re
import statistics
import sys
from pathlib import Path


APPENDIX = "## Appendix: Sources"
APPENDIX_ALIASES = (APPENDIX, "## 付録: 出典一覧")
INTERNAL = (
    r"前重心|中重心|後重心|価値の中心|"
    r"front weighting|middle weighting|rear weighting|center of value"
)
INTERNAL_CANDIDATES = (
    r"見取り図|射程|骨格|スロット|\bL1\b|\bL2\b|\bL3\b|主張[0-9]|\bclaim [0-9]\b"
)
CALQUE = (
    r"運ぶ|稼ぐ|表面積|不等式|コスト関数|去就|"
    r"足すのは|買うもの|買い戻す|肩代わり|が教えてくれる"
)
SAY_FINAL_JA = r"(述べる|書く|指摘する|明言する|論じる)。$"
SAY_FINAL_EN = r"\b(says|writes|notes|argues|points out|states)\.$"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        required=True,
        choices=("front", "middle", "rear"),
        help="Primary weighting. Used for the report and for choosing checklist tests, not for judging structure",
    )
    parser.add_argument("path", type=Path)
    return parser.parse_args()


def looks_japanese(text):
    japanese = len(re.findall(r"[\u3040-\u30ff\u4e00-\u9fff]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if japanese < 20:
        return False
    return japanese / (japanese + latin) >= 0.3


def split_report(text):
    parts = text.split("---", 2)
    body = parts[2] if len(parts) > 2 else text
    body = re.sub(r"\{% diagram.*?\{% /diagram %\}", "", body, flags=re.S)
    for heading in APPENDIX_ALIASES:
        if heading in body:
            main, appendix = body.split(heading, 1)
            return main, appendix, heading
    return body, "", None


def prose_units(main, japanese):
    paragraphs, current = [], []
    for line in main.splitlines():
        stripped = line.strip()
        if line.startswith(("#", "|")) or not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
        elif line.startswith(("-", "*", "`", ">")):
            continue
        else:
            current.append(stripped)
    if current:
        paragraphs.append(" ".join(current))
    splitter = r"(?<=。)" if japanese else r"(?<=[.!?])\s+"
    sentences = [
        sentence.strip()
        for paragraph in paragraphs
        for sentence in re.split(splitter, paragraph)
        if len(sentence.strip()) > 3
    ]
    return paragraphs, sentences


def word_count(text):
    return len(re.findall(r"\b[\w']+\b", text))


def source_names(appendix, body):
    """Collect author and organization names from the appendix for the subject-position check."""
    generic = {
        "URL", "HTTP", "HTTPS", "PDF", "ETL", "ELT", "LLM", "AI", "API", "SQL",
        "Blog", "Docs", "Forum", "Things", "Knowledge", "Proceedings", "Inc",
        "Community", "Alliance", "Engineers", "Techniques", "Keynote",
    }
    names = set()
    for line in appendix.splitlines():
        line = re.sub(r"^[-*\s]*\[?\d+\]?[.)]?\s*", "", line)
        if not line:
            continue
        head = re.split(r"[,、（(【\[]", line)[0]
        names.update(
            re.findall(
                r"[A-Z][A-Za-z0-9\-.&']{2,}"
                r"(?:\s[A-Z][A-Za-z0-9\-.&']{2,})?",
                head,
            )
        )
        names.update(
            re.findall(
                r"[\u4e00-\u9fa5\u3041-\u309f\u30a1-\u30f6]{2,6}(?=氏)",
                head,
            )
        )
    return {
        name
        for name in names
        if len(name) > 2
        and name not in generic
        and not (
            any(part in generic for part in name.split())
            and len(name.split()) == 1
        )
        and len(re.findall(re.escape(name), body)) <= 15
    }


def result(label, value, ok, note="", *, required=True):
    if required:
        mark = "OK " if ok else "NG "
    else:
        mark = "ref"
    print(f"  {mark} {label:<36} {str(value):>12}   {note}")
    return ok or not required


def main():
    args = parse_args()
    text = args.path.read_text(encoding="utf-8")
    body, appendix, appendix_heading = split_report(text)
    japanese = looks_japanese(body)
    paragraphs, sentences = prose_units(body, japanese)
    if not sentences:
        print(f"{args.path}: no prose found. Check how the body was split.")
        return 2

    if japanese:
        lengths = [len(sentence) for sentence in sentences]
        paragraph_lengths = [len(paragraph) for paragraph in paragraphs]
        body_size = len(body)
        body_size_label = "Body characters"
        body_size_note = "Reference only. No minimum"
        mean_label = "Mean characters per sentence"
        mean_note = "Advisory: 95 or fewer. No minimum"
        long_sentence_label = "Sentences over 150 characters"
        long_sentence_count = sum(length > 150 for length in lengths)
        long_sentence_note = "Consider splitting after reading the content"
        long_paragraph_label = "Paragraphs over 250 characters"
        long_paragraph_count = sum(length > 250 for length in paragraph_lengths)
    else:
        lengths = [word_count(sentence) for sentence in sentences]
        paragraph_lengths = [word_count(paragraph) for paragraph in paragraphs]
        body_size = word_count(body)
        body_size_label = "Body words"
        body_size_note = "Reference only. No minimum"
        mean_label = "Mean words per sentence"
        mean_note = "Advisory: 28 or fewer. No minimum"
        long_sentence_label = "Sentences over 40 words"
        long_sentence_count = sum(length > 40 for length in lengths)
        long_sentence_note = "Consider splitting after reading the content"
        long_paragraph_label = "Paragraphs over 120 words"
        long_paragraph_count = sum(length > 120 for length in paragraph_lengths)
    long_paragraph_note = "Split if the paragraph has two topics"
    body_chars = len(body)
    bold = re.findall(r"\*\*[^*]+\*\*", body)
    bold_density = len(bold) / body_chars * 1000 if body_chars else 0
    cites_used = {int(value) for value in re.findall(r"\[(\d+)\]", body)}
    cites_listed = {
        int(first or second)
        for first, second in re.findall(
            r"^[-*\s]*(?:\[(\d+)\]|(\d+)[.)])\s",
            appendix,
            re.M,
        )
    }
    urls = set(re.findall(r"https?://[^\s)>\]]+", appendix))
    names = source_names(appendix, body)
    name_re = "|".join(re.escape(name) for name in names) if names else r"(?!x)x"
    if japanese:
        subject_re = (
            r"^.{0,25}?(" + name_re + r")(?:\s*(?:の|は|が|も|では|による|によれば|を))"
        )
        say_pattern = SAY_FINAL_JA
        say_label = 'Sentences ending with "X states"'
    else:
        subject_re = (
            r"^.{0,80}?\b("
            + name_re
            + r")\b\s+(says|writes|notes|argues|claims|reports|states)\b"
        )
        say_pattern = SAY_FINAL_EN
        say_label = 'Sentences ending with "says" or "writes"'
    subject_pos = [
        sentence for sentence in sentences if re.search(subject_re, sentence)
    ]
    internal = re.findall(INTERNAL, body)
    internal_candidates = re.findall(INTERNAL_CANDIDATES, body)
    calque = re.findall(CALQUE, body) if japanese else []
    say = [sentence for sentence in sentences if re.search(say_pattern, sentence)]
    h2 = [line[3:].strip() for line in body.splitlines() if line.startswith("## ")]
    h3 = [line[4:].strip() for line in body.splitlines() if line.startswith("### ")]
    tldr_match = re.search(
        r"(?:^|\n)## TL;DR\s*\n(.*?)(?=\n## |\Z)",
        body,
        re.S,
    )
    tldr_items = (
        re.findall(r"^\s*[-*]\s+(.+)$", tldr_match.group(1), re.M)
        if tldr_match
        else []
    )
    sentence_mark = r"[。！？!?]" if japanese else r"[.!?]"
    tldr_multi_sentence = [
        item for item in tldr_items if len(re.findall(sentence_mark, item)) > 1
    ]

    print(f"\n{args.path}")
    print(f"Primary weighting: {args.model}")
    print(f"Body language: {'Japanese' if japanese else 'not Japanese'}")
    print("\nBody (before the source appendix, figures removed)")

    checks = []
    checks.append(
        result(
            "First H2 is ## TL;DR",
            h2[0] if h2 else "no H2",
            bool(h2) and h2[0] == "TL;DR",
            "Place it immediately after the title",
        )
    )
    checks.append(
        result(
            "TL;DR item count",
            len(tldr_items),
            3 <= len(tldr_items) <= 5,
            "3 to 5 items",
        )
    )
    checks.append(
        result(
            "TL;DR is one sentence per item",
            len(tldr_multi_sentence),
            not tldr_multi_sentence,
            "Multi-sentence items should be 0",
        )
    )
    result(body_size_label, body_size, True, body_size_note, required=False)
    result("Prose sentences", len(sentences), True, "", required=False)
    result(
        "H2 / H3 count",
        f"{len(h2)} / {len(h3)}",
        True,
        "Judge the hierarchy with the table-of-contents test",
        required=False,
    )
    result(
        mean_label,
        f"{statistics.mean(lengths):.1f}",
        True,
        mean_note,
        required=False,
    )
    result(
        long_sentence_label,
        long_sentence_count,
        True,
        long_sentence_note,
        required=False,
    )
    result(
        long_paragraph_label,
        long_paragraph_count,
        True,
        long_paragraph_note,
        required=False,
    )
    result(
        "Bold density per 1000 characters",
        f"{bold_density:.1f}",
        True,
        f"Advisory 3 to 8 (count {len(bold)})",
        required=False,
    )
    checks.append(result("[n] citations", len(cites_used), bool(cites_used), "1 or more"))
    checks.append(
        result(
            "Internal terms",
            len(internal),
            not internal,
            f"Target 0 {sorted(set(internal)) if internal else ''}",
        )
    )
    result(
        "Internal-term candidates (check context)",
        len(internal_candidates),
        True,
        f"Reference. Check hits in context {sorted(set(internal_candidates)) if internal_candidates else ''}",
        required=False,
    )
    if japanese:
        result(
            "Calque candidates (check context)",
            len(calque),
            True,
            f"Reference. Check hits in context {sorted(set(calque)) if calque else ''}",
            required=False,
        )
    checks.append(result(say_label, len(say), not say, "Target 0"))
    subject_pct = len(subject_pos) / len(sentences) * 100
    result(
        "Sentences with a source name as subject",
        f"{subject_pct:.0f}%",
        True,
        "Advisory: 10% or under. Exception when the author is the subject",
        required=False,
    )

    print("\nSources")
    checks.append(
        result(
            "## Appendix: Sources",
            appendix_heading or "missing",
            appendix_heading == APPENDIX,
            "Target of the numbered citations",
        )
    )
    result(
        "Distinct URLs",
        len(urls),
        len(urls) >= 8,
        "Advisory: 8 or more. Survey more if the set is thin for the purpose. Do not inflate the count with other editions of the same work",
        required=False,
    )
    undefined = cites_used - cites_listed
    checks.append(
        result(
            "Undefined numbers cited in the body",
            len(undefined),
            not undefined,
            f"{sorted(undefined) if undefined else ''}",
        )
    )
    unused = cites_listed - cites_used
    result(
        "Sources unused in the body",
        len(unused),
        True,
        f"Confirm they are meant to remain as a source list {sorted(unused) if unused else ''}",
        required=False,
    )

    print("\nMarkdoc")
    diagrams = re.findall(r"\{% diagram.*?\{% /diagram %\}", text, flags=re.S)
    checks.append(
        result(
            "diagram fences",
            f"{len(diagrams)}",
            all("```" in diagram for diagram in diagrams),
            "The figure does not render unless it is fenced",
        )
    )
    broken_bold = re.findall(r"\*{3,}", body)
    checks.append(
        result(
            "Broken bold markup",
            len(broken_bold),
            not broken_bold,
            "Fix `****` and nested bold",
        )
    )
    diagram_bold = [diagram for diagram in diagrams if "**" in diagram]
    checks.append(
        result(
            "Markdown bold inside a figure",
            len(diagram_bold),
            not diagram_bold,
            "Use <b> for emphasis in Mermaid",
        )
    )
    entry_urls = re.findall(
        r"^[-*\s]*(?:\[\d+\]|\d+[.)])\s.*?(https?://[^\s)>\]]+)",
        appendix,
        re.M,
    )
    duplicates = len(entry_urls) - len(set(entry_urls))
    checks.append(
        result(
            "Duplicate numbers for the same URL",
            duplicates,
            duplicates == 0,
            "Register the same page only once",
        )
    )

    failed = sum(not check for check in checks)
    print(f"\nRequired common metrics missed: {failed} / {len(checks)}")
    print(
        "Judge structure with the common tests in references/checklists.md "
        f"and the {args.model} weighting tests."
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
