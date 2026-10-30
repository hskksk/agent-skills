# Tags

Read this when writing a tag or an annotation. It is the source of truth for delimiters, attributes, shorthand, and annotations. What `if`, `table`, and `partial` do is in their own files. Which attributes a Markdown node accepts is in `nodes.md`.

The syntax follows the [Markdoc tag specification](https://markdoc.dev/spec).

## Delimiters

A tag that wraps children has an opening tag and a closing tag. A tag with no children is self-closing.

```
{% example %}
Content
{% /example %}

{% example width=40 /%}
```

`example` and `city` in this file are placeholders for a tag the host defines. They are not built in.

Tags nest. A tag with no newline inside it is inline. An inline tag is wrapped in a paragraph.

A tag may take one unnamed value immediately after its name. That is the primary attribute. `{% if $ready %}` passes `$ready` that way. There is no `=` on a primary attribute.

## Attributes

Write attributes as `name=value` with no space around `=`. Separate attributes with whitespace. A value is a number, a double-quoted string, a boolean, a JSON array, a JSON object, or a variable.

```
{% city
   index=0
   name="San Francisco"
   deleted=false
   coordinates=[1, 4, 9]
   meta={id: "id_123"}
   color=$color /%}
```

Strings use double quotes. A quote inside a string is `\"`. Object keys in an attribute may be bare, as in the example above.

## Shorthand

`#my-id` is `id="my-id"`. `.my-class` is `class="my-class"`. Repeated class shorthands join into one `class` value, in order, separated by spaces. `{% .foo .bar %}` is `class="foo bar"`.

## Annotations

A node cannot take attributes in HTML-like form. Write them in a separate `{% %}` after the node. The same form may follow a tag. The heading id below is an annotation. Shorthand inside it follows the rule above.

```
# Examples {% #examples %}
```

## Custom tags

`if`, `else`, `table`, and `partial` are built in. Any other name renders only when the host schema defines it. Defining that schema is outside this file. The pages are listed in `official-docs.md`.
