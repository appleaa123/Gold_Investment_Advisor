# investor_sentiment.py
# Purpose: Analyze investor sentiment from news and social media using NLP techniques.
# This agent uses sentiment analysis to gauge market mood and its impact on gold prices.
#
# Dependencies:
# - akshare (for news data)
# - Output: {agent, signal, confidence, reasoning}

import akshare as ak

class InvestorSentimentAgent:
    """
    Agent to analyze investor sentiment from news and social media using NLP techniques.
    Uses Akshare for news data. Users can adjust endpoints or keywords as needed.
    """
    def __init__(self, keyword="黄金"):
        self.keyword = keyword  # Users can adjust the news keyword as needed

    def analyze(self, state: dict) -> dict:
        """
        Fetches recent news using Akshare, performs simple sentiment analysis, and returns a structured output.
        """
        try:
            # Fetch latest news related to gold ("黄金")
            news_df = ak.news_cctv(keyword=self.keyword)
            if not news_df.empty:
                # Simple sentiment logic: count positive/negative words (placeholder)
                positive_words = ["上涨", "利好", "增持", "创新高"]
                negative_words = ["下跌", "利空", "减持", "创新低"]
                pos_count = news_df['content'].str.count('|'.join(positive_words)).sum()
                neg_count = news_df['content'].str.count('|'.join(negative_words)).sum()
                if pos_count > neg_count:
                    signal = "Buy"
                    confidence = 0.6
                    reasoning = f"Recent news sentiment is positive for gold (pos: {pos_count}, neg: {neg_count})."
                elif neg_count > pos_count:
                    signal = "Sell"
                    confidence = 0.6
                    reasoning = f"Recent news sentiment is negative for gold (pos: {pos_count}, neg: {neg_count})."
                else:
                    signal = "Hold"
                    confidence = 0.4
                    reasoning = f"Recent news sentiment is neutral for gold (pos: {pos_count}, neg: {neg_count})."
            else:
                signal = "Hold"
                confidence = 0.3
                reasoning = "No recent news data available."
        except Exception as e:
            signal = "Hold"
            confidence = 0.1
            reasoning = f"Error fetching news data: {e}"
        return {
            "agent": "InvestorSentimentAgent",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning
        } 