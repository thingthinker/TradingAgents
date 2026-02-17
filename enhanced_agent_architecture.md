# Enhanced TradingAgents Architecture with Macro Economics

**Version:** 2.0 (with Macro Integration)  
**Date:** February 15, 2026

---

## System Overview

The enhanced system provides TWO operational modes:

1. **Stock Analysis Mode** (Enhanced) - Individual stock BUY/SELL/HOLD decisions with macro context
2. **Asset Allocation Mode** (New) - Portfolio allocation across asset classes based on macro regime

Both modes share infrastructure but operate independently.

---

## Mode 1: Enhanced Stock Analysis Graph

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         STOCK ANALYSIS MODE                          │
│                    (Enhanced TradingAgentsGraph)                     │
└─────────────────────────────────────────────────────────────────────┘

INPUT: Stock Ticker (e.g., "AAPL") + Trade Date (e.g., "2026-02-14")

    ↓

┌─────────────────────────────────────────────────────────────────────┐
│                      PHASE 1: DATA COLLECTION                        │
│                         (Parallel Analysts)                          │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────┬──────────────┬──────────────┬──────────────┐
    │              │              │              │              │
    ↓              ↓              ↓              ↓              ↓
┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
│ Market │   │  News  │   │Fundamen│   │ Social │   │ MACRO  │ ← NEW
│Analyst │   │Analyst │   │  tals  │   │ Media  │   │Analyst │
│        │   │        │   │Analyst │   │Analyst │   │        │
└────────┘   └────────┘   └────────┘   └────────┘   └────────┘
    │              │              │              │              │
    │ Tools:       │ Tools:       │ Tools:       │ Tools:       │ Tools:
    │ • Stock      │ • News       │ • Balance    │ • News       │ • FRED API
    │   Data       │   Search     │   Sheet      │   Search     │ • GDP
    │ • Technical  │ • Global     │ • Cash Flow  │              │ • CPI
    │   Indicators │   News       │ • Income     │              │ • Unemployment
    │              │ • Macro      │   Statement  │              │ • Interest Rates
    │              │   Summary    │              │              │ • Yield Curve
    │              │   (NEW)      │              │              │
    ↓              ↓              ↓              ↓              ↓
┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
│ Market │   │  News  │   │Fundamen│   │Sentiment│   │ Macro  │
│ Report │   │ Report │   │  tals  │   │ Report │   │ Report │ ← NEW
│        │   │(Enhanced)│   │ Report │   │        │   │        │
└────────┘   └────────┘   └────────┘   └────────┘   └────────┘

    │              │              │              │              │
    └──────────────┴──────────────┴──────────────┴──────────────┘
                                  │
                                  ↓

┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE 2: INVESTMENT DEBATE                        │
│                  (Bull vs Bear with Macro Context)                   │
└─────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────┐
                    │  All Analyst Reports│
                    │  (including Macro)  │ ← Enhanced
                    └─────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ↓                           ↓
        ┌──────────────┐           ┌──────────────┐
        │     Bull     │ ←────────→│     Bear     │
        │  Researcher  │   Debate   │  Researcher  │
        │              │            │              │
        │ • Growth     │            │ • Risks      │
        │   Potential  │            │ • Overval.   │
        │ • Competitive│            │ • Headwinds  │
        │   Advantages │            │ • Macro Risks│ ← Enhanced
        │ • Macro      │            │   (Recession,│
        │   Tailwinds  │            │    Inflation)│
        └──────────────┘            └──────────────┘
                │                           │
                └─────────────┬─────────────┘
                              ↓
                    ┌─────────────────┐
                    │    Research     │
                    │     Manager     │
                    │   (Judge/PM)    │
                    │                 │
                    │ • Synthesizes   │
                    │   Bull/Bear     │
                    │ • Makes Call    │
                    │ • Creates Plan  │
                    └─────────────────┘
                              │
                              ↓
                    ┌─────────────────┐
                    │  Investment     │
                    │     Plan        │
                    └─────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE 3: TRADE EXECUTION                          │
└─────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │     Trader      │
                    │                 │
                    │ • Reviews Plan  │
                    │ • Formulates    │
                    │   Specific      │
                    │   Trade         │
                    └─────────────────┘
                              │
                              ↓
                ┌─────────────────────────┐
                │ Trader Investment Plan  │
                │ (BUY/SELL/HOLD)        │
                └─────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────────┐
