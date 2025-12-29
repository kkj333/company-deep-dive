import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="リスク分析",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ リスク要因分析")
st.markdown("---")

# データディレクトリ
data_dir = Path(__file__).parent.parent / "data"
risk_csv = data_dir / "risk_factors.csv"

if risk_csv.exists():
    try:
        df_risks = pd.read_csv(risk_csv)
        
        # 統計情報の表示
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📊 リスク分布")
            category_counts = df_risks["category"].value_counts().reset_index()
            category_counts.columns = ["カテゴリー", "件数"]
            
            fig = px.bar(
                category_counts, 
                x="件数", 
                y="カテゴリー", 
                orientation='h',
                color="カテゴリー",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📋 リスク要因の概要")
            st.write(f"有価証券報告書から **{len(df_risks)}件** のリスク要因が抽出されました。")
            st.info("💡 カテゴリーをクリックすると詳細な内容を確認できます。")

        st.markdown("---")

        # カテゴリーごとに表示
        categories = ["経営リスク", "市場リスク", "業務リスク", "財務リスク", "法令リスク", "その他"]
        
        for category in categories:
            category_risks = df_risks[df_risks["category"] == category]
            if not category_risks.empty:
                st.subheader(f"🔍 {category}")
                for _, row in category_risks.iterrows():
                    with st.expander(f"📌 {row['title']}"):
                        st.write(row['content'])
            else:
                # リスクがないカテゴリーも一応表示（任意）
                pass

    except Exception as e:
        st.error(f"データの読み込みに失敗しました: {e}")
else:
    st.warning("💾 リスク要因のデータが見つかりません。")
    st.info("以下のコマンドを実行してデータを抽出してください：\n```bash\nuv run python scripts/extract_risks.py\n```")
    
    # サンプル表示
    st.markdown("---")
    st.subheader("💡 表示イメージ")
    sample_categories = {
        "経営リスク": "会社方針・事業戦略に関連するリスク",
        "市場リスク": "市場環境の変化に関連するリスク",
        "業務リスク": "業務遂行・組織運営に関連するリスク",
    }
    for cat, desc in sample_categories.items():
        with st.expander(f"🔍 {cat} (サンプル)"):
            st.write(desc)
            st.caption("※ 実際のデータはPDFから抽出されます。")
