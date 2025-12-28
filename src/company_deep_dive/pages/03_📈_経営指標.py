import streamlit as st

st.set_page_config(
    page_title="経営指標",
    page_icon="📈",
    layout="wide"
)

st.title("📈 経営指標分析")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("ROE（自己資本利益率）", "計算中", "%")

with col2:
    st.metric("ROA（総資産利益率）", "計算中", "%")

with col3:
    st.metric("営業利益率", "計算中", "%")

st.markdown("---")

st.subheader("📊 主要指標の推移")
st.info("グラフはPDFから抽出したデータをもとに表示予定です")

st.markdown("---")

st.subheader("💹 効率性指標")
st.write("""
- 総資産回転率
- インベントリ回転率
- 売上高成長率
""")
st.info("このセクションは今後実装予定です")
