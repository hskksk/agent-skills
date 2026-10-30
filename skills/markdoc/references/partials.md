# Partials

Read this when one document includes another. `partial` is a built-in tag. The host may replace it. If the host's schema defines `partial`, follow that schema. This file is the source of truth for the built-in form.

The `file` attribute names a partial the host has registered. Registration maps that name to a parsed tree in `config.partials`. A path the host has not registered does not resolve.

```
{% partial file="header.md" /%}
```

Pass values with the `variables` attribute. Inside the partial they are ordinary variables. How to read a variable is in `variables.md`.

```
{% partial file="header.md" variables={name: "Ada"} /%}
```

```
Hello, {% $name %}.
```
