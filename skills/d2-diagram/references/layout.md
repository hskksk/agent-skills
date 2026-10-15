# レイアウトと位置

エンジン、ファイル内設定、方向、寸法、題の置き方の正本である。このスキルでは `elk` を使う。出典は [Layouts](https://d2lang.com/tour/layouts/)、[ELK](https://d2lang.com/tour/elk/)、[Positions](https://d2lang.com/tour/positions/)、[Variables](https://d2lang.com/tour/vars/) である。

## エンジン

| エンジン | 位置づけ |
| --- | --- |
| `dagre` | D2 の既定。速い階層レイアウト |
| `elk` | このスキルの標準。直交の経路、コンテナ同士の接続、SQL テーブルの行への接続 |
| `tala` | ソフトウェア構成図向け。別途インストールする |

`elk` の既定アルゴリズムは `layered` である。変えるときは CLI で渡す。

| アルゴリズム | 向き |
| --- | --- |
| `layered` | 既定。層に並べ、接続は直交する |
| `force` | 引力と斥力で広げる |
| `stress` | 経路が短い組を近くに置く |
| `mrtree` | 木を段に並べる |
| `radial` | 木を根の周りに円で並べる。木を想定する |

```shell
d2 --layout=elk --elk-algorithm=force input.d2 out.svg
```

`layered` は階層に強く、対称性はあまり見ない。経路に余分な折れが入ることがある。

## ファイル内の設定

```d2
vars: {
  d2-config: {
    layout-engine: elk
    theme-id: 4
    dark-theme-id: 200
    pad: 0
    center: true
    sketch: false
  }
}
```

これは `d2 --layout=elk --theme=4 --dark-theme=200 --pad=0 --center` と同じである。フラグと環境変数の方が優先される。`D2_LAYOUT=dagre d2 --theme=1 input.d2` のとき、ファイルの `layout-engine` と `theme-id` は使われない。

使えるレイアウトは `d2 layout`、エンジンごとのフラグは `d2 layout elk` で見られる。

## 方向

`direction` は `up`、`down`、`right`、`left` のいずれか。`dagre` と `elk` では図全体に一つだけ効く。コンテナごとに違う方向を持たせられるのは TALA だけである。

```d2
vars: {
  d2-config: {
    layout-engine: elk
  }
}
direction: right
a -> b -> c
```

## エンジンごとの制限

- `near` の定数はどのエンジンでも使える。別の図形を `near` に指定できるのは TALA だけである。
- コンテナの `width` と `height` は TALA と `elk` が扱う。TALA は中身に合わせて寸法を広げることがある。図形そのものの寸法はどのエンジンでも指定できる。
- `top` と `left` で位置を固定できるのは TALA だけである。両方を一緒に書く。
- 祖先から子孫への接続（コンテナからその中の子へ）は `dagre` では動かない。

## 題と near

題は markdown ブロックを `near: top-center` に置く。

```d2
title: |md
  # Diagram Title Here
| {near: top-center}
a -> b
```

`title: Diagram Title` は、上に固定された題にはならない。キーが `title` の図形になる。

図の周りに置ける定数は次のとおり。

`top-left`、`top-center`、`top-right`、`center-left`、`center-right`、`bottom-left`、`bottom-center`、`bottom-right`

ラベルとアイコンの `near` には、枠の外へ出す `outside-` と、枠の上に載せる `border-` を付けられる。外側の左右は `outside-left-center` と `outside-right-center` で、図全体の `center-left` とは語順が違う。

`tooltip` は通常ホバーで出る。`near` を付けると常に表示される。

長い説明も markdown ブロックで置ける。

```d2
explanation: |md
  # Why this shape
  - first reason
  - second reason
| {near: top-left}
```
