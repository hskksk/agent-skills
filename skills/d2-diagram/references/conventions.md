# D2 の記法

図を書くときに毎回使う規則をここに置く。色が何を意味するか、どのコマンドで検証するかは、このスキルの外である。

## レイアウトエンジン

ファイルの先頭で、`vars` の中に `d2-config` を書く。標準は `elk` である。

```
vars: {
  d2-config: {
    layout-engine: elk
  }
}
```

## タイトル

タイトルは markdown ブロックにし、`near: top-center` で図の上中央に置く。

```
title: |md
  # Diagram Title Here
| {near: top-center}
```

プレーンな `title: text` は使わない。

## 凡例

凡例は `vars` の `d2-legend` で自動生成する。`legend: Legend { ... }` のような手書きの凡例コンテナは作らない。

ノードの見た目とエッジの見た目を凡例に書くと、描画結果に凡例の箱が出る。色の意味はここでは決めない。下は構文の例である。

```
vars: {
  d2-config: { layout-engine: elk }
  d2-legend: {
    item: {
      label: Item
      style.fill: "#E3F2FD"
      style.stroke: "#1565C0"
    }
    link -> link_end: Link {
      style.stroke-dash: 3
    }
  }
}
```

## コンテナの外から中を指す

コンテナの外から、その中にあるノードを指すときは、完全修飾名 `container_name.node_name` を使う。短い名前のままだと、線が切れるか、別の場所へ伸びる。

```
tier0.raw_alu -> tier1.frame_supplier
lane_sales.po_verify -> lane_om.order_create
```

次のようには書かない。

```
raw_alu -> frame_supplier
po_verify -> order_create
```

同じコンテナの中に矢印もノードもあるときは、そのコンテナのスコープ内に限り、プレフィックスを省いてよい。

## 形

| 形 | 向いているもの |
| --- | --- |
| `sql_table` | 表 |
| `queue` | 待ちや仕掛 |
| `cloud` | 境界の外にある相手 |
| `oval` | 受け取る側 |
| `rectangle` | 処理 |

## ラベルに置かない文字

D2 は次の文字を構文として読む。ラベルの文言には置かない。

- `$` は置換の開始になる。通貨は "USD" のように書く。
- `()` は置換の構文になる。除くか、`-` に替える。
- `\n` は環境によって壊れる。区切りは ` / ` にするか、引用符の複数行ラベルにする。
