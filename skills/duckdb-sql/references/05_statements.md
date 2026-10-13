# DuckDB Statements

This document covers DuckDB-specific SQL statements and extensions to standard statements.
For standard CREATE TABLE, INSERT, UPDATE, DELETE, DROP, refer to
<https://duckdb.org/docs/current/sql/statements/overview>.

## Direct File Queries

DuckDB can query files directly without creating tables first. This is one of its most distinctive features.

Reference: <https://duckdb.org/docs/current/data/overview>

```sql
-- Directly query files (replacement scans)
SELECT * FROM 'data.csv';
SELECT * FROM 'data.parquet';
SELECT * FROM 'data.json';

-- Glob patterns
SELECT * FROM 'data/*.parquet';
SELECT * FROM 'logs/2024-*.csv';

-- Using read functions (more control over options)
SELECT * FROM read_csv('data.csv', header = true, delim = ',');
SELECT * FROM read_csv('data.csv', columns = {'id': 'INT', 'name': 'VARCHAR'});
SELECT * FROM read_csv('*.csv', filename = true);  -- adds source filename column

SELECT * FROM read_parquet('data.parquet');
SELECT * FROM read_parquet('data/*.parquet', hive_partitioning = true);

SELECT * FROM read_json('data.json');
SELECT * FROM read_json('data.ndjson');
-- read_json_auto is an alias of read_json

-- HTTP(S) and S3 API paths autoload the httpfs extension.
-- S3 credentials belong in CREATE SECRET, not in the SQL text.
SELECT * FROM read_parquet('https://example.com/data.parquet');
SELECT * FROM read_csv('s3://bucket/data.csv');

-- Create table from file
CREATE TABLE t AS SELECT * FROM 'data.parquet';
```

### read_csv Key Options

| Option | Description | Default |
|--------|-------------|---------|
| `auto_detect` | Sniff dialect and types | `true` |
| `header` | First row is the header. The sniffer may still detect one while `auto_detect` is on. Setting this explicitly skips sniffing for this option | `false` |
| `delim` | Column delimiter. Alias `sep`. An explicit value skips sniffing for this option | `,` |
| `quote` | Quote character | `"` |
| `escape` | Escape character | `"` |
| `nullstr` | String or list of strings that mean NULL. Alias `null` | (empty) |
| `columns` | Explicit names and types, as a struct. Disables schema detection | (empty) |
| `sample_size` | Rows sampled for detection | `20480` |
| `filename` | Compatibility flag. Since DuckDB 1.3 the path is already a virtual `filename` column | `false` |
| `all_varchar` | Read every column as `VARCHAR` | `false` |
| `skip` | Lines to skip at the start of each file | `0` |
| `hive_partitioning` | Treat the path as Hive partitions | auto-detected |

## COPY Statement

Reference: <https://duckdb.org/docs/current/sql/statements/copy>

Bulk data import and export supporting multiple formats:

```sql
-- Import CSV
COPY table_name FROM 'data.csv' (FORMAT CSV, HEADER true, DELIMITER ',');

-- Export to Parquet
COPY table_name TO 'output.parquet' (FORMAT PARQUET);

-- Export query results to CSV
COPY (SELECT * FROM t WHERE x > 10) TO 'filtered.csv' (HEADER, DELIMITER '|');

-- Export to JSON
COPY table_name TO 'output.json' (FORMAT JSON, ARRAY true);

-- Partitioned export
COPY table_name TO 'output' (FORMAT PARQUET, PARTITION_BY (year, month));
```

## PIVOT / UNPIVOT

Reference: <https://duckdb.org/docs/current/sql/statements/pivot>

### PIVOT (Long to Wide)

```sql
-- Simplified syntax (auto-detects distinct values)
PIVOT sales_data
ON year
USING sum(revenue)
GROUP BY region;
-- Creates columns: region | 2022 | 2023 | 2024

-- Multiple aggregates
PIVOT sales_data
ON year
USING sum(revenue) AS total, avg(revenue) AS average
GROUP BY region;

-- Filter specific pivot values
PIVOT sales_data
ON year IN (2023, 2024)
USING sum(revenue)
GROUP BY region;

-- SQL Standard syntax
SELECT * FROM sales_data
PIVOT (
    sum(revenue)
    FOR year IN (2022, 2023, 2024)
    GROUP BY region
);

-- In CTE or subquery
WITH pivoted AS (
    PIVOT sales_data ON year USING sum(revenue) GROUP BY region
)
SELECT * FROM pivoted WHERE "2024" > 1000;
```

`PIVOT_WIDER` is an alias of `PIVOT`.

Without `GROUP BY`, every column that is not in `ON` or `USING` is kept. `GROUP BY` names columns. It does not accept positions or expressions.

A `FILTER` clause on an aggregate in `USING` is silently ignored. Filter the input before the pivot, or aggregate with `FILTER` outside `PIVOT`.

### UNPIVOT (Wide to Long)

Reference: <https://duckdb.org/docs/current/sql/statements/unpivot>

```sql
-- Simplified syntax
UNPIVOT monthly_data
ON jan, feb, mar
INTO NAME month VALUE amount;

-- SQL Standard syntax
SELECT * FROM monthly_data
UNPIVOT (
    amount FOR month IN (jan, feb, mar)
);
```

## CREATE MACRO

Reference: <https://duckdb.org/docs/current/sql/statements/create_macro>

