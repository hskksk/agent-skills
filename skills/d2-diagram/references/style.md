# Style

The source of truth for `style`, classes, and globs that change defaults in bulk. Sources: [Styles](https://d2lang.com/tour/style/), [Classes](https://d2lang.com/tour/classes/), [Globs](https://d2lang.com/tour/globs/). What a color means sits outside this skill.

`style` can be written on a shape or on a connection. A dotted one-level form and a map are the same.

```d2
x -> y: {
  style.stroke: "#0D32B2"
  style.stroke-dash: 3
}
x.style.fill: "#F7F8FE"
```

## Values

| Key | Where it applies | Value |
| --- | --- | --- |
| `opacity` | Shapes and connections | 0 to 1 |
| `stroke` | Shapes and connections | A CSS color name, hex, or some gradients |
| `fill` | Shapes | A color. `transparent` is allowed |
| `fill-pattern` | Shapes | `dots`, `lines`, `grain`, `none` |
| `stroke-width` | Shapes and connections | An integer from 1 to 15 |
| `stroke-dash` | Shapes and connections | An integer from 0 to 10 |
| `border-radius` | Shapes. On a connection, the rounding of a bend | An integer from 0 to 20. Rounding on a connection applies on an engine that bends routes, such as `elk` |
| `shadow` | Shapes | `true` or `false` |
| `3d` | `rectangle` and `square` | `true` or `false` |
| `multiple` | Shapes | `true` or `false` |
| `double-border` | `rectangle` and `oval` | `true` or `false` |
| `font` | Text | The only value that can be set today is `mono` |
| `font-size` | Text | An integer from 8 to 100 |
| `font-color` | Text | A color |
| `animated` | Shapes and connections | `true` or `false` |
| `bold`, `italic`, `underline` | Text | `true` or `false` |
| `text-transform` | Text | `uppercase`, `lowercase`, `title`, `none` |

On `sql_table` and `class`, `fill` colors the header, `stroke` fills the body, and `font-color` colors the header text.

The root of the diagram also accepts these as background and frame: `fill`, `fill-pattern`, `stroke`, `stroke-width`, `stroke-dash`, `double-border`. When you add a frame, leave `pad` in `d2-config` above 0.

```d2
style: {
  fill: "#F7F8FE"
  stroke: "#0D32B2"
  double-border: true
}
```

## Classes

Collect a repeated look in `classes` and apply it with `class`. A key set on the shape wins over the class. An array applies classes from left to right. Classes are also written to the SVG `class` attribute.

A connection can take a class when it is declared, and later by index.

```d2
classes: {
  load balancer: {
    style: {
      fill: "#44C7B1"
      shadow: true
      border-radius: 5
    }
  }
  unhealthy: {
    style.fill: "#FE7070"
  }
}
web lb.class: load balancer
api.class: [load balancer; unhealthy]
a -> b: first
(a -> b)[0].class: unhealthy
```

## Globs

Write a default look in bulk with a glob. `*` is one level. `***` is recursive. A glob applies to shapes that already exist and to shapes declared later. Matching is case-insensitive. A connection glob does not create a connection from a shape to itself.

```d2
*.height: 300
*mini.height: 200

***.style.fill: lightblue
(*** -> ***)[*]: {
  style.stroke: red
}
```

The rest of the filter and connection-glob syntax is on [Globs](https://d2lang.com/tour/globs/).
