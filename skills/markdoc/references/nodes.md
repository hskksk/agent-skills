# Nodes

Read this when annotating a Markdown node, setting a fence, or writing a comment. Markdoc's nodes are the CommonMark blocks and inlines. Annotation syntax is in `tags.md`. This file is the source of truth for which attributes an author can set on a node, and for comments.

## Attributes an author sets

| Node | Attributes |
| --- | --- |
| `heading` | `level` from the number of `#`. `id` when the host's heading schema accepts it. |
| `image` | `src`, `alt`, `title` |
| `link` | `href`, `title`. A variable in `href` is not parsed. That rule is in `variables.md`. |
| `fence` | `language` from the info string. `process` defaults to true. |
| `list` | `ordered`. `start` when the marker is not `1`. |
| `th` | `align`, `width`, `colspan`, `rowspan` |
| `td` | `align`, `colspan`, `rowspan` |

A pipe table uses those `th` and `td` attributes. Put the annotation after the cell text.

```
| Name {% width="25%" %} | Notes {% align="right" %} |
| --- | --- |
| Ada | Kept |
```

For a cell that contains a list or a fence, use the `table` tag in `tables.md`.

## Fences

`process=false` leaves the fence body as text, so tags and variables inside it are not parsed. The default is `true`. Put the annotation on the opening line, after the language.

````
```js {% process=false %}
{% $kept_as_text %}
```
````

## Comments

An HTML comment is a comment node when the tokenizer was created with `allowComments: true`. That flag is off unless the host turns it on. When it is off, the comment is ordinary text and will render.

```
<!-- not rendered when allowComments is on -->
```
