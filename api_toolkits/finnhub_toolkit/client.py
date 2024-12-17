"""Finnhub API client implementation."""
from typing import Dict, Any, Optional, List
from ..base_client import BaseAPIClient
from ..config import APIConfig

class FinnhubClient(BaseAPIClient):
    """Client for interacting with the Finnhub API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Finnhub client.
        
        Args:
            api_key: Optional API key (will use environment variable if not provided)
        """
        api_key = api_key or APIConfig.FINNHUB_API_KEY
        if not api_key:
            raise ValueError("Finnhub API key is required")
            
        super().__init__(
            api_key=api_key,
            base_url=APIConfig.FINNHUB_BASE_URL,
            calls_per_minute=APIConfig.FINNHUB_RATE_LIMIT
        )
        
        # Set default headers
        self.session.headers.update({
            'X-Finnhub-Token': self.api_key
        })
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Get company profile information.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Company profile data
        """
        return self._make_request(
            endpoint='stock/profile2',
            params={'symbol': symbol}
        )
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time quote data.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Real-time quote data
        """
        return self._make_request(
            endpoint='quote',
            params={'symbol': symbol}
        )
    
    def get_earnings_calendar(
        self,
        from_date: str,
        to_date: str,
        symbol: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get earnings calendar.
        
        Args:
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            symbol: Optional stock symbol to filter by
            
        Returns:
            List of earnings calendar events
        """
        params = {
            'from': from_date,
            'to': to_date
        }
        if symbol:
            params['symbol'] = symbol
            
        return self._make_request(
            endpoint='calendar/earnings',
            params=params
        )
    
    def get_news(
        self,
        category: str = 'general',
        min_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get market news and sentiment data.
        
        Args:
            category: News category ('general', 'forex', 'crypto', 'merger')
            min_id: Get news after this ID
            
        Returns:
            List of news items
        """
        params = {'category': category}
        if min_id:
            params['minId'] = min_id
            
        return self._make_request(
            endpoint='news',
            params=params
        ) 