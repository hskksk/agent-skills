# Conditionals

Read this when the document shows one branch or another. It is the source of truth for `if`, `else`, and for what Markdoc treats as false. Boolean functions in `functions.md` use this falsey rule. They do not restate it.

`if` and `else` are built-in tags. The condition is the primary attribute. Tag delimiters are in `tags.md`.

Only `undefined`, `null`, and `false` are false. `0` and `""` are true.

```
{% if $ready %}
Shown when $ready is true.
{% else /%}
Shown otherwise.
{% /if %}
```

`else` is self-closing. A later `else` may carry its own condition. The last bare `else` runs when every condition above it was false.

```
{% if $ready %}
Ready.
{% else $paused /%}
Paused.
{% else /%}
Neither.
{% /if %}
```

Combine tests with the functions in `functions.md`. There is no `else if` tag.
