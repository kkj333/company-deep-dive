# company-deep-dive

Streamlitで有価証券報告書を分析する企業詳細分析レポートアプリです。

## 📊 機能

- **企業概要**: 基本情報、経営成績（5年推移）、企業沿革
- **財務分析**: 損益計算書、貸借対照表、キャッシュフロー計算書の詳細分析
- **経営指標**: ROE、ROA、営業利益率、自己資本比率、EPS（5年推移）
- **事業セグメント**: 売上・利益・キャッシュフロー推移の可視化
- **リスク分析**: 有価証券報告書記載のリスク要因をカテゴリ分類
- **企業価値評価**: 清算価値とDCF法による企業価値の多面的評価

## 🚀 セットアップ

### 必要な環境
- Python 3.11以上
- uv（Pythonパッケージマネージャー）

### インストール

```bash
# 依存関係をインストール
uv sync

# Streamlitアプリを実行
uv run streamlit run app.py
```

## ☁️ Streamlit Cloud へのデプロイ

1. GitHubリポジトリにプッシュ
2. [Streamlit Cloud](https://streamlit.io/cloud) にアクセス
3. 「New app」をクリック
4. リポジトリを選択
5. **Main file path** に `app.py` を指定
6. 「Deploy」をクリック

依存関係は `pyproject.toml` から自動的に読み込まれます。

## 📁 プロジェクト構成

```
company-deep-dive/
├── app.py                              # Streamlitメインアプリケーション
├── pages/                              # マルチページアプリ（全6ページ）
│   ├── 01_📊_企業概要.py               # 企業基本情報・経営成績・沿革
│   ├── 02_💰_財務分析.py               # P/L・B/S・C/F詳細分析
│   ├── 03_📈_経営指標.py               # 経営指標5年推移
│   ├── 04_🏢_事業セグメント.py          # セグメント分析
│   ├── 05_⚠️_リスク分析.py             # リスク要因分析
│   └── 06_💎_企業価値.py               # 企業価値評価（NEW）
├── utils/                              # ユーティリティモジュール
│   ├── __init__.py
│   ├── pdf_parser.py                   # PDF解析・テーブル抽出
│   └── data_processor.py                # データ処理・財務計算
├── scripts/                            # データ抽出スクリプト
│   ├── extract_financials.py           # 財務サマリー抽出
│   ├── extract_pl.py                   # 損益計算書抽出
│   ├── extract_bs.py                   # 貸借対照表抽出
│   ├── extract_cf.py                   # キャッシュフロー抽出
│   ├── extract_risks.py                # リスク要因抽出
│   └── extract_management_policy.py    # 経営方針抽出（NEW）
├── tests/                              # テストモジュール
│   ├── __init__.py
│   ├── test_pdf_parser.py
│   └── test_data_processor.py
├── data/                               # 抽出済みCSVデータ
│   ├── financial_summary.csv           # 5年間の経営指標
│   ├── segment_data.csv                # セグメント別データ
│   ├── consolidated_pl.csv             # 損益計算書
│   ├── consolidated_bs.csv             # 貸借対照表
│   ├── consolidated_cf.csv             # キャッシュフロー計算書
│   ├── company_history.csv             # 企業沿革
│   ├── risk_factors.csv                # リスク要因
│   └── management_policy.csv           # 経営方針（NEW）
├── documents/                          # 有価証券報告書置き場
│   └── カナレ電気有価証券報告書.pdf
├── .streamlit/
│   └── config.toml                     # Streamlit設定
├── .gitignore
├── pyproject.toml                      # uv依存関係設定
└── README.md
```

## 🧪 テスト

開発用依存関係をインストール：
```bash
uv sync --extra dev
```

### テストの実行

すべてのテストを実行：
```bash
uv run pytest
```

カバレッジ付きでテストを実行：
```bash
uv run pytest --cov
```

HTMLレポートを生成：
```bash
uv run pytest --cov --cov-report=html
```

### コード品質チェック

コードをフォーマット（Ruff）：
```bash
uv run ruff format .
```

リント（Ruff）：
```bash
uv run ruff check .
```

型チェック（mypy）：
```bash
uv run mypy .
```

全部まとめて実行：
```bash
uv run ruff format . && uv run ruff check . && uv run mypy .
```

## 🛠️ 開発

### 実装完了項目

- [x] プロジェクト構成（フラット構造）
- [x] Streamlitアプリケーション基本設定
- [x] マルチページアプリ（全6ページ）
- [x] テスト構造とテストケース
- [x] PDFからのデータ抽出機能
  - [x] テキスト抽出
  - [x] テーブル抽出
  - [x] 企業情報抽出
  - [x] リスク要因抽出
  - [x] 経営方針抽出（将来用）
- [x] 財務データのCSV化
  - [x] 財務サマリー
  - [x] セグメントデータ
  - [x] 連結損益計算書（PL）
  - [x] 貸借対照表（B/S）
  - [x] キャッシュフロー計算書（C/F）
  - [x] 企業沿革
  - [x] リスク要因
- [x] 分析ページの実装
  - [x] 企業概要（基本情報・経営成績・沿革）
  - [x] 財務分析（P/L・B/S・C/F）
  - [x] 経営指標（5年推移）
  - [x] 事業セグメント（売上・利益・CF推移）
  - [x] リスク分析（カテゴリ分類）
  - [x] 企業価値評価（清算価値・DCF法）
- [x] 対話的なグラフ表示（Plotly）
  - [x] 2軸グラフ
  - [x] 折れ線グラフ
  - [x] 棒グラフ
  - [x] 円グラフ

## 📝 ライセンス

MIT
