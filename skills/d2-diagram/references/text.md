# 文字と置換

ラベル、引用、ブロック、変数の正本である。出典は [Strings](https://d2lang.com/tour/strings/)、[Text](https://d2lang.com/tour/text/)、[Variables](https://d2lang.com/tour/vars/)、[Comments](https://d2lang.com/tour/comments/) である。

## 引用なし

引用なしの文字列は、前後の空白が削られる。次の文字で文字列は終わる。

改行、`;`、`#`、`{`、`}`、`[`、`]`

キーの中では、さらに `:`、`.`、`<`、`>`、`&`、および `--` や `->` の始まりも区切りになる。

これらの文字がラベルに要るときは、単引用符、二重引用符、またはブロック文字列にする。単引用符の中に単引用符があるときは二重引用符を使い、両方あるときは二重引用符の中で `\` を使う。

## 置換

置換は `${path}` である。`$` の直後が `{` でないと、引用なしと二重引用符ではコンパイルできない。通貨は単引用符の `'$100'` か、`USD` のように書く。

単引用符は置換を展開しない。`'${name}'` と `'$100'` はその文字のまま残る。

```d2
vars: {
  server-name: Cat
}
server1: ${server-name}-1
server2: ${server-name}-2
server1 <-> server2
```

`vars` はスコープを持つ。外側の変数は内側から見える。同名のときは、置換に近い定義が使われる。内側の変数を外側からは参照できない。

```d2
vars: {
  region: Global
}
lb: ${region} load balancer
zone1: {
  vars: {
    region: us-east-1
  }
  server: ${region} API
}
```

ネストした値は `.` で辿る。

```d2
vars: {
  primaryColors: {
    button: {
      active: "#4baae5"
    }
  }
}
button.style.fill: ${primaryColors.button.active}
```

中身がマップや配列のときは `...${name}` で広げる。

```d2
vars: {
  base-constraints: [NOT NULL; UNQ]
}
data: {
  shape: sql_table
  a: int {constraint: [PK; ...${base-constraints}]}
}
```

## 改行とエスケープ

`\n` は改行として描画される。`\t`、`\r`、`\\`、`\"` もエスケープである。引用なしの生の改行は、そこで文字列が終わる。

複数行の本文はブロック文字列にする。`|md` から、同じ段の `|` までが本文である。本文に `|` が要るときは `||`、`|||`、または `|`` と ``|` のように、最初の `|` の後の記号を終端に使う。

```d2
explanation: |md
  # Heading
  - first
  - second
|
```

単独で置いたテキストは markdown になる。図形のラベルを markdown にするときは、図形を明示してからブロックを書く。`shape: text` にすると markdown にはならない。

```d2
explanation: |md
  # Heading
  - first
|
explanation.shape: rectangle
```

コードは `md` の代わりに言語名を書く。短い別名は `md`、`tex`、`js`、`go`、`py`、`rb`、`ts` である。知らない言語は、色分け無しの本文になる。

LaTeX は `latex` か `tex` である。数式向けで、文書レイアウト一式ではない。`font-size` は効かず、大きさは LaTeX 側の `\small` や `\large` で指定する。

## コメント

行コメントは `#` から行末までである。ブロックコメントは `"""` で囲む。

```d2
# whole line
x -> y # end of line

"""
block
"""
```
