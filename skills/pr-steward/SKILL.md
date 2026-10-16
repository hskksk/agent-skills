---
name: pr-steward
description: PR 作成後の監視と軽微な修正を安価なサブエージェントに任せ、lint・format・明確な CI 修正だけを自律処理し、設計判断やスコープ拡大が要る指摘は親エージェントへ構造化してエスカレする。Use when a parent agent has opened a PR and should delegate babysitting without burning the main context on trivial follow-ups.
license: MIT
metadata:
  author: hskksk
  version: 1.6.0
---



# PR steward（親へのエスカレ付き PR 番人）

親エージェントが実装と設計の文脈を保持し、**PR 上の瑣末なフォロー**（lint、format、自明な型エラー、ログに明示された単発修正など）だけを **steward**（サブエージェントまたは専用の軽い run）に任せるための手順。

`/autopilot` のように PR 全体を別 Cloud Agent に丸投げするのではなく、**subscribe または同等の待機**でイベントを受け、**自分で直せるものだけ直し**、それ以外は **親に戻す**。

## いつ使うか

- 親が PR を出したあと、CI 赤・ボット指摘・軽いレビューコメントの対応を続けたいが、親の会話に長いログや反復修正を載せたくない
- 「安いモデル／隔離されたコンテキスト」で PR を見張り、判断が要るときだけ親を起こしたい

使わない:

- PR を開く前の実装・設計そのもの（親の仕事）
- マージ、rebase、force-push、保護ブランチの承認操作
- 人間レビュアーへの返信やスレッド resolve を自動で行う依頼（steward は **親向けの整理**まで。公開コメントは親またはユーザーが決める）

## 役割

| 役割 | 誰 | 成果物 |
| --- | --- | --- |
| 親（caller） | メインのエージェント | PR URL、意図メモ、steward 起動、エスカレ受信後の判断 |
| steward | サブエージェントまたは軽量 Cloud run | 自律修正のコミット、ステータス報告、`escalations` 付き handoff |

親がこのスキルを読むときは `references/parent-delegation.md` から。steward が読むときは `references/steward-runtime.md` と `references/triage-rubric.md` から。

## 手順（概要）

### 親

1. PR を作成し、**意図メモ**（何を変えたか、触らない範囲、関連ファイル）を短く書く。
2. steward を起動する。渡すものと起動の書き方は `references/parent-delegation.md`。
3. **ワークスペースの取り合いを避ける。** PR ヘッドブランチの編集は steward の仕事。親は `references/workspace-isolation.md` の A/B/C のどれかを選ぶ（同じブランチ名でも、別 worktree や直列ならよい）。
4. リポジトリ規約は `references/repo-conventions.md` — 全文をプロンプトに貼らず、パスと検証コマンドだけ渡す。
5. steward から handoff が返るまで、選んだ隔離モードに反する編集を親がしない。
6. `escalations` を読み、設計・スコープ・曖昧な人間コメントを処理する。自律修正だけで緑になった場合はマージ判断をユーザーに委ねる。

### steward

1. 受け取った PR と意図メモを確認し、隔離モードに従って checkout する（共有 tree なら PR ヘッド、worktree／サブブランチは `workspace-isolation.md`）。
2. 規約は `repo-conventions.md` — 渡された検証コマンドと hook／CI を正とする。
3. **待機を張る。** Cloud Agent なら PR（と必要なら CI）への subscribe または `/subscribe` スキル。ツールが無い環境では `references/steward-runtime.md` のフォールバック。
4. イベントごとに `references/triage-rubric.md` で分類する。
   - **自律**: ルーブリックの Tier A — 最小 diff で修正、関連チェックを実行、コミット・push。
   - **エスカレ**: Tier B/C — コードは変えず（または調査のみ）、`references/handoff-format.md` の JSON を親向けに埋める。
4. 終了条件: PR が merged/closed、ユーザーが停止を指示、または親が引き継ぎ。停止前に最終 handoff を返す。

## 参照ファイル

| ファイル | 内容 | いつ読むか |
| --- | --- | --- |
| `references/parent-delegation.md` | 親が steward を起動する条件と渡す情報 | 親が PR 後に委譲する直前 |
| `references/steward-runtime.md` | subscribe、サブエージェント、フォールバック待機 | steward 起動直後 |
| `references/triage-rubric.md` | 自律修正 vs エスカレの判定 | 各 CI／レビューイベント |
| `references/handoff-format.md` | 親へ返す構造化レポート | エスカレ時とセッション終了時 |
| `references/workspace-isolation.md` | worktree・直列・サブブランチ | 委譲前に隔離モードを決めるとき |
| `references/repo-conventions.md` | 規約を機械とポインタで守る | 委譲時の `conventions` 一行 |

## 他スキルとの関係

このスキルは単体で完結する。複数スキルを束ねる境界の一般則は `skill-orchestration` が正本である。ここでは名前だけを参照し、相手の `references/` は開かない。
