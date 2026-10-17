# Text and substitution

The source of truth for labels, quotes, blocks, and variables. Sources: [Strings](https://d2lang.com/tour/strings/), [Text](https://d2lang.com/tour/text/), [Variables](https://d2lang.com/tour/vars/), [Comments](https://d2lang.com/tour/comments/).

## Unquoted strings

Leading and trailing whitespace is trimmed from an unquoted string. The string ends at one of these:

a newline, `;`, `#`, `{`, `}`, `[`, `]`

Inside a key, these are also separators: `:`, `.`, `<`, `>`, `&`, and the start of `--` or `->`.

When a label needs one of those characters, use single quotes, double quotes, or a block string. When a single-quoted string needs a single quote, use double quotes. When it needs both, escape with `\` inside double quotes.

## Substitution

Substitution is `${path}`. A `$` whose next character is not `{` fails to compile in an unquoted string and in double quotes. Write currency as the single-quoted `'$100'`, or as something like `USD`.

Single quotes do not expand a substitution. `'${name}'` and `'$100'` stay as those characters.

```d2
vars: {
  server-name: Cat
}
server1: ${server-name}-1
server2: ${server-name}-2
server1 <-> server2
```

`vars` are scoped. An outer variable is visible from the inside. When the names match, the definition closer to the substitution is used. An inner variable is not visible from the outside.

```d2
vars: {
  region: Global
}
lb: ${region} load balancer
zone1: {
  vars: {
    region: us-east-1
  }
  server: ${region} API
}
```

Follow a nested value with `.`.

```d2
vars: {
  primaryColors: {
    button: {
      active: "#4baae5"
    }
  }
}
button.style.fill: ${primaryColors.button.active}
```

When the value is a map or an array, spread it with `...${name}`.

```d2
vars: {
  base-constraints: [NOT NULL; UNQ]
}
data: {
  shape: sql_table
  a: int {constraint: [PK; ...${base-constraints}]}
}
```

## Line breaks and escapes

`\n` is rendered as a line break. `\t`, `\r`, `\\`, and `\"` are escapes too. A raw newline in an unquoted string ends the string there.

A multi-line body is a block string. The body runs from `|md` to a `|` at the same indent. When the body itself needs a `|`, close the block with a longer marker such as `||` or `|||`, or with `|` followed by a symbol that you repeat at the end (for example open with `` |` `` and close with `` `| ``).

```d2
explanation: |md
  # Heading
  - first
  - second
|
```

Text standing on its own is markdown. To make a shape's label markdown, declare the shape explicitly and then write the block. `shape: text` is not markdown.

```d2
explanation: |md
  # Heading
  - first
|
explanation.shape: rectangle
```

For code, write a language name in place of `md`. Short aliases are `md`, `tex`, `js`, `go`, `py`, `rb`, and `ts`. An unknown language is plain text with no highlighting.

LaTeX is `latex` or `tex`. It is for math, not a full document layout. `font-size` has no effect; set the size on the LaTeX side with `\small` or `\large`.

## Comments

A line comment runs from `#` to the end of the line. A block comment is wrapped in `"""`.

```d2
# whole line
x -> y # end of line

"""
block
"""
```
