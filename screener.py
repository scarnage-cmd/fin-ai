import yfinance as yf
import pandas as pd

def get_screened_stocks(tickers, max_pe, min_div_yield):
    """
    Filters a list of tickers based on user-defined financial criteria.
    """
    results = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        pe = info.get("trailingPE")
        div_yield = info.get("dividendYield", 0)
        
        # Apply Filters
        if isinstance(pe, (int, float)) and pe <= max_pe:
            if div_yield >= min_div_yield:
                results.append({
                    "Ticker": ticker,
                    "Name": info.get("longName", ticker),
                    "P/E Ratio": round(pe, 2),
                    "Dividend Yield": f"{round(div_yield * 100, 2)}%"
                })
    return pd.DataFrame(results)