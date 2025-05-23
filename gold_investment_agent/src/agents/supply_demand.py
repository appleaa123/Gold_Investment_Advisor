# supply_demand.py
# Purpose: Analyze gold supply and demand factors (ETF holdings, world demand, central bank reserves, production).
# This agent evaluates supply and demand data to determine their effect on gold prices.
#
# Dependencies:
# - akshare (for gold supply/demand data)
# - Output: {agent, signal, confidence, reasoning, etf_holding, world_demand, central_bank_reserves, production}

import akshare as ak
from datetime import datetime

class SupplyDemandAgent:
    """
    Agent to analyze gold supply and demand factors (ETF holdings, world demand, central bank reserves, production)
    and assess their effect on gold prices. Uses Akshare for data.
    """

    def __init__(self):
        pass

    def fetch_etf_holding(self):
        """Fetch latest SPDR Gold Trust ETF holding (proxy for investment demand)."""
        df = ak.macro_usa_cme_merchant_goods_holding()
        latest = df[df['品种'] == '黄金-ETF']
        if not latest.empty:
            return float(latest.iloc[-1]['持仓总量'])
        return None

    def fetch_world_demand(self):
        """Fetch latest world gold demand."""
        try:
            df = ak.macro_world_gold_demand()
            if not df.empty:
                return float(df.iloc[-1]['value'])
        except Exception:
            pass
        return None

    def fetch_central_bank_reserves(self):
        """Fetch latest world central bank gold reserves."""
        try:
            df = ak.macro_world_gold_reserves()
            if not df.empty:
                return float(df.iloc[-1]['value'])
        except Exception:
            pass
        return None

    def fetch_production(self):
        """Fetch latest world gold production."""
        try:
            df = ak.macro_world_gold_production()
            if not df.empty:
                return float(df.iloc[-1]['value'])
        except Exception:
            pass
        return None

    def analyze(self, state: dict) -> dict:
        """
        Fetches gold supply/demand data using Akshare, analyzes it, and returns a structured output.
        """
        try:
            etf_holding = self.fetch_etf_holding()
            world_demand = self.fetch_world_demand()
            central_bank_reserves = self.fetch_central_bank_reserves()
            production = self.fetch_production()

            # Simple logic: rising ETF holdings or demand or reserves = bullish
            bullish = []
            bearish = []
            if etf_holding is not None and etf_holding > 900:  # adjust threshold as needed
                bullish.append(f"ETF holding high ({etf_holding})")
            elif etf_holding is not None:
                bearish.append(f"ETF holding low ({etf_holding})")
            if world_demand is not None and world_demand > 1000:
                bullish.append(f"World demand high ({world_demand})")
            elif world_demand is not None:
                bearish.append(f"World demand low ({world_demand})")
            if central_bank_reserves is not None and central_bank_reserves > 30000:
                bullish.append(f"Central bank reserves high ({central_bank_reserves})")
            elif central_bank_reserves is not None:
                bearish.append(f"Central bank reserves low ({central_bank_reserves})")
            if production is not None and production < 900:
                bullish.append(f"Production low ({production})")
            elif production is not None:
                bearish.append(f"Production high ({production})")

            if len(bullish) > len(bearish):
                signal = "Buy"
                confidence = 0.7
                reasoning = "Bullish supply/demand signals: " + "; ".join(bullish)
            elif len(bearish) > len(bullish):
                signal = "Sell"
                confidence = 0.7
                reasoning = "Bearish supply/demand signals: " + "; ".join(bearish)
            else:
                signal = "Hold"
                confidence = 0.5
                reasoning = "Mixed or neutral supply/demand signals."

        except Exception as e:
            signal = "Hold"
            confidence = 0.1
            reasoning = f"Error fetching supply/demand data: {e}"
            etf_holding = world_demand = central_bank_reserves = production = None

        return {
            "agent": "SupplyDemandAgent",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning,
            "etf_holding": etf_holding,
            "world_demand": world_demand,
            "central_bank_reserves": central_bank_reserves,
            "production": production,
            "timestamp": datetime.now().isoformat()
        } 