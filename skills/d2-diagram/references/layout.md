# Layout and position

The source of truth for engines, settings inside the file, direction, size, and where the title sits. This skill uses `elk`. Sources: [Layouts](https://d2lang.com/tour/layouts/), [ELK](https://d2lang.com/tour/elk/), [Positions](https://d2lang.com/tour/positions/), [Variables](https://d2lang.com/tour/vars/).

## Engines

| Engine | Role |
| --- | --- |
| `dagre` | D2's default. A fast hierarchical layout |
| `elk` | The standard for this skill. Orthogonal routes, container-to-container edges, and edges onto SQL table rows |
| `tala` | For software architecture diagrams. Installed separately |

`elk`'s default algorithm is `layered`. Pass a different one on the CLI.

| Algorithm | Bias |
| --- | --- |
| `layered` | Default. Layers the graph, and routes edges orthogonally |
| `force` | Spreads nodes by attraction and repulsion |
| `stress` | Pulls pairs with a short path closer together |
| `mrtree` | Lays a tree out in levels |
| `radial` | Lays a tree in a circle around the root. Expects a tree |

```shell
d2 --layout=elk --elk-algorithm=force input.d2 out.svg
```

`layered` is strong on hierarchy and pays less attention to symmetry. A route can pick up an extra bend.

## Settings inside the file

```d2
vars: {
  d2-config: {
    layout-engine: elk
    theme-id: 4
    dark-theme-id: 200
    pad: 0
    center: true
    sketch: false
  }
}
```

This matches `d2 --layout=elk --theme=4 --dark-theme=200 --pad=0 --center`. Flags and environment variables take precedence. With `D2_LAYOUT=dagre d2 --theme=1 input.d2`, the file's `layout-engine` and `theme-id` are unused.

`d2 layout` lists the layouts. `d2 layout elk` lists the flags for that engine.

## Direction

`direction` is one of `up`, `down`, `right`, or `left`. On `dagre` and `elk` it applies once, to the whole diagram. Only TALA can give each container its own direction.

```d2
vars: {
  d2-config: {
    layout-engine: elk
  }
}
direction: right
a -> b -> c
```

## Limits of each engine

- `near` constants work on every engine. Naming another shape in `near` works only on TALA.
- Container `width` and `height` are handled by TALA and `elk`. TALA may grow the size to fit the contents. The size of a shape itself can be set on every engine.
- `top` and `left` fix a position only on TALA. Write both together.
- An edge from an ancestor to a descendant (from a container to a child inside it) does not work on `dagre`.

## Title and near

Place the title as a markdown block with `near: top-center`.

```d2
title: |md
  # Diagram Title Here
| {near: top-center}
a -> b
```

`title: Diagram Title` is a shape whose key is `title`.

Constants that sit around the diagram:

`top-left`, `top-center`, `top-right`, `center-left`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right`

A label or icon `near` can take `outside-`, which places it outside the border, or `border-`, which places it on the border. The outside left and right are `outside-left-center` and `outside-right-center`. The word order differs from the diagram-level `center-left`.

A `tooltip` normally appears on hover. With `near`, it stays visible.

A long explanation can also be a markdown block.

```d2
explanation: |md
  # Why this shape
  - first reason
  - second reason
| {near: top-left}
```
