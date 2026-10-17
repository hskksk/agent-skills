# Connections and containers

The source of truth for keys, containers, connections, and arrowheads. Sources: [Connections](https://d2lang.com/tour/connections/) and [Containers](https://d2lang.com/tour/containers/).

## Keys

A connection names a key. An undeclared key becomes a new shape at that spot.

```d2
be: Backend
fe: Frontend

# Connect the shapes that already exist
be -> fe

# This would create new shapes named Backend and Frontend
# Backend -> Frontend
```

A short name at the root does not connect to a node of the same name inside a container. It creates another shape at the root. From outside a container, use the fully qualified name.

```d2
tier0: {
  raw_alu
}
tier1: {
  frame_supplier
}
tier0.raw_alu -> tier1.frame_supplier
```

Inside the same container, the prefix can be omitted. The parent is `_`. `_` steps up one scope.

```d2
christmas: {
  presents
}
birthdays: {
  presents
  _.christmas.presents -> presents: regift
}
```

Keys are case-insensitive. `postgresql` and `postgreSQL` are the same shape.

A container label goes right after the key, or in `label` inside the container.

```d2
gcloud: Google Cloud {
  api -> db
}
```

```d2
gcloud: {
  label: Google Cloud
  api -> db
}
```

Nesting lets you write the inside without repeating the outer key.

```d2
clouds: {
  aws: {
    load_balancer -> api
    api -> db
  }
  gcloud: {
    auth -> db
  }
  gcloud -> aws
}
```

## Words that cannot be keys

These words cannot be an object key. The same rule applies inside a legend.

`label`, `shape`, `icon`, `constraint`, `tooltip`, `link`, `near`, `width`, `height`, `direction`, `top`, `left`, `class`, `classes`, `vars`, `style`, `source-arrowhead`, `target-arrowhead`

`grid-rows`, `grid-columns`, `grid-gap`, `vertical-gap`, and `horizontal-gap` cannot be keys either. `near` constants (such as `top-center`) and the child keys of `style` are reserved in that context. Quote a reserved word to keep it as a label or a column name.

## Connections

There are four connection operators.

- `--`
- `->`
- `<-`
- `<->`

The label follows the connection.

```d2
replica 1 -- replica 2: Kept in sync
```

Repeating a connection between the same endpoints adds another connection. The index that names which one is 0-based.

```d2
a -> b: first
a -> b: second
(a -> b)[0].style.stroke: red
(a -> b)[1].style.stroke: blue
```

A chain can be written on one line. The chain's label is attached to each connection on that line.

```d2
High Mem Instance -> EC2 <- High CPU Instance: Hosted By
```

A cycle is allowed.

## Arrowheads

`source-arrowhead` and `target-arrowhead` set the shape and a short label at an end. On a connection that has no end in that direction, the arrowhead is not drawn. `x -> y` has no source arrowhead, so writing `source-arrowhead` draws nothing.

| `shape` | Notes |
| --- | --- |
| `triangle` | Default. `style.filled: false` leaves it unfilled |
| `arrow` | Sharper than triangle |
| `diamond` | `style.filled: true` fills it |
| `circle` | `style.filled: true` fills it |
| `box` | `style.filled: true` fills it |
| `cf-one`, `cf-one-required` | Crow's foot, one |
| `cf-many`, `cf-many-required` | Crow's foot, many |
| `cross` | A cross |

Keep an arrowhead label short. Unlike a normal label, it is not laid out automatically.

```d2
a -> b: note {
  target-arrowhead: * {
    shape: diamond
    style.filled: true
  }
}
```
