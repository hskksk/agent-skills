# 親向け handoff（構造化レポート）

steward は親への返答を **1 つの JSON オブジェクト**（前後に短い要約文を付けてもよい）として返す。親はこれをパースし、`escalations` だけを実装タスクに変換する。

## スキーマ

```json
{
  "schema": "pr-steward-handoff/v1",
  "pr": "https://github.com/org/repo/pull/123",
  "branch": "feature/example",
  "state": "open",
  "checks_summary": {
    "pending": ["integration"],
    "failed": [],
    "passed": ["lint", "unit"]
  },
  "autonomous_fixes": [
    {
      "id": "fix-001",
      "tier": "A",
      "summary": "Applied eslint --fix on src/foo.ts",
      "commit": "abc1234"
    }
  ],
  "escalations": [
    {
      "id": "esc-001",
      "tier": "C",
      "source": "review-comment",
      "author": "human-reviewer",
      "link": "https://github.com/org/repo/pull/123#discussion_r123",
      "summary": "Questions choice of caching layer",
      "decision_context": {
        "question": "Should we use Redis or in-process cache for session tokens?",
        "options_seen": ["Redis", "in-memory"],
        "impact": "Affects deployment and auth latency",
        "recommendation": null
      },
      "blocked": true
    }
  ],
  "steward_status": "waiting",
  "notes_for_parent": "Subscribe still active; do not start parallel edits on this branch."
}
```

## フィールド

| フィールド | 必須 | 説明 |
| --- | --- | --- |
| `schema` | yes | 常に `pr-steward-handoff/v1` |
| `pr` | yes | PR URL |
| `branch` | yes | ヘッドブランチ名 |
| `state` | yes | `open` / `merged` / `closed` |
| `checks_summary` | yes | チェック名の配列。詳細ログは載せない |
| `autonomous_fixes` | yes | Tier A で push したもの。無ければ `[]` |
| `escalations` | yes | Tier B/C。無ければ `[]` |
| `steward_status` | yes | `waiting`（subscribe 継続）/ `idle`（緑・未エスカレ）/ `stopped` / `error` |
| `notes_for_parent` | no | 親への一行注意 |

### `escalations[]`

| フィールド | 必須 | 説明 |
| --- | --- | --- |
| `id` | yes | 安定 ID（再開時に参照） |
| `tier` | yes | `B` または `C` |
| `source` | yes | `ci` / `review-comment` / `review-body` / `bot` / `policy` / `infra` |
| `summary` | yes | 一行 |
| `decision_context` | B/C で推奨 | 親が判断するための質問・選択肢・影響 |
| `link` | あるとき | コメントや run への URL |
| `blocked` | yes | 親の判断までマージすべきでないなら `true` |

`recommendation` は steward が **確信がある Tier B** だけ埋める。C では `null` にする。

## 更新のタイミング

- Tier B/C が 1 件でも出たら **そのイベントの終わりに** handoff を返す（foreground steward）
- subscribe 継続中でも、親が読めるよう **エスカレ追加時は都度返す**
- セッション終了時は最終スナップショットを返す

## 親が再開するとき

再開プロンプトに含める:

- 前回 handoff の `escalations[].id` のうち処理したもの
- 更新された意図メモ（あれば）

steward は処理済み ID をスキップする。
