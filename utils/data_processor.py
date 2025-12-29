"""
データ処理モジュール
抽出したデータを処理・加工するためのユーティリティ
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Any


class FinancialDataProcessor:
    """財務データ処理クラス"""

    @staticmethod
    def clean_financial_value(val: Any) -> float:
        """
        財務数値をクリーンアップしてfloatに変換
        「△1,234」-> -1234.0
        「1,234」 -> 1234.0
        「－」 -> 0.0
        """
        if pd.isna(val) or val == "－" or val == "-":
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)

        s_val = str(val).replace(",", "").strip()
        if s_val.startswith("△"):
            return -float(s_val[1:])
        try:
            return float(s_val)
        except ValueError:
            return 0.0

    @staticmethod
    def format_financial_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        財務データフレームをクリーンアップし、階層構造のためのインデントを追加
        """
        df_formatted = df.copy()

        # 数値列をクリーンアップ
        for col in df_formatted.columns:
            if col != "科目":
                df_formatted[col] = df_formatted[col].apply(FinancialDataProcessor.clean_financial_value)

        # 科目名にインデントを追加するルール
        indent_items = [
            "売上原価", "販売費及び一般管理費",
            "受取利息", "受取配当金", "不動産賃貸料", "為替差益", "投資事業組合運用益", "固定資産売却益", "物品売却益",
            "支払利息", "売上債権売却損", "不動産賃貸原価", "投資事業組合運用損", "為替差損", "固定資産除却損",
            "投資有価証券売却益", "投資有価証券売却損",
            "法人税、住民税及び事業税", "過年度法人税等", "法人税等調整額"
        ]

        def apply_style(item):
            item = item.strip()
            if item in indent_items:
                return f"　　{item}"  # 全角スペースでインデント
            return item

        df_formatted["科目"] = df_formatted["科目"].apply(apply_style)

        return df_formatted

    @staticmethod
    def calculate_financial_ratios(pl_data: pd.DataFrame, bs_data: pd.DataFrame) -> Dict[str, float]:
        """
        財務比率を計算

        Args:
            pl_data: 損益計算書データ
            bs_data: 貸借対照表データ

        Returns:
            計算された財務比率
        """
        ratios = {}
        # TODO: 実装予定
        return ratios

    @staticmethod
    def extract_key_figures(data: pd.DataFrame) -> Dict[str, Any]:
        """
        主要数字を抽出

        Args:
            data: 財務データ

        Returns:
            抽出された主要数字
        """
        figures = {}
        # TODO: 実装予定
        return figures

    @staticmethod
    def prepare_visualization_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        グラフ化用にデータを準備

        Args:
            df: 処理対象のデータフレーム

        Returns:
            処理済みデータフレーム
        """
        return df.copy()

    @staticmethod
    def extract_and_export_financials(tables: List[pd.DataFrame], output_dir: Path) -> Dict[str, Path]:
        """
        表から財務データを抽出してCSVエクスポート

        Args:
            tables: 抽出された表のリスト
            output_dir: 出力ディレクトリ

        Returns:
            保存されたCSVファイルのパス辞書
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        saved_files = {}

        # 最初の数個の表から財務データを抽出（通常は表1が主要指標）
        if len(tables) > 0:
            # 主要指標データ（通常は最初の表）
            df_financial = tables[0].copy()
            financial_path = output_dir / "financial_summary.csv"
            df_financial.to_csv(financial_path, index=False, encoding="utf-8-sig")
            saved_files["financial_summary"] = financial_path

        # その他の表も保存
        if len(tables) > 1:
            df_segment = tables[1].copy()
            segment_path = output_dir / "segment_data.csv"
            df_segment.to_csv(segment_path, index=False, encoding="utf-8-sig")
            saved_files["segment_data"] = segment_path

        return saved_files


class SegmentAnalyzer:
    """事業セグメント分析クラス"""

    @staticmethod
    def analyze_segments(segment_data: pd.DataFrame) -> Dict[str, Any]:
        """
        事業セグメントを分析

        Args:
            segment_data: セグメントデータ

        Returns:
            分析結果
        """
        analysis = {}
        # TODO: 実装予定
        return analysis


class RiskAnalyzer:
    """リスク分析クラス"""

    @staticmethod
    def extract_risk_factors(text: str) -> List[str]:
        """
        テキストからリスク要因を抽出

        Args:
            text: 抽出されたテキスト

        Returns:
            リスク要因のリスト
        """
        risks = []
        # TODO: 実装予定
        return risks

    @staticmethod
    def categorize_risks(risks: List[str]) -> Dict[str, List[str]]:
        """
        リスクを分類

        Args:
            risks: リスク要因のリスト

        Returns:
            分類されたリスク
        """
        categorized = {}
        # TODO: 実装予定
        return categorized


class HistoryExtractor:
    """企業沿革抽出クラス"""

    @staticmethod
    def extract_history_from_text(text: str) -> List[Dict[str, str]]:
        """
        テキストから企業沿革を抽出

        Args:
            text: PDFから抽出されたテキスト

        Returns:
            沿革データのリスト（年、月、事項）
        """
        history = []
        lines = text.split("\n")

        # 沿革セクションのヘッダー「年月 沿革」を探す
        history_start = -1
        for i, line in enumerate(lines):
            if "年月" in line and "沿革" in line:
                history_start = i + 1
                break

        if history_start == -1:
            return history

        # 沿革セクションから事項を抽出
        current_entry = None
        for j in range(history_start, len(lines)):
            line_text = lines[j].strip()

            # 空行はスキップ
            if not line_text:
                continue

            # セクション終了条件
            if any(x in line_text for x in ["第１", "第２", "第３", "関係会社", "従業員"]):
                if line_text.startswith(("第", "関", "従")):
                    break

            # 年月で始まる行
            if any(str(year) in line_text for year in range(1970, 2030)) and "年" in line_text:
                # 前のエントリを保存
                if current_entry:
                    history.append({"事項": current_entry})
                current_entry = line_text
            elif current_entry:
                # 前行の続きをスペースで統合
                current_entry += " " + line_text

        # 最後のエントリを保存
        if current_entry:
            history.append({"事項": current_entry})

        return history

    @staticmethod
    def export_history_to_csv(history: List[Dict[str, str]], output_dir: Path) -> Path:
        """
        沿革データをCSVにエクスポート

        Args:
            history: 沿革データのリスト
            output_dir: 出力ディレクトリ

        Returns:
            保存されたCSVファイルのパス
        """
        if not history:
            return None

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        df_history = pd.DataFrame(history)
        history_path = output_dir / "company_history.csv"
        df_history.to_csv(history_path, index=False, encoding="utf-8-sig")

        return history_path
