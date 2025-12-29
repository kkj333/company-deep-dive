import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import sys

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="事業セグメント",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 事業セグメント分析")
st.markdown("---")

# データディレクトリ
data_dir = Path(__file__).parent.parent / "data"
financial_summary_csv = data_dir / "financial_summary.csv"

if not financial_summary_csv.exists():
    st.warning("💾 financial_summary.csv が見つかりません")
    st.stop()

try:
    # データを読み込む
    df_summary = pd.read_csv(financial_summary_csv)

    # CSVの項目名から改行を削除してクリーンアップ
    df_summary.iloc[:, 0] = df_summary.iloc[:, 0].str.replace("\n", "").str.strip()

    # financial_summary.csvから行を取得するヘルパー関数
    def get_row_data(keyword):
        """キーワードで行を検索し、数値データを返す"""
        row = df_summary[df_summary.iloc[:, 0].str.contains(keyword, na=False)]
        if not row.empty:
            return row.iloc[0, 1:].str.replace(",", "").str.replace("△", "-").astype(float)
        return None

    # 年度リスト（グラフ用）
    fiscal_years_row = df_summary[df_summary.iloc[:, 0].str.contains("決算年月", na=False)]
    years = fiscal_years_row.iloc[0, 1:].tolist() if not fiscal_years_row.empty else df_summary.columns[1:].tolist()

    # === データ取得 ===

    sales_data = get_row_data("売上高 （千円")
    ordinary_income = get_row_data("経常利益")
    net_income = get_row_data("親会社株主に帰属する当期純")
    operating_cf = get_row_data("営業活動によるキャッシュ")
    investing_cf = get_row_data("投資活動によるキャッシュ")
    financing_cf = get_row_data("財務活動によるキャッシュ")

    # === セクション1: 主要指標サマリー（3カラムメトリクス） ===

    st.subheader("📊 主要経営指標（2024年12月期）")

    col1, col2, col3 = st.columns(3)

    # 売上高
    if sales_data is not None:
        sales_2024 = sales_data.iloc[-1] / 1000
        sales_2023 = sales_data.iloc[-2] / 1000
        sales_delta = sales_2024 - sales_2023
        with col1:
            st.metric(
                "売上高",
                f"¥{sales_2024:,.0f}百万円",
                delta=f"{sales_delta:+,.0f}百万円"
            )
    else:
        with col1:
            st.metric("売上高", "データなし")

    # 経常利益
    if ordinary_income is not None:
        oi_2024 = ordinary_income.iloc[-1] / 1000
        oi_2023 = ordinary_income.iloc[-2] / 1000
        oi_delta = oi_2024 - oi_2023
        with col2:
            st.metric(
                "経常利益",
                f"¥{oi_2024:,.0f}百万円",
                delta=f"{oi_delta:+,.0f}百万円"
            )
    else:
        with col2:
            st.metric("経常利益", "データなし")

    # 当期純利益
    if net_income is not None:
        ni_2024 = net_income.iloc[-1] / 1000
        ni_2023 = net_income.iloc[-2] / 1000
        ni_delta = ni_2024 - ni_2023
        with col3:
            st.metric(
                "当期純利益",
                f"¥{ni_2024:,.0f}百万円",
                delta=f"{ni_delta:+,.0f}百万円"
            )
    else:
        with col3:
            st.metric("当期純利益", "データなし")

    st.markdown("---")

    # === セクション2: 売上高推移（棒グラフ） ===

    st.subheader("📊 売上高の推移")

    if sales_data is not None:
        fig_sales = go.Figure()

        fig_sales.add_trace(go.Bar(
            x=years,
            y=sales_data / 1000,  # 百万円
            name="売上高",
            marker_color="lightskyblue",
            text=(sales_data / 1000).round(0),
            textposition="outside"
        ))

        fig_sales.update_layout(
            yaxis_title="百万円",
            height=400,
            showlegend=False,
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig_sales, use_container_width=True)
    else:
        st.warning("⚠️ 売上高データが見つかりません")

    st.markdown("---")

    # === セクション3: 利益推移（折れ線グラフ） ===

    st.subheader("💰 利益の推移")

    if ordinary_income is not None and net_income is not None:
        fig_profit = go.Figure()

        # 経常利益
        fig_profit.add_trace(go.Scatter(
            x=years,
            y=ordinary_income / 1000,
            name="経常利益",
            line=dict(color="mediumseagreen", width=2.5),
            mode="lines+markers"
        ))

        # 当期純利益
        fig_profit.add_trace(go.Scatter(
            x=years,
            y=net_income / 1000,
            name="当期純利益",
            line=dict(color="royalblue", width=2.5),
            mode="lines+markers"
        ))

        fig_profit.update_layout(
            yaxis_title="百万円",
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig_profit, use_container_width=True)
    else:
        st.warning("⚠️ 利益データが見つかりません")

    st.markdown("---")

    # === セクション4: キャッシュフロー推移 ===

    st.subheader("💵 キャッシュフローの推移")

    if all([operating_cf is not None, investing_cf is not None, financing_cf is not None]):
        fig_cf = go.Figure()

        fig_cf.add_trace(go.Bar(
            x=years,
            y=operating_cf / 1000,
            name="営業CF",
            marker_color="green"
        ))

        fig_cf.add_trace(go.Bar(
            x=years,
            y=investing_cf / 1000,
            name="投資CF",
            marker_color="orange"
        ))

        fig_cf.add_trace(go.Bar(
            x=years,
            y=financing_cf / 1000,
            name="財務CF",
            marker_color="red"
        ))

        fig_cf.update_layout(
            barmode='group',
            yaxis_title="百万円",
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig_cf, use_container_width=True)
    else:
        st.warning("⚠️ キャッシュフロー データが見つかりません")

    st.markdown("---")

    # === セクション5: 収益性指標 ===

    st.subheader("📈 収益性指標の推移")

    if sales_data is not None and ordinary_income is not None:
        profit_margin = (ordinary_income / sales_data) * 100

        fig_margin = go.Figure()

        fig_margin.add_trace(go.Scatter(
            x=years,
            y=profit_margin,
            name="売上高経常利益率",
            line=dict(color="purple", width=2.5),
            mode="lines+markers+text",
            text=profit_margin.round(1),
            textposition="top center"
        ))

        fig_margin.update_layout(
            yaxis_title="（%）",
            height=400,
            showlegend=False,
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig_margin, use_container_width=True)
    else:
        st.warning("⚠️ 収益性指標の計算に必要なデータが見つかりません")

except Exception as e:
    st.error(f"データ処理エラーが発生しました: {e}")
    st.exception(e)
