# 親エージェント（委譲側）

親は設計・実装の文脈を保持する。PR 番人は **コストの低い実行体**に任せる。

## 渡す成果物

steward 起動プロンプトに必ず含める:

1. **PR の特定子** — URL、番号、または `owner/repo#number`
2. **意図メモ** — 変更の目的、受け入れ条件、**触らないファイル／領域**
3. **親の残タスク** — steward がエスカレしたときに親がやるべきことの一行（例: 「API の破壊変更はこちらで判断」）
4. **権限の範囲** — 通常は「同一 PR ブランチへの commit & push 可」。マージ・rebase・force-push は不可

任意:

- 既知の flaky チェック名
- レビュアーが人間かボットかの区別方針（人間コメントは原則エスカレ）

## 起動方法（Cursor）

### サブエージェント（推奨: 同一セッション内）

親は **Task / サブエージェント** で steward を起動し、上記をプロンプトに載せる。

- モデルは親より軽いものを指定してよい（コスト分離）。
- steward 用の専用定義があるなら `.cursor/agents/pr-steward.md` にこのスキルの steward 手順を要約し、`/pr-steward` または名前で起動する。
- **foreground** で起動し、handoff JSON が返るまで親は同じ PR の修正をしない。

プロンプトに含める一文の例:

```text
You are the PR steward. Follow the pr-steward skill: subscribe to this PR, fix only Tier A issues per triage-rubric, escalate Tier B/C to the parent using handoff-format. Do not merge or force-push.
```

### Cloud Agent で親が PR を出した直後

親 run が PR を作成した場合、**別の full autopilot に丸投げしない**。代わりに:

- 同じ run 内でサブエージェント steward を起動する、または
- ユーザーが許すなら、軽量モデルの **別 Cloud run** を steward 専用に切る（親の会話 ID とは別。handoff は PR コメントや共有メモで親が読む）

親が subscribe まで自分でやる必要はない。subscribe は **steward の責務**。

## エスカレを受けたら

1. handoff の `escalations` を優先度順に読む。
2. `decision_context` だけで足りるものは親が修正。足りないときはユーザーに質問する。
3. steward を **再開**するか **停止**するかを決める。再開時は「前回の escalation ID を処理済みにした」旨を渡す。

## やってはいけないこと

- 親と steward が同時に同じ PR ブランチを編集する
- steward にアーキテクチャ判断を「とりあえず直して」と丸める
- `/autopilot` と steward を同一 PR で並行させる（役割が重複する）
