# 接続とコンテナ

キー、コンテナ、接続、矢じりの正本である。出典は [Connections](https://d2lang.com/tour/connections/) と [Containers](https://d2lang.com/tour/containers/) である。

## キー

接続はラベルではなくキーを指す。未宣言のキーを書くと、D2 はその場に新しい図形を作る。

```d2
be: Backend
fe: Frontend

# 既存の図形を繋ぐ
be -> fe

# Backend と Frontend という新しい図形を作る
# Backend -> Frontend
```

ルートで短い名前を書くと、コンテナ内の同名ノードには繋がらず、ルートに別の図形ができる。コンテナの外からは完全修飾名を使う。

```d2
tier0: {
  raw_alu
}
tier1: {
  frame_supplier
}
tier0.raw_alu -> tier1.frame_supplier
```

同じコンテナのスコープ内では、プレフィックスを省ける。親は `_` である。`_` は外側のスコープを一段上がる。

```d2
christmas: {
  presents
}
birthdays: {
  presents
  _.christmas.presents -> presents: regift
}
```

キーは大文字と小文字を区別しない。`postgresql` と `postgreSQL` は同じ図形である。

コンテナのラベルは、キーの直後に書くか、中の `label` に書く。

```d2
gcloud: Google Cloud {
  api -> db
}
```

```d2
gcloud: {
  label: Google Cloud
  api -> db
}
```

入れ子にすると、外側のキーを繰り返さずに中を書ける。

```d2
clouds: {
  aws: {
    load_balancer -> api
    api -> db
  }
  gcloud: {
    auth -> db
  }
  gcloud -> aws
}
```

## キーにできない語

次の語はオブジェクトのキーにできない。凡例の中でも同じである。

`label`、`shape`、`icon`、`constraint`、`tooltip`、`link`、`near`、`width`、`height`、`direction`、`top`、`left`、`class`、`classes`、`vars`、`style`、`source-arrowhead`、`target-arrowhead`

`grid-rows`、`grid-columns`、`grid-gap`、`vertical-gap`、`horizontal-gap` もキーにできない。`near` の定数（`top-center` など）と `style` の子キーも、その文脈では予約されている。予約語をラベルや列名として残すときは引用符で包む。

## 接続

接続は 4 種類ある。

- `--`
- `->`
- `<-`
- `<->`

ラベルは接続の直後に書く。

```d2
replica 1 -- replica 2: Kept in sync
```

同じ端点の接続を繰り返すと、既存の接続は上書きされず、別の接続が増える。何本目かを指すときは 0 始まりの添字を使う。

```d2
a -> b: first
a -> b: second
(a -> b)[0].style.stroke: red
(a -> b)[1].style.stroke: blue
```

一行に鎖状で書ける。鎖のラベルは、その行の各接続に付く。

```d2
High Mem Instance -> EC2 <- High CPU Instance: Hosted By
```

循環してよい。

## 矢じり

`source-arrowhead` と `target-arrowhead` で、端の形と短いラベルを指定する。その方向に端が無い接続では、矢じりは描かれない。`x -> y` には source 側の矢じりがないので、`source-arrowhead` を書いても出ない。

| `shape` | 補足 |
| --- | --- |
| `triangle` | 既定。`style.filled: false` で塗りを抜ける |
| `arrow` | triangle より尖る |
| `diamond` | `style.filled: true` で塗れる |
| `circle` | `style.filled: true` で塗れる |
| `box` | `style.filled: true` で塗れる |
| `cf-one`、`cf-one-required` | カラスの足。1 |
| `cf-many`、`cf-many-required` | カラスの足。多 |
| `cross` | 十字 |

矢じりのラベルは短くする。通常のラベルと違い、自動配置の対象にならない。

```d2
a -> b: note {
  target-arrowhead: * {
    shape: diamond
    style.filled: true
  }
}
```
