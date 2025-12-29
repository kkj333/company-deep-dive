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

            # 業績ハイライト（前年比）をトップに移動
            st.subheader("📊 業績ハイライト（2024年12月期）")
            
            key_items = ["売上高", "営業利益", "経常利益", "当期純利益"]
            key_data = df_pl[df_pl["科目"].isin(key_items)].copy()

            if not key_data.empty:
                key_data["2023年12月"] = (
                    key_data["2023年12月"].str.replace(",", "").astype(float) / 1000
                )
                key_data["2024年12月"] = (
                    key_data["2024年12月"].str.replace(",", "").astype(float) / 1000
                )

                cols = st.columns(len(key_items))
                for i, item in enumerate(key_items):
                    row = key_data[key_data["科目"] == item].iloc[0]
                    val_2023 = float(row["2023年12月"])
                    val_2024 = float(row["2024年12月"])
                    change_pct = ((val_2024 - val_2023) / val_2023 * 100) if val_2023 != 0 else 0
                    
                    with cols[i]:
                        st.metric(
                            label=item,
                            value=f"¥{val_2024:,.0f}M",
                            delta=f"{change_pct:.1f}%",
                            delta_color="normal" if change_pct >= 0 else "inverse"
                        )

            st.markdown("---")

            # グラフセクション
            st.subheader("📈 業績トレンド")
            col_chart1, col_chart2 = st.columns(2)

            if not key_data.empty:
                chart_data = key_data.set_index("科目")[["2023年12月", "2024年12月"]]

                with col_chart1:
                    # 主要科目の比較（棒グラフ）
                    fig_bar = go.Figure()
                    for col in chart_data.columns:
                        fig_bar.add_trace(go.Bar(
                            x=chart_data.index,
                            y=chart_data[col],
                            name=col
                        ))

                    fig_bar.update_layout(
                        title="主要科目の前年比較（単位：百万円）",
                        xaxis_title="科目",
                        yaxis_title="金額（百万円）",
                        barmode='group',
                        height=400,
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

                with col_chart2:
                    # 売上高と営業利益の推移（折れ線グラフ）
                    trend_items = ["売上高", "営業利益"]
                    trend_data = chart_data.loc[trend_items].T
                    
                    fig_line = go.Figure()
                    for item in trend_items:
                        fig_line.add_trace(go.Scatter(
                            x=trend_data.index,
                            y=trend_data[item],
                            name=item,
                            mode='lines+markers+text',
                            text=[f"{v:,.0f}" for v in trend_data[item]],
                            textposition="top center"
                        ))

                    fig_line.update_layout(
                        title="売上高・営業利益の推移",
                        xaxis_title="決算期",
                        yaxis_title="金額（百万円）",
                        height=400,
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig_line, use_container_width=True)

            st.markdown("---")

            # 詳細テーブル表示
            st.subheader("📄 詳細P/L（単位：千円）")
            st.caption("※ テーブル内の数値は千円単位です。重要項目は太字で強調されています。")

            # データのクリーンアップと整形
            df_pl_formatted = FinancialDataProcessor.format_financial_dataframe(df_pl)

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

            st.markdown("---")

            st.subheader("📈 B/S構成の可視化")

            # グラフ用データの抽出
            def get_val(item_name):
                row = df_bs[df_bs["科目"] == item_name]
                if not row.empty:
                    return FinancialDataProcessor.clean_financial_value(row["2024年12月"].values[0]) / 1000
                return 0

            current_assets = get_val("流動資産合計")
            fixed_assets = get_val("固定資産合計")
            current_liab = get_val("流動負債合計")
            fixed_liab = get_val("固定負債合計")
            net_assets = get_val("純資産合計")

            # B/S構成図（積上げ棒グラフ）
            fig_bs = go.Figure()

            # 資産側
            fig_bs.add_trace(go.Bar(
                name="流動資産", x=["資産"], y=[current_assets],
                marker_color="lightskyblue", text=[f"{current_assets:,.0f}"], textposition="inside"
            ))
            fig_bs.add_trace(go.Bar(
                name="固定資産", x=["資産"], y=[fixed_assets],
                marker_color="dodgerblue", text=[f"{fixed_assets:,.0f}"], textposition="inside"
            ))

            # 負債・純資産側
            fig_bs.add_trace(go.Bar(
                name="流動負債", x=["負債・純資産"], y=[current_liab],
                marker_color="lightcoral", text=[f"{current_liab:,.0f}"], textposition="inside"
            ))
            fig_bs.add_trace(go.Bar(
                name="固定負債", x=["負債・純資産"], y=[fixed_liab],
                marker_color="indianred", text=[f"{fixed_liab:,.0f}"], textposition="inside"
            ))
            fig_bs.add_trace(go.Bar(
                name="純資産", x=["負債・純資産"], y=[net_assets],
                marker_color="mediumseagreen", text=[f"{net_assets:,.0f}"], textposition="inside"
            ))

            fig_bs.update_layout(
                barmode="stack",
                title="B/S構成図（2024年12月期、単位：百万円）",
                height=500,
                yaxis_title="金額（百万円）",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig_bs, use_container_width=True)

            st.markdown("---")

            # 詳細テーブル表示（以前のコードを整理して再配置）
            st.subheader("📄 詳細B/S（単位：千円）")
            st.caption("※ 重要項目は太字で強調、内訳はインデントされています。")

            df_bs_formatted = FinancialDataProcessor.format_financial_dataframe(df_bs)

            st.dataframe(
                df_bs_formatted,
                use_container_width=True,
                height=600,
                column_config={
                    "科目": st.column_config.TextColumn("科目", width="medium"),
                    "2023年12月": st.column_config.NumberColumn("2023年12月", format="%d"),
                    "2024年12月": st.column_config.NumberColumn("2024年12月", format="%d"),
                },
                hide_index=True
            )

        except Exception as e:
            st.error(f"データの読み込みに失敗しました: {e}")
    else:
        st.warning(
            "💾 consolidated_bs.csv が見つかりません。\n\n"
            "以下を実行してください:\n"
            "```bash\n"
            "uv run python scripts/extract_financials.py\n"
            "```"
        )

with tab3:
    st.subheader("キャッシュフロー計算書（C/F）")
    st.info("PDFから抽出したキャッシュフロー計算書データを表示予定")

st.markdown("---")

st.subheader("📊 財務比率分析")

if pl_csv.exists() and bs_csv.exists():
    try:
        df_pl = pd.read_csv(pl_csv)
        df_bs = pd.read_csv(bs_csv)
        
        ratios = FinancialDataProcessor.calculate_financial_ratios(df_pl, df_bs)
        
        if ratios:
            # メトリクス表示
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("ROE", f"{ratios.get('ROE（自己資本利益率）', 0):.1f}%")
            with col2:
                st.metric("ROA", f"{ratios.get('ROA（総資産利益率）', 0):.1f}%")
            with col3:
                st.metric("営業利益率", f"{ratios.get('売上高営業利益率', 0):.1f}%")
            with col4:
                st.metric("自己資本比率", f"{ratios.get('自己資本比率', 0):.1f}%")
            with col5:
                st.metric("流動比率", f"{ratios.get('流動比率', 0):.1f}%")
            
            st.markdown("---")

            st.subheader("📌 指標の解説")
            st.info("💡 **収益性指標**\n"
                    "- **ROE（自己資本利益率）**: 自己資本に対する利益の比率。高いほど株主資本を効率的に活用しています\n"
                    "- **ROA（総資産利益率）**: 総資産に対する利益の比率。経営効率を示す総合指標です\n"
                    "- **営業利益率**: 売上高に対する営業利益の比率。本業の収益力を示します\n\n"
                    "💡 **安全性指標**\n"
                    "- **自己資本比率**: 総資産に占める自己資本の割合。高いほど財務基盤が安定しています\n"
                    "- **流動比率**: 流動負債に対する流動資産の割合。100%以上で短期的な支払い能力があります")
            
    except Exception as e:
        st.error(f"比率の計算中にエラーが発生しました: {e}")
else:
    st.warning("💾 財務比率の計算には P/L と B/S の両方のデータが必要です。")
