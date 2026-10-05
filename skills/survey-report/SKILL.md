---
name: survey-report
description: 調査依頼を Phase 1（探索型）または Phase 2（検証・構造化型）に振り分け、前・中・後重心と読者レベルを選んでレポートを構成・出力する。地図と3つの問い、または結論と根拠の対応。Use when routing research requests and writing landscape or decision-oriented survey reports.
license: MIT
metadata:
  author: hskksk
  version: 1.0.0
---

# 調査レポート（Phase × 重心 × 読者レベル）

ユーザー依頼を分析し、**Phase 1: 探索型** か **Phase 2: 検証・構造化型** かを決め、さらに**重心**（前・中・後）と**読者レベル**（入門・実務・専門）を選んでレポートを書く。三つは独立した軸で、正本は `references/`。**執筆前に `survey-report-guide.md` §1 で Phase を判定し、`gravity.md` で重心と読者レベルを決めてから、該当する構造章を読む。**

## いつ使うか

- リサーチ・調査の依頼を受け、レポート形式でまとめる
- テーマの全体像・論点整理（探索）か、比較・仮説検証・意思決定向けの結論提示（検証）かを決める
- Phase 1 のあと、合意した問いで Phase 2 に進む

単なるリンク集・用語辞典だけの出力には使わない。

## 手順

1. **Phase を判定する。** `references/survey-report-guide.md` §1 のルーティングに従う。
   - 具体論点・仮説あり → Phase 2
   - 全体像・最新動向の把握 → Phase 1
   - 曖昧 → Phase 1（概要と末尾で Phase 2 用の問いを提示）
2. **重心と読者レベルを決める。** `references/gravity.md` の三つの質問で主重心を一つ選び、前提レベルを一つ選ぶ。書いた一文（重心・読者レベル）を作業メモに残し、**本文には出さない。**
3. **構成を書く。**
   - Phase 1 なら `survey-report-guide.md` §4 の既定案に従う（必須は**全体像**と**次に解くべき3つの問い**）。
   - Phase 2 なら `references/report-structure-guide.md` の「答えと根拠の対応」に従い、`survey-report-guide.md` §5 の見出しパターンで書く。
   - どちらもタイトル直後に3〜5項目の `## TL;DR` を置く。主張数・節数・図の有無は重心に合わせて固定しない。
4. **実務連携**は `survey-report-guide.md` §6 を参照（Phase 1 発行 → 問いの合意 → Phase 2）。
5. **提出前に** `references/checklists.md` の共通・Phase 別・重心別テストを行い、`references/measure.py` で数えられる指標を確認する。

## 参照ファイル

| ファイル | 内容 | いつ読むか |
| --- | --- | --- |
| `references/survey-report-guide.md` | Phase ルーティング、三つの軸、Phase 1/2 の構造と連携フロー | 最初 |
| `references/gravity.md` | 重心モデル（前・中・後）と読者レベルの決め方・見出し階層 | 執筆前と構成決定時 |
| `references/report-structure-guide.md` | Phase 2 の答えと根拠の層設計 | Phase 2 のとき |
| `references/checklists.md` | 共通・Phase 別・重心別の提出前テスト | 提出前 |
| `references/measure.py` | 数えられる共通指標の計測（TL;DR、`[n]`、出典、字数） | 提出前（任意） |
| `references/english.md` | 英語で書くときの文の作法 | 出力が英語のとき |

日本語で書くときは、リポジトリに `japanese-writing` スキルがあれば執筆前と推敲前に読み込み、その手順に従う。

## このスキルが扱わないこと

一次調査の実行手順（検索クエリ設計、API 呼び出し、インタビュー設計）や、特定組織の社内テンプレート・保存先・TTS/PR 手順は含めない。出力は Markdown レポートの構造と論旨の型に限定する。
