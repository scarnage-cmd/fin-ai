def evaluate_risk_opportunity_signals(info, volatility):
    """
    Evaluates risk and opportunity rules based on financial metrics and volatility.
    """
    risks = []
    opportunities = []
    
    # 1. P/E Ratio Evaluation
    pe_ratio = info.get("trailingPE")
    if isinstance(pe_ratio, (int, float)):
        if pe_ratio > 35:
            risks.append(f"High Valuation Risk: Trailing P/E of {pe_ratio:.2f} is relatively high compared to broader market averages.")
        elif 0 < pe_ratio < 20:
            opportunities.append(f"Attractive Valuation: Trailing P/E of {pe_ratio:.2f} indicates reasonable pricing relative to earnings.")
            
    # 2. Volatility Evaluation (Risk)
    if isinstance(volatility, (int, float)) and volatility > 30:
        risks.append(f"High Price Volatility: Annualized volatility stands at {volatility:.2f}%, indicating short-term market uncertainty.")
    elif isinstance(volatility, (int, float)) and volatility <= 20:
        opportunities.append(f"Stable Price Action: Annualized volatility is moderate at {volatility:.2f}%, reflecting steady trading patterns.")
        
    # 3. Dividend Yield Check (Opportunity)
    dividend_yield = info.get("dividendYield")
    if isinstance(dividend_yield, (int, float)) and dividend_yield > 0.015:
        opportunities.append(f"Income Generation: Offers a dividend yield of {dividend_yield * 100:.2f}%, appealing to income-focused investors.")
        
    # Fallbacks if data is sparse
    if not risks:
        risks.append("Standard market risks apply; monitor quarterly earnings reports closely.")
    if not opportunities:
        opportunities.append("Balanced market position with steady operational footprint.")
        
    return risks, opportunities