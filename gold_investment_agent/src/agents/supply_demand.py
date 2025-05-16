# supply_demand.py
# Purpose: Analyze gold supply and demand factors (production, central bank activity, demand trends).
# This agent evaluates supply and demand data to determine their effect on gold prices.
#
# Dependencies:
# - akshare (for gold supply/demand data)
# - Output: {agent, signal, confidence, reasoning}

import akshare as ak

class SupplyDemandAgent:
    """
    Agent to analyze gold supply and demand factors (production, central bank activity, demand trends)
    and assess their effect on gold prices. Uses Akshare for data. Users can adjust endpoints as needed.
    """
    def __init__(self):
        pass

    def analyze(self, state: dict) -> dict:
        """
        Fetches gold supply/demand data using Akshare, analyzes it, and returns a structured output.
        """
        try:
            # Example: Use world gold demand data (adjust endpoint as needed)
            demand_df = ak.macro_world_gold_demand()
            if not demand_df.empty:
                # Use latest demand value
                latest_demand = float(demand_df.iloc[-1]['value'])
                # Example logic: high demand is bullish for gold
                if latest_demand > 1000:
                    signal = "Buy"
                    confidence = 0.7
                    reasoning = f"World gold demand is {latest_demand}, which is high and bullish for gold."
                elif latest_demand < 800:
                    signal = "Sell"
                    confidence = 0.7
                    reasoning = f"World gold demand is {latest_demand}, which is low and bearish for gold."
                else:
                    signal = "Hold"
                    confidence = 0.5
                    reasoning = f"World gold demand is {latest_demand}, no strong supply/demand signal."
            else:
                signal = "Hold"
                confidence = 0.3
                reasoning = "No gold demand data available."
        except Exception as e:
            signal = "Hold"
            confidence = 0.1
            reasoning = f"Error fetching gold demand data: {e}"
        return {
            "agent": "SupplyDemandAgent",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning
        } 