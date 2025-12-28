import streamlit as st

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

st.subheader("📈 直近の経営成績")
st.info("このセクションは今後実装予定です")