│                   PHASE 4: RISK MANAGEMENT                           │
│                    (3-Way Risk Debate)                               │
└─────────────────────────────────────────────────────────────────────┘

        ┌──────────────┬──────────────┬──────────────┐
        │              │              │              │
        ↓              ↓              ↓              
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Aggressive  │ │   Neutral    │ │ Conservative │
│   Analyst    │ │   Analyst    │ │   Analyst    │
│              │ │              │ │              │
│ • High Risk  │ │ • Balanced   │ │ • Capital    │
│ • High Reward│ │   View       │ │   Preservation│
│ • Opportunity│ │ • Weighs     │ │ • Downside   │
│   Focus      │ │   Both Sides │ │   Protection │
└──────────────┘ └──────────────┘ └──────────────┘
        │              │              │
        └──────────────┴──────────────┘
                       │
                       ↓
                ┌─────────────┐
                │    Risk     │
                │   Manager   │
                │   (Judge)   │
                │             │
                │ • Reviews   │
                │   Debate    │
                │ • Can       │
                │   Override  │
                │ • Final     │
                │   Decision  │
                └─────────────┘
                       │
                       ↓

OUTPUT: Final Trade Decision (BUY/SELL/HOLD) + Full Analysis Report

```

---

## Mode 2: Asset Allocation Graph (NEW)

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      ASSET ALLOCATION MODE                           │
│                    (AssetAllocationGraph - NEW)                      │
└─────────────────────────────────────────────────────────────────────┘

INPUT: User Query (e.g., "How should I allocate my portfolio?") + Date

    ↓

┌─────────────────────────────────────────────────────────────────────┐
│                  PHASE 1: MACRO REGIME ANALYSIS                      │
└─────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │  Macro Analyst  │
                    │                 │
                    │ Tools:          │
                    │ • FRED API      │
                    │ • GDP           │
                    │ • CPI           │
                    │ • Unemployment  │
                    │ • Fed Funds     │
                    │ • 10Y Treasury  │
                    │ • Yield Curve   │
                    │ • M2 Money      │
                    └─────────────────┘
                            │
                            ↓
                    ┌─────────────────┐
                    │ Regime Analysis │
                    │                 │
                    │ Determines:     │
                    │ • Recession     │
                    │ • Expansion     │
                    │ • Stagflation   │
                    │ • Soft Landing  │
                    │                 │
                    │ Assesses:       │
                    │ • Interest Rate │
                    │   Trajectory    │
                    │ • Inflation     │
                    │   Trend         │
                    │ • Employment    │
                    │   Strength      │
                    │ • Fed Policy    │
                    └─────────────────┘

    ↓

┌─────────────────────────────────────────────────────────────────────┐
│              PHASE 2: ASSET CLASS STRATEGY                           │
└─────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │     Asset       │
                    │   Strategist    │
                    │                 │
                    │ Input:          │
                    │ • Macro Regime  │
                    │ • Confidence    │
                    │ • Tail Risks    │
                    │                 │
                    │ Considers:      │
                    │ • Stocks (SPY)  │
                    │ • Bonds (TLT)   │
                    │ • Gold (GLD)    │
                    │ • Cash          │
                    │                 │
                    │ Applies Rules:  │
                    │ • Recession →   │
                    │   Defensive     │
                    │ • Expansion →   │
                    │   Aggressive    │
                    │ • Stagflation → │
                    │   Inflation     │
                    │   Hedge         │
                    └─────────────────┘
                            │
                            ↓
                    ┌─────────────────┐
                    │   Recommended   │
                    │   Allocation    │
                    │                 │
                    │ Example:        │
                    │ • Stocks: 60%   │
                    │ • Bonds: 30%    │
                    │ • Gold: 5%      │
                    │ • Cash: 5%      │
                    └─────────────────┘

    ↓

┌─────────────────────────────────────────────────────────────────────┐
│              PHASE 3: PORTFOLIO OPTIMIZATION                         │
└─────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │   Portfolio     │
                    │   Optimizer     │
                    │                 │
                    │ • Calculates    │
                    │   Historical    │
                    │   Correlations  │
                    │ • Adjusts for   │
                    │   Risk          │
                    │ • Applies       │
                    │   Constraints   │
                    │ • Generates     │
                    │   Scenarios     │
                    └─────────────────┘
                            │
                            ↓

OUTPUT: Final Allocation + Rationale + Scenarios + Rebalancing Triggers

```

