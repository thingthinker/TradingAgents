# Macro Integration Setup Guide

## Phase 1 Implementation Complete! ✅

The macro context layer has been implemented. Follow these steps to test it.

---

## Prerequisites

### 1. Install fredapi Library

```bash
pip install fredapi
```

Or if using the virtual environment:

```bash
source .venv/bin/activate
pip install fredapi
```

### 2. Get FRED API Key (FREE)

1. Visit: https://fred.stlouisfed.org/docs/api/api_key.html
2. Click "Request API Key"
3. Fill out simple form (takes 30 seconds)
4. API key is emailed instantly (usually within 1 minute)

### 3. Set Environment Variable

**macOS/Linux:**
```bash
export FRED_API_KEY='your_api_key_here'
```

**Or add to your shell profile (~/.zshrc or ~/.bashrc):**
```bash
echo 'export FRED_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

**Windows:**
```cmd
set FRED_API_KEY=your_api_key_here
```

---

## What Was Implemented

### New Files Created

1. **`tradingagents/agents/utils/macro_data_tools.py`**
   - `get_macro_indicator()` - Fetch specific economic indicators
   - `get_macro_summary()` - Get comprehensive macro overview

2. **`test_macro_integration.py`**
   - Test script to validate Phase 1 implementation

3. **`MACRO_SETUP.md`** (this file)
   - Setup and testing instructions

### Modified Files

1. **`tradingagents/agents/utils/agent_utils.py`**
   - Added exports for macro tools

2. **`tradingagents/agents/analysts/news_analyst.py`**
   - Enhanced with `get_macro_summary` tool
   - Updated system prompt to include macro context
   - Now analyzes company news within broader economic environment

---

## Testing Phase 1

### Test 1: FRED Tools (Required)

```bash
python test_macro_integration.py
```

This will:
1. Check if FRED_API_KEY is set
2. Test `get_macro_summary()` - fetches GDP, CPI, unemployment, rates
3. Test `get_macro_indicator()` - fetches unemployment rate
4. Display results

**Expected Output:**
```
============================================================
PHASE 1 MACRO INTEGRATION TEST
============================================================

✅ FRED_API_KEY found: abcd1234...
✅ Macro data tools imported successfully

------------------------------------------------------------
Testing get_macro_summary...
------------------------------------------------------------
# Macro Economic Summary as of 2026-02-14
============================================================

Real GDP (Quarterly)     : 23500.00  ↑ 2.3% YoY  [2025-12-31]
Unemployment Rate        :     4.20  ↑ 0.5% YoY  [2026-01-31]
CPI (Inflation)          :   320.30  ↑ 3.2% YoY  [2026-01-31]
...

✅ get_macro_summary works!
✅ get_macro_indicator works!

============================================================
✅ ALL TESTS PASSED - Phase 1 tools are working!
============================================================
```

### Test 2: Enhanced News Analyst (Optional)

When prompted, type `y` to test the enhanced news analyst with a real stock:

```
Run enhanced news analyst test? (y/n): y
```

This will:
1. Run TradingAgents on AAPL with only the news analyst
2. Show how news report now includes macro context
3. Takes 2-3 minutes

**What to Look For:**
The news report should now include macro economic context like:
- "Unemployment rising to 4.2%"
- "Fed holding rates at 4.25-4.50%"
- "Consumer spending weakening"
- "Sector rotation from tech to defensive"

---

## Manual Testing

### Test Macro Tools Directly

```python
from tradingagents.agents.utils.macro_data_tools import get_macro_summary, get_macro_indicator

# Get macro summary
summary = get_macro_summary.invoke({"current_date": "2026-02-14"})
print(summary)

# Get specific indicator (unemployment)
unemployment = get_macro_indicator.invoke({
    "series_id": "UNRATE",
    "lookback_days": 365
})
print(unemployment)

# Get GDP
gdp = get_macro_indicator.invoke({
    "series_id": "GDPC1",
    "lookback_days": 730
})
print(gdp)
```

### Test Enhanced News Analyst

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
import os

config = {
    "project_dir": os.path.abspath("."),
    "llm_provider": "bedrock",
    "deep_think_llm": "us.anthropic.claude-sonnet-4-20250514-v1:0",
    "quick_think_llm": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    "aws_credentials_profile": "your-aws-profile",
    "aws_region": "us-east-1",
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "data_vendors": {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    },
}

# Run with enhanced news analyst
graph = TradingAgentsGraph(
    selected_analysts=["market", "news", "fundamentals"],
    debug=False,
    config=config
)

final_state, decision = graph.propagate("AAPL", "2026-02-14")

# Check news report
print(final_state["news_report"])
```

---

## Validation Checklist

- [ ] FRED_API_KEY is set in environment
- [ ] fredapi library is installed
- [ ] `test_macro_integration.py` runs successfully
- [ ] `get_macro_summary()` returns economic indicators
- [ ] `get_macro_indicator()` fetches specific series
- [ ] Enhanced news analyst includes macro context in reports
- [ ] No errors in existing TradingAgents functionality

---

## Common Issues

### Issue: "FRED_API_KEY not set"

**Solution:**
```bash
export FRED_API_KEY='your_key_here'
```

Make sure to replace `your_key_here` with your actual API key.

### Issue: "fredapi library not installed"

**Solution:**
```bash
pip install fredapi
```

### Issue: "No module named 'fredapi'"

**Solution:**
Make sure you're using the correct Python environment:
```bash
which python
pip list | grep fredapi
```

If using virtual environment:
```bash
source .venv/bin/activate
pip install fredapi
```

### Issue: API rate limit exceeded

FRED allows 120 requests per minute. If you hit the limit:
- Wait 1 minute
- Reduce frequency of requests
- Cache results when possible

---

## What's Next?

### Phase 2: Dedicated Macro Analyst (Week 2)

After validating Phase 1, proceed to Phase 2:

1. Create `tradingagents/agents/analysts/macro_analyst.py`
2. Add `macro_report` to `AgentState`
3. Update graph to include macro analyst
4. Enhance Bull/Bear researchers to use macro context

See `macro_integration_strategy.md` for detailed Phase 2 instructions.

### Phase 3: Asset Allocation Mode (Weeks 3-4)

After Phase 2 is working:

1. Create `AssetAllocationGraph` class
2. Create `asset_strategist.py` agent
3. Implement portfolio allocation logic
4. Test with historical scenarios

---

## Success Criteria for Phase 1

✅ **Phase 1 is successful if:**

1. FRED tools fetch data correctly
2. News analyst incorporates macro context
3. News reports mention economic indicators (unemployment, inflation, rates)
4. No breaking changes to existing functionality
5. Analysis quality improves (subjective assessment)

**Example of Success:**

Before Phase 1:
> "AAPL down 10% due to weak iPhone sales and FTC scrutiny."

After Phase 1:
> "AAPL down 10% due to weak iPhone sales and FTC scrutiny. This weakness is amplified by rising unemployment (4.2%) and weakening consumer spending, as the economy transitions from expansion to potential soft landing. Fed holding rates at 4.25-4.50% creates headwinds for premium consumer discretionary stocks like AAPL."

---

## Support

If you encounter issues:

1. Check this guide's "Common Issues" section
2. Review `macro_integration_strategy.md` for architecture details
3. Check `feasibility_analysis.md` for technical background
4. Review `enhanced_agent_architecture.md` for system design

---

**Phase 1 Status:** ✅ IMPLEMENTED  
**Next Phase:** Phase 2 - Dedicated Macro Analyst  
**Timeline:** Ready to test now, Phase 2 in Week 2
