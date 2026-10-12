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

-- With lambda function
SELECT COLUMNS(c -> c LIKE '%_date') FROM t;
```

## SAMPLE Clause

Reference: <https://duckdb.org/docs/current/sql/query_syntax/sample>

Return a random sample from a table or subquery:

```sql
-- Row-count sample
SELECT * FROM large_table USING SAMPLE 1000;

-- Percentage sample
SELECT * FROM large_table USING SAMPLE 10%;

-- Specify method: bernoulli (row-level), system (block-level), reservoir
SELECT * FROM large_table USING SAMPLE 10% (bernoulli);
SELECT * FROM large_table USING SAMPLE 1000 ROWS (reservoir);

-- Reproducible with seed
SELECT * FROM large_table USING SAMPLE 10% (bernoulli, 42);

-- Alternative shorthand (after FROM, before WHERE)
SELECT * FROM large_table TABLESAMPLE 10%;
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

`QUALIFY` is evaluated after `HAVING` and window functions, similar to how `HAVING` filters
after `GROUP BY`.

## FILTER Clause

Reference: <https://duckdb.org/docs/current/sql/query_syntax/filter>

Conditionally include rows in aggregate computation:

```sql
SELECT
    count() AS total_orders,
    count() FILTER (status = 'completed') AS completed_orders,
    sum(amount) FILTER (status = 'completed') AS completed_revenue,
    avg(amount) FILTER (region = 'US') AS avg_us_amount
FROM orders;
```

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

```sql
-- Unnest a list column
SELECT unnest(tags) AS tag FROM articles;

-- Unnest with ordinality (row index)
SELECT unnest(items) WITH ORDINALITY AS (item, idx) FROM orders;

-- Unnest multiple lists in parallel
SELECT unnest(keys) AS k, unnest(vals) AS v FROM kv_pairs;

-- Unnest a struct into columns
SELECT unnest(metadata) FROM events;

-- Unnest a literal list
SELECT unnest([1, 2, 3]) AS x;

-- Recursive unnest (flatten nested lists)
SELECT unnest([[1, 2], [3, 4]], recursive := true);
```

## Special JOIN Types

### ASOF JOIN

Reference: <https://duckdb.org/docs/current/sql/query_syntax/from#as-of-joins>

Match each row to the nearest preceding row in another table by a temporal or ordered column:

```sql
-- Match each trade to the most recent quote at or before trade time
SELECT t.*, q.bid, q.ask
FROM trades t
ASOF JOIN quotes q
  ON t.symbol = q.symbol
  AND t.trade_time >= q.quote_time;

-- ASOF LEFT JOIN to keep unmatched rows
SELECT t.*, q.bid
FROM trades t
ASOF LEFT JOIN quotes q
  ON t.symbol = q.symbol
  AND t.ts >= q.ts;
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

Join two tables by row position (like `zip` in Python):

```sql
SELECT *
FROM range(3) t1(x)
POSITIONAL JOIN range(3) t2(y);
-- Result: (0,0), (1,1), (2,2)
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
