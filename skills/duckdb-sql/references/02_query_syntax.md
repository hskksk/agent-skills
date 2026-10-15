# DuckDB Query Syntax Extensions

This document covers DuckDB-specific query syntax that extends standard SQL.
For standard SELECT/FROM/WHERE/GROUP BY/HAVING/ORDER BY/LIMIT, refer to
<https://duckdb.org/docs/current/sql/query_syntax/select>.

## Star Expressions (EXCLUDE, REPLACE, COLUMNS)

Reference: <https://duckdb.org/docs/current/sql/expressions/star>

### EXCLUDE

Remove specific columns from `SELECT *`:

```sql
SELECT * EXCLUDE (created_at, updated_at) FROM orders;
```

### REPLACE

Override specific columns while keeping the rest:

```sql
SELECT * REPLACE (amount / 100.0 AS amount, upper(status) AS status) FROM orders;
```

### COLUMNS Expression

Apply an expression to multiple columns matching a pattern:

```sql
-- Match columns by regex
SELECT min(COLUMNS('.*_amount')), max(COLUMNS('.*_amount')) FROM invoices;

-- Match with EXCLUDE / REPLACE
SELECT COLUMNS(* EXCLUDE (id)) FROM t;

-- With a lambda. The first argument is the column name.
-- The arrow form `c -> ...` is deprecated.
SELECT COLUMNS(lambda c : c LIKE '%_date') FROM t;
```

## SAMPLE Clause

Reference: <https://duckdb.org/docs/current/sql/query_syntax/sample>

Return a random sample from a table or subquery.
`USING SAMPLE` is written after `WHERE` and `GROUP BY`, and it is applied before both.

A percentage uses `system` sampling by default: each vector is kept with that probability.
On a table smaller than about 10k rows that can keep every row or none of them.
`bernoulli` applies the probability per row. Only `reservoir` can ask for an exact row count,
and an exact percentage up to rounding. Reservoir is for small samples.

```sql
-- Exact row count (reservoir)
SELECT * FROM large_table USING SAMPLE 1000 ROWS;

-- Approximate percentage. Prefer bernoulli on small tables
SELECT * FROM large_table USING SAMPLE 10% (bernoulli);

-- Exact percentage, up to rounding
SELECT * FROM large_table USING SAMPLE 10 PERCENT (reservoir);

-- Reproducible seed
SELECT * FROM large_table USING SAMPLE 20% (system, 377);
SELECT * FROM large_table USING SAMPLE reservoir(50 ROWS);
```

`TABLESAMPLE` uses the same method syntax and samples that one table, before the rest of `FROM` is joined.
`USING SAMPLE` samples after the whole `FROM` clause.

```sql
SELECT * FROM large_table TABLESAMPLE bernoulli(10%);
```

## QUALIFY Clause

Reference: <https://duckdb.org/docs/current/sql/query_syntax/qualify>

Filter rows based on window function results without a subquery:

```sql
-- Keep only the latest order per customer
SELECT *
FROM orders
QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY order_date DESC) = 1;

-- Keep top 3 products by revenue per category
SELECT category, product, revenue
FROM sales
QUALIFY rank() OVER (PARTITION BY category ORDER BY revenue DESC) <= 3;
```

`QUALIFY` is written after `WINDOW` (the `WINDOW` clause itself is optional) and before `ORDER BY`.
It filters window-function results the way `HAVING` filters aggregates.
A window alias from the same `SELECT` can be used in `QUALIFY`.
At least one window function must appear in the `SELECT` list or in the `QUALIFY` clause.

## FILTER Clause

Reference: <https://duckdb.org/docs/current/sql/query_syntax/filter>

Conditionally include rows in one aggregate. The documented form omits `WHERE`.
`FILTER (WHERE condition)` is also accepted. `FILTER` drops the rows that fail the condition,
including the `NULL`s that a `CASE` expression would keep inside `list` or `array_agg`.

```sql
SELECT
    count() AS total_orders,
    count() FILTER (status = 'completed') AS completed_orders,
    sum(amount) FILTER (status = 'completed') AS completed_revenue,
    avg(amount) FILTER (region = 'US') AS avg_us_amount
FROM orders;
```

`PIVOT ... USING` ignores a `FILTER` on the aggregate. See `05_statements.md`.

## GROUPING SETS, CUBE, ROLLUP

Reference: <https://duckdb.org/docs/current/sql/query_syntax/grouping_sets>

