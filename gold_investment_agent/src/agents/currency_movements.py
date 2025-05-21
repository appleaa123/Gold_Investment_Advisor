# currency_movements.py
# Purpose: Analyze currency exchange rates (especially USD) and their impact on gold prices.
# This agent uses AKShare to fetch currency and gold price data, and summarizes their relationship.
#
# Key Components:
# - CurrencyMovementsAgent: Main agent class for analysis.
# - fetch_currency_rates: Fetches latest USD exchange rates for major currencies.
# - fetch_gold_price: Fetches latest gold ETF (SPDR) holding as a proxy for gold price.
# - analyze: Main method to perform analysis and update shared state.
#
# Dependencies:
# - akshare: For financial and macroeconomic data retrieval.
# - dotenv: For secure API key management (if needed).
#
# Usage:
#   agent = CurrencyMovementsAgent()
#   state = {}
#   updated_state = agent.analyze(state)
#
# Note:
#   - Requires AKShare to be installed: pip install akshare
#   - If using API keys for currency endpoints, set AKSHARE_CURRENCY_API_KEY in your .env file.

import akshare as ak
import os
from dotenv import load_dotenv

class CurrencyMovementsAgent:
    """
    Agent to analyze currency exchange rates (especially USD) and their impact on gold prices.
    Utilizes AKShare to fetch both currency and gold price data, then summarizes their relationship.
    """

    def __init__(self, api_key=None):
        """
        Initialize the agent, loading API key from environment if not provided.
        Args:
            api_key (str, optional): API key for AKShare currency endpoints. Defaults to None.
        """
        load_dotenv()  # Load environment variables from .env file
        self.api_key = api_key or os.getenv("AKSHARE_CURRENCY_API_KEY")
        self.base_currency = "USD"  # Default base currency for analysis

    def fetch_currency_rates(self, symbols=["EUR", "CNY", "JPY"]):
        """
        Fetch the latest exchange rates for USD against major currencies using AKShare.
        Args:
            symbols (list): List of target currency codes (e.g., ["EUR", "CNY", "JPY"]).
        Returns:
            pandas.DataFrame: DataFrame containing currency codes and their latest rates.
        """
        # Example: USD/EUR, USD/CNY, USD/JPY
        rates_df = ak.currency_latest(base=self.base_currency, symbols=",".join(symbols), api_key=self.api_key)
        return rates_df

    def fetch_gold_price(self):
        """
        Fetch the latest gold price data using AKShare's ETF SPDR Gold Trust as a proxy for gold price.
        Returns:
            pandas.DataFrame: DataFrame containing gold ETF holding data.
        """
        gold_df = ak.macro_usa_cme_merchant_goods_holding()
        return gold_df

    def analyze(self, state: dict) -> dict:
        """
        Main analysis method. Fetches relevant currency rates and gold price, analyzes their relationship,
        and updates the shared state with a summary analysis and raw data.
        Args:
            state (dict): Shared state dictionary to be updated with analysis results.
        Returns:
            dict: Updated state with currency and gold analysis.
        """
        # Fetch latest currency rates (USD vs. major currencies)
        currency_rates = self.fetch_currency_rates()
        # Fetch latest gold ETF holding data
        gold_price_df = self.fetch_gold_price()

        # Extract the latest gold ETF holding value (last row, '持仓总量' column)
        latest_gold_price = gold_price_df.iloc[-1]["持仓总量"]  # Adjust column if needed

        # Compose a human-readable analysis summary
        summary = (
            f"Latest USD exchange rates: {currency_rates[['currency', 'rates']].to_dict(orient='records')}\n"
            f"Latest Gold ETF (SPDR) holding: {latest_gold_price}\n"
            "Analysis: If USD strengthens, gold price may weaken (and vice versa). "
            "Recent trends should be monitored for correlation."
        )

        # Update the shared state with analysis and raw data
        state['currency_analysis'] = summary
        state['currency_rates'] = currency_rates
        state['gold_price'] = latest_gold_price
        return state 