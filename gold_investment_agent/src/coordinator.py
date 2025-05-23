# coordinator.py
# Purpose: Aggregate outputs from all agents, act as the debate room, and synthesize a final investment recommendation with confidence and reasoning.
# Implements decision synthesis logic, weighted voting, and summary reporting for the user interface.
#
# Dependencies:
# - Agent classes from src/agents/

class Coordinator:
    """
    Aggregates agent outputs, facilitates debate, and synthesizes a final investment recommendation.
    Each agent returns a structured output: {agent, signal, confidence, reasoning, ...}.
    The coordinator performs weighted voting and aggregates explanations.
    """
    def __init__(self, agents: list, weights: dict = None):
        """
        Initializes the Coordinator with a list of agent instances and optional custom weights.
        """
        self.agents = agents
        # Assign weights to each agent for decision synthesis
        self.weights = weights or {
            "EconomicIndicatorsAgent": 0.3,
            "TechnicalFactorsAgent": 0.2,
            "InvestorSentimentAgent": 0.2,
            "CurrencyMovementsAgent": 0.1,
            "GeopoliticalEventsAgent": 0.1,
            "SupplyDemandAgent": 0.1,
        }

    def run_analysis(self) -> dict:
        """
        Runs all agents, collects their structured outputs, and synthesizes a final recommendation.
        Returns a dict with recommendation, confidence, reasoning, all agent outputs, and a summary table.
        """
        agent_outputs = []
        for agent in self.agents:
            try:
                agent_outputs.append(agent.analyze({}))
            except Exception as e:
                agent_outputs.append({
                    "agent": agent.__class__.__name__,
                    "signal": "Hold",
                    "confidence": 0.0,
                    "reasoning": f"Error running agent: {e}"
                })
        result = self.synthesize(agent_outputs)
        return result

    def synthesize(self, agent_outputs: list) -> dict:
        """
        Synthesizes a final investment recommendation based on agent outputs using weighted voting.
        Returns a structured dict with recommendation, confidence, reasoning, agent_outputs, and a summary table.
        """
        scores = {"Buy": 0, "Sell": 0, "Hold": 0}
        explanations = []
        summary_table = []
        for output in agent_outputs:
            agent = output.get("agent", "UnknownAgent")
            signal = output.get("signal", "Hold")
            confidence = output.get("confidence", 0.5)
            reasoning = output.get("reasoning", "")
            w = self.weights.get(agent, 0.1)
            scores[signal] += w * confidence
            explanations.append(f"{agent}: {reasoning}")
            summary_table.append({
                "agent": agent,
                "signal": signal,
                "confidence": confidence,
                "reasoning": reasoning,
                **{k: v for k, v in output.items() if k not in ['agent', 'signal', 'confidence', 'reasoning']}
            })
        recommendation = max(scores, key=scores.get)
        total_score = sum(scores.values())
        confidence = scores[recommendation] / total_score if total_score > 0 else 0.0
        reasoning = " | ".join(explanations)
        return {
            "recommendation": recommendation,
            "confidence": confidence,
            "reasoning": reasoning,
            "agent_outputs": agent_outputs,
            "summary_table": summary_table
        } 