Reusable SQL expressions (scalar) or queries (table):

```sql
-- Scalar macro
CREATE MACRO add_one(x) AS x + 1;
SELECT add_one(42);  -- 43

-- With default parameter
CREATE MACRO clamp(x, lo := 0, hi := 100) AS greatest(lo, least(hi, x));
SELECT clamp(150);      -- 100
SELECT clamp(150, hi := 200);  -- 150

-- Table macro. query_table and query accept a constant string only.
-- There is no query_column function.
CREATE MACRO top_n(tbl, n := 5) AS TABLE
    SELECT * FROM query_table(tbl) LIMIT n;

SELECT * FROM top_n('sales', n := 10);

-- query() builds a statement from a constant string
CREATE MACRO stack(table_name, index_cols, name_col, value_col) AS TABLE
    FROM query(
        'UNPIVOT ' || table_name
        || ' ON COLUMNS(* EXCLUDE (' || array_to_string(index_cols, ', ')
        || ')) INTO NAME ' || name_col || ' VALUE ' || value_col
    );

-- CREATE OR REPLACE
CREATE OR REPLACE MACRO my_func(x) AS x * 2;
```

## ATTACH / DETACH

Reference: <https://duckdb.org/docs/current/sql/statements/attach>

Connect to multiple databases or external database engines:

```sql
-- Attach another DuckDB file
ATTACH 'other.duckdb' AS other_db;
SELECT * FROM other_db.main.my_table;

-- Attach read-only
ATTACH 'archive.duckdb' AS archive (READ_ONLY);

-- Attach PostgreSQL (requires postgres extension)
ATTACH 'dbname=mydb' AS pg (TYPE postgres);
SELECT * FROM pg.public.users;

-- Attach SQLite (requires sqlite extension)
ATTACH 'legacy.db' AS sqlite_db (TYPE sqlite);

-- Attach MySQL (requires mysql extension)
ATTACH 'host=localhost database=mydb user=root' AS mysql_db (TYPE mysql);

-- Detach
DETACH other_db;

-- USE to set default database/schema
USE other_db;
USE other_db.my_schema;
```

## DESCRIBE / SUMMARIZE

Reference: <https://duckdb.org/docs/current/sql/statements/describe>,
<https://duckdb.org/docs/current/sql/statements/summarize>

```sql
-- DESCRIBE: show schema (column names, types, nullability)
DESCRIBE my_table;
DESCRIBE SELECT * FROM read_csv('data.csv');

-- SUMMARIZE: descriptive statistics for all columns
SUMMARIZE my_table;
SUMMARIZE SELECT * FROM read_csv('data.csv');
-- Returns: column_name, column_type, min, max, approx_unique, avg, std, q25, q50, q75, count, null_percentage
```

## EXPORT / IMPORT DATABASE

Reference: <https://duckdb.org/docs/current/sql/statements/export>

```sql
-- Export entire database to a directory
EXPORT DATABASE 'backup_dir';
EXPORT DATABASE 'backup_dir' (FORMAT PARQUET);

-- Import database from export directory
IMPORT DATABASE 'backup_dir';
```

## CREATE TYPE

Reference: <https://duckdb.org/docs/current/sql/statements/create_type>

```sql
-- Alias for existing type
CREATE TYPE user_id AS INTEGER;

-- Enum type
CREATE TYPE color AS ENUM ('red', 'green', 'blue');

-- Composite type
CREATE TYPE address AS STRUCT(street VARCHAR, city VARCHAR, zip VARCHAR);

-- Use in table
CREATE TABLE users (id user_id, favorite_color color, home address);
```

## CREATE SECRET

Reference: <https://duckdb.org/docs/current/sql/statements/create_secret>

Manage credentials for external services (S3, GCS, Azure, and others).
The CLI stores `CREATE SECRET` in the history file as plain text.

`httpfs` is autoloaded the first time an HTTP(S) or S3 API path is used.
For plain HTTP(S) it reads files. For the S3 API it also writes and globs.

```sql
-- S3 credentials. Replace the placeholders outside the skill text.
CREATE SECRET my_s3 (
    TYPE s3,
    KEY_ID 'access_key_id',
    SECRET 'secret_access_key',
    REGION 'us-east-1'
);

-- List secrets
SELECT * FROM duckdb_secrets();

-- Drop secret
DROP SECRET my_s3;
```

## Other Useful Statements

```sql
-- SET / RESET configuration
SET threads = 4;
SET memory_limit = '2GB';
RESET threads;

-- SET VARIABLE (SQL-level variables)
SET VARIABLE my_date = DATE '2024-01-01';
SELECT * FROM t WHERE created_at > getvariable('my_date');

-- SHOW databases / tables
SHOW DATABASES;
SHOW TABLES;
SHOW ALL TABLES;  -- includes all schemas

-- EXPLAIN / EXPLAIN ANALYZE
EXPLAIN SELECT * FROM t WHERE x > 10;
EXPLAIN ANALYZE SELECT * FROM t WHERE x > 10;

-- CHECKPOINT (force WAL flush)
CHECKPOINT;

-- VACUUM does not reclaim space. A bare VACUUM is a no-op.
-- VACUUM table(column) rebuilds that column's distinct statistics.
-- VACUUM FULL is not supported.
VACUUM;
VACUUM my_table(my_column);

-- LOAD / INSTALL extensions
INSTALL httpfs;
LOAD httpfs;
```
