def generate_research_summary(company_name, ticker, current_price, pe_ratio, volatility, overall_sentiment, risks, opportunities):
    """
    Synthesizes calculated metrics and sentiment into a structured research narrative.
    Designed to prevent hallucinations by utilizing pre-calculated Python variables.
    """
    
    summary_text = f"""
    ### Executive Research Brief: {company_name} ({ticker})
    
    **Current Market Standing:**
    {company_name} is currently trading at **₹{current_price:,.2f}**. Based on our automated analysis, the trailing P/E ratio is evaluated at **{pe_ratio}** with an annualized volatility index of **{volatility:.2f}%**.
    
    **NLP Sentiment Outlook:**
    Recent market news analysis indicates a **{overall_sentiment}** trajectory across major financial publishers, reflecting prevailing market sentiment and recent headlines.
    
    **Strategic Takeaways:**
    * **Primary Opportunity Drivers:** {opportunities[0] if opportunities else 'Stable market footprint with standard growth potential.'}
    * **Key Risk Factors:** {risks[0] if risks else 'Standard market volatility applies; track upcoming quarterly disclosures.'}
    
    *Disclaimer: FinMind AI is a decision-support research platform designed for educational and analytical exploration. This output does not constitute guaranteed financial advice or investment recommendations.*
    """
    
    return summary_text