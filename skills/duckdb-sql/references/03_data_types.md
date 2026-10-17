# DuckDB Data Types

This document focuses on DuckDB-specific data types — nested/composite types and non-standard scalar types.
For standard types (INTEGER, VARCHAR, DATE, etc.), refer to
<https://duckdb.org/docs/current/sql/data_types/overview>.

## Nested / Composite Types Overview

| Type | Description | Per-row rules | Literal syntax | DDL syntax |
|------|-------------|---------------|----------------|------------|
| LIST | Ordered, variable-length sequence of same-type values | Any number of elements per row | `[1, 2, 3]` | `INTEGER[]` |
| ARRAY | Ordered, **fixed-length** sequence of same-type values | Same number of elements per row | `[1, 2, 3]::INTEGER[3]` | `INTEGER[3]` |
| STRUCT | Named fields, each with its own type | Same keys per row | `{'a': 1, 'b': 'x'}` | `STRUCT(a INT, b VARCHAR)` |
| MAP | Key-value pairs, keys same type, values same type | Keys may differ per row | `map([1,2], ['a','b'])` | `MAP(INT, VARCHAR)` |
| UNION | Tagged union of alternative types | One member active per row | `union_value(num := 2)` | `UNION(num INT, txt VARCHAR)` |
| VARIANT | Self-describing per-value type | Each row can hold different type | `42::VARIANT` | `VARIANT` |

Case sensitivity: MAP keys are case-sensitive; STRUCT and UNION keys are case-insensitive.

## LIST

Reference: <https://duckdb.org/docs/current/sql/data_types/list>

```sql
-- Creating
SELECT [1, 2, 3] AS nums;
SELECT list_value(1, 2, 3);

-- In DDL
CREATE TABLE t (tags VARCHAR[]);

-- Accessing elements (1-indexed, negative from end)
SELECT nums[1];    -- first element
SELECT nums[-1];   -- last element

-- Slicing
SELECT nums[2:3];  -- sublist from index 2 to 3

-- Nesting
SELECT [[1, 2], [3, 4]] AS nested;

-- Empty list with type
SELECT []::INTEGER[] AS empty;
```

## ARRAY (Fixed-Length)

Reference: <https://duckdb.org/docs/current/sql/data_types/array>

```sql
-- In DDL (fixed-length)
CREATE TABLE embeddings (vec FLOAT[3]);

-- Constructing
INSERT INTO embeddings VALUES ([0.1, 0.2, 0.3]);

-- Fixed-length arrays. [1.0, 0.0] alone is a DECIMAL list, which these functions reject.
SELECT array_cosine_similarity([1.0, 0.0]::DOUBLE[2], [1.0, 0.0]::DOUBLE[2]);
SELECT array_inner_product(a.vec, b.vec) FROM embeddings a, embeddings b;
```

A bare `[1, 2, 3]` is a `LIST` (`INTEGER[]`). An `ARRAY` needs a fixed-length cast such as `::INTEGER[3]` or `::DOUBLE[2]`.
`array_cosine_similarity` and `array_inner_product` take `FLOAT[n]` or `DOUBLE[n]`, not a `DECIMAL` list.
Use `ARRAY` for a fixed-size vector. Use `LIST` when the length varies.

## STRUCT

Reference: <https://duckdb.org/docs/current/sql/data_types/struct>

```sql
-- Creating
SELECT {'name': 'Alice', 'age': 30} AS person;
SELECT struct_pack(name := 'Alice', age := 30);
SELECT row('Alice', 30);

-- In DDL
CREATE TABLE t (metadata STRUCT(source VARCHAR, confidence FLOAT));

-- Accessing fields (dot notation or bracket)
SELECT person.name;
SELECT person['name'];

-- Expanding all fields into columns
SELECT s.* FROM (SELECT {'a': 1, 'b': 2} AS s) t;

-- Add a field. The new name is a named argument, not a positional string.
SELECT struct_insert(person, email := 'alice@example.com');
```

## MAP

Reference: <https://duckdb.org/docs/current/sql/data_types/map>

