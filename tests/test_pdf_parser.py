"""
PDF パーサーのテスト
"""

import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.pdf_parser import SecReportParser, get_documents_dir, list_pdf_files


class TestSecReportParser:
    """SecReportParserのテストクラス"""

    def test_get_documents_dir(self):
        """ドキュメントディレクトリの取得テスト"""
        docs_dir = get_documents_dir()
        assert docs_dir.exists()
        assert docs_dir.is_dir()

    def test_list_pdf_files(self):
        """PDFファイルのリスト取得テスト"""
        pdf_files = list_pdf_files()
        assert isinstance(pdf_files, list)
        # カナレ電気のPDFファイルが存在することを確認
        assert any("カナレ電気" in str(f) for f in pdf_files)

    def test_parser_initialization(self):
        """パーサーの初期化テスト"""
        pdf_files = list_pdf_files()
        if pdf_files:
            parser = SecReportParser(pdf_files[0])
            assert parser.pdf_path.exists()

    def test_parser_initialization_with_invalid_path(self):
        """パーサーの不正なパスでの初期化テスト"""
        with pytest.raises(FileNotFoundError):
            SecReportParser("/nonexistent/path/file.pdf")

    def test_extract_text(self):
        """テキスト抽出テスト"""
        pdf_files = list_pdf_files()
        if pdf_files:
            parser = SecReportParser(pdf_files[0])
            text = parser.extract_text()
            assert isinstance(text, str)
            assert len(text) > 0

    def test_extract_company_info(self):
        """企業情報抽出テスト"""
        pdf_files = list_pdf_files()
        if pdf_files:
            parser = SecReportParser(pdf_files[0])
            info = parser.extract_company_info()
            assert isinstance(info, dict)
            assert "file_name" in info
            assert "extracted" in info
