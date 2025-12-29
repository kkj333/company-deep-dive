import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_processor import FinancialDataProcessor

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

            # 主要指標をメトリクスで表示（単位：百万円）
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                sales_2024 = float(df_pl[df_pl["科目"] == "売上高"]["2024年12月"].values[0].replace(",", ""))
                st.metric("売上高（2024年）", f"¥{sales_2024/1000:.1f}百万円")

            with col2:
                op_profit_2024 = float(df_pl[df_pl["科目"] == "営業利益"]["2024年12月"].values[0].replace(",", ""))
                st.metric("営業利益（2024年）", f"¥{op_profit_2024/1000:.1f}百万円")

            with col3:
                ord_income_2024 = float(df_pl[df_pl["科目"] == "経常利益"]["2024年12月"].values[0].replace(",", ""))
                st.metric("経常利益（2024年）", f"¥{ord_income_2024/1000:.1f}百万円")

            with col4:
                net_income_2024 = float(df_pl[df_pl["科目"] == "当期純利益"]["2024年12月"].values[0].replace(",", ""))
                st.metric("当期純利益（2024年）", f"¥{net_income_2024/1000:.1f}百万円")

            st.markdown("---")

            # 詳細テーブル表示
            st.subheader("詳細P/L（単位：千円）")
            st.caption("※ テーブル内の数値は千円単位です。重要項目は太字で強調されています。")

            # データのクリーンアップと整形
            df_pl_formatted = FinancialDataProcessor.format_financial_dataframe(df_pl)

            # 重要項目のインデックスを取得（太字用）
            bold_items = ["売上高", "売上総利益", "営業利益", "経常利益", "税金等調整前当期純利益", "当期純利益", "親会社株主に帰属する当期純利益"]

            # Streamlitのデータフレーム表示設定
            st.dataframe(
                df_pl_formatted,
                use_container_width=True,
                height=600,
                column_config={
                    "科目": st.column_config.TextColumn("科目", width="medium"),
                    "2023年12月": st.column_config.NumberColumn("2023年12月", format="%d"),
                    "2024年12月": st.column_config.NumberColumn("2024年12月", format="%d"),
                },
                hide_index=True
            )

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

                # チャート用データを準備（単位：百万円）
                chart_data = key_data.set_index("科目")[["2023年12月", "2024年12月"]]

                # 水平棒グラフで表示
                fig = go.Figure()
                for col in chart_data.columns:
                    fig.add_trace(go.Bar(
                        y=chart_data.index,
                        x=chart_data[col],
                        name=col,
                        orientation='h'
                    ))

                fig.update_layout(
                    title="主要科目の前年比較（2023年 vs 2024年）",
                    xaxis_title="金額（百万円）",
                    yaxis_title="科目",
                    height=400,
                    barmode='group'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.caption("※ グラフの単位は百万円です")

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
                        st.write(f"2023: ¥{val_2023:,.1f}百万円")
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
    st.subheader("連結貸借対照表（B/S）")

    bs_csv = data_dir / "consolidated_bs.csv"
    if bs_csv.exists():
        try:
            df_bs = pd.read_csv(bs_csv)

            st.caption("※ テーブル内の数値は千円単位です")

            # セクション分けして表示
            st.write("**資産の部**")
            asset_items = [
                "現金及び預金",
                "受取手形及び売掛金",
                "商品及び製品",
                "仕掛品",
                "原材料及び貯蔵品",
                "その他",
                "貸倒引当金",
                "流動資産合計",
            ]
            asset_rows = df_bs[df_bs["科目"].isin(asset_items)]
            if not asset_rows.empty:
                st.dataframe(asset_rows, use_container_width=True, hide_index=True)

            st.write("**固定資産**")
            fixed_items = [
                "有形固定資産合計",
                "無形固定資産",
                "投資その他の資産合計",
                "固定資産合計",
                "資産合計",
            ]
            fixed_rows = df_bs[df_bs["科目"].isin(fixed_items)]
            if not fixed_rows.empty:
                st.dataframe(fixed_rows, use_container_width=True, hide_index=True)

            st.markdown("---")

            st.write("**負債の部**")
            liab_items = [
                "流動負債合計",
                "固定負債合計",
                "負債合計",
            ]
            liab_rows = df_bs[df_bs["科目"].isin(liab_items)]
            if not liab_rows.empty:
                st.dataframe(liab_rows, use_container_width=True, hide_index=True)

            st.markdown("---")

            st.write("**純資産の部**")
            equity_items = [
                "株主資本合計",
                "その他の包括利益累計額合計",
                "純資産合計",
            ]
            equity_rows = df_bs[df_bs["科目"].isin(equity_items)]
            if not equity_rows.empty:
                st.dataframe(equity_rows, use_container_width=True, hide_index=True)

            st.markdown("---")

            st.subheader("💡 主要指標")
            # 資産合計、負債合計、純資産合計を抽出
            total_assets = float(
                df_bs[df_bs["科目"] == "資産合計"]["2024年12月"].values[0].replace(",", "")
            )
            total_liab = float(
                df_bs[df_bs["科目"] == "負債合計"]["2024年12月"].values[0].replace(",", "")
            )
            total_equity = float(
                df_bs[df_bs["科目"] == "純資産合計"]["2024年12月"].values[0].replace(",", "")
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("総資産（2024年）", f"¥{total_assets/1000:.1f}百万円")
            with col2:
                st.metric("総負債（2024年）", f"¥{total_liab/1000:.1f}百万円")
            with col3:
                st.metric("純資産（2024年）", f"¥{total_equity/1000:.1f}百万円")

        except Exception as e:
            st.error(f"データの読み込みに失敗しました: {e}")
    else:
        st.warning(
            "💾 consolidated_bs.csv が見つかりません。\n\n"
            "以下を実行してください:\n"
            "```bash\n"
            "uv run python scripts/extract_bs.py\n"
            "```"
        )

with tab3:
    st.subheader("キャッシュフロー計算書（C/F）")
    st.info("PDFから抽出したキャッシュフロー計算書データを表示予定")

st.markdown("---")

st.subheader("📊 財務比率分析")
st.info("このセクションは今後実装予定です")
