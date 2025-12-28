#!/usr/bin/env python3
"""
連結損益計算書（PL）をCSVに抽出するスクリプト

使用方法:
    uv run python scripts/extract_pl.py
"""

import sys
import re
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.pdf_parser import list_pdf_files, SecReportParser


def extract_pl_data(text: str) -> pd.DataFrame:
    """
    テキストから連結損益計算書を抽出してDataFrameに変換

    Args:
        text: PDFから抽出されたテキスト

    Returns:
        PLデータフレーム
    """
    lines = text.split("\n")

    # 連結損益計算書のセクションを探す
    start_idx = None
    for i, line in enumerate(lines):
        if "【連結損益計算書】" in line:
            start_idx = i
            break

    if start_idx is None:
        return pd.DataFrame()

    # データを抽出
    pl_data = []
    current_section = None
    prev_2023 = None
    prev_2024 = None

    for i in range(start_idx + 1, min(start_idx + 100, len(lines))):
        line = lines[i].strip()

        if not line:
            continue

        # 計算書の終了判定
        if "【連結包括利益" in line or "当期純利益" in line and "法人税" in line:
            break

        # 項目と数値を抽出
        # パターン：「項目名 ※X XXXX XXXX」
        match = re.match(r"^([^※\d\-]+)(?:\s※\d+)?\s+([\d,△－]+)\s+(※\d+)?\s*([\d,△－]+)$", line)

        if match:
            item = match.group(1).strip()
            val_2023 = match.group(2).strip()
            val_2024 = match.group(4).strip()

            pl_data.append({
                "科目": item,
                "2023年12月": val_2023,
                "2024年12月": val_2024
            })

    return pd.DataFrame(pl_data)


def main():
    """メイン処理"""
    print("📊 連結損益計算書（PL）を抽出します...\n")

    pdf_files = list_pdf_files()
    if not pdf_files:
        print("❌ PDFファイルが見つかりません")
        return

    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in pdf_files:
        print(f"📋 処理中: {pdf_path.name}")
        try:
            parser = SecReportParser(pdf_path)
            text = parser.extract_text()

            # PL抽出
            df_pl = extract_pl_data(text)

            if not df_pl.empty:
                pl_path = output_dir / "consolidated_pl.csv"
                df_pl.to_csv(pl_path, index=False, encoding="utf-8-sig")
                print(f"   ✅ 抽出完了: {len(df_pl)}行")
                print(f"   💾 保存: {pl_path.name}")
                print("\n📊 抽出されたデータ:")
                print(df_pl.head(15).to_string())
            else:
                print("   ⚠️  PLデータが見つかりませんでした")

        except Exception as e:
            print(f"   ❌ エラー: {e}\n")

    print("\n✅ 処理完了！")


if __name__ == "__main__":
    main()
