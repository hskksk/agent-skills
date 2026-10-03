---
name: survey-report
description: 調査依頼を Phase 1（探索型）または Phase 2（検証・構造化型）に振り分け、該当するレポート構成で出力する。地図と3つの問い、または結論と根拠の三層構造。Use when routing research requests or writing landscape or decision-oriented survey reports.
license: MIT
metadata:
  author: hskksk
  version: 1.0.0
---

# 調査レポート（2段階モデル）

ユーザー依頼を分析し、**Phase 1: 探索型** か **Phase 2: 検証・構造化型** のどちらでレポートを書くか決め、定義済みの見出し・成果物で出力する。正本は `references/`。**執筆前にルーティング（`survey-report-guide.md` §1）を適用し、選んだ型の構造章（§3 または §4）と、Phase 2 では `report-structure-guide.md` を読む。**

## いつ使うか

- リサーチ・調査の依頼を受け、レポート形式でまとめる
- テーマの全体像・論点整理（探索）か、比較・仮説検証・意思決定向けの結論提示（検証）かを決める
- Phase 1 のあと、合意した問いで Phase 2 に進む

単なるリンク集・用語辞典だけの出力には使わない。

## 手順

1. **依頼文を読み、`references/survey-report-guide.md` の §1 でレポート型を判定する。**
   - 具体論点・仮説あり → Phase 2
   - 全体像・最新動向の把握 → Phase 1
   - 曖昧 → Phase 1（概要と末尾で Phase 2 用の問いを提示）
2. **Phase 1 なら** `survey-report-guide.md` §3 の構成要素どおりに書く（L1 概要に**検証すべき3つの問い**、全体像は Mermaid、対立軸で L2 を組む）。
3. **Phase 2 なら** `references/report-structure-guide.md` の三層構造に厳格に従い、`survey-report-guide.md` §4 の見出しパターン（主張型見出し）で書く。
4. **実務連携**は `survey-report-guide.md` §5 を参照（Phase 1 発行 → 問いの合意 → Phase 2）。

## 参照ファイル

| ファイル | 内容 |
| --- | --- |
| `references/survey-report-guide.md` | ルーティング、Phase 1/2 の比較、各型の章立て、連携フロー |
| `references/report-structure-guide.md` | Phase 2 の L1/L2/L3（概要・本文・付録）と論理図の要件 |

## このスキルが扱わないこと

一次調査の実行手順（検索クエリ設計、API 呼び出し、インタビュー設計）や、特定組織の社内テンプレートの版管理は含めない。出力は Markdown レポートの構造と論旨の型に限定する。
