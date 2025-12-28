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
uv run streamlit run streamlit_app.py
```

**注意:** Streamlit Cloud でのデプロイでは、自動的に `streamlit_app.py` が認識されます。

## ☁️ Streamlit Cloud へのデプロイ

1. GitHubリポジトリにプッシュ
2. [Streamlit Cloud](https://streamlit.io/cloud) にアクセス
3. 「New app」をクリック
4. リポジトリを選択
5. **Main file path** は自動的に `streamlit_app.py` が選択される
6. 「Deploy」をクリック

依存関係は `pyproject.toml` から自動的に読み込まれます。

## 📁 プロジェクト構成

```
company-deep-dive/
├── streamlit_app.py                # Streamlit Cloud用エントリーポイント
├── src/
│   └── company_deep_dive/          # メインパッケージ
│       ├── __init__.py
│       ├── app.py                  # メインアプリケーション
│       ├── pages/                  # マルチページアプリ
│       │   ├── 01_📊_企業概要.py
│       │   ├── 02_💰_財務分析.py
│       │   ├── 03_📈_経営指標.py
│       │   ├── 04_🏢_事業セグメント.py
│       │   └── 05_⚠️_リスク分析.py
│       └── utils/                  # ユーティリティモジュール
│           ├── __init__.py
│           ├── pdf_parser.py      # PDF解析
│           └── data_processor.py   # データ処理
├── tests/                          # テストモジュール
│   ├── __init__.py
│   ├── test_pdf_parser.py
│   └── test_data_processor.py
├── .streamlit/
│   └── config.toml                 # Streamlit設定
├── documents/                      # 有価証券報告書置き場
│   └── カナレ電気有価証券報告書.pdf
├── pyproject.toml                  # uv設定
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
uv run mypy src/
```

全部まとめて実行：
```bash
uv run ruff format . && uv run ruff check . && uv run mypy src/
```

## 🛠️ 開発

### 現在の実装状況

- [x] プロジェクト構成
- [x] Streamlitアプリケーション基本設定
- [x] マルチページアプリのテンプレート
- [x] テスト構造とテストケース
- [ ] PDFからのデータ抽出機能
- [ ] 財務データの可視化
- [ ] 各ページの詳細実装

## 📝 ライセンス

MIT
