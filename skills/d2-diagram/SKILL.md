---
name: d2-diagram
description: Write a D2 diagram with elk, a d2-legend, fully qualified keys, a markdown title, and ${} substitution. Use when writing or fixing a D2 diagram.
license: MIT
metadata:
  author: hskksk
  version: 1.8.0
---


# Write a D2 diagram

Use this when writing, fixing, or reviewing D2 source. `references/overview.md` is the source of truth for the choices made on every diagram. The syntax for each choice lives in the detail file that overview points at. Read `overview.md` before writing, then open only the detail files for the parts you are writing.

Which color means confidence or status, what a solid or dashed line means in the domain, and which tool renders and checks the diagram, stay with the caller.

## When to use

- Write or revise a `.d2` diagram
- Fix a diagram that fails to compile, or whose edges, legend, or title do not match the intended structure

Do not use it for:

- A product-specific palette, an artifact filename, a session directory, or the name of a validation command

## Procedure

1. Read `references/overview.md`.
2. From that table, read only the detail files for the parts you are writing.
3. Write the `.d2` the way those files specify.
4. For the meaning of colors and line styles, and for the validation command, follow the caller when one exists. Otherwise make the meaning readable from the legend labels.

## Reference files

| File | Contents | When to read |
| --- | --- | --- |
| `references/overview.md` | Choices for every diagram, and pointers to the detail | Before writing a diagram |
| `references/layout.md` | Engines, direction, size, title, and `near` | When choosing layout or a title |
| `references/legend.md` | `d2-legend` | When adding a legend |
| `references/connections.md` | Keys, containers, connections, and arrowheads | When connecting shapes |
| `references/shapes.md` | Shapes, `sql_table`, `class`, sequence diagrams, and icons | When choosing a shape |
| `references/text.md` | Quotes, line breaks, markdown, and `${}` | When writing labels or variables |
| `references/style.md` | `style`, classes, and globs | When setting fill or stroke |
