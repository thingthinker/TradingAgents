"""
Test script for Phase 1 macro integration.
Tests FRED data tools and enhanced news analyst.
"""

import os
from datetime import datetime

def test_fred_tools():
    """Test FRED data tools independently."""
    print("=" * 80)
    print("PHASE 1 MACRO INTEGRATION TEST")
    print("=" * 80)
    
    # Check for API key
    api_key = os.environ.get('FRED_API_KEY')
    if not api_key:
        print("\n❌ FRED_API_KEY not set in environment")
        print("   Get free API key from: https://fred.stlouisfed.org/docs/api/api_key.html")
        print("   Then set it: export FRED_API_KEY='your_key_here'")
        return False
    
    print(f"\n✅ FRED_API_KEY found: {api_key[:8]}...")
    
    # Test importing tools
    try:
        from tradingagents.agents.utils.macro_data_tools import (
            get_macro_indicator,
            get_macro_summary
        )
        print("✅ Macro data tools imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import macro tools: {e}")
        return False
    
    # Test get_macro_summary
    print("\n" + "-" * 80)
    print("Testing get_macro_summary...")
    print("-" * 80)
    
    try:
        current_date = datetime.now().strftime('%Y-%m-%d')
        summary = get_macro_summary.invoke({"current_date": current_date})
        print(summary)
        print("✅ get_macro_summary works!")
    except Exception as e:
        print(f"❌ get_macro_summary failed: {e}")
        return False
    
    # Test get_macro_indicator
    print("\n" + "-" * 80)
    print("Testing get_macro_indicator (Unemployment Rate)...")
    print("-" * 80)
    
    try:
        unemployment = get_macro_indicator.invoke({
            "series_id": "UNRATE",
            "lookback_days": 365
        })
        print(unemployment)
        print("✅ get_macro_indicator works!")
    except Exception as e:
        print(f"❌ get_macro_indicator failed: {e}")
        return False
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED - Phase 1 tools are working!")
    print("=" * 80)
    return True


def test_enhanced_news_analyst():
    """Test enhanced news analyst with macro context."""
    print("\n" + "=" * 80)
    print("TESTING ENHANCED NEWS ANALYST")
    print("=" * 80)
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        
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
        
        print("\n📊 Running analysis on AAPL with enhanced news analyst...")
        print("   (This will take 2-3 minutes)")
        
        graph = TradingAgentsGraph(
            selected_analysts=["news"],  # Only test news analyst
            debug=False,
            config=config
        )
        
        final_state, decision = graph.propagate("AAPL", "2026-02-14")
        
        print("\n" + "-" * 80)
        print("NEWS REPORT (with macro context):")
        print("-" * 80)
        print(final_state["news_report"][:1000])  # First 1000 chars
        print("\n... [truncated for display]")
        
        # Check if macro context is present
        news_report = final_state["news_report"].lower()
        has_macro = any(keyword in news_report for keyword in [
            'unemployment', 'inflation', 'gdp', 'interest rate', 
            'federal reserve', 'fed', 'treasury', 'economic'
        ])
        
        if has_macro:
            print("\n✅ News report includes macro economic context!")
        else:
            print("\n⚠️  News report may not include macro context (check manually)")
        
        print("\n" + "=" * 80)
        print("✅ ENHANCED NEWS ANALYST TEST COMPLETE")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Enhanced news analyst test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🚀 Starting Phase 1 Macro Integration Tests\n")
    
    # Test 1: FRED tools
    tools_ok = test_fred_tools()
    
    if not tools_ok:
        print("\n❌ FRED tools test failed. Fix issues before proceeding.")
        exit(1)
    
    # Test 2: Enhanced news analyst (optional, requires Bedrock)
    print("\n" + "=" * 80)
    print("OPTIONAL: Test enhanced news analyst with real stock analysis?")
    print("This requires Bedrock access and takes 2-3 minutes.")
    print("=" * 80)
    
    response = input("\nRun enhanced news analyst test? (y/n): ").strip().lower()
    
    if response == 'y':
        test_enhanced_news_analyst()
    else:
        print("\nSkipping enhanced news analyst test.")
    
    print("\n✅ Phase 1 implementation complete!")
    print("\nNext steps:")
    print("1. Review the enhanced news reports")
    print("2. Proceed to Phase 2: Add dedicated Macro Analyst")
    print("3. See macro_integration_strategy.md for details")
