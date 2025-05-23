# geopolitical_events.py
# Purpose: Monitor and analyze global macroeconomic and geopolitical events that influence gold prices.
# This agent processes macro event data to assess risk for gold investment.
#
# Dependencies:
# - akshare (for macro event data)
# - Output: {agent, signal, confidence, reasoning, event_count, high_importance_count, events}

import akshare as ak
from datetime import datetime

class GeopoliticalEventsAgent:
    """
    Agent to monitor and analyze global macroeconomic and geopolitical events
    that may influence gold prices. Uses Akshare for macro event data.
    """

    def __init__(self, date=None):
        # Default to today if no date is provided
        self.date = date or datetime.now().strftime("%Y%m%d")

    def fetch_macro_events(self):
        """
        Fetch global macroeconomic events for the given date using AKShare.
        Returns:
            DataFrame: Combined events from macro_info_ws and news_economic_baidu.
        """
        try:
            ws_df = ak.macro_info_ws(date=self.date)
        except Exception:
            ws_df = None
        try:
            baidu_df = ak.news_economic_baidu(date=self.date)
        except Exception:
            baidu_df = None
        return ws_df, baidu_df

    def analyze(self, state: dict) -> dict:
        """
        Fetches global macroeconomic events, analyzes their risk, and returns a structured output.
        """
        try:
            ws_df, baidu_df = self.fetch_macro_events()
            event_count = 0
            high_importance_count = 0
            reasoning = ""
            events = []

            # Analyze Wallstreetcn macro calendar
            if ws_df is not None and not ws_df.empty:
                # Importance: 3=high, 2=medium, 1=low
                high_importance = ws_df[ws_df['重要性'] >= 2]
                high_importance_count += len(high_importance)
                event_count += len(ws_df)
                events += high_importance[['时间', '地区', '事件', '重要性']].to_dict(orient='records')

            # Analyze Baidu macro events
            if baidu_df is not None and not baidu_df.empty:
                # Importance: higher number = more important
                high_importance_baidu = baidu_df[baidu_df['重要性'] >= 2]
                high_importance_count += len(high_importance_baidu)
                event_count += len(baidu_df)
                events += high_importance_baidu[['日期', '时间', '地区', '事件', '重要性']].to_dict(orient='records')

            # Simple logic: many high-importance events = risk = bullish for gold
            if high_importance_count >= 5:
                signal = "Buy"
                confidence = 0.7
                reasoning = f"{high_importance_count} high-importance macro events detected today. Gold is a safe haven."
            elif high_importance_count == 0:
                signal = "Hold"
                confidence = 0.4
                reasoning = "No significant macroeconomic/geopolitical events today."
            else:
                signal = "Hold"
                confidence = 0.5
                reasoning = f"{high_importance_count} moderate macro events. No strong risk signal."

        except Exception as e:
            signal = "Hold"
            confidence = 0.1
            reasoning = f"Error fetching macroeconomic event data: {e}"
            event_count = 0
            high_importance_count = 0
            events = []

        return {
            "agent": "GeopoliticalEventsAgent",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning,
            "event_count": event_count,
            "high_importance_count": high_importance_count,
            "events": events,
            "date": self.date
        } 