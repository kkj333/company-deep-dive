# company-deep-dive

Streamlitで有価証券報告書を分析する企業詳細分析レポートアプリです。

## 📊 機能

- **企業概要**: 基本情報と経営方針
- **財務分析**: 損益計算書、貸借対照表、キャッシュフロー計算書
- **経営指標**: ROE、ROA、営業利益率などの主要指標
- **事業セグメント**: セグメント別売上・利益の分析
- **リスク分析**: 有価証券報告書記載のリスク要因分析

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
├── app.py                          # Streamlitメインアプリケーション
├── pages/                          # マルチページアプリ
│   ├── 01_📊_企業概要.py
│   ├── 02_💰_財務分析.py
│   ├── 03_📈_経営指標.py
│   ├── 04_🏢_事業セグメント.py
│   └── 05_⚠️_リスク分析.py
├── utils/                          # ユーティリティモジュール
│   ├── __init__.py
│   ├── pdf_parser.py               # PDF解析
│   └── data_processor.py            # データ処理
├── scripts/                        # ユーティリティスクリプト
│   ├── extract_financials.py       # 財務データ抽出
│   └── extract_pl.py               # PL抽出
├── tests/                          # テストモジュール
│   ├── __init__.py
│   ├── test_pdf_parser.py
│   └── test_data_processor.py
├── data/                           # 抽出済みCSVデータ
│   ├── financial_summary.csv
│   ├── segment_data.csv
│   ├── consolidated_pl.csv
│   └── company_history.csv
├── documents/                      # 有価証券報告書置き場
│   └── カナレ電気有価証券報告書.pdf
├── .streamlit/
│   └── config.toml                 # Streamlit設定
├── .gitignore
├── pyproject.toml                  # uv依存関係設定
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

### 現在の実装状況

- [x] プロジェクト構成（フラット構造）
- [x] Streamlitアプリケーション基本設定
- [x] マルチページアプリのテンプレート
- [x] テスト構造とテストケース
- [x] PDFからのデータ抽出機能
  - [x] テキスト抽出
  - [x] 表抽出
  - [x] 企業情報抽出
- [x] 財務データのCSV化
  - [x] 財務サマリー
  - [x] セグメントデータ
  - [x] 連結損益計算書（PL）
  - [x] 企業沿革
- [x] 財務データの可視化
  - [x] 企業概要ページ
  - [x] 財務分析ページ
- [ ] 経営指標ページの詳細実装
- [ ] 事業セグメントページの詳細実装
- [ ] リスク分析ページの詳細実装

## 📝 ライセンス

MIT
