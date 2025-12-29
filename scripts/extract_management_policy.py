"""
経営方針抽出スクリプト
有価証券報告書から経営方針を抽出し、CSVとして保存
"""

import sys
from pathlib import Path
import pandas as pd

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from utils.pdf_parser import SecReportParser, list_pdf_files
from utils.data_processor import ManagementPolicyExtractor

def main():
    # PDFファイルのリストを取得
    pdf_files = list_pdf_files()
    if not pdf_files:
        print("No PDF files found in documents directory.")
        return

    # 最新のPDFを使用
    pdf_path = pdf_files[0]
    print(f"Extracting management policy from: {pdf_path.name}")

    try:
        # PDF解析
        parser = SecReportParser(pdf_path)
        text = parser.extract_text()

        # 経営方針抽出
        policies = ManagementPolicyExtractor.extract_management_policy(text)

        if not policies:
            # セクション形式が見つからない場合は、単一の方針ステートメントを抽出
            policy_statement = ManagementPolicyExtractor.extract_basic_policy_statement(text)
            if policy_statement:
                policies = [{
                    "タイトル": "経営方針",
                    "内容": policy_statement
                }]

        if not policies:
            print("No management policy found.")
            return

        # データフレームに変換して保存
        df = pd.DataFrame(policies)

        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)

        output_path = data_dir / "management_policy.csv"
        df.to_csv(output_path, index=False, encoding="utf-8-sig")

        print(f"Successfully extracted {len(df)} management policy items to {output_path}")

    except Exception as e:
        print(f"Error during extraction: {e}")

if __name__ == "__main__":
    main()
