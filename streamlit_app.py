"""
Streamlit Cloud用のエントリーポイント

このファイルはStreamlit Cloudが自動的に認識します。
実際のアプリケーションは src/company_deep_dive/app.py にあります。
"""

import sys
from pathlib import Path

# srcディレクトリをPythonパスに追加
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# 実際のアプリを実行
import runpy
runpy.run_path("src/company_deep_dive/app.py", run_name="__main__")
