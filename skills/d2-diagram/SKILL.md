---
name: d2-diagram
description: D2 の図を書く。elk、d2-legend、完全修飾の参照、タイトル、${} 置換。Use when writing or fixing a D2 diagram.
license: MIT
metadata:
  author: hskksk
  version: 1.0.0
---

# D2 の図を書く

D2 のソースを書く、直す、レビューするときに使う。毎回の判断は `references/overview.md` が正本である。構文は、そこで指している詳細ファイルが正本である。図を書き始める前に `overview.md` を読み、使う部分の詳細だけを開く。

色が確信度や状態のどれを表すか、実線と破線が業務上何を意味するか、どのツールで検証して描画するかは、このスキルでは決めない。使う側の規約に従う。

## 手順

1. `references/overview.md` を読む。
2. その表で、今回書く部分の詳細ファイルだけを読む。全部は読まない。
3. 詳細ファイルの書き方で `.d2` を書く。
4. 色や線種の意味、検証コマンドは、呼び出し側の規約があればそれに従う。無ければ、凡例のラベルで見た目の意味が読めるようにする。

## 参照ファイル

| ファイル | 内容 | いつ読むか |
| --- | --- | --- |
| `references/overview.md` | 毎回の判断と、詳細への参照 | 図を書く前 |
| `references/layout.md` | エンジン、方向、寸法、題と `near` | レイアウトや題を決めるとき |
| `references/legend.md` | `d2-legend` | 凡例を置くとき |
| `references/connections.md` | キー、コンテナ、接続、矢じり | 図形を繋ぐとき |
| `references/shapes.md` | 形、`sql_table`、`class`、シーケンス、アイコン | 形を選ぶとき |
| `references/text.md` | 引用、改行、markdown、`${}` | ラベルや変数を書くとき |
| `references/style.md` | `style`、クラス、グロブ | 塗りや線を指定するとき |

## このスキルが扱わないこと

特定プロダクトの配色、成果物のファイル名、セッションのディレクトリ、検証コマンドの名前は含めない。
