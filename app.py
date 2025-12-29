import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="企業詳細分析",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 企業詳細分析レポート")
st.markdown("---")

# サイドバー
st.sidebar.markdown("**💡 ヒント:** 上のメニューからページを選択できます")

# メインコンテンツ
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("企業名", "カナレ電気")

with col2:
    st.metric("業種", "電気機器")

with col3:
    st.metric("上場市場", "東証スタンダード")

st.markdown("---")

st.subheader("📄 有価証券報告書の分析")
st.write("""
このアプリは有価証券報告書から抽出した企業データを詳細に分析します。

**利用可能な分析：**
- 📊 企業概要・経営方針
- 💰 財務諸表分析（P/L、B/S、C/F）
- 📈 経営指標の推移
- 🏢 事業セグメント分析
- ⚠️ リスク要因の分析
""")

st.markdown("---")

st.info("💡 左側のメニューから各分析ページを選択して詳細をご覧ください")
