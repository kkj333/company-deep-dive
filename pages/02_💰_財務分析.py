import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="財務分析",
    page_icon="💰",
    layout="wide"
)

st.title("💰 財務分析")
st.markdown("---")

# データディレクトリ
data_dir = Path(__file__).parent.parent / "data"

tab1, tab2, tab3 = st.tabs(["損益計算書", "貸借対照表", "キャッシュフロー計算書"])

with tab1:
    st.subheader("連結損益計算書（P/L）")

    pl_csv = data_dir / "consolidated_pl.csv"
    if pl_csv.exists():
        try:
            df_pl = pd.read_csv(pl_csv)

            # 主要指標をメトリクスで表示
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                sales_2024 = float(df_pl[df_pl["科目"] == "売上高"]["2024年12月"].values[0].replace(",", ""))
                st.metric("売上高（2024年）", f"¥{sales_2024/1000:.1f}B")

            with col2:
                op_profit_2024 = float(df_pl[df_pl["科目"] == "営業利益"]["2024年12月"].values[0].replace(",", ""))
                st.metric("営業利益（2024年）", f"¥{op_profit_2024/1000:.1f}B")

            with col3:
                ord_income_2024 = float(df_pl[df_pl["科目"] == "経常利益"]["2024年12月"].values[0].replace(",", ""))
                st.metric("経常利益（2024年）", f"¥{ord_income_2024/1000:.1f}B")

            with col4:
                net_income_2024 = float(df_pl[df_pl["科目"] == "当期純利益"]["2024年12月"].values[0].replace(",", ""))
                st.metric("当期純利益（2024年）", f"¥{net_income_2024/1000:.1f}B")

            st.markdown("---")

            # 詳細テーブル表示
            st.subheader("詳細P/L（単位：千円）")
            st.dataframe(df_pl, use_container_width=True, height=600)

            st.markdown("---")

            st.subheader("📈 主要科目の比較")

            # 売上から当期純利益までの流れを可視化
            key_items = ["売上高", "営業利益", "経常利益", "当期純利益"]
            key_data = df_pl[df_pl["科目"].isin(key_items)].copy()

            if not key_data.empty:
                key_data["2023年12月"] = (
                    key_data["2023年12月"].str.replace(",", "").astype(float) / 1000
                )
                key_data["2024年12月"] = (
                    key_data["2024年12月"].str.replace(",", "").astype(float) / 1000
                )

                # チャート用データを準備
                chart_data = key_data.set_index("科目")[["2023年12月", "2024年12月"]]
                st.bar_chart(chart_data)

                # 変化率を表示
                st.subheader("前年比（%）")
                for idx, row in key_data.iterrows():
                    item = row["科目"]
                    val_2023 = float(row["2023年12月"])
                    val_2024 = float(row["2024年12月"])
                    change_pct = ((val_2024 - val_2023) / val_2023 * 100) if val_2023 != 0 else 0

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**{item}**")
                    with col2:
                        st.write(f"2023: ¥{val_2023:.1f}B")
                    with col3:
                        color = "🔴" if change_pct < 0 else "🟢"
                        st.write(f"{color} {change_pct:.1f}%")

        except Exception as e:
            st.error(f"データの読み込みに失敗しました: {e}")
    else:
        st.warning(
            "💾 consolidated_pl.csv が見つかりません。\n\n"
            "以下を実行してください:\n"
            "```bash\n"
            "uv run python scripts/extract_pl.py\n"
            "```"
        )

with tab2:
    st.subheader("貸借対照表（B/S）")
    st.info("PDFから抽出した貸借対照表データを表示予定")

with tab3:
    st.subheader("キャッシュフロー計算書（C/F）")
    st.info("PDFから抽出したキャッシュフロー計算書データを表示予定")

st.markdown("---")

st.subheader("📊 財務比率分析")
st.info("このセクションは今後実装予定です")
