# Tables

Read this when a cell needs a list, a fence, or another block. A pipe table is a CommonMark node. Its cell attributes are in `nodes.md`. This file is the source of truth for the built-in `table` tag.

The tag takes a list. A row is a sequence of items. `---` separates rows. The rows before the first `---` are the header. A table with no header starts with `---`.

```
{% table %}
* Heading 1
* Heading 2
---
* Row 1 Cell 1
* Row 1 Cell 2
{% /table %}
```

Annotate a cell with the `td` and `th` attributes from `nodes.md`. The annotation form is in `tags.md`.

```
{% table %}
* Narrow {% width="25%" %}
* Wide {% align="right" %}
---
* Spans both {% colspan=2 %}
{% /table %}
```

The tag is how the parser finds the list. Rendering still uses the `table` node. A custom table component is a host schema change. The page is listed in `official-docs.md`.
