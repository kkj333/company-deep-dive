import streamlit as st

st.set_page_config(
    page_title="財務分析",
    page_icon="💰",
    layout="wide"
)

st.title("💰 財務分析")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["損益計算書", "貸借対照表", "キャッシュフロー計算書"])

with tab1:
    st.subheader("損益計算書（P/L）")
    st.info("PDFから抽出した損益計算書データを表示予定")

with tab2:
    st.subheader("貸借対照表（B/S）")
    st.info("PDFから抽出した貸借対照表データを表示予定")

with tab3:
    st.subheader("キャッシュフロー計算書（C/F）")
    st.info("PDFから抽出したキャッシュフロー計算書データを表示予定")

st.markdown("---")

st.subheader("📊 財務比率分析")
st.info("このセクションは今後実装予定です")
