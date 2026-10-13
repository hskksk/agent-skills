# DuckDB Overview and SQL Dialect

Reference: <https://duckdb.org/docs/current/sql/introduction>

## What Is DuckDB

- In-process OLAP database (no server, runs embedded in the host process)
- Columnar-vectorized execution engine optimized for analytical queries
- SQL dialect closely follows **PostgreSQL** with analytical extensions
- Reads and writes CSV, Parquet, JSON, and other formats natively
- Supports querying files directly without importing (`SELECT * FROM 'data.parquet'`)

## Friendly SQL

DuckDB provides syntactic sugar to make SQL more concise and readable. Which of these to choose is decided in
`conventions.md`. This file shows the syntax.

Reference: <https://duckdb.org/docs/current/sql/dialect/friendly_sql>

### Clauses

```sql
-- FROM-first with optional SELECT (implicit SELECT *)
FROM my_table;
FROM my_table SELECT col1, col2;

-- CREATE OR REPLACE TABLE (no need for DROP IF EXISTS)
CREATE OR REPLACE TABLE t AS SELECT 1 AS x;

-- INSERT BY NAME (match by column name, not position)
INSERT INTO t BY NAME (SELECT 2 AS x);

-- INSERT OR IGNORE / INSERT OR REPLACE
INSERT OR IGNORE INTO t VALUES (1);
INSERT OR REPLACE INTO t VALUES (1);

-- GROUP BY ALL (infer group-by columns from SELECT)
SELECT city, count()
FROM weather
GROUP BY ALL;

-- ORDER BY ALL
SELECT * FROM t ORDER BY ALL;

-- SELECT * EXCLUDE (drop specific columns)
SELECT * EXCLUDE (internal_id, debug_flag) FROM t;

-- SELECT * REPLACE (override specific columns)
SELECT * REPLACE (round(price, 2) AS price) FROM t;

-- UNION BY NAME (match by column name, not position)
SELECT 1 AS a, 2 AS b UNION BY NAME SELECT 3 AS b, 4 AS a;

-- Prefix alias syntax
SELECT x: 42, y: 'hello';

-- LIMIT with percentage
SELECT * FROM t LIMIT 10%;
```

### Query Features

```sql
-- Column aliases usable in WHERE, GROUP BY, HAVING.
-- They are not usable in the ON clause of a JOIN.
SELECT city, temp_hi - temp_lo AS temp_range
FROM weather
WHERE temp_range > 10;

-- Reusable (lateral) column aliases
SELECT i + 1 AS j, j + 2 AS k
FROM range(0, 3) t(i);

-- count() shorthand for count(*)
SELECT count() FROM t;

-- Trailing commas are allowed
SELECT
    col1,
    col2,
    col3,
FROM t;

-- SWITCH(expr, MAP {value: result, ...} [, default])
-- syntactic sugar for CASE. The arrow form is not valid.
SELECT SWITCH(status, MAP {1: 'active', 2: 'inactive'}, 'unknown') AS label
FROM t;
```

### Data Import Shortcuts

```sql
-- Directly query files (replacement scans)
FROM 'data.csv';
FROM 'data.parquet';
FROM '*.csv';
FROM 'data/part-*.parquet';

-- In Python: FROM df (Pandas DataFrame)
```

### Functions and Expressions

```sql
-- Dot operator for function chaining
SELECT ('hello').upper();         -- 'HELLO'
SELECT [1, 2, 3].list_sort();    -- [1, 2, 3]

-- String formatting
SELECT format('{} + {} = {}', 1, 2, 3);  -- '1 + 2 = 3'

-- STRUCT.* notation to expand struct fields
SELECT s.* FROM (SELECT {'a': 1, 'b': 2} AS s) t;

-- List comprehension
SELECT [x * 2 FOR x IN [1, 2, 3]];  -- [2, 4, 6]

-- List slicing / negative indexing
SELECT [1, 2, 3, 4][-1];   -- 4
SELECT [1, 2, 3, 4][2:3];  -- [2, 3]
```

## PostgreSQL Compatibility

Reference: <https://duckdb.org/docs/current/sql/dialect/postgresql_compatibility>

DuckDB aims for PostgreSQL compatibility but diverges in these areas.
Reference examples below match the current compatibility page.

