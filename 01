import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Top10 Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🌍 Global Market Cap Top10 Dashboard")
st.caption("최근 1년 주가 비교")

# 글로벌 시가총액 Top10
stocks = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Meta": "META",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Tesla": "TSLA",
    "Saudi Aramco": "2222.SR"
}

selected = st.multiselect(
    "기업 선택",
    list(stocks.keys()),
    default=list(stocks.keys())
)

@st.cache_data(ttl=3600)
def load_data():

    price_df = pd.DataFrame()
    summary = []

    for company, ticker in stocks.items():

        stock = yf.Ticker(ticker)

        hist = stock.history(
            period="1y",
            auto_adjust=True
        )

        if hist.empty:
            continue

        price_df[company] = hist["Close"]

        info = stock.fast_info

        market_cap = info.get("market_cap", None)

        ret = (
            (hist["Close"].iloc[-1] / hist["Close"].iloc[0]) - 1
        ) * 100

        summary.append({
            "Company": company,
            "Ticker": ticker,
            "Current Price": round(hist["Close"].iloc[-1],2),
            "1Y Return (%)": round(ret,2),
            "Market Cap($)": market_cap
        })

    return price_df, pd.DataFrame(summary)

prices, summary = load_data()

prices = prices[selected]

prices = prices.dropna()

normalized = prices / prices.iloc[0] * 100

fig = go.Figure()

for col in normalized.columns:

    fig.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized[col],
            mode="lines",
            name=col,
            line=dict(width=3)
        )
    )

fig.update_layout(
    template="plotly_white",
    height=700,
    hovermode="x unified",
    title="최근 1년 주가 변화 (Start=100)",
    xaxis_title="Date",
    yaxis_title="Normalized Price"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

summary = summary[summary["Company"].isin(selected)]

summary = summary.sort_values(
    "1Y Return (%)",
    ascending=False
)

summary["Market Cap($)"] = summary["Market Cap($)"].apply(
    lambda x: f"{x/1e12:.2f} T" if pd.notnull(x) else "-"
)

st.subheader("📊 기업별 성과")

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

col1,col2,col3 = st.columns(3)

best = summary.iloc[0]

col1.metric(
    "🏆 최고 수익률",
    best["Company"]
)

col2.metric(
    "1년 수익률",
    f"{best['1Y Return (%)']} %"
)

col3.metric(
    "현재 주가",
    f"${best['Current Price']}"
)
