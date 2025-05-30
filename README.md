# Gold Investment AI Agent
## WARNING
This is a proof of concept for an AI-powered gold investment advisor. The goal of this project is to explore the use of AI to make gold trading decisions. This project is for educational purposes ONLY and is NOT INTENDED for real gold investment, or any investment.

## Overview
This project implements an AI agent system for gold investment analysis, inspired by the [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) project and following the [Product Requirement Document (PRD)](../Gold%20Investment%20AI%20Agent%20PRD.markdown). The system uses multiple specialized agents to analyze economic, technical, and sentiment factors affecting gold prices, synthesizing actionable investment recommendations.

## Akshare Integration & Agent Customization
This project uses [Akshare](https://akshare.akfamily.xyz/tutorial.html) for all data integration, including gold prices, macroeconomic indicators, currency rates, news, and supply/demand data. **Users can adjust currencies, gold symbols, and news keywords in all relevant agent `.py` files** to suit their region or analysis needs. For example:
- `CurrencyMovementsAgent`: Change `base_currency` and `target_currency`.
- `TechnicalFactorsAgent`: Change `symbol` for different gold contracts.
- `InvestorSentimentAgent` and `GeopoliticalEventsAgent`: Change `keyword` for news queries.
- `EconomicIndicatorsAgent` and `SupplyDemandAgent`: Adjust Akshare endpoints for different regions or data sources.

See each agent's source file for details and customization options.

## Directory Structure
```
gold_investment_agent/
├── src/
│   ├── agents/
│   │   ├── economic_indicators.py
│   │   ├── currency_movements.py
│   │   ├── geopolitical_events.py
│   │   ├── supply_demand.py
│   │   ├── investor_sentiment.py
│   │   ├── technical_factors.py
│   ├── tools/
│   │   ├── api_tools.py
│   │   ├── data_tools.py
│   ├── simulation.py
│   ├── main.py
│   ├── coordinator.py
├── data/
│   ├── historical_data.csv
├── logs/
├── .env
├── .env.example
├── web/
│   ├── index.html
├── pyproject.toml
├── README.md
```

## Setup Instructions
1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies using `pip install -r requirements.txt` or `poetry install` if using `pyproject.toml`.
4. Copy `.env.example` to `.env` and add your API keys.
5. Run the main application from `src/main.py`.

## References
- [ai-hedge-fund GitHub repository](https://github.com/virattt/ai-hedge-fund)
- [Product Requirement Document](../Gold%20Investment%20AI%20Agent%20PRD.markdown)
- [Akshare Documentation](https://akshare.akfamily.xyz/tutorial.html)

## License
MIT License 