Compute aggregates over multiple grouping levels in a single query:

```sql
-- GROUPING SETS: explicit grouping combinations
SELECT region, product, sum(sales)
FROM data
GROUP BY GROUPING SETS ((region, product), (region), ());

-- ROLLUP: hierarchical subtotals (right to left)
SELECT region, city, sum(sales)
FROM data
GROUP BY ROLLUP (region, city);
-- Produces: (region, city), (region), ()

-- CUBE: all possible combinations
SELECT region, product, sum(sales)
FROM data
GROUP BY CUBE (region, product);
-- Produces: (region, product), (region), (product), ()

-- grouping() to distinguish NULL from "subtotal"
SELECT region, product, sum(sales),
       grouping(region) AS is_region_total,
       grouping(product) AS is_product_total
FROM data
GROUP BY CUBE (region, product);
```

## Unnesting

Reference: <https://duckdb.org/docs/current/sql/query_syntax/unnest>

Expand lists, arrays, or structs into rows:

`unnest` in the `SELECT` list expands a `LIST` to rows or a `STRUCT` to columns.
An empty list or a `NULL` list produces zero rows. Several lists in one `SELECT` are aligned
by position, and the shorter list is padded with `NULL`. `unnest` is not allowed in
`WHERE`, `GROUP BY`, or `ORDER BY`.

```sql
-- Unnest a list column
SELECT unnest(tags) AS tag FROM articles;

-- 1-based position of each list entry. WITH ORDINALITY is not the DuckDB syntax.
SELECT unnest(l) AS item, generate_subscripts(l, 1) AS idx
FROM (VALUES ([10, 20]), ([30])) tbl(l);

-- Unnest multiple lists in parallel
SELECT unnest(keys) AS k, unnest(vals) AS v FROM kv_pairs;

-- Unnest a struct into columns
SELECT unnest(metadata) FROM events;

-- Unnest a literal list
SELECT unnest([1, 2, 3]) AS x;

-- Recursive unnest of nested lists. Lists stored inside structs are left intact
-- when the outer value is a struct.
SELECT unnest([[1, 2], [3, 4]], recursive := true);

-- Stop at a depth. max_depth 2 keeps the inner lists
SELECT unnest(nested, max_depth := 2) AS x FROM t;
```

## Special JOIN Types

### ASOF JOIN

Reference: <https://duckdb.org/docs/current/sql/query_syntax/from#as-of-joins>

Match each left row to at most one right row on an ordered column.
The `ON` clause needs one inequality (`>=`, `>`, `<=`, or `<`) on that column.
Every other condition is an equality. The left/right order of the tables matters.
`ASOF LEFT JOIN` keeps unmatched left rows.

```sql
-- Most recent quote at or before the trade
SELECT t.*, q.bid, q.ask
FROM trades t
ASOF JOIN quotes q
  ON t.symbol = q.symbol
  AND t.trade_time >= q.quote_time;

-- USING requires the same column names on both sides.
-- The last name is the inequality and is compared with >=.
SELECT *
FROM trades t
ASOF JOIN quotes q USING (symbol, "when");
```

### LATERAL JOIN

Reference: <https://duckdb.org/docs/current/sql/query_syntax/from#lateral-joins>

A subquery in a LATERAL join can reference columns from preceding tables:

```sql
SELECT c.name, top_orders.*
FROM customers c,
LATERAL (
    SELECT * FROM orders o
    WHERE o.customer_id = c.id
    ORDER BY o.amount DESC
    LIMIT 3
) top_orders;
```

### POSITIONAL JOIN

Reference: <https://duckdb.org/docs/current/sql/query_syntax/from#positional-joins>

Join two tables by row position. A positional join is a full outer join:
the result has as many rows as the longer input, and missing cells are `NULL`.

```sql
SELECT *
FROM range(3) t1(x)
POSITIONAL JOIN range(3) t2(y);
-- (0, 0), (1, 1), (2, 2)
```

## VALUES Clause

Reference: <https://duckdb.org/docs/current/sql/query_syntax/values>

Use VALUES to construct inline tables:

```sql
-- Standalone
VALUES (1, 'a'), (2, 'b'), (3, 'c');

-- With column names
SELECT * FROM (VALUES (1, 'a'), (2, 'b')) AS t(id, label);

-- In CTE
WITH categories(id, name) AS (VALUES (1, 'A'), (2, 'B'))
SELECT * FROM categories;
```
