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
-- Column aliases usable in WHERE, GROUP BY, HAVING
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

-- SWITCH statement (syntactic sugar for CASE)
SELECT SWITCH (
    status = 1 => 'active',
    status = 2 => 'inactive',
    => 'unknown'
) AS label
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

DuckDB aims for PostgreSQL compatibility but diverges in these areas:

| Area | DuckDB | PostgreSQL |
|------|--------|------------|
| Division of integers | Returns `DECIMAL` (e.g., `1/2 = 0.5`) | Returns `INTEGER` (e.g., `1/2 = 0`) |
| Case sensitivity | Case-insensitive identifiers, preserves original case in catalog | Case-insensitive, folds to lowercase |
| `STRING_AGG` default separator | Empty string `''` | Comma `','` |
| Implicit casting | More permissive (e.g., `VARCHAR` to `INTEGER`) | Stricter |
| `BOOLEAN` text representation | `true` / `false` | `t` / `f` |
| Schema default | `main` | `public` |

## SQL Quirks

Reference: <https://duckdb.org/docs/current/sql/dialect/sql_quirks>

- **Identifiers**: case-insensitive. Double-quote to preserve case or use reserved words as names.
  DuckDB deduplicates identifiers: `SELECT 1 AS a, 2 AS a` → columns `a`, `a:1`.
- **Numeric literals**: underscores are allowed as digit separators (`1_000_000`).
- **String literals**: single quotes only (`'text'`). Double quotes are for identifiers.
- **`NULL` handling**: `NULL` values sort last by default in ascending order (PostgreSQL-compatible).
- **Transaction semantics**: auto-commit by default. Explicit `BEGIN`/`COMMIT` for multi-statement transactions.
