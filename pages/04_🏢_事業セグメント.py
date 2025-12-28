import streamlit as st

st.set_page_config(
    page_title="事業セグメント",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 事業セグメント分析")
st.markdown("---")

st.subheader("📊 事業セグメント構成")
st.info("PDFから抽出した事業セグメント情報を表示予定")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("売上高構成")
    st.info("円グラフを表示予定")

with col2:
    st.subheader("営業利益構成")
    st.info("円グラフを表示予定")

st.markdown("---")

st.subheader("📈 セグメント別推移")
st.info("セグメント別の売上・利益推移グラフを表示予定")