---


## Detailed Agent Interaction Diagram

### Stock Analysis Mode - Detailed Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         ENHANCED STOCK ANALYSIS FLOW                          │
└──────────────────────────────────────────────────────────────────────────────┘

START (User Input: Ticker + Date)
  │
  ├─→ Initialize State
  │   • company_of_interest: "AAPL"
  │   • trade_date: "2026-02-14"
  │   • messages: []
  │
  ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ANALYST LAYER (Sequential)                           │
└─────────────────────────────────────────────────────────────────────────────┘

[Market Analyst] ──→ Tool Calls ──→ [tools_market] ──→ Loop until done
  │                    • get_stock_data(AAPL, start, end)
  │                    • get_indicators(AAPL, RSI, MACD, etc.)
  │
  ├─→ Produces: market_report
  │   "AAPL trading at $255, down from $288. RSI: 45 (neutral).
  │    MACD: -2.5 (bearish). 50-day SMA: $265 (below). 
  │    Technical outlook: Bearish momentum."
  │
  ↓
[News Analyst] ──→ Tool Calls ──→ [tools_news] ──→ Loop until done
  │                  • get_news(AAPL, start, end)
  │                  • get_global_news(current_date)
  │                  • get_macro_summary(current_date) ← NEW
  │
  ├─→ Produces: news_report (ENHANCED)
  │   "AAPL facing FTC scrutiny over App Store practices.
  │    iPhone sales weak in China. Siri AI delays vs competitors.
  │    
  │    MACRO CONTEXT: Unemployment rising to 4.2%, consumer 
  │    spending weakening. Fed holding rates at 4.25-4.50%.
  │    Tech sector under pressure from sector rotation."
  │
  ↓
[Fundamentals Analyst] ──→ Tool Calls ──→ [tools_fundamentals]
  │                         • get_fundamentals(AAPL)
  │                         • get_balance_sheet(AAPL)
  │                         • get_cashflow(AAPL)
  │                         • get_income_statement(AAPL)
  │
  ├─→ Produces: fundamentals_report
  │   "Market Cap: $3.2T, P/E: 28.5, Revenue: $400B.
  │    Debt-to-Equity: 102.63 (high), Current Ratio: 0.974 (low).
  │    Strong profitability but liquidity concerns."
  │
  ↓
[Macro Analyst] ──→ Tool Calls ──→ [tools_macro] ← NEW
  │                  • get_macro_summary(current_date)
  │                  • get_macro_indicator(GDPC1)  # GDP
  │                  • get_macro_indicator(UNRATE) # Unemployment
  │                  • get_macro_indicator(CPIAUCSL) # CPI
  │                  • get_macro_indicator(FEDFUNDS) # Fed Funds
  │                  • get_macro_indicator(DGS10) # 10Y Treasury
  │
  ├─→ Produces: macro_report ← NEW
  │   "ECONOMIC REGIME: Late-Cycle Expansion with Risks
  │    
  │    Key Indicators:
  │    • GDP Growth: 2.3% (above trend, slowing)
  │    • Unemployment: 4.2% (rising from 3.7% lows)
  │    • CPI: 3.2% (above Fed target, declining)
  │    • Fed Funds: 4.25-4.50% (restrictive)
  │    • 10Y Treasury: 4.2% (yield curve normalized)
  │    • 2Y-10Y Spread: +0.3% (inversion resolved)
  │    
  │    REGIME ASSESSMENT: Transitioning from expansion to 
  │    potential soft landing. Fed on hold, data-dependent.
  │    Risk of recession if unemployment continues rising.
  │    
  │    SECTOR IMPLICATIONS:
  │    • Tech (AAPL): Cyclical sector vulnerable in slowdown
  │    • Consumer spending weakening = iPhone sales risk
  │    • Rate cuts would help but may signal recession
  │    • Sector rotation from growth to value/defensive
  │    
  │    TAIL RISKS:
  │    • Hard landing (recession) if Fed stays restrictive
  │    • Stagflation if inflation re-accelerates
  │    • Credit market stress from high rates"
  │
  ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                      RESEARCH LAYER (Debate)                                 │
└─────────────────────────────────────────────────────────────────────────────┘

