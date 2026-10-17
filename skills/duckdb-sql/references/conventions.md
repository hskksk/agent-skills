# Which dialect to choose

For analytical DuckDB SQL, standardize on the forms below. Examples live from `01_introduction.md` onward. This file only records which form to choose.

## Preferred forms

- **FROM-first**: While exploring, write `FROM tbl SELECT col1, col2`, or `FROM tbl` with `SELECT` omitted.
- **GROUP BY ALL / ORDER BY ALL**: Leave out a column list that SELECT can infer.
- **SELECT * EXCLUDE / REPLACE**: When dropping a few columns, or replacing a few, leave the rest unlisted.
- **COLUMNS()**: Apply one transform at once to every column that matches a regular expression or a lambda.
- **Trailing commas**: In a SELECT list and a LIST literal, keep the comma on the side that makes the diff easier to read.
- **SELECT aliases in later clauses**: In WHERE, GROUP BY, and HAVING, refer to the alias from that SELECT.
- **Lateral aliases**: Use an earlier alias in the same SELECT, as in `SELECT x + 1 AS y, y * 2 AS z`.
- **count()**: The short form of `count(*)`.
- **INSERT INTO ... BY NAME**: Match columns by name.
- **CREATE OR REPLACE TABLE**: Replace the table in one statement.
- **UNION BY NAME**: When the column sets differ, match by name.

## Before and after writing

- Before a complex query, look at the shape with `DESCRIBE` or `SUMMARIZE`.
- Prefer a `WITH` CTE to a nested subquery.
- Cast explicitly with `CAST(x AS type)` or `x::type`. `'1.1' = 1` is true, and `'42' + 1` does not bind.
- The integer quotient is `//`. `/` returns `DOUBLE`.
- A lambda is `lambda x : x + 1`. The current documentation deprecates `x -> x + 1`.
- Duplicate column names become `name` and `name_1`.
- When reshaping, prefer DuckDB `PIVOT`. `FILTER` inside `USING` is ignored, so apply the condition before the pivot.
- Move a repeated expression into a scalar or table `CREATE MACRO`.
- Before creating a table, read files directly with `read_csv()`, `read_parquet()`, `read_json()`, and globs.
- Inspect a heavy query with `EXPLAIN ANALYZE`.
- Filter on a window result with `QUALIFY` in the same query.
