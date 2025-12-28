"""
データプロセッサーのテスト
"""

import pytest
import pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_processor import (
    FinancialDataProcessor,
    SegmentAnalyzer,
    RiskAnalyzer,
)


class TestFinancialDataProcessor:
    """FinancialDataProcessorのテストクラス"""

    @pytest.fixture
    def sample_dataframe(self):
        """サンプルデータフレームを作成"""
        return pd.DataFrame({
            "年度": ["2021", "2022", "2023"],
            "売上高": [1000, 1100, 1200],
            "営業利益": [100, 120, 140],
        })

    def test_prepare_visualization_data(self, sample_dataframe):
        """グラフ化用データ準備テスト"""
        result = FinancialDataProcessor.prepare_visualization_data(sample_dataframe)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_dataframe)
        # オリジナルは変更されていないことを確認
        assert sample_dataframe is not result

    def test_calculate_financial_ratios(self, sample_dataframe):
        """財務比率計算テスト"""
        ratios = FinancialDataProcessor.calculate_financial_ratios(
            sample_dataframe, sample_dataframe
        )
        assert isinstance(ratios, dict)

    def test_extract_key_figures(self, sample_dataframe):
        """主要数字抽出テスト"""
        figures = FinancialDataProcessor.extract_key_figures(sample_dataframe)
        assert isinstance(figures, dict)


class TestSegmentAnalyzer:
    """SegmentAnalyzerのテストクラス"""

    @pytest.fixture
    def sample_segment_data(self):
        """サンプルセグメントデータを作成"""
        return pd.DataFrame({
            "セグメント": ["電子部品", "情報・通信", "その他"],
            "売上高": [500, 400, 300],
            "営業利益": [50, 60, 30],
        })

    def test_analyze_segments(self, sample_segment_data):
        """セグメント分析テスト"""
        analysis = SegmentAnalyzer.analyze_segments(sample_segment_data)
        assert isinstance(analysis, dict)


class TestRiskAnalyzer:
    """RiskAnalyzerのテストクラス"""

    def test_extract_risk_factors(self):
        """リスク要因抽出テスト"""
        sample_text = """
        当社は経営リスク、市場リスク、業務リスクに直面しています。
        これらのリスク要因に対して適切な対応が必要です。
        """
        risks = RiskAnalyzer.extract_risk_factors(sample_text)
        assert isinstance(risks, list)

    def test_categorize_risks(self):
        """リスク分類テスト"""
        sample_risks = ["リスク1", "リスク2", "リスク3"]
        categorized = RiskAnalyzer.categorize_risks(sample_risks)
        assert isinstance(categorized, dict)
