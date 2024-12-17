"""Test script demonstrating combined usage of all three API toolkits."""
from api_toolkits.finnhub_toolkit import FinnhubClient
from api_toolkits.twelvedata_toolkit import TwelveDataClient
from api_toolkits.alphavantage_toolkit import AlphaVantageClient
from datetime import datetime, timedelta
import json

def format_output(data: dict, indent: int = 2) -> None:
    """Helper function to pretty print JSON data."""
    print(json.dumps(data, indent=indent))

def test_combined_apis():
    """Test combined functionality of all three API toolkits."""
    
    # Initialize all clients
    fh_client = FinnhubClient()
    td_client = TwelveDataClient()
    av_client = AlphaVantageClient()
    
    try:
        while True:
            print("\nCombined API Test Menu:")
            print("1. Comprehensive Stock Analysis")
            print("2. Multi-Source Price Comparison")
            print("3. News and Technical Analysis")
            print("4. Company Research")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "5":
                print("Exiting...")
                break
                
            if choice in ["1", "2", "3", "4"]:
                symbol = input("Enter a stock symbol (e.g., AAPL): ").upper()
            
            try:
                if choice == "1":
                    # Comprehensive Stock Analysis
                    print(f"\nPerforming comprehensive analysis for {symbol}...")
                    
                    # Get company profile from Finnhub
                    print("\n1. Company Profile (Finnhub):")
                    profile = fh_client.get_company_profile(symbol=symbol)
                    format_output(profile)
                    
                    # Get technical indicators from TwelveData
                    print("\n2. Technical Indicators (TwelveData):")
                    # Get RSI
                    rsi_data = td_client.get_technical_indicator(
                        symbol=symbol,
                        interval="1day",
                        indicator="rsi",
                        time_period=14
                    )
                    print("\nRSI (14-day):")
                    format_output(rsi_data)
                    
                    # Get MACD
                    macd_data = td_client.get_technical_indicator(
                        symbol=symbol,
                        interval="1day",
                        indicator="macd"
                    )
                    print("\nMACD:")
                    format_output(macd_data)
                    
                    # Get fundamentals from AlphaVantage
                    print("\n3. Company Overview (AlphaVantage):")
                    overview = av_client.get_company_overview(symbol)
                    format_output(overview)
                    
                elif choice == "2":
                    # Multi-Source Price Comparison
                    print(f"\nComparing price data for {symbol} across sources...")
                    
                    # Finnhub quote
                    print("\n1. Finnhub Quote:")
                    fh_quote = fh_client.get_quote(symbol)
                    format_output(fh_quote)
                    
                    # TwelveData quote
                    print("\n2. TwelveData Quote:")
                    td_quote = td_client.get_quote(symbol)
                    format_output(td_quote)
                    
                    # AlphaVantage quote
                    print("\n3. AlphaVantage Quote:")
                    av_quote = av_client.get_global_quote(symbol)
                    format_output(av_quote)
                    
                elif choice == "3":
                    # News and Technical Analysis
                    print(f"\nGathering news and technical analysis for {symbol}...")
                    
                    # Get recent news from Finnhub
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=7)
                    
                    print("\n1. Recent News (Finnhub):")
                    news = fh_client.get_company_news(
                        symbol,
                        from_date=start_date.strftime("%Y-%m-%d"),
                        to_date=end_date.strftime("%Y-%m-%d")
                    )
                    print(f"\nFound {len(news)} recent news articles")
                    for article in news[:5]:  # Show only first 5 articles
                        print(f"\nHeadline: {article.get('headline', 'N/A')}")
                        print(f"Summary: {article.get('summary', 'N/A')}")
                        print(f"Source: {article.get('source', 'N/A')}")
                    
                    # Get technical analysis from TwelveData
                    print("\n2. Technical Analysis (TwelveData):")
                    
                    # Instead of Bollinger Bands, let's use RSI and MACD
                    print("\nRSI (14-day):")
                    rsi_data = td_client.get_technical_indicator(
                        symbol=symbol,
                        interval="1day",
                        indicator="rsi",
                        time_period=14
                    )
                    format_output(rsi_data)
                    
                    print("\nMACD:")
                    macd_data = td_client.get_technical_indicator(
                        symbol=symbol,
                        interval="1day",
                        indicator="macd"
                    )
                    format_output(macd_data)
                    
                    # Add SMA for trend context
                    print("\n20-day Simple Moving Average:")
                    sma = td_client.get_technical_indicator(
                        symbol=symbol,
                        interval="1day",
                        indicator="sma",
                        time_period=20
                    )
                    format_output(sma)
                    
                elif choice == "4":
                    # Company Research
                    print(f"\nGathering comprehensive company research for {symbol}...")
                    
                    # Get company overview from AlphaVantage
                    print("\n1. Company Overview (AlphaVantage):")
                    overview = av_client.get_company_overview(symbol)
                    format_output(overview)
                    
                    # Get earnings data from AlphaVantage
                    print("\n2. Earnings Data (AlphaVantage):")
                    earnings = av_client.get_earnings(symbol)
                    if 'quarterlyEarnings' in earnings:
                        print("\nRecent Quarterly Earnings:")
                        format_output(earnings['quarterlyEarnings'][:4])  # Last 4 quarters
                    
                    # Get recommendation trends from Finnhub
                    print("\n3. Analyst Recommendations (Finnhub):")
                    recommendations = fh_client.get_recommendation_trends(symbol)
                    format_output(recommendations)
                    
                    # Get time series from TwelveData
                    print("\n4. Recent Price Action (TwelveData):")
                    time_series = td_client.get_time_series(
                        symbol=symbol,
                        interval="1day",
                        outputsize=30
                    )
                    format_output(time_series)
                
            except Exception as e:
                print(f"Error: {str(e)}")
                
    finally:
        # Close all clients
        fh_client.close()
        av_client.close()

if __name__ == "__main__":
    print("Combined API Toolkits Test")
    print("=" * 50)
    test_combined_apis() 