# 凡例

`d2-legend` の正本である。出典は [Legend](https://d2lang.com/tour/legend/) である。破線、透明度、線幅の取りうる値は `style.md` が正本である。キーに使えない語は `connections.md` が正本である。

## 宣言

凡例は `vars` の `d2-legend` に書く。中の図形と接続が、描画結果の凡例箱になる。

```d2
vars: {
  d2-config: {
    layout-engine: elk
  }
  d2-legend: {
    service: {
      label: Service
      style.fill: "#E3F2FD"
      style.stroke: "#1565C0"
    }
    store: Database {
      shape: cylinder
      style.stroke-dash: 2
    }
    service <-> store: Good {
      style.stroke: red
      style.stroke-dash: 2
      style.stroke-width: 1
    }
    service -> store: Bad
    service -> store: Tenuous {
      target-arrowhead.shape: circle
    }
  }
}
api -> db
db.shape: cylinder
```

`service -> store` は凡例に図形 2 つと接続 1 つを出す。線だけを出すときは、端の図形を `style.opacity: 0` にする。

```d2
vars: {
  d2-legend: {
    a <-> b: Good relationship {
      style.stroke: red
      style.stroke-dash: 2
    }
    a.style.opacity: 0
    b.style.opacity: 0
  }
}
```

## 見出し

ラベルを付けると、既定の "legend" を置き換えられる。非英語の図ではここを使う。

```d2
vars: {
  d2-legend: "凡例" {
    item: {
      label: 処理
    }
  }
}
x -> y
```

## キー

凡例の中のキーも、図のほかのキーと同じ予約語を使えない。`label`、`shape`、`style`、`link`、`near` などをキーにするとコンパイルできない。`link -> link_end` は `link` が予約語なので失敗する。一覧は `connections.md` にある。
