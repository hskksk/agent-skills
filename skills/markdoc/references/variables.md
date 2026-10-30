# Variables

Read this when the document interpolates a value, or reads frontmatter. A variable starts with `$`. Nested fields use dots. The value is JSON-serializable: a string, a boolean, a number, an array, or an object.

```
{% $user.name %}
```

The host passes variables on `config.variables`. A variable is immutable while the document renders. There is no assignment and no loop. A calculation that does not change a variable is a function. The call syntax is in `functions.md`. Updating a value while rendering is a host transform, outside this skill.

## Where a variable is not parsed

A variable inside a Markdown link target is not read. The link node never sees it.

```
[Docs]({% $href %})
```

Pass the variable as an attribute of a link tag the host defines.

```
{% link href=$href %}Docs{% /link %}
```

That tag exists only when the host schema includes it.

## Frontmatter

A frontmatter block at the top of the file may be YAML, TOML, or JSON. The parser stores the raw text on the document. It does not bind a variable until the host parses that text and passes the object in `config.variables`.

After the host passes `variables.frontmatter`, read `$frontmatter.title`. `@markdoc/next.js` binds the same object as `$markdoc.frontmatter.title`. The syntax overview uses that second name. Write the name the host actually passes. Do not assume YAML, and do not assume `$markdoc`, unless the host says so.
