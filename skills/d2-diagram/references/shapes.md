# 形

`shape` の正本である。出典は [Shapes](https://d2lang.com/tour/shapes/)、[SQL Tables](https://d2lang.com/tour/sql-tables/)、[UML Classes](https://d2lang.com/tour/uml-classes/)、[Sequence Diagrams](https://d2lang.com/tour/sequence-diagrams/)、[Icons](https://d2lang.com/tour/icons/) である。塗りと線の値は `style.md`、キーの予約語は `connections.md` が正本である。

既定は `rectangle` である。ラベルをキーと別にしたいときは、キーの直後にラベルを書く。

```d2
pg: PostgreSQL
cloud_box: my cloud
cloud_box.shape: cloud
```

## 一覧

`rectangle`、`square`、`page`、`parallelogram`、`document`、`cylinder`、`queue`、`package`、`step`、`callout`、`stored_data`、`person`、`diamond`、`oval`、`circle`、`hexagon`、`cloud`、`text`、`code`、`class`、`sql_table`、`image`、`sequence_diagram`、`c4-person`、`hierarchy`

`circle` と `square` は幅と高さが同じになる。長いラベルで幅が伸びると、高さも同じだけ伸びる。`width` と `height` を両方書くと、大きい方に揃う。

`queue` はキューの形をした図形である。待ちや仕掛を意味する予約語ではない。形と業務上の意味の対応は、呼び出し側の規約に従う。

## SQL テーブル

`sql_table` は ER 図である。各キーが行、コロンの後が型、`constraint` が制約になる。

| `constraint` | 図の中の短記 |
| --- | --- |
| `primary_key` | PK |
| `foreign_key` | FK |
| `unique` | UNQ |

知らない制約文字列も書けるが、短くはならない。複数は配列にする。列名が予約語のときは引用符で包む。

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

`elk` と TALA では、この接続が行に着く。`fill` はヘッダ、`stroke` は本体の塗り、`font-color` はヘッダの文字に効く。

制約の配列へ共通の要素を広げるときは、`text.md` の `...${name}` を使う。

## UML クラス

`class` の各キーはフィールドかメソッドである。フィールドの値は型である。キーに `(` があるとメソッドで、値は戻り値の型になる。値の無いメソッドの戻り値は void である。

可視性の接頭辞は、無しと `+` が public、`-` が private、`#` が protected である。`#` はコメントの開始でもあるので、行頭では `\#` と書く。

```d2
Parser: {
  shape: class
  +reader: io.RuneReader
  -lookahead: "[]rune"
  \#pos: int
  +peek(): (r rune, eof bool)
  rewind()
}
```

`fill`、`stroke`、`font-color` の効き方は `sql_table` と同じである。

## シーケンス図

`shape: sequence_diagram` を付ける。特別な矢印記法は無く、通常の接続を書く。違いは次の二つである。

- 中のアクターは、コンテナが違っても同じスコープの同じ図形を指す。
- 書いた順が、上から下、アクターは左から右の順になる。

```d2
shape: sequence_diagram
alice; bob
alice -> bob: What does it mean\nto be well-adjusted?
bob -> alice: The ability to play bridge.
```

アクターの中の図形から接続すると、その区間が span になる。

```d2
shape: sequence_diagram
alice.t1 -> bob
alice.t2 -> bob.a
alice.t2 <- bob.a
```

グループは、シーケンス図の中のコンテナで、外とは繋がず、中に接続を持つものである。グループの中から指すアクターは、先にトップレベルで宣言する。

```d2
shape: sequence_diagram
alice
bob
shower thoughts: {
  alice -> bob: A physicist is an atom's way of knowing about atoms.
}
```

アクターの中に、接続を持たない図形を書くと note になる。アクターから自分への接続は self-message になる。ライフラインの線は、アクターの `stroke` と `stroke-dash` を受け継ぐ。

## アイコン

`icon` には URL を書ける。CLI では `icon: ./file.png` のようなローカルパスも使える。公式のアイコン集は <https://icons.d2lang.com> にある。配置はエンジンが決める。コンテナでは左上、コンテナでない図形では中央に置かれることが多い。接続にも `icon` を付けられる。

```d2
deploy: {
  icon: https://icons.d2lang.com/aws%2FDeveloper%20Tools%2FAWS-CodeDeploy.svg
}
backup: {
  icon: https://icons.d2lang.com/aws%2FStorage%2FAWS-Backup.svg
}
deploy -> backup
```

図形そのものを画像にするときは `shape: image` を使う。
