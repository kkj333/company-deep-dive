import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import sys

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="経営指標",
    page_icon="📈",
    layout="wide"
)

st.title("📈 経営指標分析")
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
    # 列1以降がデータだが、最初の行に実際の決算年月がある
    fiscal_periods = df_summary.columns[1:].tolist()  # ["第48期", "第49期", ...]

    # グラフ用の年月表示を取得（決算年月行から）
    fiscal_years_row = df_summary[df_summary.iloc[:, 0].str.contains("決算年月", na=False)]
    if not fiscal_years_row.empty:
        years = fiscal_years_row.iloc[0, 1:].tolist()  # ["2020年12月", "2021年12月", ...]
    else:
        years = fiscal_periods  # fallback

    # === 指標の計算 ===

    # 1. ROE（自己資本利益率） - CSVから取得
    roe_data = get_row_data("自己資本利益率")

    # 2. ROA（総資産利益率） - 計算
    net_income = get_row_data("親会社株主に帰属する当期純")
    total_assets = get_row_data("総資産額")
    if net_income is not None and total_assets is not None:
        # ROAは平均総資産を使用（前年度と当年度の平均）
        avg_total_assets = total_assets.rolling(window=2).mean()
        roa_data = (net_income / avg_total_assets) * 100
    else:
        roa_data = None

    # 3. 営業利益率 - 計算（営業利益がないため経常利益で代替）
    ordinary_income = get_row_data("経常利益")
    sales = get_row_data("売上高 （千円")
    operating_margin_data = (ordinary_income / sales) * 100 if ordinary_income is not None and sales is not None else None

    # 4. 自己資本比率 - CSVから取得
    equity_ratio = get_row_data("自己資本比率")

    # 5. EPS（１株当たり当期純利益） - CSVから取得
    eps_data = get_row_data("１株当たり当期純利益")

    # === セクション1: 主要指標サマリー（5カラムメトリクス） ===

    st.subheader("📊 主要経営指標（2024年12月期）")

    col1, col2, col3, col4, col5 = st.columns(5)

    # ROE
    if roe_data is not None:
        roe_2024 = roe_data.iloc[-1]
        roe_2023 = roe_data.iloc[-2]
        roe_delta = roe_2024 - roe_2023
        with col1:
            st.metric("ROE", f"{roe_2024:.2f}%", delta=f"{roe_delta:+.2f}%")
    else:
        with col1:
            st.metric("ROE", "データなし")

    # ROA
    if roa_data is not None:
        roa_2024 = roa_data.iloc[-1]
        roa_2023 = roa_data.iloc[-2]
        roa_delta = roa_2024 - roa_2023
        with col2:
            st.metric("ROA", f"{roa_2024:.2f}%", delta=f"{roa_delta:+.2f}%")
    else:
        with col2:
            st.metric("ROA", "データなし")

    # 営業利益率
    if operating_margin_data is not None:
        op_margin_2024 = operating_margin_data.iloc[-1]
        op_margin_2023 = operating_margin_data.iloc[-2]
        op_margin_delta = op_margin_2024 - op_margin_2023
        with col3:
            st.metric("営業利益率", f"{op_margin_2024:.2f}%", delta=f"{op_margin_delta:+.2f}%")
    else:
        with col3:
            st.metric("営業利益率", "データなし")

    # 自己資本比率
    if equity_ratio is not None:
        equity_2024 = equity_ratio.iloc[-1]
        equity_2023 = equity_ratio.iloc[-2]
        equity_delta = equity_2024 - equity_2023
        with col4:
            st.metric("自己資本比率", f"{equity_2024:.2f}%", delta=f"{equity_delta:+.2f}%")
    else:
        with col4:
            st.metric("自己資本比率", "データなし")

    # EPS
    if eps_data is not None:
        eps_2024 = eps_data.iloc[-1]
        eps_2023 = eps_data.iloc[-2]
        eps_delta = eps_2024 - eps_2023
        with col5:
            st.metric("EPS", f"¥{eps_2024:.0f}", delta=f"{eps_delta:+.0f}円")
    else:
        with col5:
            st.metric("EPS", "データなし")

    st.markdown("---")

    # === セクション2: トレンドグラフ（メイン） ===

    st.subheader("📈 5年間の指標推移")

    if all([roe_data is not None, roa_data is not None, operating_margin_data is not None,
            equity_ratio is not None, eps_data is not None]):

        # 2軸グラフの作成
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # 左軸: パーセント系の指標
        fig.add_trace(
            go.Scatter(
                x=years, y=roe_data, name="ROE (%)",
                line=dict(color="royalblue", width=2.5),
                mode="lines+markers"
            ),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(
                x=years, y=roa_data, name="ROA (%)",
                line=dict(color="lightblue", width=2.5),
                mode="lines+markers"
            ),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(
                x=years, y=operating_margin_data, name="営業利益率 (%)",
                line=dict(color="mediumseagreen", width=2.5),
                mode="lines+markers"
            ),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(
                x=years, y=equity_ratio, name="自己資本比率 (%)",
                line=dict(color="orange", width=2.5),
                mode="lines+markers"
            ),
            secondary_y=False
        )

        # 右軸: 円単位の指標
        fig.add_trace(
            go.Scatter(
                x=years, y=eps_data, name="EPS (円)",
                line=dict(color="crimson", width=2.5),
                mode="lines+markers"
            ),
            secondary_y=True
        )

        # レイアウト調整
        fig.update_yaxes(title_text="割合 (%)", secondary_y=False)
        fig.update_yaxes(title_text="EPS (円)", secondary_y=True)
        fig.update_layout(
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ 一部のデータが欠落しており、グラフが表示できません")

    st.markdown("---")

    # === セクション3: 指標説明（エクスパンダー） ===

    st.subheader("💡 指標の説明")

    with st.expander("ROE（自己資本利益率）"):
        st.write("""
        自己資本に対する利益の比率。企業の資本をいかに効率的に使用して利益を生み出しているかを示します。
        高いほど良好です。
        """)

    with st.expander("ROA（総資産利益率）"):
        st.write("""
        総資産に対する利益の比率。企業の全資産がいかに効率的に利益を生み出しているかを示します。
        """)

    with st.expander("営業利益率"):
        st.write("""
        売上高に対する営業利益の比率。企業の本業の収益性を示します。
        高いほど本業が効率的です。
        """)

    with st.expander("自己資本比率"):
        st.write("""
        総資産に占める自己資本の割合。企業の財務安定性を示します。
        一般的に50%以上が望ましいとされています。
        """)

    with st.expander("EPS（１株当たり当期純利益）"):
        st.write("""
        1株当たりの利益額。株主にとって重要な指標です。
        高いほど1株の価値が高いことを示します。
        """)

except Exception as e:
    st.error(f"データ処理エラーが発生しました: {e}")
    st.exception(e)
