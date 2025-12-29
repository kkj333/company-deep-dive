import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from utils.data_processor import FinancialDataProcessor

st.set_page_config(
    page_title="企業価値評価",
    page_icon="💎",
    layout="wide"
)

st.title("💎 企業価値評価")
st.markdown("---")

# データディレクトリ
data_dir = Path(__file__).parent.parent / "data"
consolidated_bs_csv = data_dir / "consolidated_bs.csv"
consolidated_pl_csv = data_dir / "consolidated_pl.csv"

# ファイルの存在確認
if not consolidated_bs_csv.exists() or not consolidated_pl_csv.exists():
    st.warning("💾 財務データが見つかりません")
    st.stop()

try:
    # データを読み込む
    df_bs = pd.read_csv(consolidated_bs_csv)
    df_pl = pd.read_csv(consolidated_pl_csv)

    # CSVの項目名をクリーンアップ
    df_bs.iloc[:, 0] = df_bs.iloc[:, 0].str.replace("\n", "").str.strip()
    df_pl.iloc[:, 0] = df_pl.iloc[:, 0].str.replace("\n", "").str.strip()

    # 財務数値をクリーンアップしてfloatに変換するヘルパー関数
    def clean_value(val):
        """FinancialDataProcessorを使用して数値をクリーンアップ（千円）"""
        return FinancialDataProcessor.clean_financial_value(val)

    # B/Sから値を取得するヘルパー関数
    def get_bs_value(keyword, year="2024年12月"):
        """キーワードでB/Sから値を検索"""
        row = df_bs[df_bs.iloc[:, 0].str.contains(keyword, na=False)]
        if not row.empty:
            return clean_value(row.iloc[0][year])
        return 0.0

    # P/Lから値を取得するヘルパー関数
    def get_pl_value(keyword, year="2024年12月"):
        """キーワードでP/Lから値を検索"""
        row = df_pl[df_pl.iloc[:, 0].str.contains(keyword, na=False)]
        if not row.empty:
            return clean_value(row.iloc[0][year])
        return 0.0

    # === 清算価値の計算 ===

    def calculate_liquidation_value():
        """
        清算価値を計算

        Returns:
            dict: {
                "cash": 現金及び預金,
                "receivables": 売掛金（85%）,
                "inventory": 棚卸資産（50%）,
                "securities": 有価証券（100%）,
                "tangible_assets": 有形固定資産（50%）,
                "investments": 投資等（50%）,
                "modified_assets": 修正資産合計,
                "total_liabilities": 総負債,
                "liquidation_value": 清算価値
            }
        """
        # 修正資産の計算
        cash = get_bs_value("現金及び預金") * 1.00  # 100%
        receivables = get_bs_value("受取手形及び売掛金") * 0.85  # 85%

        # 棚卸資産（50%）
        inventory = (
            get_bs_value("商品及び製品") +
            get_bs_value("仕掛品") +
            get_bs_value("原材料及び貯蔵品")
        ) * 0.50

        # 有価証券（100%）
        securities = 0.0  # B/Sには流動資産の有価証券がないため0

        # 有形固定資産（50%）
        tangible_assets = get_bs_value("有形固定資産合計") * 0.50

        # 投資等（50%）
        investments = (
            get_bs_value("投資有価証券") +
            (get_bs_value("投資その他の資産合計") - get_bs_value("投資有価証券"))
        ) * 0.50

        # 修正資産の合計
        modified_assets = (
            cash +
            receivables +
            inventory +
            securities +
            tangible_assets +
            investments
        )

        # 総負債
        total_liabilities = get_bs_value("負債合計")

        # 清算価値
        liquidation_value = modified_assets - total_liabilities

        return {
            "cash": cash,
            "receivables": receivables,
            "inventory": inventory,
            "securities": securities,
            "tangible_assets": tangible_assets,
            "investments": investments,
            "modified_assets": modified_assets,
            "total_liabilities": total_liabilities,
            "liquidation_value": liquidation_value
        }

    # === DCF法による収益価値の計算 ===

    def calculate_dcf_value(scenario="conservative"):
        """
        DCF法で企業価値を計算

        Args:
            scenario: "conservative"（弱気）または "optimistic"（強気）

        Returns:
            dict: {
                "net_cash": ネットキャッシュ,
                "fcf": フリーキャッシュフロー,
                "discount_rate": 割引率,
                "present_value": 現在価値,
                "enterprise_value": 企業価値
            }
        """
        # ネットキャッシュ = 現金 - 有利子負債
        # 簡易版：現金が主資産となるため、現金をベースに計算
        cash = get_bs_value("現金及び預金")

        # 有利子負債（B/Sには明記されていないため簡易的に0と仮定）
        interest_bearing_debt = 0.0
        net_cash = cash - interest_bearing_debt

        # FCF（フリーキャッシュフロー）の計算
        # 簡易版：当期純利益をベースに計算
        net_income = get_pl_value("親会社株主に帰属する当期純")

        # 割引率
        discount_rate = 0.10  # 10%

        if scenario == "conservative":
            # 弱気：現在のFCFを永続的に得られると仮定
            fcf = net_income
            present_value = fcf / discount_rate

        else:  # optimistic
            # 強気：5年間20%成長、6年目以降は成長なし
            fcf_base = net_income
            growth_rate = 0.20

            # 5年間の成長期のPV
            pv_growth = 0.0
            for year in range(1, 6):
                fcf_year = fcf_base * ((1 + growth_rate) ** year)
                pv_year = fcf_year / ((1 + discount_rate) ** year)
                pv_growth += pv_year

            # 6年目以降の永続価値（成長なし）
            fcf_terminal = fcf_base * ((1 + growth_rate) ** 5)
            terminal_value = fcf_terminal / discount_rate
            pv_terminal = terminal_value / ((1 + discount_rate) ** 5)

            present_value = pv_growth + pv_terminal

        # 企業価値 = ネットキャッシュ + 現在価値
        enterprise_value = net_cash + present_value

        return {
            "net_cash": net_cash,
            "fcf": net_income,
            "discount_rate": discount_rate,
            "present_value": present_value,
            "enterprise_value": enterprise_value,
            "scenario": scenario
        }

    # === 計算実行 ===

    liquidation = calculate_liquidation_value()
    conservative = calculate_dcf_value("conservative")
    optimistic = calculate_dcf_value("optimistic")

    # === ページ構成の再編 ===

    # 1. サマリーセクション
    st.success("### 🎯 企業価値評価サマリー")
    s_col1, s_col2, s_col3 = st.columns(3)
    
    with s_col1:
        st.metric("清算価値 (資産ベース)", f"¥{liquidation['liquidation_value']/1000:,.0f}百万円")
        st.caption("解散した場合の価値（保守的）")
    
    with s_col2:
        st.metric("収益価値 (弱気DCF)", f"¥{conservative['enterprise_value']/1000:,.0f}百万円")
        st.caption("現状維持を前提とした価値")
    
    with s_col3:
        st.metric("収益価値 (強気DCF)", f"¥{optimistic['enterprise_value']/1000:,.0f}百万円")
        st.caption("成長を織り込んだ価値")

    st.markdown("---")

    # 2. 詳細分析（タブ分け）
    tab_assets, tab_earnings, tab_comparison = st.tabs(["💰 資産バリュー分析", "📈 収益バリュー分析", "🔄 総合比較"])

    with tab_assets:
        st.subheader("清算価値の算出（資産バリューチェック）")
        st.write("企業の保有資産を時価評価（割引評価）し、負債を差し引いた「正味の財産価値」を算出します。")
        
        col_a1, col_a2 = st.columns([1, 1])
        
        with col_a1:
            st.markdown("#### 修正資産の内訳")
            asset_labels = ["現金", "売掛金(85%)", "棚卸資産(50%)", "有形固定資産(50%)", "投資等(50%)"]
            asset_values = [
                liquidation["cash"], liquidation["receivables"], liquidation["inventory"],
                liquidation["tangible_assets"], liquidation["investments"]
            ]
            
            non_zero_indices = [i for i, v in enumerate(asset_values) if v > 0]
            fig_assets = go.Figure(data=[go.Pie(
                labels=[asset_labels[i] for i in non_zero_indices],
                values=[asset_values[i] for i in non_zero_indices],
                hole=.3,
                marker=dict(colors=px.colors.qualitative.Pastel)
            )])
            fig_assets.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_assets, use_container_width=True)

        with col_a2:
            st.markdown("#### 計算サマリー")
            st.write(f"- **修正資産合計**: ¥{liquidation['modified_assets']/1000:,.0f}百万円")
            st.write(f"- **総負債**: ¥{liquidation['total_liabilities']/1000:,.0f}百万円")
            st.divider()
            st.write(f"### 清算価値: ¥{liquidation['liquidation_value']/1000:,.0f}百万円")
            st.info("💡 この金額が株価の「下値支持線」としての目安になります。")

    with tab_earnings:
        st.subheader("収益価値の算出（DCF法）")
        st.write("将来生み出すキャッシュフローを現在価値に割り引いて算出します。")
        
        col_e1, col_e2 = st.columns(2)
        
        with col_e1:
            st.markdown("#### 弱気シナリオ（現状維持）")
            st.metric("企業価値", f"¥{conservative['enterprise_value']/1000:,.0f}百万円")
            st.write(f"- ネットキャッシュ: ¥{conservative['net_cash']/1000:,.0f}百万円")
            st.write(f"- 事業価値(PV): ¥{conservative['present_value']/1000:,.0f}百万円")
            st.caption("前提: 成長率0%、割引率10%")

        with col_e2:
            st.markdown("#### 強気シナリオ（成長期待）")
            st.metric("企業価値", f"¥{optimistic['enterprise_value']/1000:,.0f}百万円")
            st.write(f"- ネットキャッシュ: ¥{optimistic['net_cash']/1000:,.0f}百万円")
            st.write(f"- 事業価値(PV): ¥{optimistic['present_value']/1000:,.0f}百万円")
            st.caption("前提: 5年間20%成長、割引率10%")

    with tab_comparison:
        st.subheader("評価手法別の企業価値比較")
        
        fig_comparison = go.Figure(data=[
            go.Bar(name="清算価値", x=["資産ベース"], y=[liquidation["liquidation_value"] / 1000], marker_color="skyblue"),
            go.Bar(name="弱気DCF", x=["収益ベース"], y=[conservative["enterprise_value"] / 1000], marker_color="lightgreen"),
            go.Bar(name="強気DCF", x=["収益ベース"], y=[optimistic["enterprise_value"] / 1000], marker_color="gold")
        ])
        
        fig_comparison.update_layout(
            title="評価手法別の企業価値（単位：百万円）",
            yaxis_title="金額（百万円）",
            barmode="group",
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

    st.markdown("---")

    # 3. 前提条件とデータ
    with st.expander("📝 計算の前提条件と使用データ"):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown("**使用した財務データ (2024年12月期)**")
            st.write(f"- 現金及び預金: ¥{get_bs_value('現金及び預金')/1000:,.0f}百万円")
            st.write(f"- 受取手形及び売掛金: ¥{get_bs_value('受取手形及び売掛金')/1000:,.0f}百万円")
            st.write(f"- 総負債: ¥{get_bs_value('負債合計')/1000:,.0f}百万円")
            st.write(f"- 当期純利益: ¥{get_pl_value('親会社株主に帰属する当期純')/1000:,.0f}百万円")
        
        with col_d2:
            st.markdown("**評価のロジック**")
            st.write("- **清算価値**: 資産ごとに換金性を考慮（現金100%、売掛85%、棚卸・固定資産50%）")
            st.write("- **DCF法**: 割引率10%を使用。ネットキャッシュ（現金-有利子負債）を加算。")

except Exception as e:
    st.error(f"データ処理エラーが発生しました: {e}")
    st.exception(e)
