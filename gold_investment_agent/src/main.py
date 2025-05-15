# main.py
# Purpose: Application entry point. Sets up LangGraph, loads agents, and orchestrates the analysis workflow.
# This file runs the end-to-end gold investment analysis pipeline.
#
# Dependencies:
# - All agent classes from src/agents/
# - Coordinator from src/coordinator.py

from src.agents.economic_indicators import EconomicIndicatorsAgent
from src.agents.currency_movements import CurrencyMovementsAgent
from src.agents.geopolitical_events import GeopoliticalEventsAgent
from src.agents.supply_demand import SupplyDemandAgent
from src.agents.investor_sentiment import InvestorSentimentAgent
from src.agents.technical_factors import TechnicalFactorsAgent
from src.coordinator import Coordinator


def main():
    """
    Instantiates all agents, passes them to the Coordinator, runs the analysis,
    and prints the results in a readable format.
    """
    agents = [
        EconomicIndicatorsAgent(),
        CurrencyMovementsAgent(),
        GeopoliticalEventsAgent(),
        SupplyDemandAgent(),
        InvestorSentimentAgent(),
        TechnicalFactorsAgent()
    ]
    coordinator = Coordinator(agents)
    results = coordinator.run_analysis()
    print("\n=== Gold Investment Analysis Results ===")
    for key, value in results.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main() 