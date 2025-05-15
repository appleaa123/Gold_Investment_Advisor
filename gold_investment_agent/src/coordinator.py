# coordinator.py
# Purpose: Aggregate outputs from all agents and synthesize a final investment recommendation.
# Implements decision synthesis logic and summary reporting for the user interface.
#
# Dependencies:
# - Agent classes from src/agents/

class Coordinator:
    """
    Aggregates agent outputs and synthesizes a final investment recommendation.
    """
    def __init__(self, agents: list):
        """
        Initializes the Coordinator with a list of agent instances.
        """
        self.agents = agents

    def run_analysis(self) -> dict:
        """
        Runs all agents in sequence, collects their outputs, and synthesizes a final recommendation.
        Returns the full state dictionary including all agent analyses and the final recommendation.
        """
        state = {}
        for agent in self.agents:
            state = agent.analyze(state)
        # Synthesize a final recommendation based on agent outputs
        recommendation = self.synthesize(state)
        state['final_recommendation'] = recommendation
        return state

    def synthesize(self, state: dict) -> str:
        """
        Synthesizes a final investment recommendation based on agent outputs in the state.
        This is a placeholder; real logic can be more sophisticated.
        """
        # Example: simple rule-based synthesis (placeholder)
        # You can expand this logic based on actual agent outputs
        analyses = [
            state.get('economic_analysis', ''),
            state.get('currency_analysis', ''),
            state.get('geopolitical_analysis', ''),
            state.get('supply_demand_analysis', ''),
            state.get('sentiment_analysis', ''),
            state.get('technical_analysis', '')
        ]
        summary = " | ".join([a for a in analyses if a])
        # Placeholder recommendation logic
        if "high" in summary.lower() or "bullish" in summary.lower():
            return "Buy (placeholder logic)"
        elif "low" in summary.lower() or "bearish" in summary.lower():
            return "Sell (placeholder logic)"
        else:
            return "Hold (placeholder logic)" 