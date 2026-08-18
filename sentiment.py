def analyze_news_sentiment(news_list):
    """
    Performs basic keyword-based sentiment scoring on news headlines.
    Categorizes articles as Positive, Negative, or Neutral.
    """
    positive_keywords = ['growth', 'strong', 'profit', 'surge', 'gain', 'high', 'up', 'record', 'deal', 'success', 'expand']
    negative_keywords = ['fall', 'drop', 'loss', 'decline', 'slump', 'miss', 'probe', 'down', 'risk', 'debt', 'concern']
    
    scored_articles = []
    pos_count = 0
    neg_count = 0
    neu_count = 0
    
    for article in news_list:
        title_lower = article['title'].lower()
        
        # Count keyword occurrences
        pos_score = sum(1 for word in positive_keywords if word in title_lower)
        neg_score = sum(1 for word in negative_keywords if word in title_lower)
        
        if pos_score > neg_score:
            sentiment = "Positive 🟢"
            pos_count += 1
        elif neg_score > pos_score:
            sentiment = "Negative 🔴"
            neg_count += 1
        else:
            sentiment = "Neutral ⚪"
            neu_count += 1
            
        scored_articles.append({
            "title": article['title'],
            "publisher": article['publisher'],
            "link": article['link'],
            "sentiment": sentiment
        })
        
    # Calculate overall market sentiment summary
    total = len(news_list)
    if total == 0:
        overall = "Neutral"
    elif pos_count > neg_count:
        overall = "Bullish / Positive 🟢"
    elif neg_count > pos_count:
        overall = "Bearish / Negative 🔴"
    else:
        overall = "Neutral ⚪"
        
    return scored_articles, overall