[Bull Researcher] ──→ Reads ALL Reports (including macro) ← ENHANCED
  │                    • market_report
  │                    • news_report (with macro context)
  │                    • fundamentals_report
  │                    • macro_report ← NEW
  │                    • past_memories (similar situations)
  │
  ├─→ Builds Bull Case:
  │   "AAPL has strong fundamentals: $400B revenue, dominant 
  │    ecosystem, $3.2T market cap shows market confidence.
  │    
  │    MACRO CONSIDERATION: While unemployment rising, we're 
  │    likely heading for soft landing, not recession. Fed 
  │    rate cuts in H2 2025 would be tailwind for tech.
  │    
  │    AAPL is defensive within tech: Services revenue (30%) 
  │    provides stability. Installed base of 2B devices = 
  │    recurring revenue stream less sensitive to cycles."
  │
  ↓
[Bear Researcher] ──→ Reads ALL Reports + Bull's Argument
  │                    • All analyst reports (including macro)
  │                    • Bull's argument
  │                    • past_memories
  │
  ├─→ Builds Bear Case:
  │   "AAPL down 11% for good reason: FTC scrutiny, weak 
  │    China sales, AI delays. Debt-to-Equity 102.63 is high.
  │    
  │    MACRO CONCERN: Unemployment rising to 4.2% signals 
  │    consumer weakness. AAPL is NOT defensive - it's a 
  │    premium consumer discretionary play. In recession, 
  │    consumers delay iPhone upgrades.
  │    
  │    Bull's 'soft landing' is optimistic. If Fed cuts rates, 
  │    it's because economy is weakening, not because all is 
  │    well. Sector rotation from tech to defensive is real.
  │    
  │    Current ratio 0.974 < 1.0 = liquidity risk in downturn."
  │
  ↓
[Research Manager] ──→ Synthesizes Debate
  │                     • Reviews bull_history
  │                     • Reviews bear_history
  │                     • Considers macro_report ← ENHANCED
  │                     • Retrieves past_memories
  │
  ├─→ Makes Decision:
  │   "RECOMMENDATION: SELL
  │    
  │    The bear's macro argument is more compelling. Rising 
  │    unemployment (4.2%) + weakening consumer spending + 
  │    sector rotation = headwinds for premium tech.
  │    
  │    Bull's soft landing thesis is possible but not probable.
  │    Risk/reward skewed to downside. Better opportunities in
  │    defensive sectors or wait for clearer macro signals.
  │    
  │    INVESTMENT PLAN:
  │    • Exit AAPL positions over 2-3 weeks
  │    • Rotate to defensive (healthcare, utilities)
  │    • Monitor unemployment and consumer spending
  │    • Re-evaluate if macro improves or valuation compresses"
  │
  ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TRADER LAYER                                          │
└─────────────────────────────────────────────────────────────────────────────┘

[Trader] ──→ Reviews Investment Plan
  │          • Reads investment_plan from Research Manager
  │          • Considers all analyst reports
  │          • Retrieves trader_memory (past trades)
  │
  ├─→ Formulates Trade:
  │   "FINAL TRANSACTION PROPOSAL: **SELL**
  │    
  │    Concur with Research Manager's bearish assessment.
  │    Macro headwinds (rising unemployment, sector rotation)
  │    combined with company-specific issues (FTC, China, AI)
  │    create unfavorable risk/reward.
  │    
  │    EXECUTION PLAN:
  │    • Sell 50% of position immediately
  │    • Sell remaining 50% over 2 weeks
  │    • Set stop-loss at $240 (5% below current)
  │    • Monitor macro data (unemployment, consumer spending)"
  │
  ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                      RISK MANAGEMENT LAYER                                   │
└─────────────────────────────────────────────────────────────────────────────┘

[Aggressive Analyst] ──→ Reviews Trader's SELL Decision
  │                       • Reads trader_investment_plan
  │                       • Reads all reports (including macro)
  │
  ├─→ Argues for Risk-Taking:
  │   "SELL is too conservative! AAPL at $255 is 11% off highs.
  │    This is a buying opportunity, not selling time.
  │    
  │    Macro concerns are overblown. Unemployment 4.2% is still
  │    historically low. Fed will cut rates = tech rally.
  │    
  │    AAPL's ecosystem moat is undervalued. Services growing
  │    30% = recession-resistant revenue. Don't sell winners!"
  │
  ↓
