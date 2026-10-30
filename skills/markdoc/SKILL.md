---
name: markdoc
description: Write Markdoc with its tags, attributes, annotations, variables, functions, conditionals, and partials, and return that source. Use when writing or revising a Markdoc document. Do not use it for a host's custom tag set, a validation command, or the output language.
license: MIT
metadata:
  author: hskksk
  version: 1.10.0
---



# Write Markdoc

Markdoc is CommonMark plus tags, annotations, variables, and functions. This file says which reference owns each rule. Read only the reference for the part you are writing.

A custom tag, a custom function, and the variable name for frontmatter exist only when the host registers them. The four built-in tags are `if`, `else`, `table`, and `partial`. This skill does not choose a renderer, a validation command, or an output language.

## When to use

- Write or revise a Markdoc document
- Use a tag, a variable, a function, a conditional, a partial, or a table

Do not use it for:

- The host's inventory of custom tags
- The command that validates or previews the file
- Which language the prose is written in

## Procedure

1. Read the reference for the part you are writing.
2. Write CommonMark for the prose structure. Use a built-in tag when that reference says the tag is built in.
3. Use any other tag or function only when the host schema includes it. Do not invent one.
4. Return the Markdoc source.

## Reference files

| File | Contents | When to read |
| --- | --- | --- |
| `references/tags.md` | Delimiters, attributes, shorthand, and annotations | When writing a tag or an annotation |
| `references/conditionals.md` | `if` and `else`, and what counts as false | When the document branches |
| `references/tables.md` | The list-based `table` tag | When a cell needs content a pipe table cannot hold |
| `references/partials.md` | The `partial` tag | When including another document |
| `references/variables.md` | Variables and frontmatter | When interpolating a value |
| `references/functions.md` | Call syntax and the built-in functions | When transforming a value |
| `references/nodes.md` | Node attributes, fences, and comments | When annotating a Markdown node, or writing a comment |
| `references/official-docs.md` | Official pages | When defining a tag or a function in the host schema |
