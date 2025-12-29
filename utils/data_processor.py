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
            # P/L items
            "売上原価", "販売費及び一般管理費",
            "受取利息", "受取配当金", "不動産賃貸料", "為替差益", "投資事業組合運用益", "固定資産売却益", "物品売却益",
            "支払利息", "売上債権売却損", "不動産賃貸原価", "投資事業組合運用損", "為替差損", "固定資産除却損",
            "投資有価証券売却益", "投資有価証券売却損",
            "法人税、住民税及び事業税", "過年度法人税等", "法人税等調整額",
            # B/S items
            "現金及び預金", "受取手形及び売掛金", "商品及び製品", "仕掛品", "原材料及び貯蔵品", "貸倒引当金",
            "建物及び構築物", "減価償却累計額", "建物及び構築物（純額）",
            "機械装置及び運搬具", "機械装置及び運搬具（純額）",
            "工具、器具及び備品", "工具、器具及び備品（純額）",
            "土地", "リース資産", "リース資産（純額）",
            "無形固定資産", "投資有価証券", "繰延税金資産",
            "買掛金", "未払金", "未払法人税等", "賞与引当金", "役員賞与引当金",
            "繰延税金負債", "役員退職慰労引当金", "退職給付に係る負債",
            "資本金", "資本剰余金", "利益剰余金", "自己株式",
            "その他有価証券評価差額金", "繰延ヘッジ損益", "土地再評価差額金", "為替換算調整勘定"
        ]

        def apply_style(item):
            item = item.strip()
            if item in indent_items:
                return f"　　{item}"  # 全角スペースでインデント
            return item

        df_formatted["科目"] = df_formatted["科目"].apply(apply_style)

        return df_formatted

    @staticmethod
    def calculate_financial_ratios(pl_data: pd.DataFrame, bs_data: pd.DataFrame) -> Dict[str, Any]:
        """
        財務比率を計算

        Args:
            pl_data: 損益計算書データ
            bs_data: 貸借対照表データ

        Returns:
            計算された財務比率の辞書
        """
        ratios = {}

        def get_pl_val(item, year="2024年12月"):
            row = pl_data[pl_data["科目"] == item]
            if not row.empty:
                return FinancialDataProcessor.clean_financial_value(row[year].values[0])
            return 0

        def get_bs_val(item, year="2024年12月"):
            row = bs_data[bs_data["科目"] == item]
            if not row.empty:
                return FinancialDataProcessor.clean_financial_value(row[year].values[0])
            return 0

        # 2024年の値を取得
        sales = get_pl_val("売上高")
        op_profit = get_pl_val("営業利益")
        net_income = get_pl_val("当期純利益")

        total_assets_2024 = get_bs_val("資産合計")
        total_assets_2023 = get_bs_val("資産合計", "2023年12月")
        net_assets_2024 = get_bs_val("純資産合計")
        net_assets_2023 = get_bs_val("純資産合計", "2023年12月")
        
        current_assets = get_bs_val("流動資産合計")
        current_liabilities = get_bs_val("流動負債合計")

        # 収益性指標
        if sales > 0:
            ratios["売上高営業利益率"] = (op_profit / sales) * 100
        
        avg_assets = (total_assets_2024 + total_assets_2023) / 2
        if avg_assets > 0:
            ratios["ROA（総資産利益率）"] = (net_income / avg_assets) * 100

        avg_net_assets = (net_assets_2024 + net_assets_2023) / 2
        if avg_net_assets > 0:
            ratios["ROE（自己資本利益率）"] = (net_income / avg_net_assets) * 100

        # 安全性指標
        if total_assets_2024 > 0:
            ratios["自己資本比率"] = (net_assets_2024 / total_assets_2024) * 100
        
        if current_liabilities > 0:
            ratios["流動比率"] = (current_assets / current_liabilities) * 100

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
    def extract_risk_factors(text: str) -> List[Dict[str, str]]:
        """
        テキストからリスク要因を抽出

        Args:
            text: 抽出されたテキスト

        Returns:
            リスク要因のリスト（タイトルと内容の辞書）
        """
        import re

        # 「【事業等のリスク】」セクションを探す
        risk_section_match = re.search(r"【事業等のリスク】(.*?)(?=【|\Z)", text, re.DOTALL)

        if not risk_section_match:
            return []

        section_text = risk_section_match.group(1)

        # 個別のリスク項目を抽出（括弧付き番号: (１)、(２)など）
        risk_items = []

        # リスク項目の検出パターン: (１)（括弧番号）で始まる行とそれに続く内容
        lines = section_text.split("\n")
        current_title = ""
        current_content = []

        for line in lines:
            # リスク項目のタイトル行を検出: (１)タイトルのような形式
            title_match = re.match(r"^\(\d+\)(.+)$", line)
            if title_match:
                # 前の項目を保存
                if current_title:
                    risk_items.append({
                        "title": current_title,
                        "content": "\n".join(current_content).strip()
                    })
                # 新しい項目を開始
                current_title = title_match.group(1).strip()
                current_content = []
            elif current_title and line.strip():
                # タイトルが設定されていて、空白でない行なら内容に追加
                current_content.append(line)

        # 最後の項目を追加
        if current_title:
            risk_items.append({
                "title": current_title,
                "content": "\n".join(current_content).strip()
            })

        return risk_items

    @staticmethod
    def categorize_risks(risks: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        リスクを分類

        Args:
            risks: リスク要因のリスト

        Returns:
            分類情報が追加されたリスクリスト
        """
        categories = {
            "経営リスク": ["経営", "戦略", "方針", "競合", "人材", "技術"],
            "市場リスク": ["市場", "需要", "景気", "価格", "為替", "金利"],
            "業務リスク": ["業務", "運営", "品質", "供給", "災害", "システム", "情報"],
            "財務リスク": ["財務", "資金", "借入", "格付"],
            "法令リスク": ["法令", "遵守", "規制", "訴訟", "知的財産", "環境"],
        }

        categorized_risks = []
        for risk in risks:
            title = risk["title"]
            content = risk["content"]
            found_category = "その他"

            # タイトルと内容からキーワードを探す
            for category, keywords in categories.items():
                if any(kw in title or kw in content for kw in keywords):
                    found_category = category
                    break
            
            categorized_risks.append({
                "category": found_category,
                "title": title,
                "content": content
            })

        return categorized_risks


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


class ManagementPolicyExtractor:
    """経営方針抽出クラス"""

    @staticmethod
    def extract_management_policy(text: str) -> List[Dict[str, str]]:
        """
        テキストから経営方針を抽出

        Args:
            text: PDFから抽出されたテキスト

        Returns:
            経営方針データのリスト
        """
        import re

        policies = []

        # 経営方針セクションを探す（複数のパターンに対応）
        policy_patterns = [
            r"【経営方針】(.*?)(?=【|第|参考|最後のページ|ページの終わり|\Z)",
            r"経営方針(.*?)(?=【|第|参考|最後のページ|ページの終わり|\Z)",
        ]

        policy_text = ""
        for pattern in policy_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                policy_text = match.group(1)
                break

        if not policy_text:
            return policies

        # 経営方針をセクションごとに分割
        # セクションは通常「１．」「２．」などの番号で区切られている
        sections = re.split(r"(?=\n\s*[０-９１-９]\s*[．、])", policy_text)

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # 見出しと内容を分割
            lines = section.split("\n", 1)
            if len(lines) >= 1:
                title = lines[0].strip()
                content = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

                # 見出しをクリーンアップ（番号を削除）
                title_cleaned = re.sub(r"^[０-９１-９\s．、]+", "", title).strip()

                if title_cleaned and content:
                    policies.append({
                        "タイトル": title_cleaned,
                        "内容": content
                    })

        return policies

    @staticmethod
    def extract_basic_policy_statement(text: str) -> str:
        """
        基本的な経営方針ステートメント（1段落）を抽出

        Args:
            text: PDFから抽出されたテキスト

        Returns:
            経営方針ステートメント
        """
        import re

        # 経営方針セクションを探す
        patterns = [
            r"【経営方針】\s*(.*?)(?=【|第|\Z)",
            r"経営方針\s*(.*?)(?=【|第|１\s*[．、]|\Z)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                policy_text = match.group(1).strip()
                # 最初の段落（改行で区切られた部分）を取得
                first_paragraph = policy_text.split("\n\n")[0].strip()
                if first_paragraph:
                    # 余分なスペースを削除
                    return re.sub(r"\s+", " ", first_paragraph)

        return ""

    @staticmethod
    def export_policy_to_csv(policies: List[Dict[str, str]], output_dir: Path) -> Path:
        """
        経営方針データをCSVにエクスポート

        Args:
            policies: 経営方針データのリスト
            output_dir: 出力ディレクトリ

        Returns:
            保存されたCSVファイルのパス
        """
        if not policies:
            return None

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        df_policy = pd.DataFrame(policies)
        policy_path = output_dir / "management_policy.csv"
        df_policy.to_csv(policy_path, index=False, encoding="utf-8-sig")

        return policy_path
