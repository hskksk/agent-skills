# Official docs

Read this when you are defining a tag, a node, or a function in the host schema, or when a rule you need is not in the other references. Those references are the source of truth for writing a document. These pages are the source of truth for configuring the library.

| Page | What it owns |
| --- | --- |
| https://markdoc.dev/docs/syntax | The language overview |
| https://markdoc.dev/spec | Tag grammar, including the primary attribute |
| https://markdoc.dev/docs/tags | Built-in tags, and the fields of a tag schema |
| https://markdoc.dev/docs/attributes | Attribute types, `matches`, `required`, and `errorLevel` |
| https://markdoc.dev/docs/nodes | The node list, and the fields of a node schema |
| https://markdoc.dev/docs/variables | Passing `config.variables`, including into a partial |
| https://markdoc.dev/docs/functions | The built-in functions, and registering a custom function |
| https://markdoc.dev/docs/partials | Registering `config.partials` |
| https://markdoc.dev/docs/frontmatter | Parsing YAML, TOML, or JSON and passing it as a variable |

Do not copy a schema example into the document you are writing. Schema belongs in the host's config.
