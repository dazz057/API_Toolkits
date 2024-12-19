"""Test script for AlphaVantage API toolkit - Fundamental Data."""
from api_toolkits.alphavantage_toolkit import AlphaVantageClient
import json
from datetime import datetime, timedelta

def format_output(data: dict, indent: int = 2) -> None:
    """Helper function to pretty print JSON data."""
    print(json.dumps(data, indent=indent))

def test_fundamentals():
    """Test various AlphaVantage fundamental data functionalities."""
    
    # Initialize the AlphaVantage client
    client = AlphaVantageClient()
    
    while True:
        print("\nAlphaVantage Fundamental Data Test Menu:")
        print("1. Company Overview")
        print("2. ETF Profile")
        print("3. Dividends History")
        print("4. Stock Splits History")
        print("5. Financial Statements")
        print("6. Earnings Data")
        print("7. Listing Status")
        print("8. Earnings Calendar")
        print("9. IPO Calendar")
        print("10. Top Gainers/Losers")
        print("11. Exit")
        
        choice = input("\nEnter your choice (1-11): ")
        
        if choice == "11":
            print("Exiting...")
            break
            
        try:
            if choice in ["1", "2", "3", "4", "5", "6"]:
                symbol = input("Enter a stock symbol (e.g., AAPL, IBM, QQQ): ").upper()
            
            if choice == "1":
                # Company Overview
                print(f"\nFetching company overview for {symbol}...")
                data = client.get_company_overview(symbol)
                format_output(data)
                
            elif choice == "2":
                # ETF Profile
                print(f"\nFetching ETF profile for {symbol}...")
                data = client.get_etf_profile(symbol)
                format_output(data)
                
            elif choice == "3":
                # Dividends History
                print(f"\nFetching dividend history for {symbol}...")
                data = client.get_dividends(symbol)
                format_output(data)
                
            elif choice == "4":
                # Stock Splits
                print(f"\nFetching stock split history for {symbol}...")
                data = client.get_splits(symbol)
                format_output(data)
                
            elif choice == "5":
                # Financial Statements
                print(f"\nFinancial Statements for {symbol}")
                print("1. Income Statement")
                print("2. Balance Sheet")
                print("3. Cash Flow")
                
                statement_choice = input("\nChoose statement type (1-3): ")
                
                if statement_choice == "1":
                    print("\nFetching income statement...")
                    data = client.get_income_statement(symbol)
                elif statement_choice == "2":
                    print("\nFetching balance sheet...")
                    data = client.get_balance_sheet(symbol)
                elif statement_choice == "3":
                    print("\nFetching cash flow statement...")
                    data = client.get_cash_flow(symbol)
                else:
                    print("Invalid choice")
                    continue
                    
                format_output(data)
                
            elif choice == "6":
                # Earnings Data
                print(f"\nFetching earnings data for {symbol}...")
                data = client.get_earnings(symbol)
                
                if 'annualEarnings' in data:
                    print("\nAnnual Earnings:")
                    format_output(data['annualEarnings'])
                if 'quarterlyEarnings' in data:
                    print("\nQuarterly Earnings:")
                    format_output(data['quarterlyEarnings'])
                
            elif choice == "7":
                # Listing Status
                print("\nListing Status Options:")
                print("1. Currently Active Stocks")
                print("2. Delisted Stocks")
                print("3. Historical Date")
                
                status_choice = input("\nChoose option (1-3): ")
                
                if status_choice == "1":
                    data = client.get_listing_status(state='active')
                elif status_choice == "2":
                    data = client.get_listing_status(state='delisted')
                elif status_choice == "3":
                    date = input("Enter date (YYYY-MM-DD, must be after 2010-01-01): ")
                    data = client.get_listing_status(date=date, state='active')
                else:
                    print("Invalid choice")
                    continue
                
                # Display first 10 entries and total count
                print(f"\nTotal entries: {len(data)}")
                print("\nFirst 10 entries:")
                format_output(data[:10])
                
            elif choice == "8":
                # Earnings Calendar
                print("\nEarnings Calendar Options:")
                print("1. Next 3 months")
                print("2. Next 6 months")
                print("3. Next 12 months")
                print("4. Specific Symbol")
                
                calendar_choice = input("\nChoose option (1-4): ")
                
                if calendar_choice == "4":
                    symbol = input("Enter symbol: ").upper()
                    data = client.get_earnings_calendar(symbol=symbol, horizon='12month')
                else:
                    horizon_map = {'1': '3month', '2': '6month', '3': '12month'}
                    if calendar_choice in horizon_map:
                        data = client.get_earnings_calendar(horizon=horizon_map[calendar_choice])
                    else:
                        print("Invalid choice")
                        continue
                
                # Display first 10 entries and total count
                print(f"\nTotal earnings events: {len(data)}")
                print("\nNext 10 earnings events:")
                format_output(data[:10])
                
            elif choice == "9":
                # IPO Calendar
                print("\nFetching upcoming IPOs...")
                data = client.get_ipo_calendar()
                
                # Display all IPOs
                print(f"\nTotal upcoming IPOs: {len(data)}")
                format_output(data)
                
            elif choice == "10":
                # Top Gainers/Losers
                print("\nFetching top gainers, losers, and most active stocks...")
                data = client.get_tops()
                
                # Display each category separately for better readability
                if 'top_gainers' in data:
                    print("\nTop Gainers:")
                    format_output(data['top_gainers'])
                if 'top_losers' in data:
                    print("\nTop Losers:")
                    format_output(data['top_losers'])
                if 'most_actively_traded' in data:
                    print("\nMost Actively Traded:")
                    format_output(data['most_actively_traded'])
                
            else:
                print("Invalid choice. Please try again.")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            
    # Close the client
    client.close()

if __name__ == "__main__":
    print("AlphaVantage Fundamental Data Test")
    print("=" * 50)
    test_fundamentals() 