import pandas as pd
from pathlib import Path
import sys

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_processor import FinancialDataProcessor

def verify():
    pl_csv = Path(__file__).parent.parent / "data" / "consolidated_pl.csv"
    if not pl_csv.exists():
        print(f"File not found: {pl_csv}")
        return

    df = pd.read_csv(pl_csv)
    print("--- Original Data (First 10 rows) ---")
    print(df.head(10))

    df_formatted = FinancialDataProcessor.format_financial_dataframe(df)
    print("\n--- Formatted Data (First 10 rows) ---")
    print(df_formatted.head(10))

    # Check for negative values (△)
    tax_adjustment = df[df["科目"] == "法人税等調整額"]
    if not tax_adjustment.empty:
        orig_val = tax_adjustment["2024年12月"].values[0]
        clean_val = FinancialDataProcessor.clean_financial_value(orig_val)
        print(f"\n--- Negative Value Check ---")
        print(f"Original: {orig_val}")
        print(f"Cleaned: {clean_val}")

    # Check for indentation
    sales_cost = df_formatted[df_formatted["科目"].str.contains("売上原価")]
    if not sales_cost.empty:
        print(f"\n--- Indentation Check ---")
        print(f"Formatted Item: '{sales_cost['科目'].values[0]}'")

if __name__ == "__main__":
    verify()
