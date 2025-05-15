# technical_factors.py
# Purpose: Perform technical analysis (moving averages, RSI, etc.) on gold price data.
# This agent generates technical signals to inform gold investment decisions.
#
# Dependencies:
# - src.tools.data_tools.add_technical_indicators

from src.tools.data_tools import add_technical_indicators, load_historical_data

class TechnicalFactorsAgent:
    """
    Agent to perform technical analysis (moving averages, RSI, etc.) on gold price data.
    Generates technical signals to inform gold investment decisions.
    """
    def __init__(self, data_path=None):
        self.data_path = data_path or "data/historical_data.csv"

    def analyze(self, state: dict) -> dict:
        """
        Adds technical indicators to gold price data and updates the state with a summary analysis.
        """
        df = load_historical_data(self.data_path)
        if df is not None:
            df = add_technical_indicators(df)
            # Example: summarize latest technicals
            latest = df.iloc[-1] if not df.empty else None
            summary = f"MA20: {latest['ma_20'] if latest is not None else 'N/A'}, " \
                      f"MA50: {latest['ma_50'] if latest is not None else 'N/A'}, " \
                      f"RSI14: {latest['rsi_14'] if latest is not None else 'N/A'}"
        else:
            summary = "Technical analysis not available (no data)."
        state['technical_analysis'] = summary
        return state 