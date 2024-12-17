"""Test script for Finnhub API toolkit - News fetching functionality."""
from datetime import datetime, timedelta
from api_toolkits.finnhub_toolkit import FinnhubClient

def get_recent_news():
    """Fetch news articles from the last 7 days for a user-specified ticker."""
    
    # Initialize the Finnhub client
    client = FinnhubClient()
    
    # Get user input for ticker
    ticker = input("Enter a stock ticker (e.g., AAPL): ").upper()
    
    # Calculate date range (last 7 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Format dates as required by the API (YYYY-MM-DD)
    from_date = start_date.strftime("%Y-%m-%d")
    to_date = end_date.strftime("%Y-%m-%d")
    
    try:
        # Fetch news articles
        print(f"\nFetching news for {ticker} from {from_date} to {to_date}...")
        news = client.get_company_news(ticker, from_date, to_date)
        
        if not news:
            print(f"No news articles found for {ticker} in the last 7 days.")
            return
        
        # Display the news articles
        print(f"\nFound {len(news)} articles:\n")
        for i, article in enumerate(news, 1):
            print(f"Article {i}:")
            print(f"Headline: {article.get('headline', 'N/A')}")
            print(f"Summary: {article.get('summary', 'N/A')}")
            print(f"Source: {article.get('source', 'N/A')}")
            print(f"URL: {article.get('url', 'N/A')}")
            print(f"Date: {datetime.fromtimestamp(article.get('datetime', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 80 + "\n")
            
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    print("Finnhub News Fetcher")
    print("=" * 50)
    get_recent_news() 