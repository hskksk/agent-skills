# DuckDB Functions

This document covers DuckDB-specific functions not found in standard SQL.
For full function reference, see <https://duckdb.org/docs/current/sql/functions/overview>.

## Lambda Functions

Reference: <https://duckdb.org/docs/current/sql/functions/lambda>

The current syntax is `lambda param : expr`. The arrow form `x -> expr` still runs and is deprecated.

The index argument is 1-based. A `COLUMNS` lambda receives the column name, and an optional second argument receives the 1-based column index.

```sql
-- Single-argument lambda
SELECT list_transform([1, 2, 3], lambda x : x * 2);         -- [2, 4, 6]
SELECT list_filter([1, 2, 3, 4], lambda x : x > 2);         -- [3, 4]

-- Element and 1-based index: 10+1, 20+2, 30+3
SELECT list_transform([10, 20, 30], lambda x, i : x + i);   -- [11, 22, 33]

-- Reduce. An optional third argument is the initial value.
SELECT list_reduce([1, 2, 3], lambda a, b : a + b);         -- 6

-- COLUMNS lambda filters by column name
SELECT COLUMNS(lambda c : c LIKE '%_id') FROM t;
```

## List Functions

Reference: <https://duckdb.org/docs/current/sql/functions/list>

| Function | Description | Example |
|----------|-------------|---------|
| `list_transform(list, lambda)` | Apply lambda to each element | `list_transform([1,2], lambda x : x * 2)` → `[2, 4]` |
| `list_filter(list, lambda)` | Keep elements matching predicate | `list_filter([1,2,3], lambda x : x > 1)` → `[2, 3]` |
| `list_reduce(list, lambda)` | Reduce list to single value | `list_reduce([1,2,3], lambda a, b : a + b)` → `6` |
| `list_sort(list)` | Sort elements | `list_sort([3,1,2])` → `[1, 2, 3]` |
| `list_reverse_sort(list)` | Sort descending | `list_reverse_sort([3,1,2])` → `[3, 2, 1]` |
| `list_distinct(list)` | Drop duplicates and `NULL`. Order is not kept | `list_distinct([1, 1, NULL, -3, 1, 5])` → `[5, -3, 1]` |
| `list_unique(list)` | Count unique elements | `list_unique([1,1,2])` → `2` |
| `list_contains(list, val)` | Check membership | `list_contains([1,2,3], 2)` → `true` |
| `list_aggregate(list, fn)` | Apply aggregate function | `list_aggregate([1,2,3], 'sum')` → `6` |
| `list_concat(l1, l2)` | Concatenate two lists | `list_concat([1],[2,3])` → `[1,2,3]` |
| `flatten(list)` | Flatten one nesting level | `flatten([[1,2],[3]])` → `[1,2,3]` |
| `unnest(list)` | Expand list to rows | `SELECT unnest([1,2,3])` → 3 rows |
| `generate_series(start, stop, step)` | Inclusive sequence. A scalar call returns a list; `FROM generate_series(...)` returns rows | `generate_series(1, 5, 2)` → `[1, 3, 5]` |
| `range(start, stop, step)` | Same, with an exclusive end | `range(0, 3)` → `[0, 1, 2]` |
| `list_zip(l1, l2, ...)` | Zip multiple lists into list of structs | `list_zip([1,2],['a','b'])` |

### List Comprehension

```sql
SELECT [x * 2 FOR x IN [1, 2, 3]];               -- [2, 4, 6]
SELECT [x FOR x IN [1, 2, 3, 4] IF x > 2];       -- [3, 4]
```

## Struct Functions

Reference: <https://duckdb.org/docs/current/sql/functions/struct>

| Function | Description | Example |
|----------|-------------|---------|
| `struct_pack(k := v, ...)` | Create struct | `struct_pack(a := 1, b := 'x')` |
| `struct_extract(s, key)` | Extract field (or use `s.key`) | `struct_extract(s, 'a')` |
| `struct_insert(s, name := v, ...)` | Add fields by named argument | `struct_insert(s, c := 3)` |
| `row(v1, v2, ...)` | Create unnamed struct | `row(1, 'x')` |

## Map Functions

Reference: <https://duckdb.org/docs/current/sql/functions/map>

| Function | Description |
|----------|-------------|
| `map(keys[], vals[])` | Create map from key/value lists |
| `map_from_entries(list)` | Create map from list of (key, value) pairs |
| `map_keys(m)` | Return list of keys |
| `map_values(m)` | Return list of values |
| `map_entries(m)` | Return list of (key, value) structs |
| `element_at(m, key)` / `map_extract(m, key)` | Value as a list. Missing key returns `[]` |
| `m[key]` / `map_extract_value(m, key)` | Value as a scalar. Missing key returns `NULL` |
| `cardinality(m)` | Number of entries |

## Aggregate Function Extensions

Reference: <https://duckdb.org/docs/current/sql/functions/aggregates>

### Top-N in Group

`min(col, n)`, `max(col, n)`, `arg_min(arg, val, n)`, `arg_max(arg, val, n)` return a list of the
top/bottom N values:

```sql
-- Get top 3 values per group
SELECT grp, max(val, 3) FROM t GROUP BY grp;
-- Returns: grp='a' → [3, 2, 1], grp='b' → [6, 5, 4]

-- Get the 3 rows with highest val, returning their name
SELECT grp, arg_max(name, val, 3) FROM t GROUP BY grp;
```

### Other Useful Aggregates

