"""AlphaVantage API client implementation."""
from typing import Dict, Any, Optional, List
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