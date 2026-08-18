import streamlit as st
import yfinance as yf
import pandas as pd
from analysis import calculate_technical_indicators
from news import fetch_company_news
from sentiment import analyze_news_sentiment
from rules import evaluate_risk_opportunity_signals
from report import generate_research_summary
from database import init_db, save_search_record, get_search_history
from query_parser import parse_natural_language_query
from screener import get_screened_stocks
from pdf_generator import generate_pdf_report

# 1. Initialize SQLite Database
init_db()

# 2. Page Configuration
st.set_page_config(
    page_title="FinMind AI — Financial Research",
    page_icon="📈",
    layout="wide"
)

# Force Dark Mode & Modern CSS Injection
st.markdown("""
<style>
    /* Global Dark Theme Overrides */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    /* Card Container Styling */
    div.stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    /* Headers Polish */
    h1, h2, h3 {
        letter-spacing: -0.5px;
        color: #58a6ff;
    }
    /* Sidebar adjustments */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation & Mode Selector
st.sidebar.header("Research Navigation")
app_mode = st.sidebar.radio("Select Mode", [
    "Single Stock Research", 
    "Compare Companies", 
    "Ask FinMind AI (NL Queries)",
    "Stock Screener"
])

st.sidebar.markdown("---")
st.sidebar.subheader("Recent Search History")
history_records = get_search_history()
if history_records:
    for rec in history_records:
        st.sidebar.text(f"{rec[0]} | ₹{rec[2]} | {rec[4].split()[1]}")
else:
    st.sidebar.text("No history recorded yet.")

# 4. Main Application Modes
if app_mode == "Single Stock Research":
    st.title("FinMind AI — Automated Financial Research Platform")
    st.markdown("---")
    
    ticker_input = st.text_input("Enter Stock Ticker (e.g., RELIANCE.NS, TCS.NS):", value="RELIANCE.NS").upper()
    fetch_btn = st.button("Fetch Analysis")
    
    if fetch_btn:
        with st.spinner(f"Analyzing {ticker_input}..."):
            try:
                stock = yf.Ticker(ticker_input)
                hist = stock.history(period="1y")
                info = stock.info
                
                if hist.empty:
                    st.error(f"No market data found for '{ticker_input}'.")
                else:
                    st.success(f"Successfully loaded research profile for {ticker_input}!")
                    processed_hist, volatility = calculate_technical_indicators(hist)
                    
                    company_name = info.get("longName", ticker_input)
                    sector = info.get("sector", "N/A")
                    industry = info.get("industry", "N/A")
                    
                    st.subheader(f"Company Profile: {company_name}")
                    st.write(f"**Sector:** {sector} | **Industry:** {industry}")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
                    previous_close = info.get("previousClose", current_price)
                    price_change = current_price - previous_close
                    price_change_pct = (price_change / previous_close) * 100 if previous_close else 0
                    market_cap = info.get("marketCap", 0)
                    pe_ratio = info.get("trailingPE", "N/A")
                    
                    with col1:
                        st.metric("Stock Price", f"₹{current_price:,.2f}", f"{price_change_pct:.2f}%")
                    with col2:
                        st.metric("Market Cap", f"₹{market_cap:,.0f}" if market_cap else "N/A")
                    with col3:
                        st.metric("Trailing P/E", f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A")
                    with col4:
                        st.metric("Annualized Volatility (Risk)", f"{volatility:.2f}%" if not pd.isna(volatility) else "N/A")
                    
                    st.markdown("---")
                    st.subheader("1-Year Price Trend & Moving Averages")
                    st.line_chart(processed_hist[['Close', 'SMA_50', 'SMA_200']].dropna())
                    
                    st.markdown("---")
                    st.subheader("Explainable Risk & Opportunity Signals")
                    risks, opportunities = evaluate_risk_opportunity_signals(info, volatility)
                    sig_col1, sig_col2 = st.columns(2)
                    with sig_col1:
                        st.markdown("### 🛑 Risk Signals")
                        for r in risks: st.warning(r)
                    with sig_col2:
                        st.markdown("### 🎯 Opportunity Signals")
                        for o in opportunities: st.success(o)
                    
                    st.markdown("---")
                    st.subheader("Market News & NLP Sentiment Scoring")
                    news_items = fetch_company_news(ticker_input)
                    scored_news, overall_sentiment = analyze_news_sentiment(news_items)
                    st.markdown(f"**Overall News Sentiment Outlook:** {overall_sentiment}")
                    for article in scored_news:
                        st.markdown(f"- **[{article['publisher']}]** [{article['title']}]({article['link']}) — *Sentiment:* **{article['sentiment']}**")
                    
                    save_search_record(ticker_input, company_name, current_price, pe_ratio, overall_sentiment)
                    
                    st.markdown("---")
                    st.subheader("🤖 Automated AI Research Report Brief")
                    report_content = generate_research_summary(company_name, ticker_input, current_price, pe_ratio, volatility, overall_sentiment, risks, opportunities)
                    st.info(report_content)
                    
                    # PDF Export Button Integration
                    pdf_filename = generate_pdf_report(
                        company_name=company_name,
                        ticker=ticker_input,
                        current_price=current_price,
                        pe_ratio=pe_ratio,
                        volatility=volatility,
                        sentiment=overall_sentiment,
                        risks=risks,
                        opportunities=opportunities
                    )
                    
                    with open(pdf_filename, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download Executive PDF Report",
                            data=pdf_file,
                            file_name=pdf_filename,
                            mime="application/pdf"
                        )
                    
            except Exception as e:
                st.error(f"Error: {e}")

elif app_mode == "Compare Companies":
    st.title("FinMind AI — Multi-Company Comparison Terminal")
    st.markdown("Compare two equities side-by-side to evaluate valuation, volatility, and market positioning.")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        ticker1 = st.text_input("First Ticker:", value="RELIANCE.NS").upper()
    with col_b:
        ticker2 = st.text_input("Second Ticker:", value="TCS.NS").upper()
        
    if st.button("Compare Tickers"):
        with st.spinner("Fetching comparative market data..."):
            try:
                stock1 = yf.Ticker(ticker1)
                stock2 = yf.Ticker(ticker2)
                
                info1 = stock1.info
                info2 = stock2.info
                hist1 = stock1.history(period="1y")['Close']
                hist2 = stock2.history(period="1y")['Close']
                
                name1 = info1.get("longName", ticker1)
                name2 = info2.get("longName", ticker2)
                
                st.subheader(f"Comparative Breakdown: {name1} vs {name2}")
                
                comp_data = {
                    "Metric": ["Company Name", "Sector", "Current Price (INR)", "Market Cap", "Trailing P/E Ratio"],
                    name1: [
                        name1,
                        info1.get("sector", "N/A"),
                        f"₹{info1.get('currentPrice', info1.get('regularMarketPrice', 0)):,.2f}",
                        f"₹{info1.get('marketCap', 0):,.0f}" if info1.get('marketCap') else "N/A",
                        str(info1.get('trailingPE', 'N/A'))
                    ],
                    name2: [
                        name2,
                        info2.get("sector", "N/A"),
                        f"₹{info2.get('currentPrice', info2.get('regularMarketPrice', 0)):,.2f}",
                        f"₹{info2.get('marketCap', 0):,.0f}" if info2.get('marketCap') else "N/A",
                        str(info2.get('trailingPE', 'N/A'))
                    ]
                }
                
                st.table(pd.DataFrame(comp_data))
                
                st.markdown("### Normalized Price Trend Comparison (1 Year)")
                combined_df = pd.DataFrame({ticker1: hist1, ticker2: hist2}).dropna()
                st.line_chart(combined_df)
                
            except Exception as e:
                st.error(f"Comparison error: {e}")

elif app_mode == "Ask FinMind AI (NL Queries)":
    st.title("FinMind AI — Natural Language Query Assistant")
    st.markdown("Ask financial questions in plain English (e.g., *'How to start investing as a beginner?'* or *'What is the price of Reliance?'*)")
    st.markdown("---")
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    with st.form(key="nl_query_form", clear_on_submit=True):
        user_query = st.text_input("Type your financial research question here and press Enter:")
        submit_btn = st.form_submit_button("Ask Assistant")
        
    if submit_btn and user_query:
        with st.spinner("Processing natural language query..."):
            answer = parse_natural_language_query(user_query)
            st.session_state["chat_history"].insert(0, {"question": user_query, "answer": answer})
            
    if st.session_state["chat_history"]:
        st.markdown("### Conversation History")
        for chat in st.session_state["chat_history"]:
            st.markdown(f"**🗣️ You asked:** {chat['question']}")
            st.success("Answer:")
            st.markdown(chat['answer'])
            st.markdown("---")

elif app_mode == "Stock Screener":
    st.title("FinMind AI — Automated Stock Screener")
    st.markdown("Filter major Indian equities by valuation and yield.")
    
    col1, col2 = st.columns(2)
    with col1:
        max_pe = st.slider("Maximum P/E Ratio:", 0, 100, 30)
    with col2:
        min_yield = st.slider("Minimum Dividend Yield (%):", 0.0, 5.0, 0.5) / 100
        
    if st.button("Run Screener"):
        with st.spinner("Scanning markets..."):
            watchlist = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "ITC.NS", "WIPRO.NS"]
            df_screened = get_screened_stocks(watchlist, max_pe, min_yield)
            
            if not df_screened.empty:
                st.success(f"Found {len(df_screened)} stocks matching your criteria:")
                st.table(df_screened)
            else:
                st.warning("No stocks found matching these criteria. Try relaxing your filters.")