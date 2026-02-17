# Macro Economics Integration Strategy for TradingAgents

**Professional Recommendations from Architecture Review**

---

## Executive Summary

**Recommended Approach: Incremental Integration (3 Phases)**

Don't rebuild from scratch. Extend TradingAgents incrementally with macro capabilities while preserving what works. This minimizes risk and allows validation at each step.

**Timeline:** 3-4 weeks  
**Risk Level:** LOW (incremental, reversible)  
**Effort:** MODERATE (leverages existing patterns)

---

## Phase 1: Add Macro Context Layer (Week 1)

### Goal
Enhance existing stock analysis with macro economic context WITHOUT changing core architecture.

### Implementation

#### 1.1 Add FRED Data Tools (2 days)

**Location:** `tradingagents/agents/utils/macro_data_tools.py` (NEW FILE)

```python
from langchain_core.tools import tool
from typing import Annotated
from fredapi import Fred
import os
from datetime import datetime, timedelta

@tool
def get_macro_indicator(
    series_id: Annotated[str, "FRED series ID (e.g., 'GDPC1' for GDP)"],
    lookback_days: Annotated[int, "Number of days to look back"] = 365
) -> str:
    """
    Fetch macro economic indicator from FRED API.
    
    Common series IDs:
    - GDPC1: Real GDP
    - UNRATE: Unemployment Rate
    - CPIAUCSL: Consumer Price Index
    - FEDFUNDS: Federal Funds Rate
    - DGS10: 10-Year Treasury Yield
    """
    fred = Fred(api_key=os.environ.get('FRED_API_KEY'))
    end_date = datetime.now()
    start_date = end_date - timedelta(days=lookback_days)
    
    data = fred.get_series(
        series_id, 
        observation_start=start_date.strftime('%Y-%m-%d')
    )
    
    # Format as CSV with recent values
    recent = data.tail(12)  # Last 12 data points
    csv_output = recent.to_csv()
    
    header = f"# {series_id} - Last 12 observations\n"
    header += f"# Latest value: {data.iloc[-1]:.2f}\n"
    header += f"# Date: {data.index[-1].strftime('%Y-%m-%d')}\n\n"
    
    return header + csv_output


@tool
def get_macro_summary(
    current_date: Annotated[str, "Current date in YYYY-MM-DD format"]
) -> str:
    """
    Get a summary of key macro economic indicators.
    Returns GDP growth, unemployment, inflation, and interest rates.
    """
    fred = Fred(api_key=os.environ.get('FRED_API_KEY'))
    
    indicators = {
        'Real GDP (Quarterly)': 'GDPC1',
        'Unemployment Rate': 'UNRATE',
        'CPI (Inflation)': 'CPIAUCSL',
        'Federal Funds Rate': 'FEDFUNDS',
        '10-Year Treasury': 'DGS10',
        '2-Year Treasury': 'DGS2'
    }
    
    summary = f"# Macro Economic Summary as of {current_date}\n\n"
    
    for name, series_id in indicators.items():
        try:
            data = fred.get_series(series_id)
            latest = data.iloc[-1]
            latest_date = data.index[-1].strftime('%Y-%m-%d')
            
            # Calculate YoY change if applicable
            year_ago = data.iloc[-252] if len(data) > 252 else data.iloc[0]
            change = ((latest - year_ago) / year_ago * 100) if year_ago != 0 else 0
            
            summary += f"{name}: {latest:.2f}"
            if abs(change) > 0.01:
                summary += f" ({change:+.1f}% YoY)"
            summary += f" [as of {latest_date}]\n"
        except Exception as e:
            summary += f"{name}: Data unavailable\n"
    
    return summary
```

**Why this approach:**
- ✅ Minimal changes to existing code
- ✅ Tools follow existing pattern (like `get_stock_data`)
- ✅ Can be used by any analyst agent
- ✅ Easy to test independently

---

#### 1.2 Enhance News Analyst with Macro Context (1 day)

**Location:** `tradingagents/agents/analysts/news_analyst.py`

**Current:** News analyst only looks at company-specific news  
**Enhanced:** Add macro economic context to news analysis

```python
# Add to news_analyst_node tools list:
tools = [
    get_news,
    get_global_news,
    get_macro_summary,  # NEW
]

# Update system prompt:
system_message = (
    "You are a news researcher analyzing recent news and macro economic trends. "
    "Use get_macro_summary to understand the current economic environment, then "
    "analyze how company-specific news fits into the broader macro context. "
    "Consider: Are we in a recession? Is inflation high? Are rates rising? "
    "How does this affect the company's prospects?"
    # ... rest of prompt
)
```

