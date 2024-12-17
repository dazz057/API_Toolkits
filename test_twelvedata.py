"""Test script for TwelveData API toolkit - Time series and technical analysis."""
from api_toolkits.twelvedata_toolkit import TwelveDataClient
from datetime import datetime
import json

def format_output(data: dict, indent: int = 2) -> None:
    """Helper function to pretty print JSON data."""
    print(json.dumps(data, indent=indent))

def test_twelvedata():
    """Test various TwelveData API functionalities."""
    
    # Initialize the TwelveData client
    client = TwelveDataClient()
    
    while True:
        print("\nTwelveData API Test Menu:")
        print("1. Get Time Series Data")
        print("2. Get Real-time Quote")
        print("3. Get Technical Indicators")
        print("4. Get Stock List")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "5":
            print("Exiting...")
            break
            
        # Get symbol input for all options except 4
        if choice != "4":
            symbol = input("Enter a stock symbol (e.g., AAPL): ").upper()
        
        try:
            if choice == "1":
                # Time Series Data
                interval = input("Enter interval (1min, 5min, 1hour, 1day, 1week, 1month): ")
                outputsize = int(input("Enter number of data points (1-5000): "))
                
                print(f"\nFetching time series data for {symbol}...")
                data = client.get_time_series(
                    symbol=symbol,
                    interval=interval,
                    outputsize=outputsize,
                    timezone="America/New_York"
                )
                format_output(data)
                
            elif choice == "2":
                # Real-time Quote
                print(f"\nFetching real-time quote for {symbol}...")
                quote = client.get_quote(symbol)
                format_output(quote)
                
            elif choice == "3":
                # Technical Indicators
                print("\nAvailable indicators: sma, ema, rsi, macd, bbands")
                indicator = input("Enter indicator name: ").lower()
                interval = input("Enter interval (1min, 5min, 1hour, 1day): ")
                
                # Get additional parameters based on indicator
                params = {}
                if indicator in ['sma', 'ema', 'rsi']:
                    time_period = int(input("Enter time period: "))
                    params['time_period'] = time_period
                elif indicator == 'macd':
                    params.update({
                        'fast_period': int(input("Enter fast period (default 12): ") or "12"),
                        'slow_period': int(input("Enter slow period (default 26): ") or "26"),
                        'signal_period': int(input("Enter signal period (default 9): ") or "9")
                    })
                elif indicator == 'bbands':
                    params.update({
                        'time_period': int(input("Enter time period (default 20): ") or "20"),
                        'std_dev': float(input("Enter standard deviation (default 2): ") or "2")
                    })
                
                print(f"\nFetching {indicator.upper()} data for {symbol}...")
                data = client.get_technical_indicator(
                    symbol=symbol,
                    interval=interval,
                    indicator=indicator,
                    **params
                )
                format_output(data)
                
            elif choice == "4":
                # Stock List
                exchange = input("Enter exchange (e.g., NASDAQ) or press Enter for all: ")
                stock_type = input("Enter type (e.g., Common Stock) or press Enter for all: ")
                
                print("\nFetching stock list...")
                stocks = client.get_stocks_list(
                    exchange=exchange or None,
                    type=stock_type or None
                )
                
                # Display first 10 stocks
                print("\nFirst 10 stocks in the list:")
                format_output(stocks[:10])
                print(f"\nTotal stocks found: {len(stocks)}")
                
            else:
                print("Invalid choice. Please try again.")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            
if __name__ == "__main__":
    print("TwelveData API Toolkit Test")
    print("=" * 50)
    test_twelvedata() 