"""
Module: env_loader.py
Purpose: Securely load environment variables for the Gold Investment Advisor project using python-dotenv.
Key Variables:
    - OPENROUTER_API_KEY: API key for OpenRouter LLM access
    - OPENROUTER_MODEL: Model name for OpenRouter (default: qwen/qwen3-4b:free)
Usage:
    from tools.env_loader import get_openrouter_config
    api_key, model = get_openrouter_config()
Dependencies:
    - python-dotenv (install with `pip install python-dotenv`)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_openrouter_config():
    """
    Returns OpenRouter API key and model name from environment variables.
    Raises an error if the API key is missing.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "qwen/qwen3-4b:free")
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY is not set in the environment.")
    return api_key, model 