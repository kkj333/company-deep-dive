import streamlit as st

st.set_page_config(
    page_title="リスク分析",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ リスク要因分析")
st.markdown("---")

st.subheader("📋 有価証券報告書記載のリスク要因")
st.info("PDFから抽出したリスク要因を以下に表示予定です")

st.markdown("---")

risk_categories = {
    "経営リスク": "会社方針・事業戦略に関連するリスク",
    "市場リスク": "市場環境の変化に関連するリスク",
    "業務リスク": "業務遂行・組織運営に関連するリスク",
    "財務リスク": "資金調達・為替・金利に関連するリスク",
    "法令リスク": "法令遵守・コンプライアンスに関連するリスク",
}

for category, description in risk_categories.items():
    with st.expander(f"🔍 {category}"):
        st.write(description)
        st.info("詳細内容はPDFから抽出予定です")

st.markdown("---")

st.subheader("📊 リスク評価マトリックス")
st.info("リスク評価マトリックスを表示予定です")
