# data_tools.py
# Purpose: Provide utilities for loading, cleaning, and preprocessing historical datasets for gold and macroeconomic data.
# Used by agents and simulation modules for offline and fallback analysis.
#
# References:
# - https://github.com/virattt/ai-hedge-fund/blob/main/src/tools/api.py

import pandas as pd
import numpy as np
import os
from typing import Optional


def load_historical_data(filepath: str) -> Optional[pd.DataFrame]:
    """
    Loads historical data from a CSV file into a pandas DataFrame.
    Returns None if the file does not exist or cannot be loaded.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    try:
        df = pd.read_csv(filepath, comment='#')
        return df
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
        return None


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the input DataFrame by handling missing values and outliers.
    - Fills missing values with forward fill, then backward fill.
    - Optionally, clips outliers (can be customized).
    Returns the cleaned DataFrame.
    """
    df = df.copy()
    df = df.fillna(method='ffill').fillna(method='bfill')
    # Example: clip gold price to reasonable range (customize as needed)
    if 'gold_price_usd' in df.columns:
        df['gold_price_usd'] = df['gold_price_usd'].clip(lower=0)
    return df


def merge_macro_and_gold(gold_df: pd.DataFrame, macro_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges gold price data and macroeconomic data on the 'date' column.
    Returns the merged DataFrame.
    """
    merged = pd.merge(gold_df, macro_df, on='date', how='outer', suffixes=('_gold', '_macro'))
    merged = merged.sort_values('date').reset_index(drop=True)
    return merged


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds basic technical indicators (e.g., moving averages, RSI) to the DataFrame.
    Uses pandas for moving averages; TA-Lib can be added for more advanced indicators.
    Returns the DataFrame with new columns.
    """
    df = df.copy()
    if 'gold_price_usd' in df.columns:
        df['ma_20'] = df['gold_price_usd'].rolling(window=20).mean()
        df['ma_50'] = df['gold_price_usd'].rolling(window=50).mean()
        # Example RSI calculation (simple version)
        delta = df['gold_price_usd'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-9)
        df['rsi_14'] = 100 - (100 / (1 + rs))
    return df 