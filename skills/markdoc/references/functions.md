# Functions

Read this when a value is transformed or compared. A call looks like JavaScript. Arguments are separated by commas. A trailing comma is a syntax error. Calls are allowed in the body, in an annotation, and in an attribute.

```
{% uppercase($name) %}

{% item title=uppercase($key) /%}
```

`uppercase` in that example exists only when the host registers it. Do not call a function the schema does not define.

## Built-in functions

These six are built in. Boolean tests use the falsey rule in `conditionals.md`: only `undefined`, `null`, and `false` are false.

| Function | Returns | Example | Rule |
| --- | --- | --- | --- |
| `equals` | boolean | `equals($name, "Ada")` | Strict equality. Primitive types only. |
| `and` | boolean | `and($a, $b)` | True when every argument is true under the falsey rule. |
| `or` | boolean | `or($a, $b)` | True when any argument is true under the falsey rule. |
| `not` | boolean | `not($a)` | Negates one value under the falsey rule. |
| `default` | the value | `default($show, true)` | Returns the second argument when the first is `undefined`. `null` does not trigger it. |
| `debug` | string | `debug($value)` | Renders the value as JSON. |

```
{% if and(not($a), or($b, $c)) %}
Shown when $a is false and either $b or $c is true.
{% /if %}
```

How to register a custom function is on the functions page listed in `official-docs.md`.
