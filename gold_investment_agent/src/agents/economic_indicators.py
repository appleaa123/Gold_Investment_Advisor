# economic_indicators.py
# Purpose: Analyze macroeconomic indicators affecting gold prices (inflation, interest rates, GDP, unemployment)
# This agent fetches and analyzes economic data to assess its impact on gold prices.
#
# Dependencies:
# - akshare (for macroeconomic data)
# - Output: {agent, signal, confidence, reasoning}

import akshare as ak

class EconomicIndicatorsAgent:
    """
    Agent to analyze macroeconomic indicators (inflation, interest rates, GDP, unemployment)
    and assess their impact on gold prices. Uses Akshare for data.
    """
    def __init__(self):
        pass

    def analyze(self, state: dict) -> dict:
        """
        Fetches macroeconomic indicators using Akshare, analyzes them, and returns a structured output.
        Users can adjust endpoints or currencies as needed.
        """
        try:
            # Example: Use global CPI and interest rate (adjust endpoints as needed)
            cpi_df = ak.macro_euro_cpi_yearly()  # Example: Eurozone CPI
            ir_df = ak.macro_euro_interest_rate()  # Example: Eurozone interest rate
            # Use latest values
            cpi = float(cpi_df.iloc[-1]['value']) if not cpi_df.empty else None
            ir = float(ir_df.iloc[-1]['value']) if not ir_df.empty else None
            # Example logic: high inflation and low rates are bullish for gold
            if cpi and ir is not None:
                if cpi > 2.5 and ir < 2.0:
                    signal = "Buy"
                    confidence = 0.8
                    reasoning = f"CPI is {cpi}%, interest rate is {ir}%. High inflation and low rates are bullish for gold."
                elif cpi < 1.5 and ir > 2.5:
                    signal = "Sell"
                    confidence = 0.7
                    reasoning = f"CPI is {cpi}%, interest rate is {ir}%. Low inflation and high rates are bearish for gold."
                else:
                    signal = "Hold"
                    confidence = 0.5
                    reasoning = f"CPI is {cpi}%, interest rate is {ir}%. No strong macro signal for gold."
            else:
                signal = "Hold"
                confidence = 0.3
                reasoning = "Could not fetch macroeconomic data."
        except Exception as e:
            signal = "Hold"
            confidence = 0.1
            reasoning = f"Error fetching macroeconomic data: {e}"
        return {
            "agent": "EconomicIndicatorsAgent",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning
        } 