# api_tools.py
# Purpose: Provide functions and classes for accessing financial APIs (MetalpriceAPI, Metals-API, macroeconomic data, etc.)
# Handles API requests, error handling, and rate limiting for agent modules.
#
# References:
# - https://github.com/virattt/ai-hedge-fund/blob/main/src/tools/api.py
# - https://github.com/virattt/ai-hedge-fund/blob/main/.env.example

import os
import requests
from typing import Optional, Dict, Any

class APIKeyError(Exception):
    """Custom exception for missing API keys."""
    pass

class MetalPriceAPIClient:
    """
    Client for MetalpriceAPI (https://metalpriceapi.com/)
    Fetches gold price and currency rates.
    """
    BASE_URL = "https://api.metalpriceapi.com/v1/"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("METALPRICE_API_KEY")
        if not self.api_key:
            raise APIKeyError("METALPRICE_API_KEY is not set in environment variables.")

    def get_gold_price(self, currency: str = "USD") -> Optional[float]:
        """
        Fetches the latest gold price in the specified currency.
        Returns the price as a float, or None if the request fails.
        """
        endpoint = f"{self.BASE_URL}latest"
        params = {"api_key": self.api_key, "base": "XAU", "currencies": currency}
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data["rates"].get(currency)
        except Exception as e:
            print(f"Error fetching gold price: {e}")
            return None

    def get_currency_rate(self, base: str = "USD", target: str = "EUR") -> Optional[float]:
        """
        Fetches the latest exchange rate between two currencies.
        Returns the rate as a float, or None if the request fails.
        """
        endpoint = f"{self.BASE_URL}latest"
        params = {"api_key": self.api_key, "base": base, "currencies": target}
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data["rates"].get(target)
        except Exception as e:
            print(f"Error fetching currency rate: {e}")
            return None

class MacroDataAPIClient:
    """
    Client for macroeconomic data (example: Metals-API or other free sources).
    Fetches indicators like inflation, interest rates, GDP growth, etc.
    """
    BASE_URL = "https://metals-api.com/api/"  # Example; replace with actual endpoint as needed

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("METALS_API_KEY")
        if not self.api_key:
            raise APIKeyError("METALS_API_KEY is not set in environment variables.")

    def get_indicator(self, indicator: str) -> Optional[Any]:
        """
        Fetches a macroeconomic indicator by name.
        Returns the value, or None if the request fails.
        """
        # This is a placeholder; actual implementation depends on the API's capabilities
        endpoint = f"{self.BASE_URL}{indicator}"
        params = {"access_key": self.api_key}
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("value")
        except Exception as e:
            print(f"Error fetching macro indicator '{indicator}': {e}")
            return None

def load_api_keys() -> Dict[str, str]:
    """
    Loads all relevant API keys from environment variables.
    Returns a dictionary of API keys.
    """
    keys = {
        "METALPRICE_API_KEY": os.environ.get("METALPRICE_API_KEY", ""),
        "METALS_API_KEY": os.environ.get("METALS_API_KEY", ""),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "HUGGINGFACE_API_KEY": os.environ.get("HUGGINGFACE_API_KEY", ""),
    }
    return keys 