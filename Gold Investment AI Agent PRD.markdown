# Gold Investment AI Agent - Product Requirement Document (MVP)

## 1. Product Overview

This document outlines the requirements for the Minimum Viable Product (MVP) of an AI agent designed to assist with gold investment decisions. The MVP will include core features such as multi-agent analysis, data integration from free sources, decision synthesis, and a basic user interface for interaction. The system will be built using the [LangGraph framework](https://langchain-ai.github.io/langgraph/) and will leverage free APIs or open datasets for data access, ensuring functionality even without paid financial API access.

The agent aims to provide actionable investment recommendations by analyzing key factors affecting gold prices, making it a valuable tool for investors and advisors. Future iterations can add advanced features like predictive models and broader asset analysis.

## 2. Target Audience

- **Individual Investors**: Users seeking informed gold investment decisions.
- **Financial Advisors**: Professionals needing tools to analyze gold markets for clients.
- **Educational Users**: Individuals learning about gold investment through simulations.

The system is designed to be intuitive, delivering clear insights from complex data.

## 3. Key Features

1. **Multi-Agent Analysis**:
   - Six specialized agents analyze factors influencing gold prices:
     - **Economic Indicators Agent**: Examines inflation, interest rates, GDP growth, and unemployment.
     - **Currency Movements Agent**: Tracks currency exchange rates, focusing on the US Dollar.
     - **Geopolitical Events Agent**: Monitors wars, elections, and trade tensions driving safe-haven demand.
     - **Supply and Demand Agent**: Analyzes gold production, central bank purchases, and demand.
     - **Investor Sentiment Agent**: Uses NLP to gauge sentiment from news and social media.
     - **Technical Factors Agent**: Performs technical analysis using indicators like moving averages and RSI.

2. **Data Integration**:
   - Integrates real-time data from free APIs like [MetalpriceAPI](https://metalpriceapi.com/) or [Metals-API](https://metals-api.com/).
   - Uses historical data from open datasets like [datahub.io](https://datahub.io/core/gold-prices) or [Kaggle](https://www.kaggle.com/datasets/sid321axn/gold-price-prediction-dataset) if APIs are unavailable.

3. **Decision Synthesis**:
   - A central coordinator aggregates agent outputs to provide a comprehensive recommendation (e.g., buy, sell, hold).
   - Includes summaries of each agent’s analysis for transparency.

4. **Simulation Mode**:
   - Simulates investment strategies using historical data, providing metrics like return on investment and risk.

5. **User Interface**:
   - A web interface built with [React](https://reactjs.org/) and [Tailwind CSS](https://tailwindcss.com/) allows users to trigger analyses, input parameters, and view results.

## 4. Functional Requirements

1. **Agent Development**:
   - Implement each agent as a Python class in LangGraph.
   - Use specific prompts to define agent roles (e.g., “Analyze inflation rates to assess gold price impact”).
   - Enable data processing from APIs or datasets.

2. **Data Access**:
   - Handle API rate limits and errors for free APIs.
   - Load and update datasets periodically for offline use.

3. **Agent Interaction**:
   - Share data via LangGraph’s shared state.
   - Coordinator aggregates outputs for a final recommendation.

4. **User Interface**:
   - Provide a dashboard with a “Run Analysis” button and recommendation display.
   - Show detailed agent analyses and visualizations.

5. **Simulation**:
   - Simulate strategies with historical data, displaying basic metrics.

6. **Data Flexibility**:
   - Support switching between API and dataset sources via configuration.

7. **Error Handling**:
   - Manage API downtime or missing data with fallbacks (e.g., cached data).

## 5. Non-Functional Requirements

1. **Performance**:
   - Respond to queries within 5 seconds.
   - Optimize data processing for efficiency.

2. **Security**:
   - Store API keys securely using environment variables.
   - Protect user data (e.g., investment amounts).

3. **Scalability**:
   - Handle multiple users simultaneously.
   - Support future feature additions.

4. **Maintainability**:
   - Document code clearly and use modular design.
   - Use Git for version control.

## 6. Technical Requirements

1. **Framework**:
   - [LangGraph](https://langchain-ai.github.io/langgraph/) for multi-agent orchestration.

2. **Programming Language**:
   - Python 3.11+.

3. **Data Sources**:
   - **Primary**: Free APIs ([MetalpriceAPI](https://metalpriceapi.com/), [Metals-API](https://metals-api.com/)).
   - **Secondary**: Open datasets ([datahub.io](https://datahub.io/core/gold-prices), [Kaggle](https://www.kaggle.com/datasets/sid321axn/gold-price-prediction-dataset)).

4. **Libraries**:
   - **Data Analysis**: [pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/), [TA-Lib](https://ta-lib.org/).
   - **NLP**: [Hugging Face Transformers](https://huggingface.co/docs/transformers/index).
   - **Web Development**: [React](https://reactjs.org/), [Tailwind CSS](https://tailwindcss.com/).

5. **Debugging**:
   - Use [LangSmith](https://smith.langchain.com/) for monitoring and debugging.

6. **API Key Management**:
   - Store keys in `.env` files or secure vaults.

## 7. User Stories

| **User Story** | **Description** |
|----------------|---------------|
| As an investor | I want a daily summary of gold price factors to make informed decisions. |
| As a financial advisor | I want to simulate strategies to advise clients. |
| As a user | I want real-time insights on geopolitical impacts on gold prices. |

## 8. Success Metrics

1. **Accuracy**: Compare recommendations to market outcomes.
2. **User Satisfaction**: Gather feedback on usability.
3. **Adoption Rate**: Track user numbers and usage frequency.
4. **Simulation Accuracy**: Measure alignment with historical data.

## 9. System Architecture

The system uses LangGraph to manage agents as nodes in a state graph. The workflow:
1. User triggers analysis via the web interface.
2. Coordinator activates agents in parallel.
3. Agents process data and store results in shared state.
4. Coordinator synthesizes outputs for a recommendation.
5. Results are displayed to the user.

## 10. Code Snippets

### 10.1 Economic Indicators Agent
```python
from langgraph.graph import StateGraph
from langchain_community.tools import FinancialDatasetsTool
from dataclasses import dataclass

@dataclass
class AgentState:
    economic_data: dict
    analysis: str

class EconomicIndicatorsAgent:
    def __init__(self):
        self.tool = FinancialDatasetsTool(api_key="YOUR_API_KEY")  # Use MetalpriceAPI
        self.prompt = """
        Analyze recent economic indicators such as inflation rates, interest rates, GDP growth, and unemployment rates to assess their impact on gold prices. Summarize trends, highlight historical correlations, and predict near-term price effects based on current data.
        """

    def analyze(self, state: AgentState) -> AgentState:
        inflation = self.tool.get_economic_indicator("inflation_rate")
        interest_rates = self.tool.get_economic_indicator("interest_rate")
        gdp_growth = self.tool.get_economic_indicator("gdp_growth")
        unemployment = self.tool.get_economic_indicator("unemployment_rate")

        state.economic_data = {
            "inflation": inflation,
            "interest_rates": interest_rates,
            "gdp_growth": gdp_growth,
            "unemployment": unemployment
        }

        analysis = f"""
        Inflation: {inflation}% - High inflation typically supports gold prices.
        Interest Rates: {interest_rates}% - Rising rates may pressure gold.
        GDP Growth: {gdp_growth}% - Slow growth may increase gold demand.
        Unemployment: {unemployment}% - High unemployment may boost safe-haven demand.
        Overall: Bullish if inflation is high and rates are low, otherwise neutral.
        """
        state.analysis = analysis
        return state
```

### 10.2 Investor Sentiment Agent
```python
from transformers import pipeline
from langgraph.graph import StateGraph
from dataclasses import dataclass

@dataclass
class AgentState:
    sentiment_data: dict
    sentiment_analysis: str

class InvestorSentimentAgent:
    def __init__(self):
        self.sentiment_pipeline = pipeline("sentiment-analysis")

    def analyze(self, state: AgentState) -> AgentState:
        texts = ["Gold prices are rising due to geopolitical tensions.", "Investors are selling gold amid rising interest rates."]
        sentiments = self.sentiment_pipeline(texts)
        state.sentiment_data = sentiments

        positive_count = sum(1 for s in sentiments if s['label'] == 'POSITIVE')
        negative_count = sum(1 for s in sentiments if s['label'] == 'NEGATIVE')
        state.sentiment_analysis = f"Positive sentiments: {positive_count}, Negative sentiments: {negative_count}"
        return state
```

### 10.3 Central Coordinator
```python
class Coordinator:
    def synthesize(self, state):
        overall_analysis = ""
        if state.economic_analysis:
            overall_analysis += f"Economic Indicators: {state.economic_analysis}\n"
        if state.currency_analysis:
            overall_analysis += f"Currency Movements: {state.currency_analysis}\n"

        final_recommendation = "Based on the analyses, the overall outlook for gold is bullish."
        return final_recommendation
```

### 10.4 System Setup in LangGraph
```python
from langgraph.graph import StateGraph
from agents.economic_indicators import EconomicIndicatorsAgent
from agents.currency_movements import CurrencyMovementsAgent

@dataclass
class GlobalState:
    economic_analysis: str
    currency_analysis: str
    final_recommendation: str

def main():
    graph = StateGraph(GlobalState)
    economic_agent = EconomicIndicatorsAgent()
    graph.add_node("economic", economic_agent.analyze)
    currency_agent = CurrencyMovementsAgent()
    graph.add_node("currency", currency_agent.analyze)
    graph.add_edge("economic", "coordinator")
    graph.add_edge("currency", "coordinator")
    graph.set_entry_point("coordinator")
    final_state = graph.run()
    print(final_state.final_recommendation)

if __name__ == "__main__":
    main()
```

### 10.5 Web Interface (React)
```html
<!DOCTYPE html>
<html>
<head>
  <title>Gold Investment Agent</title>
  <script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.development.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/babel-standalone@7/babel.min.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const App = () => {
      const [recommendation, setRecommendation] = React.useState('');

      const runAnalysis = () => {
        // Placeholder for API call to backend
        setRecommendation('Based on the analyses, the overall outlook for gold is bullish.');
      };

      return (
        <div className="container mx-auto p-4">
          <h1 className="text-2xl font-bold mb-4">Gold Investment Agent</h1>
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded"
            onClick={runAnalysis}
          >
            Run Analysis
          </button>
          {recommendation && (
            <div className="mt-4 p-4 bg-gray-100 rounded">
              <h2 className="text-xl font-semibold">Recommendation</h2>
              <p>{recommendation}</p>
            </div>
          )}
        </div>
      );
    };

    ReactDOM.render(<App />, document.getElementById('root'));
  </script>
</body>
</html>
```

## 11. Directory Structure
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
│   ├── main.py
│   ├── coordinator.py
├── data/
│   ├── historical_data.csv
├── logs/
├── .env
├── web/
│   ├── index.html
```

## 12. Next Steps
1. **Setup Environment**: Install Python, LangGraph, and required libraries.
2. **Test Agents**: Implement and test one agent (e.g., Economic Indicators) with sample data.
3. **Integrate Data**: Connect to a free API or load a dataset.
4. **Build UI**: Develop the React interface and connect it to the backend.
5. **Iterate**: Add agents and refine based on testing.