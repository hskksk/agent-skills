# Legend

The source of truth for `d2-legend`. Source: [Legend](https://d2lang.com/tour/legend/). Allowed values for dash, opacity, and stroke width have their source of truth in `style.md`. Words that cannot be keys have their source of truth in `connections.md`.

## Declaration

Write the legend as `d2-legend` under `vars`. The shapes and connections inside it become the legend box in the rendering.

```d2
vars: {
  d2-config: {
    layout-engine: elk
  }
  d2-legend: {
    service: {
      label: Service
      style.fill: "#E3F2FD"
      style.stroke: "#1565C0"
    }
    store: Database {
      shape: cylinder
      style.stroke-dash: 2
    }
    service <-> store: Good {
      style.stroke: red
      style.stroke-dash: 2
      style.stroke-width: 1
    }
    service -> store: Bad
    service -> store: Tenuous {
      target-arrowhead.shape: circle
    }
  }
}
api -> db
db.shape: cylinder
```

`service -> store` adds two shapes and one connection to the legend. To show only the line, set the endpoint shapes to `style.opacity: 0`.

```d2
vars: {
  d2-legend: {
    a <-> b: Good relationship {
      style.stroke: red
      style.stroke-dash: 2
    }
    a.style.opacity: 0
    b.style.opacity: 0
  }
}
```

## Heading

A label replaces the default heading `legend`. Use it when the diagram's language is not English.

```d2
vars: {
  d2-legend: "凡例" {
    item: {
      label: 処理
    }
  }
}
x -> y
```

## Keys

Keys inside the legend follow the same reserved words as the rest of the diagram. A key such as `label`, `shape`, `style`, `link`, or `near` fails to compile. `link -> link_end` fails because `link` is reserved. The list is in `connections.md`.
