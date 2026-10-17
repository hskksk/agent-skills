---
name: duckdb-sql
description: Write analytical DuckDB SQL. Choose Friendly SQL, nested types, direct file queries, PIVOT, and macros. Use when writing or reviewing analytical DuckDB SQL.
license: MIT
metadata:
  author: hskksk
  version: 1.0.0
---

# Write DuckDB SQL

Use this when writing, fixing, or reviewing analytical SQL for DuckDB. `references/conventions.md` is the source of truth for which dialect to choose. Read only the reference for the feature you are using.

How to open a connection, locks, path limits, a product's tool names, and the language of the output stay outside this skill.

## When to use

- Write or review an analytical query in DuckDB
- Choose among Friendly SQL, a nested type, a direct file read, PIVOT, or a macro

Do not use it for:

- An introduction to standard SQL, choosing a database product, or application-specific names and comment language

## Procedure

1. Read `references/conventions.md` before writing the query.
2. Read only the reference that matches the feature you are using.
3. For a check that the bundled references do not cover, open the official page from the table in `references/official-docs.md`.

## Reference files

| File | Contents | When to read |
| --- | --- | --- |
| `references/conventions.md` | The dialect to prefer, and what to do before writing | Before writing a query |
| `references/01_introduction.md` | Overview, Friendly SQL, differences from PostgreSQL, and quirks | When checking the shape of the dialect |
| `references/02_query_syntax.md` | EXCLUDE, REPLACE, COLUMNS, QUALIFY, and special JOINs | When using that syntax |
| `references/03_data_types.md` | LIST, STRUCT, MAP, ARRAY, UNION, and VARIANT | When choosing a nested type |
| `references/04_functions.md` | Lists, structs, lambdas, and aggregate extensions | When using those functions |
| `references/05_statements.md` | Direct file queries, PIVOT, MACRO, and COPY | When exploring before a table, or reshaping |
| `references/official-docs.md` | Paths to the official documentation | When the bundled explanation does not cover it |
