"""Test script for AlphaVantage API toolkit - Market data and company information."""
from api_toolkits.alphavantage_toolkit import AlphaVantageClient
import json

def format_output(data: dict, indent: int = 2) -> None:
    """Helper function to pretty print JSON data."""
    print(json.dumps(data, indent=indent))

def test_alphavantage():
    """Test various AlphaVantage API functionalities."""
    
    # Initialize the AlphaVantage client
    client = AlphaVantageClient()
    
    while True:
        print("\nAlphaVantage API Test Menu:")
        print("1. Get Daily Time Series")
        print("2. Get Company Overview")
        print("3. Get Earnings Data")
        print("4. Get Global Quote")
        print("5. Search Symbols")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "6":
            print("Exiting...")
            break
            
        try:
            if choice == "1":
                # Daily Time Series
                symbol = input("Enter a stock symbol (e.g., AAPL): ").upper()
                size = input("Enter size (compact/full) [default: compact]: ").lower() or 'compact'
                data_type = input("Enter data type (json/csv) [default: json]: ").lower() or 'json'
                
                print(f"\nFetching daily time series for {symbol}...")
                data = client.get_time_series_daily(
                    symbol=symbol,
                    outputsize=size,
                    datatype=data_type
                )
                format_output(data)
                
            elif choice == "2":
                # Company Overview
                symbol = input("Enter a stock symbol (e.g., AAPL): ").upper()
                
                print(f"\nFetching company overview for {symbol}...")
                overview = client.get_company_overview(symbol)
                format_output(overview)
                
            elif choice == "3":
                # Earnings Data
                symbol = input("Enter a stock symbol (e.g., AAPL): ").upper()
                
                print(f"\nFetching earnings data for {symbol}...")
                earnings = client.get_earnings(symbol)
                
                # Display annual and quarterly earnings separately
                if 'annualEarnings' in earnings:
                    print("\nAnnual Earnings:")
                    format_output(earnings['annualEarnings'])
                if 'quarterlyEarnings' in earnings:
                    print("\nQuarterly Earnings:")
                    format_output(earnings['quarterlyEarnings'])
                
            elif choice == "4":
                # Global Quote
                symbol = input("Enter a stock symbol (e.g., AAPL): ").upper()
                
                print(f"\nFetching current quote for {symbol}...")
                quote = client.get_global_quote(symbol)
                format_output(quote)
                
            elif choice == "5":
                # Symbol Search
                keywords = input("Enter search keywords: ")
                
                print(f"\nSearching for symbols matching '{keywords}'...")
                results = client.search_symbol(keywords)
                format_output(results)
                
            else:
                print("Invalid choice. Please try again.")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            
    # Close the client
    client.close()

if __name__ == "__main__":
    print("AlphaVantage API Toolkit Test")
    print("=" * 50)
    test_alphavantage() 