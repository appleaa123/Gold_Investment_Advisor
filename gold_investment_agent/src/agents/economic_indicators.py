# economic_indicators.py
# Purpose: Analyze US macroeconomic indicators affecting gold prices (inflation, interest rates, GDP, unemployment)
# This agent fetches and analyzes economic data to assess its impact on gold prices.
#
# Dependencies:
# - akshare (for macroeconomic data)
# - Output: {agent, signal, confidence, reasoning, cpi, interest_rate, gdp, unemployment, timestamp}

import akshare as ak
from datetime import datetime

class EconomicIndicatorsAgent:
    """
    Agent to analyze US macroeconomic indicators (CPI, interest rates, GDP, unemployment)
    and assess their impact on gold prices. Uses Akshare for data.
    """

    def __init__(self):
        pass

    def fetch_us_cpi(self):
        """
        Fetch the latest US CPI (inflation) value using AKShare.
        Returns:
            float or None: Latest CPI value if available, else None.
        """
        df = ak.macro_usa_cpi_monthly()
        latest = df.iloc[-1]
        return float(latest['cpi']) if 'cpi' in latest else None

    def fetch_us_interest_rate(self):
        """
        Fetch the latest US Fed Funds Rate using AKShare.
        Returns:
            float or None: Latest interest rate if available, else None.
        """
        df = ak.macro_usa_interest_rate()
        latest = df.iloc[-1]
        return float(latest['value']) if 'value' in latest else None

    def fetch_us_gdp(self):
        """
        Fetch the latest US GDP growth rate using AKShare.
        Returns:
            float or None: Latest GDP value if available, else None.
        """
        df = ak.macro_usa_gdp_yearly()
        latest = df.iloc[-1]
        return float(latest['gdp']) if 'gdp' in latest else None

    def fetch_us_unemployment(self):
        """
        Fetch the latest US unemployment rate using AKShare.
        Returns:
            float or None: Latest unemployment rate if available, else None.
        """
        df = ak.macro_usa_unemployment_rate()
        latest = df.iloc[-1]
        return float(latest['unemployment_rate']) if 'unemployment_rate' in latest else None

    def analyze(self, state: dict) -> dict:
        """
        Fetches US macroeconomic indicators, analyzes them, and returns a structured output.
        Args:
            state (dict): Shared state dictionary (not used here, but for interface consistency).
        Returns:
            dict: Analysis result with agent, signal, confidence, reasoning, and raw values.
        """
        try:
            cpi = self.fetch_us_cpi()
            ir = self.fetch_us_interest_rate()
            gdp = self.fetch_us_gdp()
            unemp = self.fetch_us_unemployment()

            # Example logic: high inflation and low rates are bullish for gold
            if cpi is not None and ir is not None:
                if cpi > 3.0 and ir < 2.0:
                    signal = "Buy"
                    confidence = 0.8
                    reasoning = f"High inflation ({cpi}%) and low rates ({ir}%) are bullish for gold."
                elif cpi < 2.0 and ir > 3.0:
                    signal = "Sell"
                    confidence = 0.7
                    reasoning = f"Low inflation ({cpi}%) and high rates ({ir}%) are bearish for gold."
                else:
                    signal = "Hold"
                    confidence = 0.5
                    reasoning = f"Mixed macro: CPI={cpi}%, IR={ir}%, GDP={gdp}, Unemployment={unemp}."
            else:
                signal = "Hold"
                confidence = 0.3
                reasoning = "Could not fetch all macroeconomic data."
        except Exception as e:
            signal = "Hold"
            confidence = 0.1
            reasoning = f"Error fetching macroeconomic data: {e}"

        return {
            "agent": "EconomicIndicatorsAgent",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning,
            "cpi": cpi if 'cpi' in locals() else None,
            "interest_rate": ir if 'ir' in locals() else None,
            "gdp": gdp if 'gdp' in locals() else None,
            "unemployment": unemp if 'unemp' in locals() else None,
            "timestamp": datetime.now().isoformat()
        } 