```sql
-- Creating
SELECT map(['key1', 'key2'], ['val1', 'val2']);
SELECT map_from_entries([('a', 1), ('b', 2)]);
SELECT MAP {'a': 1, 'b': 2};

-- In DDL
CREATE TABLE t (props MAP(VARCHAR, INTEGER));

-- Scalar lookup. A missing key returns NULL.
SELECT m['key1'] FROM t;
SELECT map_extract_value(m, 'key1') FROM t;

-- List lookup. A missing key returns an empty list, not NULL.
SELECT element_at(m, 'key1') FROM t;
SELECT map_extract(m, 'key1') FROM t;

-- Utility
SELECT map_keys(m), map_values(m), map_entries(m), cardinality(m) FROM t;
```

Map keys are case-sensitive: `MAP {'A': 1}['a']` is `NULL`. Struct keys are not.
Use `STRUCT` when the keys are fixed in the schema. Use `MAP` when the keys differ per row.

## UNION

Reference: <https://duckdb.org/docs/current/sql/data_types/union>

```sql
-- Creating
SELECT union_value(num := 42)::UNION(num INTEGER, txt VARCHAR);
SELECT union_value(txt := 'hello')::UNION(num INTEGER, txt VARCHAR);

-- In DDL
CREATE TABLE events (payload UNION(click STRUCT(x INT, y INT), scroll INT));

-- Accessing the active member
SELECT union_tag(payload) FROM events;     -- 'click' or 'scroll'
SELECT payload.click FROM events;          -- NULL if tag is 'scroll'
```

## VARIANT

Reference: <https://duckdb.org/docs/current/sql/data_types/variant>

A semi-structured type where each value is self-contained with its own type information:

```sql
SELECT 42::VARIANT;
SELECT 'hello'::VARIANT;
SELECT [1, 2, 3]::VARIANT;
SELECT {'name': 'Alice', 'age': 30}::VARIANT;

CREATE TABLE events (id INTEGER, data VARIANT);

-- Per-row type, then a field. Extraction returns VARIANT.
SELECT variant_typeof(data) FROM events;
SELECT data.name FROM events;
SELECT variant_extract(data, 'name') FROM events;
```

`VARIANT` stores a typed value per row. `JSON` is stored as text. Nested fields use dot notation or `variant_extract`.

## ENUM

Reference: <https://duckdb.org/docs/current/sql/data_types/enum>

```sql
-- Define a custom enum type
CREATE TYPE status AS ENUM ('active', 'inactive', 'archived');

-- Use in table
CREATE TABLE users (name VARCHAR, status status);
INSERT INTO users VALUES ('Alice', 'active');

-- Enum ordering follows declaration order
SELECT * FROM users ORDER BY status;  -- active < inactive < archived
```

## DuckDB-Specific Scalar Types

| Type | Description |
|------|-------------|
| HUGEINT | Signed 128-bit integer |
| UHUGEINT | Unsigned 128-bit integer |
| UBIGINT | Unsigned 64-bit integer |
| UINTEGER | Unsigned 32-bit integer |
| USMALLINT | Unsigned 16-bit integer |
| UTINYINT | Unsigned 8-bit integer. Alias: `UINT8` |
| BIGNUM | Variable-length integer |
| BIT / BITSTRING | String of 1s and 0s |
| BLOB | Variable-length binary data (aliases: BYTEA, BINARY, VARBINARY) |
| UUID | Universally unique identifier |

`INT8` is an alias of `BIGINT` (8 bytes), not an 8-bit integer. `INT1`, `INT2`, and `INT4` are byte widths. `INT16`, `INT32`, and `INT64` are bit widths. `UINT8` is `UTINYINT`.

## Typecasting

Reference: <https://duckdb.org/docs/current/sql/data_types/typecasting>

```sql
-- Explicit cast
CAST(expr AS target_type)
expr::target_type

-- TRY_CAST: returns NULL on failure instead of error
SELECT TRY_CAST('not_a_number' AS INTEGER);  -- NULL
```

### Implicit Casting Rules

Numeric types widen without a cast when the value still fits: `TINYINT` → `SMALLINT` → `INTEGER` → `BIGINT` → `HUGEINT`.

Equality is more permissive than arithmetic. `'1.1' = 1` and `true = 1` are `true`. `'true' = 1` errors.
`'42' + 1` does not bind. Cast the string before arithmetic: `'42'::INTEGER + 1`.
