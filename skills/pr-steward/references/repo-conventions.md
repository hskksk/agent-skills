# リポジトリ規約（コンテキストを食わない）

steward に長いスタイルガイドをプロンプトへ貼らない。規約は **リポジトリの正本** と **機械的ゲート** に寄せ、エージェントには **どこを見るか・何を実行するか** だけ渡す。

## レイヤー（上ほどトークン不要）

| レイヤー | 例 | steward の使い方 |
| --- | --- | --- |
| 自動整形・lint | `eslint --fix`, `prettier`, `ruff format`, `gofmt` | Tier A の前後に **同じコマンドを実行**。ルール本文は読まない |
| コミット時フック | `husky`, `pre-commit`, `commitlint` | `git commit` 時に失敗すれば修正。メッセージ規約もここで検証 |
| CI | GitHub Actions の lint / test | 緑にするまで push；CI ログは要約だけ handoff に |
| 静的設定 | `commitlint.config.*`, `.editorconfig`, `biome.json` | 失敗したときだけ該当ファイルを **必要行だけ** 読む |
| 人向けドキュメント | `AGENTS.md`, `CONTRIBUTING.md` | **パスだけ**渡す。「コミット前に `AGENTS.md` の Commits 節に従う」 |

親の意図メモに **規約ポインタ** を足す（全文は載せない）:

```yaml
conventions:
  agent: AGENTS.md
  commits: conventional commits; scope optional
  verify: npm run lint && npm test -- --related
```

## Cursor / エージェント側（短く保つ）

- **Project Rules**（`.cursor/rules`）や **`AGENTS.md`** にコミット形式・禁止事項を書く。Always Apply はトークンが重いので、**globs**（例: `**/*.{ts,tsx}`）や `apply when committing` 相当のスコープに絞る。
- **`.cursor/agents/pr-steward.md`**（任意）に 5〜10 行: 「`AGENTS.md` と `commitlint` に従う。検証は `npm run lint`」程度。スキル本文の複製はしない。
- **steward 用スキル**（`pr-steward`）は手順とルーブリックだけ。リポジトリ固有の型名や例外は **リポジトリの AGENTS.md** が正本。

## コミットメッセージ

1. 親が `conventions.commits` に一行（例: `type(scope): imperative subject`）。
2. steward は `git commit` を実行し、**commitlint / hook が落ちたら** エラーメッセージだけで直す（ルール全文を再掲しない）。
3. Tier A のまとめ push が複数コミットになる場合、**1 論点 1 コミット**はチームが要求するときだけ。さもなくば `fix: address lint on PR` のような単一コミットでもよい（commitlint が許す範囲）。

## コーディングスタイル

- **formatter / linter が正本**。steward は「スタイル判断」せずツールを回す。
- ツールが直せない指摘だけ triage-rubric で Tier B/C に回す。
- 巨大な `STYLE.md` を毎回読ませない。Explore サブエージェントに「`eslint` 設定の overrides を要約」と頼むのは **エスカレ後**でよい。

## handoff に載せるもの

`notes_for_parent` に、規約違反で止まったときだけ:

- どのゲートが落ちたか（`commitlint`, `eslint`, CI 名）
- ログの **最後の 20 行以内** または 1 行エラー

規約全文や長い diff は載せない。
