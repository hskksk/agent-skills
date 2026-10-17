# D2 overview

Read this file before writing a diagram. It holds only the choices used every time. The source of truth for syntax is the detail file below; open only the ones you need. What a color means, and which command checks the diagram, sit outside this skill.

The source is the [D2 tour](https://d2lang.com/tour/).

| File | Source of truth for | When to open |
| --- | --- | --- |
| `layout.md` | Engines, `d2-config`, direction, size, title, and `near` | When choosing layout or a title |
| `legend.md` | `d2-legend` | When adding a legend |
| `connections.md` | Keys, containers, the parent `_`, connections, and arrowheads | When connecting shapes |
| `shapes.md` | The shape list, `sql_table`, `class`, sequence diagrams, and icons | When choosing a shape |
| `text.md` | Quotes, line breaks, markdown, `${}`, and comments | When writing labels or variables |
| `style.md` | `style` values, classes, and globs | When setting fill or stroke |

## Layout

D2's default engine is `dagre`. This skill sets `layout-engine: elk` in `d2-config` at the top of the file. `--layout` and `D2_LAYOUT` take precedence over the setting in the file. Direction, title, size, and the limits of each engine have their source of truth in `layout.md`.

## Title

Place the title as a markdown block with `near: top-center`. `title: some words` is a shape whose key is `title`. The spelling has its source of truth in `layout.md`.

## Legend

Build the legend with `d2-legend` under `vars`. How to hide an endpoint shape, and how to change the heading, have their source of truth in `legend.md`. The allowed values for dash and opacity have their source of truth in `style.md`.

## Pointing into a container from outside

A connection names a key. An undeclared key becomes a new shape at that spot. From outside a container, use the fully qualified name, and name the parent with `_`. Inside the same container, omit the prefix. The spelling has its source of truth in `connections.md`.

## Shapes

The default `shape` is `rectangle`. `sql_table`, `class`, and `sequence_diagram` each have their own contents. The list and the spelling have their source of truth in `shapes.md`. How a shape maps to a domain meaning follows the caller's convention.

## Labels

Substitution is `${path}`. A `$` that is not the start of `${`, in an unquoted string or in double quotes, fails to compile. Single quotes do not expand a substitution. Line breaks, markdown, and variable scope have their source of truth in `text.md`.
