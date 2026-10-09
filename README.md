# agent-skills

AI エージェント向けスキルのカタログ。 [Agent Skills](https://agentskills.io/specification) の `SKILL.md` を `skills/` に置き、[skills.sh](https://skills.sh) からインストールできるようにしてある。

<a href="https://skills.sh/hskksk/agent-skills"><img alt="skills.sh" src="https://skills.sh/b/hskksk/agent-skills?style=for-the-badge" height="28"></a>

## インストール

```bash
npx skills add hskksk/agent-skills
```

一つのスキルだけ入れる場合:

```bash
npx skills add hskksk/agent-skills --skill japanese-writing
```

## 入っているスキル

| スキル | 説明（`SKILL.md` の `description`） |
| --- | --- |
| `how-to-survey` | テーマを分解して検索計画を立て、WebSearch と WebFetch で広く一次情報を集め、出典対応表を残す。調査の薄さの判定まで。Use when planning and executing web-based landscape or decision-support research before writing a report. |
| `japanese-writing` | 日本語の技術文・レポート・ドキュメントを書く、英訳する、推敲する。直訳調・官公庁調・AI構文（〜と考えられます、見ていきましょう）を直す。Use when writing or revising Japanese technical prose. |
| `survey-report` | 調査依頼を Phase 1（探索型）または Phase 2（検証・構造化型）に振り分け、前・中・後重心と読者レベルを選んでレポートを構成・出力する。Use when routing research requests and writing landscape or decision-oriented survey reports. |
| `narrative-report` | ビジネスナラティブの考え方を使い、分野を問わず、事実や変化を背景・意味・目指す未来・関係者の役割が伝わるレポートに構成する。Use when a report in any field needs to explain why a change matters, what it means, and what future or choices it points toward—not merely prose or fictional storytelling. |
| `skill-orchestration` | 複数のスキルを一つの仕事に組み合わせるとき、呼び出し側の書き方を決める。他スキルのファイルやスクリプトのパスは指さず、スキル名と相手の手順だけをインターフェースにする。Use when writing, editing, or reviewing a skill that calls, routes, or composes other skills. |

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

## CI とリリース

`main` への pull request では、フロントマター、ディレクトリ名、参照ファイル、`skills.sh.json` を検証する（Agent Skills Discovery workflow）。

Issue や PR のコメント・本文で `/oc` や `/opencode` を書くと OpenCode workflow（`hskksk/gh-actions` の reusable workflow）が動く。調査用の `/oci`・`/oca` なども同様。リポジトリの **Secrets** に `OPENCODE_API_KEY`（Zen / `opencode/*`）と、必要なら `OPENCODE_GO_API_KEY`（`opencode-go/*`）を登録する。追加でトリガーできる GitHub ログインは **Variables** の `OPENCODE_TRIGGER_ALLOWLIST`（カンマ区切り）で指定する。

`main` への push では [semantic-release](https://github.com/semantic-release/semantic-release) が [Conventional Commits](https://www.conventionalcommits.org/) から **リポジトリの semver**（`v1.2.3` タグ）と GitHub Release を作る。npm パッケージは公開しない。

リリース時の流れ:

1. 前回タグ以降に変更のあった `skills/<name>/` の `SKILL.md` だけ、`metadata.version` をその semver に更新する
2. ワークツリーから discovery index（`dist/`）をビルドし、Release アセットに添付する
3. `CHANGELOG.md` と更新した `SKILL.md` を `[skip ci]` でコミットする

各スキルの版は `SKILL.md` の `metadata.version`（skills.sh 向け）で管理する。リポジトリに `package.json` の version は持たない。

コミットと PR タイトルは [Conventional Commits](https://www.conventionalcommits.org/)（英語・命令形）。squash マージでは PR タイトルがそのままリリース履歴になる。詳細と型ごとの semver は [AGENTS.md](AGENTS.md)。PR タイトルは CI（Conventional Commits workflow）で検証する。

成果物は [Agent Skills discovery 0.2.0](https://schemas.agentskills.io/discovery/0.2.0/schema.json) の `index.json` と、スキルごとのファイルである。単一の `SKILL.md` だけなら `skill-md`、参照ファイルがあるスキルは `tar.gz` になる。URL はリリースのダウンロード先を指す。

```bash
npm ci --ignore-scripts
node scripts/build-discovery-index.mjs https://example.com/skills
```

`dist/index.json` が生成される。生成物はコミットしない。

skills.sh のリーダーボードへの掲載は、このリリースとは別に、`npx skills add` の匿名テレメトリで集計される。リポジトリを push しただけでは掲載されない。

## ライセンス

MIT
