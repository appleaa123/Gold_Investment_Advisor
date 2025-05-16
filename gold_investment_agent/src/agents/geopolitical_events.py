# geopolitical_events.py
# Purpose: Monitor and analyze geopolitical events (wars, elections, trade tensions) that influence gold prices.
# This agent processes news and event data to assess geopolitical risk for gold investment.
#
# Dependencies:
# - akshare (for news data)
# - Output: {agent, signal, confidence, reasoning}

import akshare as ak

class GeopoliticalEventsAgent:
    """
    Agent to monitor and analyze geopolitical events (wars, elections, trade tensions)
    that may influence gold prices. Uses Akshare for news data. Users can adjust endpoints or keywords as needed.
    """
    def __init__(self, keyword="地缘政治"):
        self.keyword = keyword  # Users can adjust the news keyword as needed

    def analyze(self, state: dict) -> dict:
        """
        Fetches recent news using Akshare, looks for geopolitical event keywords, and returns a structured output.
        """
        try:
            # Fetch latest news related to geopolitics
            news_df = ak.news_cctv(keyword=self.keyword)
            if not news_df.empty:
                # Simple logic: count number of news items mentioning "冲突" (conflict), "战争" (war), etc.
                event_words = ["冲突", "战争", "制裁", "选举", "危机"]
                event_count = news_df['content'].str.count('|'.join(event_words)).sum()
                if event_count > 2:
                    signal = "Buy"
                    confidence = 0.6
                    reasoning = f"{event_count} recent news items mention geopolitical risks. Bullish for gold."
                elif event_count == 0:
                    signal = "Hold"
                    confidence = 0.4
                    reasoning = "No recent news of geopolitical risk."
                else:
                    signal = "Hold"
                    confidence = 0.5
                    reasoning = f"{event_count} recent news items mention minor geopolitical risks."
            else:
                signal = "Hold"
                confidence = 0.3
                reasoning = "No recent geopolitical news data available."
        except Exception as e:
            signal = "Hold"
            confidence = 0.1
            reasoning = f"Error fetching geopolitical news data: {e}"
        return {
            "agent": "GeopoliticalEventsAgent",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning
        } 