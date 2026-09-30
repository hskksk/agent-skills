# agent-skills

AI エージェント向けスキルのカタログ。 [Agent Skills](https://agentskills.io/specification) の `SKILL.md` を `skills/` に置き、[skills.sh](https://skills.sh) からインストールできるようにしてある。

[![skills.sh](https://skills.sh/b/hskksk/agent-skills)](https://skills.sh/hskksk/agent-skills)

## インストール

```bash
npx skills add hskksk/agent-skills
```

一つのスキルだけ入れる場合:

```bash
npx skills add hskksk/agent-skills --skill japanese-writing
```

## 入っているスキル

| スキル | 用途 |
| --- | --- |
| `japanese-writing` | 日本語の技術文を書き、英語からの直訳調を直す。正本は `skills/japanese-writing/references/japanese.md` |

`japanese.md` は [hskksk/podcaster](https://github.com/hskksk/podcaster) の `podcast-research2` にある同名ファイルである。

## スキルの置き方

skills.sh の CLI は、リポジトリの `skills/<name>/SKILL.md` を探す。`name` はディレクトリ名と一致させ、小文字・数字・ハイフンだけにする。

```text
skills.sh.json
skills/
  japanese-writing/
    SKILL.md
    references/
      japanese.md
```

長い規則は `references/` に分ける。`SKILL.md` には、いつそのファイルを読むかを書く。

`skills.sh.json` は skills.sh のリポジトリページでのグループ表示だけを変える。インストール内容は変わらない。新しいスキルは `groupings` に追加する。

## CI

`main` への pull request では、フロントマター、ディレクトリ名、参照ファイル、`skills.sh.json` を検証する。`main` へ入ると、同じ検証のあと GitHub Release に discovery index を公開する。

成果物は [Agent Skills discovery 0.2.0](https://schemas.agentskills.io/discovery/0.2.0/schema.json) の `index.json` と、スキルごとのファイルである。単一の `SKILL.md` だけなら `skill-md`、参照ファイルがあるスキルは `tar.gz` になる。URL はリリースのダウンロード先を指す。

```bash
npm ci --ignore-scripts
node scripts/build-discovery-index.mjs https://example.com/skills
```

`dist/index.json` が生成される。生成物はコミットしない。

skills.sh のリーダーボードへの掲載は、このリリースとは別に、`npx skills add` の匿名テレメトリで集計される。リポジトリを push しただけでは掲載されない。

## ライセンス

MIT