[Conservative Analyst] ──→ Reviews Trader + Aggressive
  │                         • Reads both arguments
  │                         • Focuses on downside risks
  │
  ├─→ Argues for Caution:
  │   "SELL is correct. Aggressive analyst ignoring macro risks.
  │    
  │    Unemployment rising from 3.7% to 4.2% = trend reversal.
  │    Current ratio 0.974 < 1.0 = liquidity risk if credit 
  │    tightens. Debt-to-Equity 102.63 = vulnerability.
  │    
  │    'Don't sell winners' is emotional, not analytical. 
  │    Winners become losers when fundamentals deteriorate.
  │    
  │    Capital preservation > catching falling knives."
  │
  ↓
[Neutral Analyst] ──→ Reviews All Arguments
  │                    • Weighs aggressive vs conservative
  │                    • Considers macro uncertainty
  │
  ├─→ Provides Balanced View:
  │   "Both sides have merit. Macro is uncertain (soft landing
  │    vs recession). AAPL has strengths (ecosystem) and 
  │    weaknesses (valuation, liquidity).
  │    
  │    RECOMMENDATION: Partial SELL (50%) is prudent.
  │    • Reduces risk if bear case materializes
  │    • Maintains exposure if bull case plays out
  │    • Allows reassessment as macro clarifies"
  │
  ↓
[Risk Manager] ──→ Final Decision
  │                 • Reviews all three risk analysts
  │                 • Considers trader's plan
  │                 • Retrieves risk_manager_memory
  │                 • Can override trader
  │
  ├─→ FINAL DECISION:
  │   "FINAL TRADE DECISION: **SELL**
  │    
  │    Conservative analyst's risk assessment is most compelling.
  │    Macro headwinds (unemployment, sector rotation) combined
  │    with company-specific risks (liquidity, debt, FTC) create
  │    unfavorable risk/reward.
  │    
  │    Aggressive analyst's 'buying opportunity' thesis assumes
  │    soft landing, which is uncertain. Neutral analyst's 50%
  │    sell is reasonable but we prefer full exit given:
  │    • Current ratio < 1.0 (liquidity risk)
  │    • Debt-to-Equity > 100 (leverage risk)
  │    • Macro deterioration (unemployment rising)
  │    
  │    EXECUTION:
  │    • Sell 100% of position over 2-3 weeks
  │    • Stop-loss at $240 (5% below current)
  │    • Re-evaluate if:
  │      - Unemployment stabilizes below 4.0%
  │      - Valuation compresses to P/E < 25
  │      - Macro signals improve (Fed cuts without recession)"
  │
  ↓
END (Output: SELL + Full Analysis Report)

```

---

## Data Flow Architecture

### Phase 1 Enhancement: Macro Data Integration

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                                 │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Yahoo Finance   │  │   Alpha Vantage  │  │   FRED API       │ ← NEW
│                  │  │                  │  │                  │
│ • Stock Prices   │  │ • Stock Prices   │  │ • GDP            │
│ • Fundamentals   │  │ • Fundamentals   │  │ • CPI            │
│ • News           │  │ • News           │  │ • Unemployment   │
│ • Insider Trades │  │ • Insider Trades │  │ • Interest Rates │
│                  │  │                  │  │ • Yield Curve    │
│                  │  │                  │  │ • M2 Money       │
│                  │  │                  │  │ • 800K+ series   │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        │                      │                      │
        └──────────────────────┴──────────────────────┘
                               │
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA ABSTRACTION LAYER                          │
│                   (tradingagents/dataflows/)                         │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  y_finance.py    │  │alpha_vantage.py  │  │ fred_data.py     │ ← NEW
│                  │  │                  │  │                  │
│ • get_stock_data │  │ • get_stock      │  │ • get_macro_     │
│ • get_indicators │  │ • get_indicator  │  │   indicator      │
│ • get_fundamentals│  │ • get_fundamentals│  │ • get_macro_    │
│ • get_news       │  │ • get_news       │  │   summary        │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        │                      │                      │
        └──────────────────────┴──────────────────────┘
                               │
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         TOOL LAYER                                   │
│                  (tradingagents/agents/utils/)                       │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│core_stock_tools  │  │fundamental_data  │  │ macro_data_tools │ ← NEW
│                  │  │     _tools       │  │                  │
│ @tool            │  │ @tool            │  │ @tool            │
│ get_stock_data() │  │ get_fundamentals()│  │ get_macro_       │
│                  │  │ get_balance_     │  │   indicator()    │
│technical_        │  │   sheet()        │  │ get_macro_       │
│  indicators_tools│  │ get_cashflow()   │  │   summary()      │
│                  │  │ get_income_      │  │                  │
│ @tool            │  │   statement()    │  │                  │
│ get_indicators() │  │                  │  │                  │
│                  │  │                  │  │                  │
│news_data_tools   │  │                  │  │                  │
│                  │  │                  │  │                  │
│ @tool            │  │                  │  │                  │
│ get_news()       │  │                  │  │                  │
│ get_global_news()│  │                  │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        │                      │                      │
        └──────────────────────┴──────────────────────┘
                               │
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         AGENT LAYER                                  │
│                    (tradingagents/agents/)                           │
└─────────────────────────────────────────────────────────────────────┘

Uses tools via LangChain tool binding:
  llm.bind_tools([get_stock_data, get_indicators, get_macro_summary])

```

