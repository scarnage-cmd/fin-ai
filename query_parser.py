import os
import yfinance as yf
from google import genai
from dotenv import load_dotenv

# Load settings
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def parse_natural_language_query(query_text):
    if not query_text or len(query_text.strip()) < 3:
        return "Please enter a valid financial question (e.g., 'What is the P/E of TCS?')."

    query_lower = query_text.lower().strip()
    
    # 1. Deterministic Lookups (Fastest, no API cost)
    ticker_map = {
        "reliance": "RELIANCE.NS",
        "tcs": "TCS.NS",
        "infosys": "INFY.NS",
        "infy": "INFY.NS",
        "hdfc": "HDFCBANK.NS",
        "icici": "ICICIBANK.NS"
    }
    
    ticker = next((v for k, v in ticker_map.items() if k in query_lower), None)
    
    if ticker and any(word in query_lower for word in ["price", "pe", "p/e", "market cap", "valuation"]):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            name = info.get("longName", ticker)
            
            if "price" in query_lower:
                return f"The current price of **{name}** is **₹{info.get('currentPrice', 'N/A')}**."
            elif "pe" in query_lower or "p/e" in query_lower:
                return f"The trailing P/E of **{name}** is **{info.get('trailingPE', 'N/A')}**."
            elif "market cap" in query_lower:
                mcap = info.get('marketCap', 0)
                return f"The Market Cap of **{name}** is **₹{mcap:,}**."
        except Exception:
            pass # Fallback to LLM if yfinance fails

# 2. Generative AI Fallback (For general investment questions)
    if not api_key:
        return "I'm ready! Please configure your GEMINI_API_KEY to enable AI answers."
        
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-3.5-flash',  # Switched to gemini-3.5-flash for high stability
            contents=f"You are a finance expert. Answer this: {query_text}",
        )
        return response.text
    except Exception as e:
        # Instant local backup answer if servers are busy, so the app never fails!
        query_lower = query_text.lower()
        if "invest" in query_lower:
            return (
                "### 💡 Guide: How to Start Investing\n"
                "1. **Define Goals:** Align investments with your financial timeline.\n"
                "2. **Emergency Fund:** Secure 3-6 months of living expenses first.\n"
                "3. **Open Demat Account:** Use a registered broker in India.\n"
                "4. **Diversify:** Spread risk across mutual funds, index funds, and blue-chip equities."
            )
        return f"💡 **FinMind AI Assistant:** The AI service is momentarily busy. Please try clicking **Ask Assistant** again in a few seconds!"