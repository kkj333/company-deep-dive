"""
リスク要因抽出スクリプト
有価証券報告書からリスク要因を抽出し、CSVとして保存
"""

import sys
from pathlib import Path
import pandas as pd

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from utils.pdf_parser import SecReportParser, list_pdf_files
from utils.data_processor import RiskAnalyzer

def main():
    # PDFファイルのリストを取得
    pdf_files = list_pdf_files()
    if not pdf_files:
        print("No PDF files found in documents directory.")
        return

    # 最新のPDFを使用
    pdf_path = pdf_files[0]
    print(f"Extracting risks from: {pdf_path.name}")

    try:
        # PDF解析
        parser = SecReportParser(pdf_path)
        text = parser.extract_text()

        # リスク抽出
        raw_risks = RiskAnalyzer.extract_risk_factors(text)
        categorized_risks = RiskAnalyzer.categorize_risks(raw_risks)

        if not categorized_risks:
            print("No risk factors found.")
            return

        # データフレームに変換して保存
        df = pd.DataFrame(categorized_risks)
        
        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)
        
        output_path = data_dir / "risk_factors.csv"
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        
        print(f"Successfully extracted {len(df)} risk factors to {output_path}")

    except Exception as e:
        print(f"Error during extraction: {e}")

if __name__ == "__main__":
    main()
