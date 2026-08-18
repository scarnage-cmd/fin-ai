import pandas as pd
import numpy as np

def calculate_technical_indicators(hist_df):
    """
    Calculates moving averages and volatility using Pandas and NumPy.
    This demonstrates custom data processing instead of relying on external APIs.
    """
    if hist_df.empty:
        return hist_df
    
    # Copy DataFrame to avoid modifying original data
    df = hist_df.copy()
    
    # 1. Moving Averages (Trend Analysis)
    # 50-day and 200-day moving averages are standard financial trend indicators
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # 2. Daily Returns Percentage
    df['Daily_Return'] = df['Close'].pct_change() * 100
    
    # 3. Volatility (Risk Indicator) calculated via standard deviation of daily returns
    # Annualized volatility = daily volatility * square root of 252 trading days
    daily_volatility = df['Daily_Return'].std()
    annualized_volatility = daily_volatility * np.sqrt(252)
    
    return df, annualized_volatility