| Area | DuckDB | PostgreSQL |
|------|--------|------------|
| Division of integers | `1 / 2` is float division and returns `0.5` (`DOUBLE`). Integer division is `1 // 2` | `1 / 2` returns `0` |
| Float division by zero | IEEE 754: `Infinity`, `-Infinity`, or `NaN` | Error |
| Identifiers | Case-insensitive, including quoted identifiers. The catalog keeps the original spelling. `SET preserve_identifier_case = false` folds new unquoted names to lowercase | Unquoted names are folded to lowercase. Quoted names are case-sensitive |
| `string_agg` | `string_agg(expr)` joins with a comma. `string_agg(expr, sep)` takes an explicit separator. An empty group returns `NULL` | The separator argument is required |
| Equality casts | `'1.1' = 1` and `true = 1` are `true`. `'true' = 1` is an error. `VARCHAR + INTEGER`, such as `'42' + 1`, does not bind | Stricter. `true = 1` is an error |
| `BOOLEAN` text | `true` / `false` | `t` / `f` |
| Default schema | `main` | `public` |
| `==` | Compares equal, the same as `=`. Prefer `=` | Syntax error |
| `~` | Full match (`regexp_full_match`). `'aaa' ~ '(a|b)'` is `false`. `~*` and `!~*` are not supported | Partial match. `~*` is a case-insensitive partial match |
| `regexp_extract` | No match returns `''` | `regexp_substr` returns `NULL` |
| `to_date` | Not defined. Use `strptime` | `to_date` |
| Functional dependency in `GROUP BY` | A selected column must be grouped or aggregated. Use `GROUP BY ALL` or `any_value` | A primary key can imply the other columns of its row |
| `UNION` of boolean and integer | Succeeds. `true` becomes `1` | Error |
| `VACUUM` | A no-op, except `VACUUM table(column)`, which rebuilds statistics. It does not reclaim space | Garbage-collects and analyzes |

## SQL Quirks

Reference: <https://duckdb.org/docs/current/sql/dialect/sql_quirks>

- **Identifiers**: case-insensitive, by an ASCII comparison (`col_A` matches `col_a`; `col_á` does not). Double quotes allow reserved words and spaces. Quoted identifiers stay case-insensitive.
  Duplicate names are renamed `name`, `name_1`, `name_2`, …. `SELECT 1 AS a, 2 AS a` yields `a` and `a_1`.
  In `SELECT a FROM (SELECT *, 2 AS a FROM tbl)`, the first `a` shadows the later one.
- **Numeric literals**: underscores are digit separators (`1_000_000`).
- **String literals**: single quotes only (`'text'`). Double quotes are identifiers. Escape a single quote by doubling it (`'it''s'`).
- **`NULL` sort**: the default is `NULLS LAST` for both `ASC` and `DESC`. That matches PostgreSQL for `ASC` only. PostgreSQL puts `NULL` first on `DESC`. `SET default_null_order = 'NULLS_LAST_ON_ASC_FIRST_ON_DESC'` matches PostgreSQL in both directions.
- **Empty aggregates**: `sum`, `list`, and `string_agg` on an empty group return `NULL`, not `0`, `[]`, or `''`.
- **Indexing**: lists, arrays, strings, and window functions such as `row_number` are 1-based. JSON subscripts are 0-based.
- **`INT8` and `UINT8`**: `INT8` is `BIGINT` (8 bytes). `UINT8` is `UTINYINT` (8 bits). `INT1`/`INT2`/`INT4` are byte widths. `INT16`/`INT32`/`INT64` are bit widths.
- **Unary minus and power**: `-2 ^ 2` is `4.0`, because unary minus binds tighter than `^`. Write `-(2 ^ 2)` or `-pow(2, 2)` for `-4`.
- **`IN` and lists**: `1 IN (0, NULL)` is `NULL`. `1 IN [0, NULL]` is `false`.
- **`NULL` and concatenation**: `concat('abc', NULL)` is `'abc'`. `'abc' || NULL` is `NULL`.
- **`USING SAMPLE`**: it is written after `WHERE` and `GROUP BY`, and it is applied before both.
- **`age(x)`**: one argument means `current_date - x`, not `current_timestamp - x`.
- **Extract on a missing key**: `struct_extract` errors, because struct keys are like columns. `element_at` / `map_extract` on a map return a list, and an empty list when the key is absent. `map[key]` and `map_extract_value` return the scalar, or `NULL` when the key is absent.
- **Transactions**: `BEGIN TRANSACTION`, `COMMIT`, and `ROLLBACK`. `COMMIT` outside a transaction fails. A statement that is not inside an explicit transaction is committed when it succeeds.
