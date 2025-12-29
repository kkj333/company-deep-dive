#!/usr/bin/env python3
"""
連結貸借対照表（B/S）をCSVに抽出するスクリプト

使用方法:
    uv run python scripts/extract_bs.py
"""

import sys
import re
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.pdf_parser import list_pdf_files, SecReportParser


def extract_bs_data(text: str) -> pd.DataFrame:
    """
    テキストから連結貸借対照表を抽出してDataFrameに変換

    Args:
        text: PDFから抽出されたテキスト

    Returns:
        B/Sデータフレーム
    """
    lines = text.split("\n")

    # 連結貸借対照表のセクションを探す
    start_idx = None
    for i, line in enumerate(lines):
        if "【連結貸借対照表】" in line:
            start_idx = i
            break

    if start_idx is None:
        print("警告: 連結貸借対照表が見つかりません")
        return pd.DataFrame()

    # データを抽出
    bs_data = []

    # 終了条件：【連結損益計算書】または連結損益計算書が出現するまで
    end_idx = None
    for i in range(start_idx + 1, len(lines)):
        if "【連結損益計算書】" in lines[i] or (
            "連結損益計算書及び連結包括利益" in lines[i]
        ):
            end_idx = i
            break

    if end_idx is None:
        end_idx = min(start_idx + 300, len(lines))

    for i in range(start_idx + 1, end_idx):
        line = lines[i].strip()

        if not line or line.startswith("(") or line.startswith("-"):
            continue

        # セクションヘッダーは除外（単位、日付等）
        if any(
            x in line
            for x in ["単位：", "前連結会計年度", "当連結会計年度", "2023年", "2024年"]
        ):
            if "(" not in line:  # 日付除外
                continue

        # 項目と数値を抽出
        # より柔軟なパターン：「項目名 ※X 数値 ※X 数値」
        match = re.match(
            r"^(.+?)\s+(※\d+)?\s*([\d,△－]+)\s+(※\d+)?\s*([\d,△－]+)\s*$", line
        )

        if match:
            item = match.group(1).strip()
            val_2023 = match.group(3).strip() if match.group(3) else ""
            val_2024 = match.group(5).strip() if match.group(5) else ""

            # 不要な注記記号を削除
            item = re.sub(r"\s※\d+\s*", "", item).strip()

            if val_2023 and val_2024:
                bs_data.append(
                    {"科目": item, "2023年12月": val_2023, "2024年12月": val_2024}
                )

    return pd.DataFrame(bs_data)


def main():
    """メイン処理"""
    print("📊 連結貸借対照表（B/S）を抽出します...\n")

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

            # B/S抽出
            df_bs = extract_bs_data(text)

            if not df_bs.empty:
                bs_path = output_dir / "consolidated_bs.csv"
                df_bs.to_csv(bs_path, index=False, encoding="utf-8-sig")
                print(f"   ✅ 抽出完了: {len(df_bs)}行")
                print(f"   💾 保存: {bs_path.name}")
                print("\n📊 抽出されたデータ:")
                print(df_bs.head(20).to_string())
            else:
                print("   ⚠️  B/Sデータが見つかりませんでした")

        except Exception as e:
            print(f"   ❌ エラー: {e}\n")

    print("\n✅ 処理完了！")


if __name__ == "__main__":
    main()
