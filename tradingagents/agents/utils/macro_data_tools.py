"""
Macro economic data tools using FRED API.
Provides access to Federal Reserve Economic Data for macro analysis.
"""

from langchain_core.tools import tool
from typing import Annotated
import os
from datetime import datetime, timedelta


@tool
def get_macro_indicator(
    series_id: Annotated[str, "FRED series ID (e.g., 'GDPC1' for GDP, 'UNRATE' for unemployment)"],
    lookback_days: Annotated[int, "Number of days to look back"] = 365
) -> str:
    """
    Fetch macro economic indicator from FRED API.
    
    Common series IDs:
    - GDPC1: Real GDP (Quarterly)
    - UNRATE: Unemployment Rate (Monthly)
    - CPIAUCSL: Consumer Price Index (Monthly)
    - CPILFESL: Core CPI (Monthly)
    - FEDFUNDS: Federal Funds Rate (Monthly)
    - DGS10: 10-Year Treasury Yield (Daily)
    - DGS2: 2-Year Treasury Yield (Daily)
    - M2SL: M2 Money Supply (Monthly)
    - PCEPI: PCE Price Index (Monthly)
    
    Args:
        series_id: FRED series identifier
        lookback_days: Number of days to look back from today
    
    Returns:
        Formatted string with recent indicator values
    """
    try:
        from fredapi import Fred
        
        api_key = os.environ.get('FRED_API_KEY')
        if not api_key:
            return (
                "ERROR: FRED_API_KEY not set in environment. "
                "Get free API key from: https://fred.stlouisfed.org/docs/api/api_key.html"
            )
        
        fred = Fred(api_key=api_key)
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)
        
        # Fetch data
        data = fred.get_series(
            series_id, 
            observation_start=start_date.strftime('%Y-%m-%d')
        )
        
        if data.empty:
            return f"No data available for series {series_id}"
        
        # Get recent values (last 12 data points)
        recent = data.tail(12)
        
        # Calculate year-over-year change if enough data
        latest = data.iloc[-1]
        latest_date = data.index[-1]
        
        yoy_change = None
        if len(data) > 252:  # Roughly 1 year of daily data
            year_ago = data.iloc[-252]
            yoy_change = ((latest - year_ago) / year_ago * 100) if year_ago != 0 else 0
        
        # Format output
        header = f"# {series_id} - Recent Values\n"
        header += f"# Latest: {latest:.2f} (as of {latest_date.strftime('%Y-%m-%d')})\n"
        if yoy_change is not None:
            header += f"# YoY Change: {yoy_change:+.2f}%\n"
        header += f"# Data points: {len(recent)}\n\n"
        
        # Convert to CSV
        csv_output = recent.to_csv()
        
        return header + csv_output
        
    except ImportError:
        return (
            "ERROR: fredapi library not installed. "
            "Install with: pip install fredapi"
        )
    except Exception as e:
        return f"ERROR fetching {series_id}: {str(e)}"


@tool
def get_macro_summary(
    current_date: Annotated[str, "Current date in YYYY-MM-DD format"]
) -> str:
    """
    Get a comprehensive summary of key macro economic indicators.
    
    Returns current values for:
    - GDP growth
    - Unemployment rate
    - Inflation (CPI)
    - Federal Funds Rate
    - Treasury yields (2Y, 10Y)
    - Yield curve spread
    
    Args:
        current_date: Reference date for the analysis
    
    Returns:
        Formatted summary of macro indicators with latest values and trends
    """
    try:
        from fredapi import Fred
        
        api_key = os.environ.get('FRED_API_KEY')
        if not api_key:
            return (
                "ERROR: FRED_API_KEY not set in environment. "
                "Get free API key from: https://fred.stlouisfed.org/docs/api/api_key.html"
            )
        
        fred = Fred(api_key=api_key)
        
        # Define key indicators
        indicators = {
            'Real GDP (Quarterly)': 'GDPC1',
            'Unemployment Rate': 'UNRATE',
            'CPI (Inflation)': 'CPIAUCSL',
            'Core CPI': 'CPILFESL',
            'Federal Funds Rate': 'FEDFUNDS',
            '10-Year Treasury': 'DGS10',
            '2-Year Treasury': 'DGS2',
            'M2 Money Supply': 'M2SL'
        }
        
        summary = f"# Macro Economic Summary as of {current_date}\n"
        summary += "=" * 60 + "\n\n"
        
        # Fetch and format each indicator
        for name, series_id in indicators.items():
            try:
                data = fred.get_series(series_id)
                
                if data.empty:
                    summary += f"{name:25s}: Data unavailable\n"
                    continue
                
                latest = data.iloc[-1]
                latest_date = data.index[-1].strftime('%Y-%m-%d')
                
                # Calculate YoY change for applicable indicators
                yoy_change = None
                if len(data) > 252:  # ~1 year of data
                    year_ago_idx = max(0, len(data) - 252)
                    year_ago = data.iloc[year_ago_idx]
                    if year_ago != 0:
                        yoy_change = ((latest - year_ago) / year_ago * 100)
                
                # Format output
                summary += f"{name:25s}: {latest:>8.2f}"
                
                if yoy_change is not None and abs(yoy_change) > 0.01:
                    direction = "↑" if yoy_change > 0 else "↓"
                    summary += f"  {direction} {abs(yoy_change):.1f}% YoY"
                
                summary += f"  [{latest_date}]\n"
                
            except Exception as e:
                summary += f"{name:25s}: Error - {str(e)[:30]}\n"
        
        # Calculate yield curve spread
        try:
            dgs10 = fred.get_series('DGS10')
            dgs2 = fred.get_series('DGS2')
            
            if not dgs10.empty and not dgs2.empty:
                spread = dgs10.iloc[-1] - dgs2.iloc[-1]
                summary += "\n" + "=" * 60 + "\n"
                summary += f"Yield Curve (10Y-2Y):     {spread:>8.2f}  "
                
                if spread < 0:
                    summary += "⚠️  INVERTED (Recession signal)\n"
                elif spread < 0.5:
                    summary += "⚠️  FLAT (Caution)\n"
                else:
                    summary += "✓  NORMAL (Healthy)\n"
        except:
            pass
        
        summary += "=" * 60 + "\n"
        
        return summary
        
    except ImportError:
        return (
            "ERROR: fredapi library not installed. "
            "Install with: pip install fredapi"
        )
    except Exception as e:
        return f"ERROR generating macro summary: {str(e)}"
