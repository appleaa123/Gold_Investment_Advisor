# technical_factors.py
# Purpose: Perform technical analysis (moving averages, RSI, etc.) on gold price data.
# This agent generates technical signals to inform gold investment decisions.
#
# Dependencies:
# - akshare (for gold price data)
# - Output: {agent, signal, confidence, reasoning}

import akshare as ak
import pandas as pd


class TechnicalFactorsAgent:
    """
    Agent to perform technical analysis (moving averages, RSI, etc.) on gold price data.
    Uses Akshare for gold price data. Users can adjust endpoints or currencies as needed.
    """
    def __init__(self, symbol="AU9999"):
        self.symbol = symbol  # Users can adjust the gold symbol as needed

    def analyze(self, state: dict) -> dict:
        """
        Fetches gold price data using Akshare, computes technical indicators, and returns a structured output.
        """
        try:
            # Fetch historical gold price data (Shanghai Gold Exchange AU9999 as example)
            df = ak.gold_spot_hist_sina(symbol=self.symbol)
            if not df.empty:
                df['close'] = pd.to_numeric(df['close'], errors='coerce')
                ma20 = df['close'].rolling(window=20).mean().iloc[-1]
                ma50 = df['close'].rolling(window=50).mean().iloc[-1]
                # Simple RSI calculation
                delta = df['close'].diff()
                gain = delta.where(delta > 0, 0).rolling(window=14).mean().iloc[-1]
                loss = -delta.where(delta < 0, 0).rolling(window=14).mean().iloc[-1]
                rs = gain / (loss + 1e-9)
                rsi14 = 100 - (100 / (1 + rs))
                # Example logic
                if ma20 > ma50 and rsi14 < 70:
                    signal = "Buy"
                    confidence = 0.7
                    reasoning = f"MA20 ({ma20:.2f}) > MA50 ({ma50:.2f}), RSI14={rsi14:.1f}. Bullish technicals."
                elif ma20 < ma50 and rsi14 > 30:
                    signal = "Sell"
                    confidence = 0.7
                    reasoning = f"MA20 ({ma20:.2f}) < MA50 ({ma50:.2f}), RSI14={rsi14:.1f}. Bearish technicals."
                else:
                    signal = "Hold"
                    confidence = 0.5
                    reasoning = f"MA20={ma20:.2f}, MA50={ma50:.2f}, RSI14={rsi14:.1f}. No strong technical signal."
            else:
                signal = "Hold"
                confidence = 0.3
                reasoning = "No gold price data available."
        except Exception as e:
            signal = "Hold"
            confidence = 0.1
            reasoning = f"Error fetching gold price data: {e}"
        return {
            "agent": "TechnicalFactorsAgent",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning
        } 