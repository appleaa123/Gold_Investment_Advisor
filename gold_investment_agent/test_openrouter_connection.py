"""
Script: test_openrouter_connection.py
Purpose: Test the connection to the OpenRouter LLM API using environment variables and the env_loader utility.
Usage:
    python test_openrouter_connection.py
Dependencies:
    - requests
    - python-dotenv
    - src/tools/env_loader.py
"""

import sys
import requests
from src.tools.env_loader import get_openrouter_config

def main():
    # Get API key and model from environment
    try:
        api_key, model = get_openrouter_config()
    except EnvironmentError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # Prepare request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello, world!"}]
    }
    url = "https://openrouter.ai/api/v1/chat/completions"

    # Make API call
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to connect to OpenRouter API: {e}")
        sys.exit(1)

    # Parse and display result
    try:
        result = response.json()
        print("[SUCCESS] OpenRouter API connection successful!")
        print("Sample response:", result.get("choices", [{}])[0].get("message", {}).get("content", "No content returned."))
    except Exception as e:
        print(f"[ERROR] Could not parse API response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 