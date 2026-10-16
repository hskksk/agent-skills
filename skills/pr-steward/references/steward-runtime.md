# steward の実行環境と待機

steward は **イベント駆動**で動く。ポーリングだけに頼るのは最後の手段。

## 1. Cloud Agent（ユーザー所有 run）

利用可能なら、PR 作成後（または起動直後）に **PR 活動への subscribe** を張る。

- プロンプトで「この PR を subscribe し、CI・レビュー・push イベントで再開」と書く
- 組み込みの `/subscribe` スキルで同じルーティングをしてよい
- subscribe した **のは steward の run／サブエージェント**である。親は待機しない

自動 subscribe（自分が作った PR に CI autofix が付く環境）がある場合でも、**設計エスカレのルーブリック**はこのスキルに従う。CI だけ直してスコープ拡大の指摘を黙って直さない。

## 2. サブエージェント（エディタ / CLI / Cloud 内）

親から隔離されたコンテキストで動く。

- 履歴は無い。親が渡した PR・意図メモ・ブランチ名が全部
- 長い CI ログは steward 内に閉じ、親には handoff の要約だけ返す
- **background** は `worktree` / `sub-branch` 隔離があるときだけ推奨。共有 checkout では foreground か直列（`workspace-isolation.md`）

モデルは軽量を推奨。探索が要るエスカレは Tier C として親へ返し、steward で深掘りしない。

## 3. subscribe が使えない環境

次のいずれか。いずれも **ルーブリックと handoff 形式は同じ**。

| 状況 | フォールバック |
| --- | --- |
| Automation が service account 実行 | イベントごとに Automation が新規 run になる設計にし、各 run で「未処理の CI／コメントだけ」を 1 パス処理して handoff を PR コメント（下書き）や親への返信に残す |
| ローカルで subscribe ツールなし | `gh pr view` / `gh run list` で状態を取り、ユーザーまたは親が「もう一度 steward を起動」と依頼するまで待つ。自動ループでポーリングする場合は指数バックオフし、レート制限を守る |
| GitHub MCP の `subscribe_pr_activity` がある | そのツールで PR を購読し、イベントで同じ steward 手順を実行 |

フォールバック時も **Tier A だけ直す**。曖昧ならエスカレを溜めて親起動時にまとめて返す。

## 4. 作業ループ（1 イベントあたり）

1. PR の mergeable 状態、チェック一覧、未解決のレビュー指摘を取得する（`gh` またはホストの PR API）。
2. 前回処理済みの finding ID をメモし、重複対応しない。
3. `triage-rubric.md` で各 finding を分類。
4. Tier A: 修正 → ローカルで関連コマンド（lint / test のスコープ内）→ commit → push。
5. Tier B/C: `handoff-format.md` に追記。push はしない（調査コミットが必要なら Tier B の条件を満たす場合のみ）。
6. 人間レビュアーのコメントには **返信しない**。`escalations` に要約する。

## 5. 終了

次のいずれかで steward を終える:

- `state` が `merged` または `closed`
- 親またはユーザーが停止指示
- すべてのチェックが成功し、未処理の Tier B/C が無く、親が「引き上げ不要」と指示

終了時は **最終 handoff**（空の `escalations` でも可）を親に返す。
