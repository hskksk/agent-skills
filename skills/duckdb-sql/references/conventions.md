# どの方言を選ぶか

DuckDB の分析 SQL では、下の形を標準にする。構文の例は `01_introduction.md` 以降にあり、ここには選ぶ基準だけを置く。

## 優先する形

- **FROM-first**: 探索では `FROM tbl SELECT col1, col2`、または `SELECT` を省いた `FROM tbl`。
- **GROUP BY ALL / ORDER BY ALL**: SELECT から推論できる列リストを繰り返さない。
- **SELECT * EXCLUDE / REPLACE**: 数本を除く、または数本だけ置き換えるときに、残りの列を書き出さない。
- **COLUMNS()**: 正規表現かラムダに合う複数列へ、同じ変換を一度にかける。
- **末尾カンマ**: SELECT リストと LIST リテラルでは、差分が読みやすい側を取る。
- **SELECT の別名を後続句で使う**: WHERE、GROUP BY、HAVING では、直前の SELECT で付けた別名を参照する。
- **横方向の別名**: `SELECT x + 1 AS y, y * 2 AS z` のように、同じ SELECT の中で前の別名を使う。
- **count()**: `count(*)` の短い形。
- **INSERT INTO ... BY NAME**: 位置ではなく列名で対応させる。
- **CREATE OR REPLACE TABLE**: `DROP TABLE IF EXISTS` と `CREATE TABLE` を並べない。
- **UNION BY NAME**: 列の集合が揃わないときは、位置の `UNION` より名前で合わせる。

## 書く前と書いた後

- 複雑な問い合わせの前に、`DESCRIBE` か `SUMMARIZE` で形を見る。
- 入れ子の副問い合わせより、`WITH` の CTE を使う。
- 暗黙の変換に任せず、`CAST(x AS type)` か `x::type` で明示する。
- 形を変えるときは、CASE を並べたピボットより DuckDB の PIVOT を使う。
- 繰り返す式は、スカラーかテーブルの `CREATE MACRO` に出す。
- テーブルを作る前の探索は、`read_csv()`、`read_parquet()`、`read_json()` とグロブでファイルを直接読む。
- 重い問い合わせは `EXPLAIN ANALYZE` で見る。
- ウィンドウ関数の結果で絞るときは、副問い合わせで包まず `QUALIFY` を使う。
