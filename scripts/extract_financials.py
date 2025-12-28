#!/usr/bin/env python3
"""
有価証券報告書からCSVデータを抽出するスクリプト

使用方法:
    uv run python scripts/extract_financials.py
"""

import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.pdf_parser import SecReportParser, list_pdf_files
from utils.data_processor import FinancialDataProcessor, HistoryExtractor


def main():
    """メイン処理"""
    print("📄 有価証券報告書からCSVを抽出します...\n")

    # PDFファイルを取得
    pdf_files = list_pdf_files()
    if not pdf_files:
        print("❌ PDFファイルが見つかりません")
        return

    # 出力ディレクトリ
    output_dir = Path(__file__).parent.parent / "data"

    for pdf_path in pdf_files:
        print(f"📋 処理中: {pdf_path.name}")
        try:
            # PDFから表とテキストを抽出
            parser = SecReportParser(pdf_path)
            tables = parser.extract_tables()
            text = parser.extract_text()
            print(f"   ✅ {len(tables)} 個の表を抽出")

            # 財務データをCSVにエクスポート
            saved_files = FinancialDataProcessor.extract_and_export_financials(
                tables, output_dir
            )

            for name, path in saved_files.items():
                print(f"   💾 保存: {path.name}")

            # 沿革を抽出
            print("   📜 沿革を抽出中...")
            history = HistoryExtractor.extract_history_from_text(text)
            if history:
                history_path = HistoryExtractor.export_history_to_csv(history, output_dir)
                print(f"   💾 保存: {history_path.name} ({len(history)}件)")
            else:
                print("   ⚠️  沿革データが見つかりませんでした")

            print()
        except Exception as e:
            print(f"   ❌ エラー: {e}\n")

    print("✅ 処理完了！")
    print(f"📁 出力場所: {output_dir}")


if __name__ == "__main__":
    main()