| Function | Description |
|----------|-------------|
| `list(expr)` / `array_agg(expr)` | Collect values into a list |
| `string_agg(expr)` / `string_agg(expr, sep)` | Join strings. The one-argument form uses a comma. An empty group returns `NULL` |
| `histogram(expr)` | Return MAP of value → count |
| `mode(expr)` | Most frequent value |
| `quantile_cont(expr, q)` | Continuous quantile (interpolated) |
| `quantile_disc(expr, q)` | Discrete quantile (actual value) |
| `approx_quantile(expr, q)` | Approximate quantile (faster) |
| `approx_count_distinct(expr)` | Approximate distinct count (HyperLogLog) |
| `median(expr)` | Shorthand for `quantile_cont(expr, 0.5)` |
| `mad(expr)` | Median absolute deviation |
| `entropy(expr)` | Shannon entropy |
| `kurtosis(expr)` | Excess kurtosis (Fisher) with the sample-size correction. `kurtosis_pop` omits that correction |
| `skewness(expr)` | Skewness |
| `regr_*` family | Linear regression functions |
| `bitstring_agg(expr)` | Aggregate into bitstring |
| `bool_and(expr)` / `bool_or(expr)` | Logical aggregate |

### FILTER Clause with Aggregates

```sql
SELECT
    count() AS total,
    count() FILTER (status = 'active') AS active,
    sum(amount) FILTER (region IN ('US', 'CA')) AS north_america_total
FROM orders;
```

## Date and Time Functions (DuckDB-Specific)

Reference: <https://duckdb.org/docs/current/sql/functions/date>,
<https://duckdb.org/docs/current/sql/functions/timestamp>

```sql
-- date_trunc: truncate to precision
SELECT date_trunc('month', TIMESTAMP '2024-03-15 10:30:00');  -- 2024-03-01 00:00:00

-- date_part / extract
SELECT date_part('year', DATE '2024-03-15');   -- 2024
SELECT date_part('dow', DATE '2024-03-15');    -- day of week (0=Sunday)

-- date_diff: difference between dates
SELECT date_diff('day', DATE '2024-01-01', DATE '2024-03-15');   -- 74
SELECT datediff('month', DATE '2024-01-01', DATE '2024-06-15');  -- 5

-- make_date / make_timestamp
SELECT make_date(2024, 3, 15);
SELECT make_timestamp(2024, 3, 15, 10, 30, 0);

-- generate_series for date ranges
SELECT * FROM generate_series(DATE '2024-01-01', DATE '2024-01-05', INTERVAL 1 DAY);

-- range for dates (exclusive end)
SELECT * FROM range(DATE '2024-01-01', DATE '2024-01-04', INTERVAL 1 DAY);

-- strftime / strptime
SELECT strftime(TIMESTAMP '2024-03-15', '%Y/%m/%d');       -- '2024/03/15'
SELECT strptime('2024/03/15', '%Y/%m/%d')::DATE;           -- 2024-03-15

-- age(start, end) is the interval between the two timestamps.
-- age(x) with one argument is current_date - x, not current_timestamp - x.
SELECT age(TIMESTAMP '2024-03-15', TIMESTAMP '2020-01-01');

-- current date/time
SELECT current_date, current_timestamp, now();

-- Interval arithmetic
SELECT DATE '2024-01-01' + INTERVAL 3 MONTH;
SELECT TIMESTAMP '2024-01-01' - INTERVAL '2 hours 30 minutes';
```

## Utility Functions

| Function | Description | Example |
|----------|-------------|---------|
| `typeof(expr)` | Return type name as string | `typeof(42)` → `'INTEGER'` |
| `hash(expr)` | Hash value | `hash('hello')` |
| `md5(expr)` | MD5 hash as hex string | `md5('hello')` |
| `current_setting(name)` | Read a DuckDB setting | `current_setting('threads')` |
| `alias(col)` | Return column alias | `alias(x)` |
| `coalesce(a, b, ...)` | First non-NULL | `coalesce(NULL, 1, 2)` → `1` |
| `ifnull(a, b)` | Alias for `coalesce(a, b)` | |
| `nullif(a, b)` | NULL if a = b | `nullif(0, 0)` → `NULL` |
| `greatest(a, b, ...)` | Largest value | `greatest(1, 3, 2)` → `3` |
| `least(a, b, ...)` | Smallest value | `least(1, 3, 2)` → `1` |
| `gen_random_uuid()` | Generate random UUID | |
| `encode(string)` | `VARCHAR` to `BLOB` | `encode('hello')` |
| `decode(blob [, on_error])` | `BLOB` to `VARCHAR`. `on_error` is `'strict'`, `'replace'`, or `'ignore'` | `decode('\xC3\xBC'::BLOB)` → `ü` |
| `hex(blob)` / `unhex(string)` | Hexadecimal text and `BLOB` | `hex('\xAA\xBB'::BLOB)` → `AABB` |

## Window Functions

Reference: <https://duckdb.org/docs/current/sql/functions/window_functions>

Standard window functions (row_number, rank, dense_rank, ntile, lag, lead, first_value, last_value,
nth_value, cume_dist, percent_rank) are all supported. DuckDB-specific additions:

```sql
-- Use QUALIFY to filter on window results (no subquery needed)
SELECT *, row_number() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
FROM employees
QUALIFY rn <= 3;

-- WINDOW clause for reusable window definitions
SELECT
    name,
    sum(sales) OVER w AS running_total,
    avg(sales) OVER w AS running_avg
FROM monthly_sales
WINDOW w AS (PARTITION BY region ORDER BY month ROWS UNBOUNDED PRECEDING);
```
