"""AlphaVantage API client implementation."""
from typing import Dict, Any, Optional, List
import csv
from io import StringIO
from ..base_client import BaseAPIClient
from ..config import APIConfig

class AlphaVantageClient(BaseAPIClient):
    """Client for interacting with the AlphaVantage API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AlphaVantage client.
        
        Args:
            api_key: Optional API key (will use environment variable if not provided)
        """
        api_key = api_key or APIConfig.ALPHAVANTAGE_API_KEY
        if not api_key:
            raise ValueError("AlphaVantage API key is required")
            
        super().__init__(
            api_key=api_key,
            base_url=APIConfig.ALPHAVANTAGE_BASE_URL,
            calls_per_minute=APIConfig.ALPHAVANTAGE_RATE_LIMIT
        )
    
    def get_time_series_daily(
        self,
        symbol: str,
        outputsize: str = 'compact',
        datatype: str = 'json'
    ) -> Dict[str, Any]:
        """Get daily time series for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            outputsize: 'compact' (last 100 data points) or 'full' (up to 20 years)
            datatype: 'json' or 'csv'
            
        Returns:
            Daily time series data
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'apikey': self.api_key,
                'outputsize': outputsize,
                'datatype': datatype
            }
        )
    
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company information and financial ratios.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Company overview data
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'OVERVIEW',
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def get_etf_profile(self, symbol: str) -> Dict[str, Any]:
        """Get ETF profile and holdings information.
        
        Args:
            symbol: ETF symbol (e.g., 'QQQ')
            
        Returns:
            ETF profile and holdings data
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'ETF_PROFILE',
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def get_dividends(self, symbol: str) -> Dict[str, Any]:
        """Get historical and future dividend distributions.
        
        Args:
            symbol: Stock symbol (e.g., 'IBM')
            
        Returns:
            Dividend distribution data
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'DIVIDENDS',
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def get_splits(self, symbol: str) -> Dict[str, Any]:
        """Get historical split events.
        
        Args:
            symbol: Stock symbol (e.g., 'IBM')
            
        Returns:
            Split events data
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'SPLITS',
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def get_income_statement(self, symbol: str) -> Dict[str, Any]:
        """Get annual and quarterly income statements.
        
        Args:
            symbol: Stock symbol (e.g., 'IBM')
            
        Returns:
            Income statement data
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'INCOME_STATEMENT',
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def get_balance_sheet(self, symbol: str) -> Dict[str, Any]:
        """Get annual and quarterly balance sheets.
        
        Args:
            symbol: Stock symbol (e.g., 'IBM')
            
        Returns:
            Balance sheet data
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'BALANCE_SHEET',
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def get_cash_flow(self, symbol: str) -> Dict[str, Any]:
        """Get annual and quarterly cash flow statements.
        
        Args:
            symbol: Stock symbol (e.g., 'IBM')
            
        Returns:
            Cash flow statement data
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'CASH_FLOW',
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def get_earnings(self, symbol: str) -> Dict[str, Any]:
        """Get quarterly and annual earnings data.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Earnings history data
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'EARNINGS',
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def get_listing_status(
        self,
        date: Optional[str] = None,
        state: str = 'active'
    ) -> List[Dict[str, Any]]:
        """Get list of active or delisted US stocks and ETFs.
        
        Args:
            date: Optional date in YYYY-MM-DD format (must be after 2010-01-01)
            state: 'active' or 'delisted'
            
        Returns:
            List of stocks/ETFs matching the criteria
        """
        params = {
            'function': 'LISTING_STATUS',
            'apikey': self.api_key,
            'state': state
        }
        if date:
            params['date'] = date
            
        response = self.session.get(
            self.base_url,
            params=params
        )
        response.raise_for_status()
        
        # Parse CSV response
        csv_data = csv.DictReader(StringIO(response.text))
        return list(csv_data)
    
    def get_earnings_calendar(
        self,
        symbol: Optional[str] = None,
        horizon: str = '3month'
    ) -> List[Dict[str, Any]]:
        """Get list of company earnings expected in the next 3, 6, or 12 months.
        
        Args:
            symbol: Optional stock symbol to filter by
            horizon: '3month', '6month', or '12month'
            
        Returns:
            List of upcoming earnings events
        """
        params = {
            'function': 'EARNINGS_CALENDAR',
            'apikey': self.api_key,
            'horizon': horizon
        }
        if symbol:
            params['symbol'] = symbol
            
        response = self.session.get(
            self.base_url,
            params=params
        )
        response.raise_for_status()
        
        # Parse CSV response
        csv_data = csv.DictReader(StringIO(response.text))
        return list(csv_data)
    
    def get_ipo_calendar(self) -> List[Dict[str, Any]]:
        """Get list of IPOs expected in the next 3 months.
        
        Returns:
            List of upcoming IPO events
        """
        response = self.session.get(
            self.base_url,
            params={
                'function': 'IPO_CALENDAR',
                'apikey': self.api_key
            }
        )
        response.raise_for_status()
        
        # Parse CSV response
        csv_data = csv.DictReader(StringIO(response.text))
        return list(csv_data)
    
    def get_global_quote(self, symbol: str) -> Dict[str, Any]:
        """Get current quote data for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Latest quote data
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def search_symbol(self, keywords: str) -> List[Dict[str, Any]]:
        """Search for symbols based on keywords.
        
        Args:
            keywords: Search keywords
            
        Returns:
            List of matching symbols and their details
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'SYMBOL_SEARCH',
                'keywords': keywords,
                'apikey': self.api_key
            }
        )
    
    def get_tops(self) -> Dict[str, Any]:
        """Get top 20 gainers, losers, and most actively traded tickers in the US market.
        
        Note:
            By default, this data is updated at the end of each trading day.
            Premium API keys may receive real-time or 15-minute delayed data.
        
        Returns:
            Dictionary containing three lists:
            - top_gainers: List of stocks with highest % gains
            - top_losers: List of stocks with highest % losses
            - most_actively_traded: List of stocks with highest trading volume
            
            Each stock entry contains:
            - ticker: Stock symbol
            - price: Current price
            - change_amount: Price change
            - change_percentage: Percentage change
            - volume: Trading volume (for most active stocks)
        """
        return self._make_request(
            endpoint='',
            params={
                'function': 'TOP_GAINERS_LOSERS',
                'apikey': self.api_key
            }
        ) 