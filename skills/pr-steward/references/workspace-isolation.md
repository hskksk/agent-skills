# ワークスペース隔離（ブランチとディレクトリ）

PR 対応では **PR のヘッドブランチを編集する**のが正しい。禁止したいのは「同じブランチを触れない」ことではなく、**同じ checkout（作業ディレクトリ）を親と steward が同時に編集する**ことである。

## 何が競合するか

| 共有するもの | 同時編集 | 典型な結果 |
| --- | --- | --- |
| 同じ working tree（未コミット含む） | 親と steward が並行 | 上書き、中途半端な merge、lint が別バージョンを見る |
| 同じブランチ名・別 working tree | 通常は安全 | PR 向けの push は steward 側から行える |
| 別ブランチ → 後で PR ブランチへ統合 | 親が feature 継続中でも可 | 統合ステップが 1 回増える |

Cursor のサブエージェントは **デフォルトで親と同じ checkout を共有**する。並列編集は上書きしうる（[Subagents — Isolated project copies](https://cursor.com/docs/subagents)）。

## 推奨パターン

### A. 直列（シンプル）

- steward は **foreground**。
- 親は steward 稼働中 **その PR ブランチのファイルを編集しない**（別タスク・別ブランチなら可）。
- steward は **PR ヘッドブランチ**で commit & push。

コンテキスト消費は少ない。親が同じ feature を触り続けたいときは B か C。

### B. 隔離 worktree（同じブランチ名）

- steward 起動時に **own environment / isolated copy / git worktree** を明示する。
- worktree でも **チェックアウトするのは PR のヘッドブランチ**（例: `feature/foo`）。ブランチ名は PR と同じでよい。
- 親は元の working tree で別ブランチやドキュメントを触ってよい。steward は別ディレクトリで PR ブランチのみ編集。

プロンプト例:

```text
Run the PR steward in its own isolated worktree on the PR head branch <branch>. Do not edit files in the parent's working tree.
```

### C. サブブランチ（親が同じ feature を触り続ける）

親が **まだ同じ feature ブランチ**で未 push の作業をしているとき:

1. steward は `feature/foo--steward` など **子ブランチ**を worktree 上で切る（ベースは PR の最新コミット）。
2. Tier A 修正を子ブランチに commit & push。
3. **PR のヘッドを更新する**方法はリポジトリ流儀に合わせる:
   - PR ブランチに **merge commit** または **rebase して fast-forward push**（force-push 禁止なら merge 推奨）
   - または子ブランチを PR に **追加コミットとして push し PR base を変えない**（PR が子ブランチを向いている場合は不可 — 通常は PR ヘッド＝`feature/foo` に統合）

force-push が禁止なら、steward は **PR ヘッドへの通常 push（merge）** だけにする。rebase 必須のチームでは steward を **foreground + 親は触らない（A）** に寄せる。

## 親が書く一文

意図メモに **隔離モード**を一行で書く:

- `isolation: serial` — 親は PR ブランチを触らない
- `isolation: worktree, branch: <pr-head>` — 同ブランチ・別ディレクトリ
- `isolation: sub-branch, integrate: merge-to-<pr-head>` — 子ブランチで直して PR ヘッドへ統合

## Cloud steward

Cloud subagent / 別 Cloud run は **別 VM + clone** がデフォルト。PR ヘッドブランチを checkout して push すればよく、ローカル親とのファイル競合は起きない。
