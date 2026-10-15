# 見た目

`style`、クラス、既定を一括で変えるグロブの正本である。出典は [Styles](https://d2lang.com/tour/style/)、[Classes](https://d2lang.com/tour/classes/)、[Globs](https://d2lang.com/tour/globs/) である。色が何を意味するかは、このスキルの外である。

`style` は図形にも接続にも書ける。ドットで一段に書いても、マップに書いても同じである。

```d2
x -> y: {
  style.stroke: "#0D32B2"
  style.stroke-dash: 3
}
x.style.fill: "#F7F8FE"
```

## 値

| キー | どこに効くか | 値 |
| --- | --- | --- |
| `opacity` | 図形と接続 | 0 から 1 |
| `stroke` | 図形と接続 | CSS の色名、16 進、一部のグラデーション |
| `fill` | 図形 | 色。`transparent` も書ける |
| `fill-pattern` | 図形 | `dots`、`lines`、`grain`、`none` |
| `stroke-width` | 図形と接続 | 1 から 15 の整数 |
| `stroke-dash` | 図形と接続 | 0 から 10 の整数 |
| `border-radius` | 図形。接続では折れの丸み | 0 から 20 の整数。接続の丸みは折れがあるエンジン（`elk` など）で効く |
| `shadow` | 図形 | `true` か `false` |
| `3d` | `rectangle` と `square` | `true` か `false` |
| `multiple` | 図形 | `true` か `false` |
| `double-border` | `rectangle` と `oval` | `true` か `false` |
| `font` | 文字 | 現在指定できるのは `mono` |
| `font-size` | 文字 | 8 から 100 の整数 |
| `font-color` | 文字 | 色 |
| `animated` | 図形と接続 | `true` か `false` |
| `bold`、`italic`、`underline` | 文字 | `true` か `false` |
| `text-transform` | 文字 | `uppercase`、`lowercase`、`title`、`none` |

`sql_table` と `class` では、`fill` がヘッダ、`stroke` が本体の塗り、`font-color` がヘッダの文字に効く。

図のルートにも、背景と外枠として次を書ける。`fill`、`fill-pattern`、`stroke`、`stroke-width`、`stroke-dash`、`double-border`。外枠を付けるときは `d2-config` の `pad` を 0 のままにしない。

```d2
style: {
  fill: "#F7F8FE"
  stroke: "#0D32B2"
  double-border: true
}
```

## クラス

同じ見た目は `classes` にまとめ、`class` で付ける。図形側に同じキーがあると、図形側が勝つ。配列で複数付けると、左から順に適用される。クラスは SVG の `class` 属性にも残る。

接続は宣言のときにも、あとから添字で指すときにも付けられる。

```d2
classes: {
  load balancer: {
    style: {
      fill: "#44C7B1"
      shadow: true
      border-radius: 5
    }
  }
  unhealthy: {
    style.fill: "#FE7070"
  }
}
web lb.class: load balancer
api.class: [load balancer; unhealthy]
a -> b: first
(a -> b)[0].class: unhealthy
```

## グロブ

既定の見た目はグロブで一括に書く。`*` は一段、`***` は再帰である。既存の図形にも、その後で宣言する図形にも効く。大文字と小文字は区別しない。接続のグロブは、自分自身への接続を作らない。

```d2
*.height: 300
*mini.height: 200

***.style.fill: lightblue
(*** -> ***)[*]: {
  style.stroke: red
}
```

フィルタや接続グロブの残りの書き方は [Globs](https://d2lang.com/tour/globs/) を見る。
