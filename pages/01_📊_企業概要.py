import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="企業概要",
    page_icon="📊",
    layout="wide"
)

st.title("📊 企業概要")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("基本情報")
    st.write("""
    **企業名：** カナレ電気

    **業種：** 電気機器

    **上場市場：** 東証プライム
    """)

with col2:
    st.subheader("経営方針")
    st.write("""
    経営方針は有価証券報告書から抽出予定です。

    PDFパーサーの実装後に表示されます。
    """)

st.markdown("---")

# データディレクトリ
data_dir = Path(__file__).parent.parent / "data"

# タブを作成
tab1, tab2 = st.tabs(["📈 経営成績", "📜 沿革"])

with tab1:
    st.subheader("直近の経営成績")

    financial_csv = data_dir / "financial_summary.csv"
    if financial_csv.exists():
        try:
            df = pd.read_csv(financial_csv)
            st.dataframe(df, use_container_width=True)

            st.markdown("---")
            st.subheader("📊 売上推移")

            # 売上高データを抽出
            sales_row = df[df.iloc[:, 0].str.contains("売上高", na=False)]
            if not sales_row.empty:
                sales_data = sales_row.iloc[0, 1:].str.replace(",", "").astype(float) / 1000
                st.line_chart(sales_data)

        except Exception as e:
            st.error(f"データの読み込みに失敗しました: {e}")
    else:
        st.warning("💾 financial_summary.csv が見つかりません。\n\n以下を実行してください:\n```bash\nuv run python scripts/extract_financials.py\n```")

with tab2:
    st.subheader("企業沿革")

    history_csv = data_dir / "company_history.csv"
    if history_csv.exists():
        try:
            df_history = pd.read_csv(history_csv)

            col1, col2 = st.columns([1, 4])
            with col1:
                st.metric("履歴件数", len(df_history))

            st.markdown("---")

            # スクロール可能なテーブルとして表示
            st.dataframe(df_history, use_container_width=True, height=400)

        except Exception as e:
            st.error(f"沿革データの読み込みに失敗しました: {e}")
    else:
        st.warning("💾 company_history.csv が見つかりません。\n\n以下を実行してください:\n```bash\nuv run python scripts/extract_financials.py\n```")