**Impact:**
- News analysis now includes macro context
- Example: "AAPL earnings beat, but consumer spending is weakening (unemployment rising to 4.2%)"
- Zero changes to graph structure

---

#### 1.3 Test with Existing Stocks (1 day)

Run analysis on stocks you've already tested:
- NVDA
- AAPL  
- BRK-B

Compare outputs:
- Before: "AAPL down 10% due to weak iPhone sales"
- After: "AAPL down 10% due to weak iPhone sales amid rising unemployment (4.2%) and consumer spending concerns"

**Validation:** Does macro context improve analysis quality?

---


## Phase 2: Add Dedicated Macro Analyst (Week 2)

### Goal
Create a specialized macro analyst that runs alongside existing analysts, providing economic regime analysis.

### Implementation

#### 2.1 Create Macro Analyst Agent (2 days)

**Location:** `tradingagents/agents/analysts/macro_analyst.py` (NEW FILE)

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def create_macro_analyst(llm):
    def macro_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        
        tools = [
            get_macro_indicator,
            get_macro_summary,
        ]
        
        system_message = (
            "You are a macro economist analyzing the current economic environment. "
            "Your role is to determine the economic regime and assess implications for investments.\n\n"
            
            "Key Analysis Areas:\n"
            "1. Economic Regime: Recession, Expansion, Stagflation, or Soft Landing?\n"
            "2. Interest Rate Environment: Rising, Falling, or Stable?\n"
            "3. Inflation Trend: Accelerating, Decelerating, or Stable?\n"
            "4. Employment Situation: Strong, Weakening, or Deteriorating?\n"
            "5. Fed Policy Stance: Hawkish, Dovish, or Neutral?\n\n"
            
            "Regime Definitions:\n"
            "- Recession: GDP declining, unemployment rising, defensive positioning\n"
            "- Expansion: GDP growing, unemployment low, risk-on environment\n"
            "- Stagflation: High inflation + weak growth, challenging for all assets\n"
            "- Soft Landing: Inflation cooling without recession, goldilocks scenario\n\n"
            
            "For the company {ticker}, assess:\n"
            "- How does current macro regime affect this sector?\n"
            "- Is this a cyclical or defensive stock?\n"
            "- What macro risks should investors watch?\n\n"
            
            "Use get_macro_summary first for overview, then get_macro_indicator for specific data.\n"
            "Provide a clear regime assessment and sector-specific implications."
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are a helpful AI assistant, collaborating with other assistants."
             " Use the provided tools to progress towards answering the question."
             " You have access to the following tools: {tool_names}.\n{system_message}"
             " Current date: {current_date}. Company: {ticker}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)
        
        chain = prompt | llm.bind_tools(tools)
        result = chain.invoke(state["messages"])
        
        report = ""
        if len(result.tool_calls) == 0:
            report = result.content
        
        return {
            "messages": [result],
            "macro_report": report,  # NEW state field
        }
    
    return macro_analyst_node
```

**Why this design:**
- ✅ Follows existing analyst pattern exactly
- ✅ Produces `macro_report` like other analysts produce reports
- ✅ Can be added to graph without breaking existing flow

---

#### 2.2 Update Agent State (1 day)

**Location:** `tradingagents/agents/utils/agent_states.py`

```python
class AgentState(MessagesState):
    company_of_interest: Annotated[str, "Company that we are interested in trading"]
    trade_date: Annotated[str, "What date we are trading at"]
    
    # Existing analyst reports
    market_report: Annotated[str, "Report from the Market Analyst"]
    sentiment_report: Annotated[str, "Report from the Social Media Analyst"]
    news_report: Annotated[str, "Report from the News Researcher"]
    fundamentals_report: Annotated[str, "Report from the Fundamentals Researcher"]
    
    # NEW: Macro report
    macro_report: Annotated[str, "Report from the Macro Economist"]
    
    # ... rest of state
```

---

#### 2.3 Add to Graph (1 day)

**Location:** `tradingagents/graph/setup.py`

```python
def setup_graph(self, selected_analysts=["market", "social", "news", "fundamentals", "macro"]):
    
    # Add macro analyst
    if "macro" in selected_analysts:
        analyst_nodes["macro"] = create_macro_analyst(self.quick_thinking_llm)
        delete_nodes["macro"] = create_msg_delete()
        tool_nodes["macro"] = ToolNode([get_macro_indicator, get_macro_summary])
    
    # ... rest of setup
```

**Graph Flow:**
```
START → Market → Social → News → Fundamentals → Macro → Bull Researcher
```

**Why this works:**
- ✅ Macro analyst runs with other analysts
- ✅ Bull/Bear researchers now have macro context
- ✅ Zero changes to debate or risk management
- ✅ Can be toggled on/off via `selected_analysts`

---

#### 2.4 Update Researchers to Use Macro Context (1 day)

**Location:** `tradingagents/agents/researchers/bull_researcher.py`

```python
def bull_node(state) -> dict:
    # ... existing code ...
    
    market_research_report = state["market_report"]
    sentiment_report = state["sentiment_report"]
    news_report = state["news_report"]
    fundamentals_report = state["fundamentals_report"]
    macro_report = state.get("macro_report", "")  # NEW
    
    curr_situation = (
        f"{market_research_report}\n\n"
        f"{sentiment_report}\n\n"
        f"{news_report}\n\n"
        f"{fundamentals_report}\n\n"
        f"{macro_report}"  # NEW
    )
    
    prompt = f"""You are a Bull Analyst advocating for investing in the stock.
    
    Consider the macro economic environment:
    {macro_report}
    
    Build your bull case considering:
    - Is the current macro regime favorable for this stock?
    - Is this a cyclical stock benefiting from expansion?
    - Or a defensive stock that's overvalued in this environment?
    
    # ... rest of prompt
    """
```

**Impact:**
- Bull/Bear debate now includes macro reasoning
- Example: "While fundamentals are strong, we're entering a recession (GDP -0.5%, unemployment 4.5%). This cyclical stock will face headwinds."

---

#### 2.5 Test Phase 2 (1 day)

Run full analysis with macro analyst enabled:

```python
graph = TradingAgentsGraph(
    selected_analysts=["market", "news", "fundamentals", "macro"],
    config={
        "llm_provider": "bedrock",
        "deep_think_llm": "us.anthropic.claude-sonnet-4-20250514-v1:0",
        "quick_think_llm": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
        # ... rest of config
    }
)

final_state, decision = graph.propagate("AAPL", "2026-02-14")
```

**Validation Questions:**
- Does macro report provide useful context?
- Do researchers incorporate macro reasoning?
- Does final decision quality improve?

---

## Phase 3: Asset Allocation Mode (Week 3-4)

### Goal
Add a new mode that recommends asset class allocation instead of individual stock picks.

### Implementation Strategy

#### 3.1 Create Asset Allocation Mode (3 days)

**Location:** `tradingagents/graph/asset_allocation_graph.py` (NEW FILE)

This is a SEPARATE graph for asset allocation, not modifying the stock analysis graph.

```python
class AssetAllocationGraph:
    """
    Separate graph for macro-driven asset allocation.
    Recommends allocation across stocks, bonds, gold, crypto.
    """
    
    def __init__(self, debug=False, config=None):
        self.debug = debug
        self.config = config or DEFAULT_CONFIG
        
        # Use same LLM setup as TradingAgents
        self.deep_thinking_llm = create_llm_client(...)
        self.quick_thinking_llm = create_llm_client(...)
        
        # Create specialized agents for asset allocation
        self.macro_analyst = create_macro_analyst(self.quick_thinking_llm)
        self.asset_strategist = create_asset_strategist(self.deep_thinking_llm)
        self.portfolio_optimizer = create_portfolio_optimizer(self.quick_thinking_llm)
        
        self.graph = self._setup_allocation_graph()
    
    def _setup_allocation_graph(self):
        workflow = StateGraph(AssetAllocationState)
        
        # Simpler flow: Macro → Strategist → Optimizer
        workflow.add_node("Macro Analyst", self.macro_analyst)
        workflow.add_node("Asset Strategist", self.asset_strategist)
        workflow.add_node("Portfolio Optimizer", self.portfolio_optimizer)
        
        workflow.add_edge(START, "Macro Analyst")
        workflow.add_edge("Macro Analyst", "Asset Strategist")
        workflow.add_edge("Asset Strategist", "Portfolio Optimizer")
        workflow.add_edge("Portfolio Optimizer", END)
        
        return workflow.compile()
    
    def allocate(self, query: str, current_date: str):
        """
        Run asset allocation analysis.
        
        Args:
            query: User query (e.g., "How should I allocate my portfolio?")
            current_date: Current date for analysis
        
        Returns:
            Allocation recommendation (e.g., {"stocks": 60, "bonds": 30, "gold": 10})
        """
        init_state = {
            "query": query,
            "current_date": current_date,
            "messages": [],
        }
        
        final_state = self.graph.invoke(init_state)
        return final_state["allocation"]
```

---

#### 3.2 Create Asset Strategist Agent (2 days)

**Location:** `tradingagents/agents/strategists/asset_strategist.py` (NEW FILE)

```python
def create_asset_strategist(llm):
    """
    Agent that recommends asset class allocation based on macro regime.
    """
    def asset_strategist_node(state):
        macro_report = state["macro_report"]
        current_date = state["current_date"]
        
        system_message = (
            "You are an Asset Allocation Strategist. Based on the macro economic analysis, "
            "recommend allocation percentages across asset classes.\n\n"
            
            "Asset Classes:\n"
            "- Stocks (SPY): High growth potential, high risk, benefits from expansion\n"
            "- Bonds (TLT): Lower risk, benefits from rate cuts, safe haven\n"
            "- Gold (GLD): Inflation hedge, safe haven, no yield\n"
            "- Cash: Zero risk, opportunity cost in expansion\n\n"
            
            "Regime-Based Guidelines:\n"
            "- Recession: 30% stocks, 50% bonds, 15% gold, 5% cash (defensive)\n"
            "- Expansion: 70% stocks, 20% bonds, 5% gold, 5% cash (aggressive)\n"
            "- Stagflation: 40% stocks, 20% bonds, 30% gold, 10% cash (inflation hedge)\n"
            "- Soft Landing: 60% stocks, 30% bonds, 5% gold, 5% cash (balanced)\n\n"
            
            "Adjust based on:\n"
            "- Confidence in regime assessment\n"
            "- Transition risks (e.g., late expansion → recession)\n"
            "- Tail risks (e.g., financial crisis, policy shock)\n\n"
            
            "Output format:\n"
            "{\n"
            '  "regime": "Expansion",\n'
            '  "confidence": "High",\n'
            '  "allocation": {"stocks": 65, "bonds": 25, "gold": 5, "cash": 5},\n'
            '  "rationale": "...",\n'
            '  "risks": "..."\n'
            "}"
        )
        
        prompt = f"""Based on this macro analysis:

{macro_report}

Recommend asset allocation for current date: {current_date}

Provide your recommendation in JSON format as specified."""
        
        result = llm.invoke([
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ])
        
        # Parse JSON from response
        import json
        import re
        
        json_match = re.search(r'\{.*\}', result.content, re.DOTALL)
        if json_match:
            allocation_data = json.loads(json_match.group())
        else:
            # Fallback to balanced allocation
            allocation_data = {
                "regime": "Unknown",
                "confidence": "Low",
                "allocation": {"stocks": 60, "bonds": 30, "gold": 5, "cash": 5},
                "rationale": "Unable to parse recommendation, using balanced allocation",
                "risks": "Analysis incomplete"
            }
        
        return {
            "allocation": allocation_data["allocation"],
            "allocation_report": result.content,
        }
    
    return asset_strategist_node
```

---

#### 3.3 Usage Example (1 day)

```python
# Stock analysis (existing)
stock_graph = TradingAgentsGraph(
    selected_analysts=["market", "news", "fundamentals", "macro"]
)
decision = stock_graph.propagate("AAPL", "2026-02-14")
# Output: BUY/SELL/HOLD for AAPL

# Asset allocation (new)
allocation_graph = AssetAllocationGraph()
allocation = allocation_graph.allocate(
    query="How should I allocate my portfolio given current macro conditions?",
    current_date="2026-02-14"
)
# Output: {"stocks": 60, "bonds": 30, "gold": 10}
```

**Why separate graphs:**
- ✅ Different use cases (stock picking vs allocation)
- ✅ Different outputs (BUY/SELL vs percentages)
- ✅ Can evolve independently
- ✅ Existing stock analysis unchanged

---

## Integration Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    TradingAgents System                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Stock Analysis Graph (Enhanced)               │  │
│  │                                                        │  │
│  │  Analysts: Market, News, Fundamentals, Macro (NEW)   │  │
│  │  Researchers: Bull, Bear (with macro context)         │  │
│  │  Trader: BUY/SELL/HOLD                                │  │
│  │  Risk Managers: Aggressive, Conservative, Neutral     │  │
│  │                                                        │  │
│  │  Output: BUY/SELL/HOLD for individual stocks          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │      Asset Allocation Graph (New, Optional)           │  │
│  │                                                        │  │
│  │  Macro Analyst: Economic regime analysis              │  │
│  │  Asset Strategist: Allocation recommendations         │  │
│  │  Portfolio Optimizer: Risk-adjusted allocation        │  │
│  │                                                        │  │
│  │  Output: % allocation across asset classes            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Shared Components                         │  │
│  │                                                        │  │
│  │  - FRED Data Tools (macro indicators)                 │  │
│  │  - Bedrock LLM Integration                            │  │
│  │  - Memory Systems                                      │  │
│  │  - Logging & State Management                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Design Principles

### 1. Incremental, Not Revolutionary
- ✅ Phase 1: Add tools, enhance existing analysts
- ✅ Phase 2: Add macro analyst to existing graph
- ✅ Phase 3: Create separate allocation graph
- ❌ Don't rebuild everything from scratch

### 2. Preserve What Works
- ✅ Keep existing debate structure (Bull vs Bear)
- ✅ Keep risk management team
- ✅ Keep Bedrock integration
- ✅ Keep memory systems
- ❌ Don't break existing functionality

### 3. Separation of Concerns
- ✅ Stock analysis graph for individual securities
- ✅ Asset allocation graph for portfolio decisions
- ✅ Shared tools and infrastructure
- ❌ Don't mix stock picking with asset allocation

### 4. Testability at Each Phase
- ✅ Phase 1: Test macro tools independently
- ✅ Phase 2: Test macro analyst with existing stocks
- ✅ Phase 3: Test allocation graph separately
- ❌ Don't deploy untested changes

---

## Risk Mitigation

### Technical Risks

**Risk:** FRED API rate limits  
**Mitigation:** Cache data, batch requests, use 120 req/min wisely

**Risk:** LLM hallucinations on macro data  
**Mitigation:** Always validate against actual FRED data, use structured outputs

**Risk:** Integration bugs  
**Mitigation:** Incremental rollout, extensive testing, feature flags

### Performance Risks

**Risk:** Macro analysis adds latency  
**Mitigation:** Run macro analyst in parallel with other analysts (Phase 2+)

**Risk:** Poor allocation recommendations  
**Mitigation:** Start with rule-based baselines, validate with historical scenarios

**Risk:** Overconfident regime calls  
**Mitigation:** Always provide confidence levels and scenario analysis

---

## Success Metrics

### Phase 1 Success
- ✅ FRED tools fetch data correctly
- ✅ News analyst incorporates macro context
- ✅ Analysis quality improves (subjective assessment)

### Phase 2 Success
- ✅ Macro analyst produces coherent regime analysis
- ✅ Researchers incorporate macro reasoning in debates
- ✅ Final decisions show macro awareness

### Phase 3 Success
- ✅ Asset allocation graph produces reasonable allocations
- ✅ Allocations align with macro regime
- ✅ Backtesting shows sensible behavior (2008, 2020, 2022)

---

## Timeline & Effort

| Phase | Duration | Effort | Risk |
|-------|----------|--------|------|
| Phase 1: Macro Context | 1 week | LOW | LOW |
| Phase 2: Macro Analyst | 1 week | MEDIUM | LOW |
| Phase 3: Asset Allocation | 2 weeks | MEDIUM | MEDIUM |
| **Total** | **4 weeks** | **MODERATE** | **LOW-MEDIUM** |

---

## Recommended Next Steps

### This Week
1. Get FRED API key (5 minutes)
2. Install fredapi: `pip install fredapi`
3. Create `macro_data_tools.py` with basic tools
4. Test FRED data fetching independently

### Next Week
1. Implement Phase 1 (macro context layer)
2. Test with AAPL, NVDA, BRK-B
3. Validate improvement in analysis quality

### Week 3
1. Implement Phase 2 (macro analyst)
2. Update graph to include macro analyst
3. Run full analysis with macro context

### Week 4
1. Design asset allocation graph
2. Implement asset strategist agent
3. Test with historical scenarios

---

## Conclusion

**Professional Recommendation: Incremental Integration**

Don't try to build everything at once. Start with Phase 1 (macro context), validate it works, then move to Phase 2 (macro analyst), then Phase 3 (asset allocation).

This approach:
- ✅ Minimizes risk (each phase is reversible)
- ✅ Provides value early (Phase 1 improves existing analysis)
- ✅ Allows learning (validate before investing more)
- ✅ Preserves existing functionality (no breaking changes)

**Confidence:** 90% that this approach will succeed

The key insight: You don't need to choose between stock analysis and asset allocation. You can have both, with shared infrastructure, by using separate graphs for different use cases.

---

**Author:** Kiro AI  
**Date:** February 15, 2026  
**Review Status:** Ready for Implementation
