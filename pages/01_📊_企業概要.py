import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

st.set_page_config(
    page_title="企業概要",
    page_icon="📊",
    layout="wide"
)

st.title("📊 企業概要")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("基本情報")
    st.write("""
    **企業名：** カナレ電気

    **業種：** 電気機器

    **上場市場：** 東証プライム
    """)

with col2:
    st.subheader("経営方針")
    st.write("""
    経営方針は有価証券報告書から抽出予定です。

    PDFパーサーの実装後に表示されます。
    """)

st.markdown("---")

# データディレクトリ
data_dir = Path(__file__).parent.parent / "data"

# タブを作成
tab1, tab2 = st.tabs(["📈 経営成績", "📜 沿革"])

with tab1:
    st.subheader("直近の経営成績")

    financial_csv = data_dir / "financial_summary.csv"
    if financial_csv.exists():
        try:
            # CSVの読み込みとクリーンアップ
            df = pd.read_csv(financial_csv)
            
            # 1列目（項目名）のクリーンアップ（改行や余分な空白を削除）
            df.iloc[:, 0] = df.iloc[:, 0].str.replace("\n", "").str.replace(" ", "").str.strip()
            
            # 表示用のデータフレーム
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    col: st.column_config.TextColumn(col, width="small") for col in df.columns
                }
            )

            st.markdown("---")
            
            # グラフ用データの準備
            years = df.columns[1:].tolist()
            
            def get_row_data(keyword):
                row = df[df.iloc[:, 0].str.contains(keyword, na=False)]
                if not row.empty:
                    # カンマを除去して数値化
                    return row.iloc[0, 1:].str.replace(",", "").str.replace("△", "-").astype(float)
                return None

            sales = get_row_data("売上高")
            net_income = get_row_data("当期純利益")
            roe = get_row_data("自己資本利益率")
            equity_ratio = get_row_data("自己資本比率")

            col_g1, col_g2 = st.columns(2)

            with col_g1:
                st.subheader("📈 売上高・当期純利益の推移")
                if sales is not None and net_income is not None:
                    # 2軸グラフの作成
                    fig = make_subplots(specs=[[{"secondary_y": True}]])

                    # 売上高（棒グラフ）
                    fig.add_trace(
                        go.Bar(x=years, y=sales/1000, name="売上高 (百万円)", marker_color="lightskyblue"),
                        secondary_y=False,
                    )

                    # 当期純利益（折れ線グラフ）
                    fig.add_trace(
                        go.Scatter(x=years, y=net_income/1000, name="当期純利益 (百万円)", 
                                 line=dict(color="royalblue", width=3), mode="lines+markers+text",
                                 text=(net_income/1000).round(0), textposition="top center"),
                        secondary_y=True,
                    )

                    fig.update_layout(
                        height=450,
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        margin=dict(l=0, r=0, t=30, b=0)
                    )
                    fig.update_yaxes(title_text="売上高 (百万円)", secondary_y=False)
                    fig.update_yaxes(title_text="当期純利益 (百万円)", secondary_y=True)

                    st.plotly_chart(fig, use_container_width=True)

            with col_g2:
                st.subheader("📊 収益性・安全性の推移")
                if roe is not None and equity_ratio is not None:
                    fig_ratio = go.Figure()

                    fig_ratio.add_trace(go.Scatter(
                        x=years, y=roe, name="ROE (%)",
                        line=dict(color="mediumseagreen", width=3), mode="lines+markers"
                    ))
                    
                    fig_ratio.add_trace(go.Scatter(
                        x=years, y=equity_ratio, name="自己資本比率 (%)",
                        line=dict(color="orange", width=3), mode="lines+markers"
                    ))

                    fig_ratio.update_layout(
                        height=450,
                        yaxis_title="割合 (%)",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        margin=dict(l=0, r=0, t=30, b=0)
                    )
                    st.plotly_chart(fig_ratio, use_container_width=True)

        except Exception as e:
            st.error(f"データの読み込みまたは可視化に失敗しました: {e}")
            st.exception(e)
    else:
        st.warning("💾 financial_summary.csv が見つかりません。\n\n以下を実行してください:\n```bash\nuv run python scripts/extract_financials.py\n```")

with tab2:
    st.subheader("企業沿革")

    history_csv = data_dir / "company_history.csv"
    if history_csv.exists():
        try:
            df_history = pd.read_csv(history_csv)

            col1, col2 = st.columns([1, 4])
            with col1:
                st.metric("履歴件数", len(df_history))

            st.markdown("---")

            # スクロール可能なテーブルとして表示
            st.dataframe(df_history, use_container_width=True, height=400)

        except Exception as e:
            st.error(f"沿革データの読み込みに失敗しました: {e}")
    else:
        st.warning("💾 company_history.csv が見つかりません。\n\n以下を実行してください:\n```bash\nuv run python scripts/extract_financials.py\n```")
