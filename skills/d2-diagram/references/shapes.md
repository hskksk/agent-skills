# Shapes

The source of truth for `shape`. Sources: [Shapes](https://d2lang.com/tour/shapes/), [SQL Tables](https://d2lang.com/tour/sql-tables/), [UML Classes](https://d2lang.com/tour/uml-classes/), [Sequence Diagrams](https://d2lang.com/tour/sequence-diagrams/), [Icons](https://d2lang.com/tour/icons/). Fill and stroke values have their source of truth in `style.md`. Reserved keys have their source of truth in `connections.md`.

The default is `rectangle`. To give a label that differs from the key, write the label right after the key.

```d2
pg: PostgreSQL
cloud_box: my cloud
cloud_box.shape: cloud
```

## List

`rectangle`, `square`, `page`, `parallelogram`, `document`, `cylinder`, `queue`, `package`, `step`, `callout`, `stored_data`, `person`, `diamond`, `oval`, `circle`, `hexagon`, `cloud`, `text`, `code`, `class`, `sql_table`, `image`, `sequence_diagram`, `c4-person`, `hierarchy`

`circle` and `square` keep width and height equal. When a long label stretches the width, the height stretches by the same amount. When both `width` and `height` are set, the larger one wins.

`queue` is a shape that looks like a queue. It is a flowchart shape. How a shape maps to a domain meaning follows the caller's convention.

## SQL tables

`sql_table` is an ER diagram. Each key is a row, the value after the colon is the type, and `constraint` is the constraint.

| `constraint` | Short form in the diagram |
| --- | --- |
| `primary_key` | PK |
| `foreign_key` | FK |
| `unique` | UNQ |

An unknown constraint string is allowed, and it is not shortened. Several constraints go in an array. Quote a column name that is a reserved word.

```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  name: string
}
orders: {
  shape: sql_table
  id: int {constraint: primary_key}
  user_id: int {constraint: [foreign_key; unique]}
}
orders.user_id -> users.id
```

On `elk` and TALA, this connection lands on the row. `fill` colors the header, `stroke` fills the body, and `font-color` colors the header text.

To spread shared items into a constraint array, use `...${name}` from `text.md`.

## UML classes

Each key of `class` is a field or a method. A field's value is its type. A key that contains `(` is a method, and the value is the return type. A method with no value returns void.

Visibility prefixes: none and `+` are public, `-` is private, and `#` is protected. `#` also starts a comment, so at the start of a line write `\#`.

```d2
Parser: {
  shape: class
  +reader: io.RuneReader
  -lookahead: "[]rune"
  \#pos: int
  +peek(): (r rune, eof bool)
  rewind()
}
```

`fill`, `stroke`, and `font-color` apply the same way as on `sql_table`.

## Sequence diagrams

Set `shape: sequence_diagram`. There is no special arrow syntax; write ordinary connections. Two things differ.

- Actors inside the diagram share one scope, even when they sit in different containers. The same actor name is the same actor.
- Source order is visual order: top to bottom, and actors from left to right.

```d2
shape: sequence_diagram
alice; bob
alice -> bob: What does it mean\nto be well-adjusted?
bob -> alice: The ability to play bridge.
```

A connection from a shape nested on an actor is a span.

```d2
shape: sequence_diagram
alice.t1 -> bob
alice.t2 -> bob.a
alice.t2 <- bob.a
```

A group is a container inside the sequence diagram that is not connected outward and that holds connections inside. Declare an actor that a group refers to at the top level first.

```d2
shape: sequence_diagram
alice
bob
shower thoughts: {
  alice -> bob: A physicist is an atom's way of knowing about atoms.
}
```

A shape nested on an actor with no connections is a note. A connection from an actor to itself is a self-message. A lifeline inherits the actor's `stroke` and `stroke-dash`.

## Icons

`icon` takes a URL. The CLI also accepts a local path such as `icon: ./file.png`. The official catalog is at <https://icons.d2lang.com>. The engine places the icon. On a container it tends toward the top left; on a shape that is not a container it tends toward the center. A connection can have an `icon` too.

```d2
deploy: {
  icon: https://icons.d2lang.com/aws%2FDeveloper%20Tools%2FAWS-CodeDeploy.svg
}
backup: {
  icon: https://icons.d2lang.com/aws%2FStorage%2FAWS-Backup.svg
}
deploy -> backup
```

To make the shape itself an image, use `shape: image`.
