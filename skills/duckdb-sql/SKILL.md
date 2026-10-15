---
name: duckdb-sql
description: DuckDB の分析 SQL を書く。Friendly SQL、ネスト型、ファイルの直接クエリ、PIVOT、マクロを選ぶ。Use when writing or reviewing analytical DuckDB SQL.
license: MIT
metadata:
  author: hskksk
  version: 1.0.0
---

# DuckDB SQL を書く

DuckDB 向けの分析 SQL を書く、直す、レビューするときに使う。どの方言を選ぶかは `references/conventions.md` が正本である。構文の詳細は、使う機能の reference だけを読む。

接続の開き方、ロック、ファイルパスの制限、特定プロダクトのツール名や出力言語は扱わない。

## 手順

1. 問い合わせを書く前に `references/conventions.md` を読む。
2. 使う機能に対応する reference だけを読む。全部は読まない。
3. 同梱の reference に無い確認は、`references/official-docs.md` の表から公式ページを開く。

## 参照ファイル

| ファイル | 内容 | いつ読むか |
| --- | --- | --- |
| `references/conventions.md` | 優先する方言と、書く前にやること | クエリを書く前 |
| `references/01_introduction.md` | 概要、Friendly SQL、PostgreSQL との差、quirks | 方言の形を確認するとき |
| `references/02_query_syntax.md` | EXCLUDE、REPLACE、COLUMNS、QUALIFY、特殊な JOIN | その構文を使うとき |
| `references/03_data_types.md` | LIST、STRUCT、MAP、ARRAY、UNION、VARIANT | ネスト型を選ぶとき |
| `references/04_functions.md` | リスト、構造体、ラムダ、集約の拡張 | その関数を使うとき |
| `references/05_statements.md` | ファイル直接クエリ、PIVOT、MACRO、COPY | 表を作る前の探索や形の変換 |
| `references/official-docs.md` | 公式ドキュメントへのパス | 同梱の説明に無いとき |

## このスキルが扱わないこと

標準 SQL の入門、データベース製品の選定、アプリケーション固有の命名やコメントの言語は含めない。
