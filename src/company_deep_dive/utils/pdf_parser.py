"""
PDF解析モジュール
有価証券報告書からデータを抽出するためのユーティリティ
"""

from pathlib import Path
import pdfplumber
import pandas as pd
from typing import Dict, List, Any


class SecReportParser:
    """有価証券報告書パーサー"""

    def __init__(self, pdf_path: str | Path):
        """
        PDFファイルを初期化

        Args:
            pdf_path: PDFファイルのパス
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    def extract_text(self) -> str:
        """
        PDFから全テキストを抽出

        Returns:
            抽出されたテキスト
        """
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

    def extract_tables(self) -> List[pd.DataFrame]:
        """
        PDFから表を抽出

        Returns:
            抽出された表のデータフレームリスト
        """
        tables = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    for table in page_tables:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        tables.append(df)
        return tables

    def extract_company_info(self) -> Dict[str, Any]:
        """
        企業情報を抽出

        Returns:
            企業情報の辞書
        """
        text = self.extract_text()
        return {
            "file_name": self.pdf_path.name,
            "extracted": True,
        }


def get_documents_dir() -> Path:
    """ドキュメントディレクトリのパスを取得"""
    return Path(__file__).parent.parent / "documents"


def list_pdf_files() -> List[Path]:
    """ドキュメントディレクトリ内のPDFファイルをリスト"""
    docs_dir = get_documents_dir()
    return list(docs_dir.glob("*.pdf"))