---

## State Management

### Enhanced AgentState

```python
class AgentState(MessagesState):
    # Core
    company_of_interest: str
    trade_date: str
    sender: str
    
    # Analyst Reports
    market_report: str
    sentiment_report: str
    news_report: str              # ENHANCED with macro context
    fundamentals_report: str
    macro_report: str             # NEW
    
    # Investment Debate
    investment_debate_state: InvestDebateState
    investment_plan: str
    
    # Trading
    trader_investment_plan: str
    
    # Risk Debate
    risk_debate_state: RiskDebateState
    
    # Final Output
    final_trade_decision: str
```

### New: AssetAllocationState

```python
class AssetAllocationState(TypedDict):
    # Input
    query: str
    current_date: str
    
    # Analysis
    macro_report: str
    regime: str  # "Recession", "Expansion", "Stagflation", "Soft Landing"
    confidence: str  # "High", "Medium", "Low"
    
    # Allocation
    allocation: Dict[str, float]  # {"stocks": 60, "bonds": 30, "gold": 10}
    allocation_report: str
    
    # Scenarios
    scenarios: Dict[str, Dict[str, float]]  # {"base": {...}, "bull": {...}, "bear": {...}}
```

---

## Configuration

### Enhanced Config

```python
DEFAULT_CONFIG = {
    # ... existing config ...
    
    # NEW: Macro data configuration
    "fred_api_key": os.getenv("FRED_API_KEY"),
    "macro_lookback_days": 365,
    
    # NEW: Asset allocation configuration
    "asset_classes": ["stocks", "bonds", "gold", "cash"],
    "rebalance_threshold": 0.05,  # 5% drift triggers rebalance
}
```

---

## Summary of Changes

### What's Added

1. ✅ **Macro Analyst Agent** - New analyst in stock analysis graph
2. ✅ **FRED Data Tools** - New tools for macro indicators
3. ✅ **Enhanced News Analyst** - Now includes macro context
4. ✅ **Enhanced Researchers** - Bull/Bear consider macro regime
5. ✅ **Asset Allocation Graph** - Separate graph for portfolio allocation
6. ✅ **Asset Strategist Agent** - New agent for allocation decisions
7. ✅ **macro_report** - New state field

### What's Unchanged

1. ✅ Core graph structure (sequential analysts → debate → trader → risk)
2. ✅ Debate mechanism (Bull vs Bear)
3. ✅ Risk management (3-way debate)
4. ✅ Memory systems
5. ✅ Bedrock integration
6. ✅ Existing data sources (yfinance, Alpha Vantage)
7. ✅ Output format (BUY/SELL/HOLD)

### Integration Points

```
Existing System          New Components           Integration Method
─────────────────        ───────────────          ──────────────────
news_analyst.py    ←──→  macro_data_tools.py     Add tool to tools list
                         get_macro_summary()      

setup.py           ←──→  macro_analyst.py        Add to selected_analysts
                         create_macro_analyst()   

agent_states.py    ←──→  macro_report: str       Add new state field

bull_researcher.py ←──→  macro_report            Read from state
bear_researcher.py       

(New)              ←──→  asset_allocation_       Separate graph
                         graph.py                 
```

---

**Version:** 2.0  
**Status:** Design Complete, Ready for Implementation  
**Next Step:** Phase 1 Implementation (Macro Context Layer)
