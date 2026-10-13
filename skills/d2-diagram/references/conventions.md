# D2 の記法

図を書くときに毎回使う規則をここに置く。色が何を意味するか、どのコマンドで検証するかは、このスキルの外である。記法の出典は [D2 の公式ツアー](https://d2lang.com/tour/) である。

## レイアウトエンジン

D2 の既定エンジンは `dagre` である。このスキルでは `elk` を使う。公式の説明では、`elk` は直交の経路を引き、コンテナ同士の接続を `dagre` より扱い、SQL テーブルの接続を行へ着ける。

ファイルの先頭で、`vars` の中に `d2-config` を書く。

```d2
vars: {
  d2-config: {
    layout-engine: elk
  }
}
```

- `--layout` と環境変数 `D2_LAYOUT` は、ファイル内の `d2-config` より優先される。
- `direction` は `up`、`down`、`right`、`left` のいずれか。`elk` では図全体に一つだけ効く。コンテナごとの `direction` は TALA だけが持つ。
- `near` の定数はどのエンジンでも使える。別の図形を `near` に指定できるのは TALA だけである。
- コンテナの `width` と `height` は TALA と `elk` が扱う。図形そのものの寸法はどのエンジンでも指定できる。
- `elk` の既定アルゴリズムは `layered` である。変えるときは CLI の `--elk-algorithm` に `force`、`stress`、`mrtree`、`radial` を渡す。`radial` は木を想定する。

## タイトル

公式の題の置き方は、markdown ブロックを `near: top-center` に置く形である。

```d2
title: |md
  # Diagram Title Here
| {near: top-center}
```

`title: Diagram Title` は、上に固定された題にはならない。キーが `title` の図形になる。

`near` の定数は次のとおり。

`top-left`、`top-center`、`top-right`、`center-left`、`center-right`、`bottom-left`、`bottom-center`、`bottom-right`

## 凡例

凡例は `vars` の `d2-legend` で自動生成する。

`a -> b` は凡例に図形 2 つと接続 1 つを出す。線だけを出すときは、端の図形を `style.opacity: 0` にする。見出しはラベルで変えられる。非英語の図ではここを使う。

凡例のキーに予約語は置かない。`label`、`shape`、`icon`、`style`、`link`、`near`、`direction`、`class`、`constraint` などはキーにするとコンパイルできない。`link -> link_end` はそのため失敗する。

`style.opacity` は 0 から 1 の数、`style.stroke-dash` は 0 から 10 の整数、`style.stroke-width` は 1 から 15 の整数である。

```d2
vars: {
  d2-config: { layout-engine: elk }
  d2-legend: "凡例" {
    item: {
      label: Item
      style.fill: "#E3F2FD"
      style.stroke: "#1565C0"
    }
    a -> b: Link {
      style.stroke-dash: 3
    }
    a.style.opacity: 0
    b.style.opacity: 0
  }
}
```

## コンテナの外から中を指す

接続はラベルではなくキーを指す。未宣言のキーを書くと、D2 はその場に新しい図形を作る。ルートで短い名前を書くと、コンテナ内の同名ノードには繋がらず、ルートに別の図形ができる。

コンテナの外からは完全修飾名を使う。

```d2
tier0.raw_alu -> tier1.frame_supplier
lane_sales.po_verify -> lane_om.order_create
```

同じコンテナのスコープ内では、プレフィックスを省いてよい。親コンテナは `_` で指す。

```d2
birthdays: {
  presents
  _.christmas.presents -> presents: regift
}
```

キーは大文字と小文字を区別しない。`postgresql` と `postgreSQL` は同じ図形である。

接続の書き方は `--`、`->`、`<-`、`<->` の 4 つである。同じ端点の接続を繰り返すと、既存の接続は上書きされず、別の接続が増える。

## 形

既定の `shape` は `rectangle` である。

公式の値は次のとおり。

`rectangle`、`square`、`page`、`parallelogram`、`document`、`cylinder`、`queue`、`package`、`step`、`callout`、`stored_data`、`person`、`diamond`、`oval`、`circle`、`hexagon`、`cloud`、`text`、`code`、`class`、`sql_table`、`image`、`sequence_diagram`、`c4-person`、`hierarchy`

`circle` と `square` は幅と高さが同じになる。長いラベルで幅が伸びると、高さも同じだけ伸びる。

`sql_table` は ER 図である。各キーが行、コロンの後が型、`constraint` が制約になる。`primary_key` は PK、`foreign_key` は FK、`unique` は UNQ と短く描かれる。複数の制約は配列で書く。列名が予約語のときは引用符で包む。`elk` と TALA では、テーブル同士の接続が行に着く。

```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  name: string
}
orders: {
  shape: sql_table
  id: int {constraint: primary_key}
  user_id: int {constraint: [foreign_key; unique]}
}
orders.user_id -> users.id
```

`sql_table` と `class` では、`fill` がヘッダの塗り、`stroke` が本体の塗りになる。

`queue` はキューの形をした図形である。待ちや仕掛を意味する予約語ではない。形と業務上の意味の対応は、呼び出し側の規約に従う。

## ラベル、引用、置換

置換の構文は `${path}` である。`vars` はスコープを持ち、外側の変数は内側から見える。同名のときは、置換に近い定義が使われる。展開した中身がマップや配列のときは `...${x}` で広げられる。

- 引用なしの文字列と二重引用符の中では、`$` が置換の開始になる。`${` で始まらない `$` はコンパイルエラーになる。通貨は単引用符の `'$100'` か、`USD` のように書く。
- 単引用符は置換を展開しない。`'${name}'` はその文字のまま残る。
- `()` は置換の構文ではない。ラベルに置ける。
- 引用なしの文字列は、改行、`;`、`#`、`{`、`}`、`[`、`]` で終わる。これらの文字が要るときは引用符かブロック文字列にする。
- `\n` は改行として描画される。`\t`、`\r`、`\\`、`\"` もエスケープである。複数行の本文はブロック文字列にする。

```d2
explanation: |md
  # Heading
  - first
  - second
|
```

markdown のラベルを図形に付けるときは、その図形を明示してからラベルを書く。単独のテキストは markdown として扱われる。`shape: text` にすると markdown にはならない。
